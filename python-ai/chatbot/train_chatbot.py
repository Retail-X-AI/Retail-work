
from pathlib import Path

import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline


# 1. Locate the chatbot folder
BASE_DIR = Path(__file__).resolve().parent

DATA_FILE = BASE_DIR / "training_data.csv"
MODEL_DIR = BASE_DIR / "models"
MODEL_FILE = MODEL_DIR / "intent_classifier.joblib"


# 2. Load training data
print("Loading chatbot training data...")

if not DATA_FILE.exists():
    raise FileNotFoundError(f"Training file not found: {DATA_FILE}")

df = pd.read_csv(DATA_FILE)

required_columns = {"text", "intent"}

if not required_columns.issubset(df.columns):
    raise ValueError("CSV must contain text and intent columns.")

df = df.dropna(subset=["text", "intent"])

df["text"] = df["text"].astype(str).str.strip()
df["intent"] = df["intent"].astype(str).str.strip()

df = df[(df["text"] != "") & (df["intent"] != "")]

if df["intent"].nunique() < 2:
    raise ValueError("At least two different intents are required.")

print(f"Total training examples: {len(df)}")
print(f"Number of intent categories: {df['intent'].nunique()}")

print("\nExamples per intent:")
print(df["intent"].value_counts().sort_index())


# 3. Separate messages and labels
X = df["text"]
y = df["intent"]


# 4. Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)

print(f"\nTraining examples: {len(X_train)}")
print(f"Testing examples: {len(X_test)}")


# 5. Build the machine learning pipeline
model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            sublinear_tf=True
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=2000,
            class_weight="balanced",
            random_state=42
        )
    )
])


# 6. Train the classifier
print("\nTraining chatbot intent classifier...")

model.fit(X_train, y_train)

print("Training completed successfully.")


# 7. Evaluate the model on unseen test examples
predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("\n===== CHATBOT MODEL EVALUATION =====")
print(f"Accuracy: {accuracy:.4f}")
print(f"Accuracy percentage: {accuracy * 100:.2f}%")

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        predictions,
        zero_division=0
    )
)


# 8. Save the trained model
MODEL_DIR.mkdir(parents=True, exist_ok=True)

joblib.dump(model, MODEL_FILE)

print("\n===== MODEL SAVING =====")
print(f"Model saved successfully: {MODEL_FILE}")
