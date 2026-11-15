"""Interactive terminal entry point for competitive price recommendations."""
from service import format_recommendation, recommend_price


def _read_positive_amount(prompt):
    while True:
        try:
            amount = float(input(prompt).strip())
            if amount <= 0:
                raise ValueError
            return amount
        except ValueError:
            print("Please enter an amount greater than zero.")


def main():
    print("=" * 56)
    print("RETAIL-X-AI COMPETITIVE PRICE RECOMMENDATIONS")
    print("=" * 56)
    print("Use prices for the same product size and packaging.\n")

    cost = _read_positive_amount("Product cost price (R): ")
    current = _read_positive_amount("Current selling price (R): ")
    margin_text = input("Minimum gross margin percentage [15]: ").strip()
    try:
        margin = float(margin_text) if margin_text else 15.0
    except ValueError:
        print("Please enter a valid margin percentage.")
        return

    competitor_text = input(
        "Competitor prices in rand, separated by commas (blank if unknown): "
    ).strip()
    competitors = []
    if competitor_text:
        try:
            competitors = [float(value.strip()) for value in competitor_text.split(",")]
            if any(value <= 0 for value in competitors):
                raise ValueError
        except ValueError:
            print("Enter valid competitor prices greater than zero.")
            return

    try:
        result = recommend_price(
            cost_price=cost,
            current_price=current,
            competitor_prices=competitors,
            minimum_margin_percent=margin,
        )
    except ValueError as error:
        print(f"Unable to calculate recommendation: {error}")
        return

    print()
    print(format_recommendation(result))


if __name__ == "__main__":
    main()
