from fastapi import FastAPI
from fastapi.responses import JSONResponse
from data.rate_curve import get_calculated_rates
from data.schemas import RateInput

app = FastAPI(tile="Float rate calculator")


@app.post(
    "/forward_rates",
    response_description="Calculate rate based on SOFR rate rerefence",
)
def forward_rates(input: RateInput):
    rates = get_calculated_rates(
        maturity_date=input.maturity_date,
        rate_floor=input.rate_floor,
        rate_ceiling=input.rate_ceiling,
        rate_spread=input.rate_spread,
    )
    return JSONResponse(content=rates)
