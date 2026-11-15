# Competitive Price Intelligence and Recommendation

## Purpose

The pricing feature compares a shop's selling price with manually captured
prices from nearby competitors. It recommends a price that can undercut the
lowest observed competitor price when doing so still meets the shop's
minimum gross margin requirement.

## Current implementation

The first version uses a transparent rule-based pricing engine. It does not
use an unverified machine-learning model or claim to predict customer
response to a price change.

The user supplies the product cost price, current selling price, minimum
gross margin percentage and competitor prices. The engine calculates the
minimum selling price required to meet the margin floor. If possible, it
recommends a price one cent below the lowest captured competitor price.
It never recommends an undercut that violates the margin floor.

## Gross margin calculation

Gross margin = ((Selling Price - Cost Price) / Selling Price) * 100

Minimum selling price = Cost Price / (1 - Minimum Margin Percentage / 100)

The minimum price is rounded upward to the next cent so the required margin
is not accidentally breached by rounding.

## Running the feature

From the repository root, run:

    python application/backend/pricing/cli.py

Enter the cost price, current selling price, required margin and competitor
prices. Competitor prices should refer to the same product size, brand and
packaging. Leave the competitor field blank when no reliable comparison is
available.

The backend function can also be imported by other Retail-X-AI components:

    from application.backend.pricing import recommend_price

## Example

The following values are illustrative only:

- Cost price: R28.00
- Current selling price: R35.00
- Competitor prices: R34.00 and R33.50
- Minimum gross margin: 15%

The lowest competitor price is R33.50. The rule-based recommendation is
R33.49, which is below the captured competitor price and remains above the
minimum price required by the margin rule.

## Data and limitations

- Competitor prices are manually entered observations in this first version.
- The project does not currently perform live competitor price monitoring.
- The dataset's Competitor Pricing field is not treated as a verified current
  price for a named nearby shop.
- Cost prices must be supplied by the shop because the historical dataset
  does not provide verified purchase costs for each product.
- The comparison assumes equivalent product size and packaging and a current
  competitor observation.
- The rule does not estimate price elasticity, sales volume changes or total
  profit after a price change. A future model would require shop-specific
  records containing changing selling prices, costs and resulting sales.

## Tests

Run the unit tests from the repository root:

    python -m unittest discover -s python-ai/tests -p "test_pricing_service.py" -v

The tests cover profitable undercutting, margin protection, missing
competitor data, already competitive prices, named competitor records and
invalid input.
