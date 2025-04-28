from data.models import ForwardCurve as Fc
from datetime import date
from data.database import session


def calculate_rate(reference_rate, rate_spread, rate_floor, rate_ceiling):
    """
    Calculate the interest based on the forward curve rate spread,
    rate floor and rate ceiling.
    reference_rate + rate_spread between the ceiling and floor
    """
    return min(rate_ceiling, max(reference_rate + rate_spread, rate_floor))


def get_calculated_rates(
    maturity_date,
    rate_floor,
    rate_ceiling,
    rate_spread,
):
    curve_data = (
        session.query(Fc.market_expectations, Fc.reset_date)
        .filter(Fc.reset_date.between(date.today().day, maturity_date))
        .all()
    )
    if curve_data:
        return [
            {
                "date": data[1].strftime("%Y-%m-%d"),
                "rate": f"{calculate_rate(data[0], rate_spread, rate_floor, rate_ceiling):.5}",
            }
            for data in curve_data
        ]
    else:
        return []
