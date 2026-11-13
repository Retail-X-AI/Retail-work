
from pathlib import Path
import re
import pandas as pd


# Project directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Dataset locations
SUPPLIERS_FILE = BASE_DIR / "dataset" / "supplier" / "suppliers.csv"
PRODUCTS_FILE = BASE_DIR / "dataset" / "supplier" / "products.csv"
SUPPLIER_LINKS_FILE = (
    BASE_DIR / "dataset" / "supplier" / "processed"
    / "supplier_recommendation_data.csv"
)
RECOMMENDATIONS_FILE = (
    BASE_DIR / "dataset" / "supplier" / "processed"
    / "supplier_recommendations.csv"
)


def load_supplier_data():
    """Load supplier, product and recommendation data."""

    suppliers = pd.read_csv(SUPPLIERS_FILE)
    products = pd.read_csv(PRODUCTS_FILE)
    links = pd.read_csv(SUPPLIER_LINKS_FILE)
    recommendations = pd.read_csv(RECOMMENDATIONS_FILE)

    return suppliers, products, links, recommendations


def identify_product(question, products):
    """Identify a product using its ID or name."""

    question_lower = question.lower()

    # Match IDs such as P0002 or product 2
    id_match = re.search(
        r"\b(?:p0*(\d+)|product\s+0*(\d+))\b",
        question_lower
    )

    if id_match:
        product_id = int(id_match.group(1) or id_match.group(2))

        match = products[products["id"] == product_id]

        if not match.empty:
            return match.iloc[0]

    # Match product names
    for _, product in products.iterrows():
        name = str(product["name"]).lower()

        if name and name in question_lower:
            return product

    return None


def format_contact(supplier):
    """Display available supplier contact details."""

    details = []

    if pd.notna(supplier.get("contact_email")):
        details.append(f"Email: {supplier['contact_email']}")

    if pd.notna(supplier.get("phone")):
        details.append(f"Phone: {supplier['phone']}")

    return "\n".join(details) if details else "No contact details available."


def supplier_query(question):
    """Answer questions about registered suppliers and products."""

    suppliers, products, links, _ = load_supplier_data()
    question_lower = question.lower()

    # List all suppliers
    if any(term in question_lower for term in [
        "all suppliers",
        "list suppliers",
        "registered suppliers",
        "available suppliers",
        "show suppliers"
    ]):
        supplier_records = suppliers.dropna(subset=["name"])

        return (
            f"There are {len(supplier_records)} registered supplier records:\n"
    + "\n".join(
        f"{index}. Supplier ID: {row['id']} | {row['name']}"
        for index, (_, row) in enumerate(
            supplier_records.iterrows(), 1)
            )
        )

    # Identify a product
    product = identify_product(question, products)

    if product is not None:
        product_id = product["id"]

        matches = links[
            links["product_id"] == product_id
        ]

        if matches.empty:
            return f"No supplier is linked to {product['name']}."

        response = [
            f"Suppliers for {product['name']} "
            f"(Product ID: {product_id}):"
        ]

        for _, row in matches.iterrows():
            response.append(
                f"\nSupplier: {row['supplier_name']}"
                f"\nLead time: {row['lead_time_days']} days"
                f"\nMinimum order quantity: "
                f"{row['minimum_order_quantity']}"
                f"\nSupply frequency: "
                f"Every {row['supply_frequency_days']} days"
            )

        return "\n".join(response)

    # Search for a supplier by name
    for _, supplier in suppliers.iterrows():
        supplier_name = str(supplier["name"])

        if supplier_name.lower() in question_lower:
            supplier_id = supplier["id"]

            supplied_products = links[
                links["supplier_id"] == supplier_id
            ]

            if any(term in question_lower for term in [
                "products", "provide", "supplies", "supply"
            ]):
                if supplied_products.empty:
                    return f"No products are linked to {supplier_name}."

                names = supplied_products[
                    "product_name"
                ].drop_duplicates().tolist()

                return (
                    f"{supplier_name} supplies:\n"
                    + "\n".join(f"- {name}" for name in names)
                )

            return (
                f"Supplier: {supplier_name}\n"
                f"{format_contact(supplier)}"
            )

    return (
        "I could not identify the supplier or product in your question. "
        "Try using a product name, product ID or supplier name."
    )


def supplier_recommendation(question):
    """Recommend suppliers using the existing scoring system."""

    _, products, _, recommendations = load_supplier_data()
    question_lower = question.lower()

    product = identify_product(question, products)

    if product is None:
        return (
            "Please provide a valid product name or product ID "
            "so I can compare its available suppliers."
        )

    product_id = product["id"]

    matches = recommendations[
        recommendations["product_id"] == product_id
    ].sort_values("rank")

    if matches.empty:
        return f"No supplier recommendations are available for {product['name']}."

    # Check what information the user is requesting
    limitations = []

    if any(word in question_lower for word in [
        "cheap", "cheapest", "price", "cost", "cheaper"
    ]):
        limitations.append(
            "Supplier purchase prices are not available, "
            "so I cannot identify the cheapest supplier."
        )

    if any(word in question_lower for word in [
        "stock", "available quantity", "enough stock"
    ]):
        limitations.append(
            "Supplier stock quantities are not available "
            "in the current dataset."
        )

    if any(word in question_lower for word in [
        "reliable", "reliability", "on time", "delivery record"
    ]):
        limitations.append(
            "Historical delivery records are unavailable, "
            "so actual supplier reliability cannot be measured."
        )

    response = [
        f"Supplier recommendations for {product['name']}:"
    ]

    for _, row in matches.iterrows():
        response.append(
            f"\nRank: {int(row['rank'])}"
            f"\nSupplier: {row['supplier_name']}"
            f"\nLead time: {row['lead_time_days']} days"
            f"\nMinimum order quantity: "
            f"{row['minimum_order_quantity']}"
            f"\nSupply frequency: "
            f"Every {row['supply_frequency_days']} days"
        )

        if pd.notna(row["recommendation_score"]):
            response.append(
                f"Recommendation score: "
                f"{row['recommendation_score']:.2f}/100"
            )

    if limitations:
        response.append("\nData limitations:")
        response.extend(limitations)

    if len(matches) == 1:
        response.append(
            "\nThis is the only available supplier in the dataset. "
            "A comparative recommendation score cannot be calculated."
        )
    else:
        response.append(
            "\nRanking method: Lead time 50%, minimum order quantity "
            "30%, and supply frequency 20%. "
            "Scores compare suppliers for this product only."
        )

    return "\n".join(response)


def supplier_performance():
    """Explain the current supplier performance data limitation."""

    return (
        "I cannot calculate actual supplier performance yet.\n\n"
        "The current dataset contains supplier lead times, minimum "
        "order quantities and supply frequencies. However, it does "
        "not contain historical orders, actual delivery dates, "
        "late deliveries, quality ratings or order fulfilment records.\n\n"
        "These records would be needed to calculate genuine supplier "
        "reliability and delivery performance."
    )


def handle_supplier_intent(intent, question):
    """Route supplier questions to the correct handler."""

    if intent == "SUPPLIER_QUERY":
        return supplier_query(question)

    if intent == "SUPPLIER_RECOMMENDATION":
        return supplier_recommendation(question)

    if intent == "SUPPLIER_PERFORMANCE":
        return supplier_performance()

    return "I could not process that supplier request."

