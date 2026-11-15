"""Rule-based competitive price recommendations.

Uses manually captured competitor prices and a minimum gross margin.
It does not assume competitor prices are current or predict price elasticity.
"""
from decimal import Decimal, InvalidOperation, ROUND_CEILING, ROUND_HALF_UP
from typing import Iterable

CENT = Decimal("0.01")


def _money(value, field_name):
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        raise ValueError(f"{field_name} must be a valid number.") from None
    if not amount.is_finite() or amount < 0:
        raise ValueError(f"{field_name} must be finite and non-negative.")
    return amount


def _round_money(value):
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


def _normalise_competitors(competitor_prices: Iterable):
    normalised = []
    if competitor_prices is None:
        return normalised
    for index, competitor in enumerate(competitor_prices, start=1):
        if isinstance(competitor, dict):
            name = str(competitor.get("name") or f"Competitor {index}").strip()
            raw_price = competitor.get("price")
        else:
            name = f"Competitor {index}"
            raw_price = competitor
        if not name:
            name = f"Competitor {index}"
        price = _money(raw_price, f"{name} price")
        if price <= 0:
            raise ValueError(f"{name} price must be greater than zero.")
        normalised.append({"name": name, "price": _round_money(price)})
    return normalised


def recommend_price(
    cost_price,
    current_price,
    competitor_prices=None,
    minimum_margin_percent=15,
    undercut_amount=0.01,
):
    """Return a price recommendation while protecting the gross-margin floor.

    Gross margin = (selling price - cost price) / selling price.
    When feasible, the target is one cent below the lowest captured
    competitor price. If that target breaches the margin floor, the engine
    retains a profitable current price and explains why it cannot undercut.
    """
    cost = _money(cost_price, "Cost price")
    current = _money(current_price, "Current selling price")
    undercut = _money(undercut_amount, "Undercut amount")
    try:
        margin = Decimal(str(minimum_margin_percent))
    except (InvalidOperation, TypeError, ValueError):
        raise ValueError("Minimum margin must be a valid percentage.") from None

    if not margin.is_finite() or margin < 0 or margin >= 100:
        raise ValueError("Minimum margin must be at least 0 and below 100 percent.")
    if cost <= 0:
        raise ValueError("Cost price must be greater than zero.")
    if current <= 0:
        raise ValueError("Current selling price must be greater than zero.")
    if undercut <= 0:
        raise ValueError("Undercut amount must be greater than zero.")

    competitors = _normalise_competitors(competitor_prices)
    margin_floor = (cost / (Decimal("1") - margin / Decimal("100"))).quantize(
        CENT, rounding=ROUND_CEILING
    )
    lowest = min((item["price"] for item in competitors), default=None)

    recommended = current
    status = "NO_COMPETITOR_DATA"
    reason = (
        "No competitor prices were supplied. The current price is retained "
        "unless it falls below the minimum price required by the margin rule."
    )

    if lowest is not None:
        target = _round_money(lowest - undercut)
        if target >= margin_floor:
            recommended = max(margin_floor, min(current, target))
            if current < margin_floor:
                status = "MARGIN_FLOOR_PRICE_INCREASE"
                reason = (
                    "The current price is below the required margin floor. "
                    "The recommendation raises it to the minimum profitable "
                    "price while remaining below the lowest captured competitor."
                )
            elif recommended < current and recommended < lowest:
                status = "UNDERCUT_RECOMMENDED"
                reason = (
                    f"The recommendation is below the lowest captured competitor "
                    f"price of R{lowest:.2f} and meets the {margin}% minimum gross margin."
                )
            else:
                status = "PRICE_ALREADY_COMPETITIVE"
                reason = (
                    "The current price is already at or below the competitive "
                    "target and meets the minimum gross margin."
                )
        elif current < margin_floor:
            recommended = margin_floor
            status = "MARGIN_FLOOR_PRICE_INCREASE"
            reason = (
                f"Undercutting the lowest captured competitor price of R{lowest:.2f} "
                "would breach the minimum gross margin. The current price is "
                "also below the required minimum, so it is raised to the margin floor."
            )
        else:
            recommended = current
            status = "CANNOT_UNDERCUT_PROFITABLY"
            reason = (
                f"The lowest captured competitor price of R{lowest:.2f} is too "
                f"low to undercut while maintaining the {margin}% minimum gross "
                "margin. The current price is retained."
            )
    elif current < margin_floor:
        recommended = margin_floor
        status = "MARGIN_FLOOR_PRICE_INCREASE"
        reason = (
            "The current price is below the minimum price required by the "
            "gross-margin rule. No competitor prices were supplied."
        )

    recommended = _round_money(recommended)
    gross_profit = _round_money(recommended - cost)
    gross_margin = (
        (recommended - cost) / recommended * Decimal("100")
    ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    return {
        "status": status,
        "currency": "ZAR",
        "cost_price": float(_round_money(cost)),
        "current_price": float(_round_money(current)),
        "recommended_price": float(recommended),
        "minimum_price_for_margin": float(margin_floor),
        "minimum_margin_percent": float(margin),
        "gross_profit_per_unit": float(gross_profit),
        "gross_margin_percent": float(gross_margin),
        "lowest_competitor_price": float(lowest) if lowest is not None else None,
        "competitor_count": len(competitors),
        "competitors": [
            {"name": item["name"], "price": float(item["price"])}
            for item in competitors
        ],
        "reason": reason,
        "data_note": (
            "Competitor prices are manually supplied observations. Confirm "
            "they refer to the same product size and are still current."
        ),
    }


def format_recommendation(result):
    """Format a recommendation for terminal or chatbot display."""
    lines = [
        "COMPETITIVE PRICE RECOMMENDATION",
        f"Status: {result['status']}",
        f"Current selling price: R{result['current_price']:.2f}",
        f"Recommended selling price: R{result['recommended_price']:.2f}",
        f"Minimum price for required margin: R{result['minimum_price_for_margin']:.2f}",
        f"Gross profit per unit: R{result['gross_profit_per_unit']:.2f}",
        f"Gross margin: {result['gross_margin_percent']:.2f}%",
    ]
    if result["lowest_competitor_price"] is not None:
        lines.append(
            f"Lowest captured competitor price: R{result['lowest_competitor_price']:.2f}"
        )
    else:
        lines.append("Competitor prices: Not supplied")
    lines.extend(["", f"Reason: {result['reason']}", f"Note: {result['data_note']}"])
    return "\n".join(lines)
