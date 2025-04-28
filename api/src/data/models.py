from sqlalchemy import Column, DateTime, Integer, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ForwardCurve(Base):
    __tablename__ = "forward_curve"

    index = Column(Integer, primary_key=True)
    reset_date = Column(DateTime(timezone=False))
    market_expectations = Column(Float(precision=6))
