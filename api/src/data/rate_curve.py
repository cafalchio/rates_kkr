import numpy as np
from sqlalchemy.orm import Session
from data.models import ForwardCurve as Fc
from data.database import engine_db

from datetime import date

def calculate_rate(reference_rate, rate_spread, rate_floor, rate_ceiling):
    return min(rate_ceiling, max(reference_rate + rate_spread, rate_floor))

def calculate_rates(
        maturity_date = date(2025, 10, 10),
        rate_floor = 1,
        rate_ceiling = 10,
        rate_spread = 2,
        ):
    with Session(engine_db) as session:
        curve_data = session.query(
            Fc.market_expectations, Fc.reset_date
            ).filter(Fc.reset_date.between(date.today(), maturity_date)).all()
        if curve_data:
            print([{
                "date": data[1].strftime("%Y-%m-%d"), 
                "rate": calculate_rate(data[0], rate_spread, rate_floor, rate_ceiling)
                } for data in curve_data])
        else:
            return {}


if __name__ == "__main__":
    calculate_rates()