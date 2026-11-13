
import pandas as pd
from pathlib import Path


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASET_PATH = (
    PROJECT_ROOT
    / "dataset"
    / "supplier"
    / "processed"
    / "supplier_recommendation_data.csv"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "dataset"
    / "supplier"
    / "processed"
    / "supplier_recommendations.csv"
)


# Recommendation weights
LEAD_TIME_WEIGHT = 0.50
MOQ_WEIGHT = 0.30
SUPPLY_FREQUENCY_WEIGHT = 0.20


def load_supplier_data():
    """Load eligible supplier and product relationships."""

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Supplier dataset not found: {DATASET_PATH}"
        )

    df = pd.read_csv(DATASET_PATH)

    required_columns = [
        "product_id",
        "product_name",
        "supplier_id",
        "supplier_name",
        "lead_time_days",
        "minimum_order_quantity",
        "supply_frequency_days"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    return df


def calculate_metric_score(values):
    """
    Calculate an inverse min-max score.
    Lower values receive higher scores.
    """

    minimum = values.min()
    maximum = values.max()

    if maximum == minimum:
        return pd.Series(1.0, index=values.index)

    return (maximum - values) / (maximum - minimum)



def recommend_suppliers(df):
    """Rank eligible suppliers separately for each product."""

    results = []

    for product_id, group in df.groupby("product_id"):

        group = group.copy()

        # Calculate individual supplier scores
        group["lead_time_score"] = calculate_metric_score(
            group["lead_time_days"]
        )

        group["moq_score"] = calculate_metric_score(
            group["minimum_order_quantity"]
        )

        group["supply_frequency_score"] = calculate_metric_score(
            group["supply_frequency_days"]
        )

        # Calculate weighted recommendation score
        group["recommendation_score"] = (
            group["lead_time_score"] * LEAD_TIME_WEIGHT
            + group["moq_score"] * MOQ_WEIGHT
            + group["supply_frequency_score"]
            * SUPPLY_FREQUENCY_WEIGHT
        ) * 100

        # Rank suppliers
        group = group.sort_values(
            by="recommendation_score",
            ascending=False
        )

        # Identify products with only one supplier
        if len(group) == 1:

            group["recommendation_status"] = (
                "ONLY_AVAILABLE_SUPPLIER"
            )

            group["recommendation_score"] = float("nan")

        else:

            group["recommendation_status"] = (
                "COMPARED_SUPPLIER"
            )

        group["rank"] = range(1, len(group) + 1)

        results.append(group)

    if not results:
        return pd.DataFrame()

    return pd.concat(results, ignore_index=True)

def main():

    print("===== SUPPLIER RECOMMENDATION SYSTEM =====")

    df = load_supplier_data()

    print(f"Supplier relationships loaded: {len(df)}")
    print(f"Unique products: {df['product_id'].nunique()}")
    print(f"Unique suppliers: {df['supplier_id'].nunique()}")

    recommendations = recommend_suppliers(df)

    recommendations.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print("\n===== RECOMMENDATION RESULTS =====")

    print(
        recommendations[
            [
                "product_id",
                "product_name",
                "supplier_name",
                "recommendation_score",
                "rank",
                "recommendation_status"
            ]
        ].head(15).to_string(index=False)
    )

    print("\n===== SYSTEM SUMMARY =====")

    print(
        "Products processed:",
        recommendations["product_id"].nunique()
    )

    print(
        "Supplier recommendations generated:",
        len(recommendations)
    )

    print(
        "Products with multiple suppliers:",
        (
            recommendations.groupby("product_id").size() > 1
        ).sum()
    )

    print("\nResults saved to:")
    print(OUTPUT_PATH)


if __name__ == "__main__":
    main()
