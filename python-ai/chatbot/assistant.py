
from pathlib import Path
import re
import sqlite3
import sys
import tempfile
import wave
from datetime import datetime

import joblib
import numpy as np
import pandas as pd
import sounddevice as sd
from faster_whisper import WhisperModel

from supplier_handler import handle_supplier_intent
PROJECT_ROOT_FOR_IMPORT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT_FOR_IMPORT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT_FOR_IMPORT))
    
from application.backend.database.service import (
    get_sku_code,
    record_spoilage,
    record_damage,
    get_spoilage_records,
    get_damage_records,
)
# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BASE_DIR.parents[1]

MODEL_FILE = BASE_DIR / "models" / "intent_classifier.joblib"

RESTOCKING_DIR = REPO_ROOT / "python-ai" / "restocking"
OUTPUT_DIR = RESTOCKING_DIR / "outputs"

REORDER_FILE = (
    OUTPUT_DIR / "retail_restocking_recommendations_m12_02.csv"
)

STOCKOUT_FILE = (
    OUTPUT_DIR / "retail_stockout_detection_m12_03.csv"
)

FORECAST_SERVICE_DIR = (
    REPO_ROOT / "application" / "backend" / "forecasts"
)

if str(FORECAST_SERVICE_DIR) not in sys.path:
    sys.path.insert(0, str(FORECAST_SERVICE_DIR))


# --------------------------------------------------
# FORECAST SERVICE
# --------------------------------------------------

from service import (
    load_forecasts,
    load_forecast_metadata,
    validate_forecast_metadata,
    summarize_forecasts,
)
# --------------------------------------------------
# SALES ANALYSIS
# --------------------------------------------------

ANALYSIS_DIR = REPO_ROOT / "python-ai" / "analysis"

if str(ANALYSIS_DIR) not in sys.path:
    sys.path.insert(0, str(ANALYSIS_DIR))

from sales_analysis import (
    generate_sales_summary,
    analyze_sales_factors,
    get_top_selling_products,
)

# --------------------------------------------------
# SPEECH RECOGNITION
# --------------------------------------------------

SPEECH_MODEL = None
MICROPHONE_DEVICE = 1
SAMPLE_RATE = 16000
RECORDING_DURATION = 7


def load_speech_model():
    """Load the Faster Whisper speech recognition model once."""

    global SPEECH_MODEL

    if SPEECH_MODEL is None:
        print("\nChatbot: Loading speech recognition model...")
        SPEECH_MODEL = WhisperModel(
            "small",
            device="cpu",
            compute_type="int8"
        )

    return SPEECH_MODEL


def record_voice_question():
    """Record and transcribe a spoken question."""

    audio = sd.rec(
        int(RECORDING_DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
        device=MICROPHONE_DEVICE
    )

    print("Chatbot: Listening... Speak now.")
    sd.wait()

    if np.max(np.abs(audio)) < 0.01:
        print("Chatbot: No clear audio detected. Please try again.")
        return ""

    samples = (
        audio.flatten() * 32767
    ).astype(np.int16)

    temp_file = tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False
    )

    audio_path = temp_file.name
    temp_file.close()

    try:
        with wave.open(audio_path, "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(SAMPLE_RATE)
            wav_file.writeframes(samples.tobytes())

        model = load_speech_model()

        segments, info = model.transcribe(
            audio_path,
            language="en",
            beam_size=5
        )

        question = " ".join(
            segment.text.strip()
            for segment in segments
        ).strip()

        if question:
            print(f"\nYou (voice): {question}")
        else:
            print("Chatbot: I could not recognise your speech.")

        return question

    finally:
        if Path(audio_path).exists():
            Path(audio_path).unlink()

# --------------------------------------------------
# MODEL LOADING
# --------------------------------------------------

def load_chatbot_model():
    """Load the trained intent classification model."""

    if not MODEL_FILE.exists():
        raise FileNotFoundError(
            f"Chatbot model not found: {MODEL_FILE}"
        )

    return joblib.load(MODEL_FILE)


chatbot_model = load_chatbot_model()


# --------------------------------------------------
# DATA LOADING
# --------------------------------------------------

def load_reorder_data():
    """Load generated historical reorder recommendations."""

    if not REORDER_FILE.is_file():
        raise FileNotFoundError(
            f"Reorder recommendations not found: {REORDER_FILE}. "
            "Run python .\\python-ai\\restocking\\recommendations.py first."
        )

    data = pd.read_csv(
        REORDER_FILE,
        dtype={"Store ID": str, "Product ID": str}
    )

    data["Date"] = pd.to_datetime(
        data["Date"],
        errors="coerce"
    )

    return data


def load_stockout_data():
    """Load generated historical stockout detection results."""

    if not STOCKOUT_FILE.is_file():
        raise FileNotFoundError(
            f"Stockout results not found: {STOCKOUT_FILE}. "
            "Run python .\\python-ai\\restocking\\stockout.py first."
        )

    data = pd.read_csv(
        STOCKOUT_FILE,
        dtype={"Store ID": str, "Product ID": str}
    )

    data["Date"] = pd.to_datetime(
        data["Date"],
        errors="coerce"
    )

    return data


# --------------------------------------------------
# QUESTION FILTERING
# --------------------------------------------------

def extract_identifiers(question):
    """Extract store and product identifiers from a question."""

    product_match = re.search(
        r"\bP\d+\b",
        question,
        re.IGNORECASE
    )

    store_match = re.search(
        r"\bS\d+\b",
        question,
        re.IGNORECASE
    )

    product_id = (
        product_match.group(0).upper()
        if product_match else None
    )

    store_id = (
        store_match.group(0).upper()
        if store_match else None
    )

    return store_id, product_id


def filter_latest_records(data, question):
    """Filter records and return the latest matching historical date."""

    store_id, product_id = extract_identifiers(question)

    filtered = data.copy()

    if store_id:
        filtered = filtered[
            filtered["Store ID"] == store_id
        ]

    if product_id:
        filtered = filtered[
            filtered["Product ID"] == product_id
        ]

    if filtered.empty:
        return filtered

    latest_date = filtered["Date"].max()

    filtered = filtered[
        filtered["Date"] == latest_date
    ].copy()

    return filtered.sort_values(
        ["Store ID", "Product ID"]
    ).reset_index(drop=True)


def format_number(value, decimals=0):
    """Format numeric values safely."""

    if pd.isna(value):
        return "Unavailable"

    return f"{float(value):,.{decimals}f}"


def historical_date_message(data):
    """Describe the date represented by the returned records."""

    if data.empty:
        return ""

    date_value = data["Date"].iloc[0]

    return (
        f"Historical record date: "
        f"{date_value.strftime('%Y-%m-%d')}"
    )


# --------------------------------------------------
# INVENTORY LEVEL HANDLER
# --------------------------------------------------

def handle_inventory_level(question):
    """Retrieve inventory levels from generated reorder records."""

    data = load_reorder_data()

    records = filter_latest_records(data, question)

    if records.empty:
        return (
            "No matching inventory records were found. "
            "Please check the store ID and product ID."
        )

    response = [
        "INVENTORY LEVEL SUMMARY",
        historical_date_message(records),
        ""
    ]

    for _, record in records.head(15).iterrows():

        response.append(
            f"Store: {record['Store ID']}\n"
            f"Product: {record['Product ID']}\n"
            f"Inventory level: "
            f"{format_number(record['Inventory Level'])} units\n"
            f"Reorder point: "
            f"{format_number(record['reorder_point'])} units\n"
            f"Status: {record['recommendation_status']}\n"
        )

    if len(records) > 15:
        response.append(
            f"Showing 15 of {len(records)} matching records."
        )

    response.append(
        "Note: These are historical inventory records, "
        "not live stock levels."
    )

    return "\n".join(response)


# --------------------------------------------------
# REORDER RECOMMENDATION HANDLER
# --------------------------------------------------

def handle_reorder_recommendation(question):
    """Retrieve reorder recommendations from the generated CSV."""

    data = load_reorder_data()

    records = filter_latest_records(data, question)

    if records.empty:
        return (
            "No matching reorder recommendations were found. "
            "Please check the store ID and product ID."
        )

    response = [
        "REORDER RECOMMENDATIONS",
        historical_date_message(records),
        ""
    ]

    for _, record in records.head(15).iterrows():

        response.append(
            f"Store: {record['Store ID']}\n"
            f"Product: {record['Product ID']}\n"
            f"Current stock: "
            f"{format_number(record['Inventory Level'])} units\n"
            f"Forecast demand: "
            f"{format_number(record['Forecast Units Sold'], 2)} units\n"
            f"Reorder point: "
            f"{format_number(record['reorder_point'])} units\n"
            f"Target stock: "
            f"{format_number(record['target_stock'])} units\n"
            f"Suggested order quantity: "
            f"{format_number(record['suggested_order_quantity'])} units\n"
            f"Recommendation: "
            f"{record['recommendation_status']}\n"
            f"Reason: {record['recommendation_reason']}\n"
        )

    if len(records) > 15:
        response.append(
            f"Showing 15 of {len(records)} matching records."
        )

    response.append(
        "Note: These are historical advisory recommendations. "
        "They do not create purchase orders."
    )

    return "\n".join(response)


# --------------------------------------------------
# STOCKOUT HANDLER
# --------------------------------------------------

def handle_stockout_status(question):
    """Retrieve stockout detection results."""

    data = load_stockout_data()

    records = filter_latest_records(data, question)

    if records.empty:
        return (
            "No matching stockout records were found. "
            "Please check the store ID and product ID."
        )

    response = [
        "STOCKOUT DETECTION SUMMARY",
        historical_date_message(records),
        ""
    ]

    for _, record in records.head(15).iterrows():

        response.append(
            f"Store: {record['Store ID']}\n"
            f"Product: {record['Product ID']}\n"
            f"Inventory level: "
            f"{format_number(record['Inventory Level'])} units\n"
            f"Forecast demand: "
            f"{format_number(record['Forecast Units Sold'], 2)} units\n"
            f"Days of cover: "
            f"{format_number(record['days_of_cover'], 2)} days\n"
            f"Reorder point: "
            f"{format_number(record['reorder_point'])} units\n"
            f"Stockout status: {record['stockout_status']}\n"
            f"Reason: {record['stockout_reason']}\n"
        )

    if len(records) > 15:
        response.append(
            f"Showing 15 of {len(records)} matching records."
        )

    response.append(
        "Note: These are historical stockout detection results, "
        "not live stockout alerts."
    )

    return "\n".join(response)


# --------------------------------------------------
# DEMAND FORECAST HANDLER
# --------------------------------------------------

def handle_demand_forecast():
    """Retrieve and summarize existing demand forecast results."""

    forecasts = load_forecasts()
    metadata = load_forecast_metadata()

    validate_forecast_metadata(forecasts, metadata)

    summary = summarize_forecasts(forecasts)

    return (
        "DEMAND FORECAST SUMMARY\n\n"
        f"Model: {metadata['model_name']}\n"
        f"Forecast period: {summary['start_date']} "
        f"to {summary['end_date']}\n"
        f"Forecast records: {summary['records']:,}\n"
        f"Stores covered: {summary['stores']}\n"
        f"Products covered: {summary['products']}\n\n"
        f"Actual demand: "
        f"{summary['actual_demand_total']:,.2f} units\n"
        f"Forecast demand: "
        f"{summary['forecast_demand_total']:,.2f} units\n"
        f"Mean Absolute Error (MAE): {summary['mae']:.2f}\n"
        f"Root Mean Squared Error (RMSE): "
        f"{summary['rmse']:.2f}\n\n"
        "Note: These are historical one-step-ahead evaluation "
        "results, not predictions for future days."
    )

# --------------------------------------------------
# SALES SUMMARY HANDLER
# --------------------------------------------------

def handle_sales_summary():
    """Display an overall historical sales summary."""

    summary = generate_sales_summary()

    response = [
        "HISTORICAL SALES SUMMARY",
        "",
        f"Period: {summary['start_date'].strftime('%Y-%m-%d')} "
        f"to {summary['end_date'].strftime('%Y-%m-%d')}",
        f"Sales records: {summary['total_records']:,}",
        f"Total units sold: {summary['total_units_sold']:,.0f}",
        f"Average daily sales across all stores: "
        f"{summary['average_daily_sales']:,.2f} units",
        f"Highest sales day: "
        f"{summary['highest_sales_day'].strftime('%Y-%m-%d')}",
        f"Units sold on highest sales day: "
        f"{summary['highest_daily_sales']:,.0f}",
        "",
        "SALES BY STORE"
    ]

    for store, units in summary["store_sales"].items():
        response.append(
            f"{store}: {units:,.0f} units"
        )

    response.append("")
    response.append("SALES BY CATEGORY")

    for category, units in summary["category_sales"].items():
        response.append(
            f"{category}: {units:,.0f} units"
        )

    response.append(
        "\nNote: These are historical sales volumes, not live sales."
    )

    response.append(
        "Category totals describe the dataset's recorded categories. "
        "Product category assignments are inconsistent."
    )

    return "\n".join(response)


# --------------------------------------------------
# SALES FACTOR ANALYSIS HANDLER
# --------------------------------------------------

def handle_sales_factor_analysis():
    """Display relationships between sales and recorded factors."""

    results = analyze_sales_factors()

    response = [
        "SALES FACTOR ANALYSIS",
        "",
        "PROMOTION COMPARISON"
    ]

    for promotion, row in results["promotion_sales"].iterrows():

        label = (
            "Promotion active"
            if promotion == 1
            else "No promotion"
        )

        response.append(
            f"{label}: "
            f"{row['mean']:.2f} average units sold "
            f"({int(row['count']):,} records)"
        )

    response.extend([
        "",
        "WEATHER COMPARISON"
    ])

    for weather, row in results["weather_sales"].iterrows():
        response.append(
            f"{weather}: {row['mean']:.2f} average units sold"
        )

    response.extend([
        "",
        "SEASONAL COMPARISON"
    ])

    for season, row in results["seasonal_sales"].iterrows():
        response.append(
            f"{season}: {row['mean']:.2f} average units sold"
        )

    response.extend([
        "",
        "NUMERIC FACTOR CORRELATIONS"
    ])

    for factor, correlation in results["numeric_correlations"].items():
        response.append(
            f"{factor}: {correlation:.4f}"
        )

    response.extend([
        "",
        "Interpretation: These results show statistical "
        "relationships in the historical dataset. They do not "
        "establish that any factor caused a change in sales."
    ])

    return "\n".join(response)


# --------------------------------------------------
# TOP SELLING PRODUCTS HANDLER
# --------------------------------------------------

def handle_top_selling_products(question):
    """Display the highest selling products."""

    store_id, _ = extract_identifiers(question)

    products = get_top_selling_products(
        store_id=store_id,
        limit=10
    )

    if products.empty:
        return (
            "No sales records were found for the requested store. "
            "Please check the store ID."
        )

    response = [
        "TOP SELLING PRODUCTS",
        (
            f"Store: {store_id}"
            if store_id
            else "All stores combined"
        ),
        "Ranking based on total historical units sold.",
        ""
    ]

    for _, product in products.iterrows():

        response.append(
            f"Rank: {product['Rank']}\n"
            f"Product ID: {product['Product ID']}\n"
            f"Total units sold: "
            f"{product['total_units_sold']:,.0f}\n"
            f"Average units per record: "
            f"{product['average_units_sold']:.2f}\n"
        )

    response.append(
        "Note: Product IDs have inconsistent category assignments "
        "in the supplied dataset."
    )

    return "\n".join(response)

def handle_sku_lookup(question):
    """Look up the SKU code for a product."""

    store_id, product_id = extract_identifiers(question)

    if not product_id:
        return "Please include a Product ID, for example: What is the SKU for P0001?"

    sku_code = get_sku_code(product_id)

    if sku_code:
        return (
            "SKU LOOKUP RESULT\n"
            f"Product ID: {product_id}\n"
            f"SKU Code: {sku_code}"
        )

    return f"No SKU code was found for Product ID {product_id}."


def handle_spoilage_query(question):
    """Display recorded spoiled stock."""

    records = get_spoilage_records()
    store_id, product_id = extract_identifiers(question)

    if store_id:
        records = [r for r in records if r["store_id"] == store_id]

    if product_id:
        records = [r for r in records if r["product_id"] == product_id]

    if not records:
        return "No spoilage records were found for that request."

    total_quantity = sum(record["quantity"] for record in records)

    lines = [
        "SPOILAGE RECORDS",
        f"Number of records: {len(records)}",
        f"Total spoiled units: {total_quantity}",
        ""
    ]

    for record in records[:15]:
        lines.extend([
            f"Date: {record['record_date']}",
            f"Store: {record['store_id']}",
            f"Product: {record['product_id']}",
            f"Quantity: {record['quantity']}",
            f"Reason: {record['reason']}",
            ""
        ])

    if len(records) > 15:
        lines.append("Only the first 15 records are displayed.")

    return "\n".join(lines)


def handle_damage_query(question):
    """Display recorded damaged stock."""

    records = get_damage_records()
    store_id, product_id = extract_identifiers(question)

    if store_id:
        records = [r for r in records if r["store_id"] == store_id]

    if product_id:
        records = [r for r in records if r["product_id"] == product_id]

    if not records:
        return "No damage records were found for that request."

    total_quantity = sum(record["quantity"] for record in records)

    lines = [
        "DAMAGE RECORDS",
        f"Number of records: {len(records)}",
        f"Total damaged units: {total_quantity}",
        ""
    ]

    for record in records[:15]:
        lines.extend([
            f"Date: {record['record_date']}",
            f"Store: {record['store_id']}",
            f"Product: {record['product_id']}",
            f"Quantity: {record['quantity']}",
            f"Reason: {record['reason']}",
            ""
        ])

    if len(records) > 15:
        lines.append("Only the first 15 records are displayed.")

    return "\n".join(lines)



# --------------------------------------------------
# SPOILAGE AND DAMAGE RECORDING CONVERSATION
# --------------------------------------------------

PENDING_STOCK_LOSS = None


def handle_pending_stock_loss(answer):
    """Collect and validate information for spoilage or damage records."""

    global PENDING_STOCK_LOSS

    answer = answer.strip()

    if answer.lower() == "cancel":
        PENDING_STOCK_LOSS = None
        return "Stock loss recording cancelled."

    record_type = PENDING_STOCK_LOSS["type"]
    step = PENDING_STOCK_LOSS["step"]
    data = PENDING_STOCK_LOSS["data"]

    if step == "date":
        try:
            datetime.strptime(answer, "%Y-%m-%d")
            data["record_date"] = answer
        except ValueError:
            return "Invalid date. Please use YYYY-MM-DD, for example 2026-11-13."

        PENDING_STOCK_LOSS["step"] = "store_id"
        return "Which store? Enter its Store ID, for example S001."

    if step == "store_id":
        if not re.fullmatch(r"S\d+", answer, re.IGNORECASE):
            return "Invalid Store ID. Please enter a value such as S001."

        data["store_id"] = answer.upper()
        PENDING_STOCK_LOSS["step"] = "product_id"
        return "Which product? Enter its Product ID, for example P0001."

    if step == "product_id":
        if not re.fullmatch(r"P\d+", answer, re.IGNORECASE):
            return "Invalid Product ID. Please enter a value such as P0001."

        product_id = answer.upper()

        try:
            sku_code = get_sku_code(product_id)
        except (FileNotFoundError, ValueError, KeyError) as error:
            return f"Unable to verify the product: {error}"

        if sku_code is None:
            return f"Product {product_id} was not found. Please enter a registered Product ID."

        data["product_id"] = product_id
        PENDING_STOCK_LOSS["step"] = "quantity"

        return (
            f"Product verified. SKU: {sku_code}\n"
            "How many units were spoiled or damaged? Enter a positive whole number."
        )

    if step == "quantity":
        try:
            quantity = int(answer)

            if quantity <= 0:
                raise ValueError

        except ValueError:
            return "Invalid quantity. Please enter a positive whole number."

        data["quantity"] = quantity
        PENDING_STOCK_LOSS["step"] = "reason"

        return "What was the reason for the spoilage or damage?"

    if step == "reason":
        if not answer:
            return "Please provide a reason."

        data["reason"] = answer

        try:
            if record_type == "spoilage":
                record_id = record_spoilage(
                    data["record_date"],
                    data["store_id"],
                    data["product_id"],
                    data["quantity"],
                    data["reason"]
                )
            else:
                record_id = record_damage(
                    data["record_date"],
                    data["store_id"],
                    data["product_id"],
                    data["quantity"],
                    data["reason"]
                )

        except (ValueError, sqlite3.Error) as error:
            PENDING_STOCK_LOSS = None
            return f"Unable to save the record: {error}"

        PENDING_STOCK_LOSS = None

        return (
            f"{record_type.upper()} RECORD SAVED SUCCESSFULLY\n"
            f"Record ID: {record_id}\n"
            f"Date: {data['record_date']}\n"
            f"Store: {data['store_id']}\n"
            f"Product: {data['product_id']}\n"
            f"Quantity: {data['quantity']} units\n"
            f"Reason: {data['reason']}"
        )

    PENDING_STOCK_LOSS = None
    return "The recording process encountered an unexpected error."

# --------------------------------------------------
# MAIN CHATBOT MESSAGE PROCESSING
# --------------------------------------------------

def process_message(question):
    """Predict intent and generate the appropriate response."""

    global PENDING_STOCK_LOSS

    question = question.strip()

    if not question:
        return "Please enter a question."

    if PENDING_STOCK_LOSS is not None:
        return handle_pending_stock_loss(question)

    intent = chatbot_model.predict([question])[0]

    print(f"\nDetected intent: {intent}")

    if intent == "OUT_OF_SCOPE":
        return (
            "I'm sorry, I can only assist with Retail-X-AI functions.\n"
            "Please ask me about inventory, sales, demand forecasting, "
            "reordering, stockouts, suppliers, SKU codes, spoilage or damage."
        )

    if intent == "GREETING":
        return (
            "Hello! Welcome to Retail-X-AI. "
            "How can I help you with your shop today?"
        )

    if intent == "HELP":
        return (
            "I can help you with:\n"
            "1. Demand forecasting\n"
            "2. Inventory levels\n"
            "3. Reorder recommendations\n"
            "4. Stockout detection\n"
            "5. Sales summaries and analysis\n"
            "6. Top-selling products\n"
            "7. Supplier information\n"
            "8. Supplier recommendations\n"
            "9. Supplier performance information\n"
            "10. SKU code lookup\n"
            "11. Record spoiled stock\n"
            "12. View spoilage records\n"
            "13. Record damaged stock\n"
            "14. View damage records"
        )

    if intent == "GOODBYE":
        return "Goodbye! Thank you for using Retail-X-AI."

    if intent == "SKU_LOOKUP":
        try:
            return handle_sku_lookup(question)
        except (FileNotFoundError, ValueError, KeyError) as error:
            return f"Unable to retrieve SKU information: {error}"

    if intent == "SPOILAGE_RECORD":
        PENDING_STOCK_LOSS = {
            "type": "spoilage",
            "step": "date",
            "data": {}
        }
        return (
            "Let's record spoiled stock.\n"
            "What is the record date? Use YYYY-MM-DD."
        )

    if intent == "SPOILAGE_QUERY":
        try:
            return handle_spoilage_query(question)
        except (FileNotFoundError, ValueError, KeyError) as error:
            return f"Unable to retrieve spoilage records: {error}"

    if intent == "DAMAGE_RECORD":
        PENDING_STOCK_LOSS = {
            "type": "damage",
            "step": "date",
            "data": {}
        }
        return (
            "Let's record damaged stock.\n"
            "What is the record date? Use YYYY-MM-DD."
        )

    if intent == "DAMAGE_QUERY":
        try:
            return handle_damage_query(question)
        except (FileNotFoundError, ValueError, KeyError) as error:
            return f"Unable to retrieve damage records: {error}"

    if intent == "DEMAND_FORECAST":
        try:
            return handle_demand_forecast()
        except (FileNotFoundError, ValueError, KeyError) as error:
            return f"Unable to retrieve demand forecast results: {error}"

    if intent == "INVENTORY_LEVEL":
        try:
            return handle_inventory_level(question)
        except (FileNotFoundError, ValueError, KeyError) as error:
            return f"Unable to retrieve inventory levels: {error}"

    if intent == "REORDER_RECOMMENDATION":
        try:
            return handle_reorder_recommendation(question)
        except (FileNotFoundError, ValueError, KeyError) as error:
            return f"Unable to retrieve reorder recommendations: {error}"

    if intent == "STOCKOUT_STATUS":
        try:
            return handle_stockout_status(question)
        except (FileNotFoundError, ValueError, KeyError) as error:
            return f"Unable to retrieve stockout results: {error}"

    if intent == "SALES_SUMMARY":
        try:
            return handle_sales_summary()
        except (FileNotFoundError, ValueError, KeyError) as error:
            return f"Unable to retrieve sales summary: {error}"

    if intent == "SALES_FACTOR_ANALYSIS":
        try:
            return handle_sales_factor_analysis()
        except (FileNotFoundError, ValueError, KeyError) as error:
            return f"Unable to analyse sales factors: {error}"

    if intent == "TOP_SELLING_PRODUCTS":
        try:
            return handle_top_selling_products(question)
        except (FileNotFoundError, ValueError, KeyError) as error:
            return f"Unable to retrieve top selling products: {error}"

    supplier_intents = [
        "SUPPLIER_QUERY",
        "SUPPLIER_RECOMMENDATION",
        "SUPPLIER_PERFORMANCE"
    ]

    if intent in supplier_intents:
        return handle_supplier_intent(intent, question)

    return (
        f"I recognised your question as {intent}, "
        "but this functionality has not been integrated yet."
    )




# --------------------------------------------------
# CHATBOT TERMINAL
# --------------------------------------------------


def main():
    """Run the chatbot with text and voice input."""

    print("=" * 50)
    print("RETAIL-X-AI CHATBOT")
    print("=" * 50)
    print("Type your question or type 'voice' to speak.")
    print("Type 'exit' to close.")

    while True:
        try:
            question = input("\nYou: ").strip()

            if question.lower() == "voice":
                try:
                    question = record_voice_question()
                except Exception as error:
                    print(
                        f"\nChatbot: Speech recognition error: {error}"
                    )
                    continue

            if question.lower() in ["exit", "quit"]:
                print("\nChatbot: Goodbye!")
                break

            if not question:
                continue

            response = process_message(question)

            print("\nChatbot:", response)

        except KeyboardInterrupt:
            print("\n\nChatbot: Goodbye!")
            break


if __name__ == "__main__":
    main()
