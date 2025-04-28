from pydantic import BaseModel, Field, AfterValidator
from datetime import date

MAX_CEILING = 9999


def validate_libor_not_implemented(reference_rate):
    if reference_rate != "SOFR":
        raise ValueError("Only SOFR reference rate is available")
    return reference_rate


class RateInput(BaseModel):
    maturity_date: date = Field(examples=["2025-10-01"], description="Required: Maturity date of the loan")
    reference_rate: str | None = Field(default="SOFR", examples=["SOFR"], description="Only SOFR option available")
    rate_floor: float | None = Field(default=0, examples=[0.4])
    rate_ceiling: float | None = Field(default=MAX_CEILING, examples=[3.5])
    rate_spread: float = Field(examples=[1.8], description="Required: rate spread of the loan")
