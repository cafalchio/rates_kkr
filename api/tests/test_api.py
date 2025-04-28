from fastapi.testclient import TestClient
import unittest
from sqlalchemy import create_engine
from datetime import date
from unittest.mock import patch
from data.models import Base, ForwardCurve
from app import app
from data.database import session, engine_db


def create_memory_database_engine(*args):
    return create_engine("sqlite:///:memory:")


class TestApi(unittest.TestCase):
    @patch("data.database.create_engine", new=create_memory_database_engine)
    def setUp(self):
        engine_db.dispose()
        self.client = TestClient(app)
        # I think there is a better way to do it instead of dropping and create table
        ForwardCurve.__table__.drop(engine_db)
        Base.metadata.create_all(engine_db)
        return super().setUp()

    def tearDown(self):
        del self.client
        return super().tearDown()

    def test_forward_rates(self):
        mock_forward_curve = [
            ForwardCurve(
                index=0,
                reset_date=date(year=2025, month=1, day=1),
                market_expectations=0.015,
            ),
            ForwardCurve(
                index=1,
                reset_date=date(year=2025, month=2, day=1),
                market_expectations=0.0175,
            ),
            ForwardCurve(
                index=2,
                reset_date=date(year=2025, month=3, day=1),
                market_expectations=0.02,
            ),
        ]
        mock_post_data = {
            "maturity_date": "2025-03-01",
            "reference_rate": "SOFR",
            "rate_floor": 0.02,
            "rate_ceiling": 0.10,
            "rate_spread": 0.02,
        }
        expected_response = [
            {"date": "2025-01-01", "rate": "0.035"},
            {"date": "2025-02-01", "rate": "0.0375"},
        ]
        session.add_all(mock_forward_curve)
        session.commit()
        response = self.client.post("/forward_rates", json=mock_post_data)
        assert response.status_code == 200
        assert response.json() == expected_response

    def test_forward_rates_no_ceiling_or_floor(self):
        mock_forward_curve = [
            ForwardCurve(
                index=0,
                reset_date=date(year=2025, month=1, day=1),
                market_expectations=0.015,
            ),
            ForwardCurve(
                index=1,
                reset_date=date(year=2025, month=2, day=1),
                market_expectations=0.0175,
            ),
            ForwardCurve(
                index=2,
                reset_date=date(year=2025, month=3, day=1),
                market_expectations=0.02,
            ),
        ]
        mock_post_data = {
            "maturity_date": "2025-03-01",
            "reference_rate": "SOFR",
            "rate_spread": 0.02,
        }
        expected_response = [
            {"date": "2025-01-01", "rate": "0.035"},
            {"date": "2025-02-01", "rate": "0.0375"},
        ]
        session.add_all(mock_forward_curve)
        session.commit()
        response = self.client.post("/forward_rates", json=mock_post_data)
        assert response.status_code == 200
        assert response.json() == expected_response

    def test_forward_rates_no_data(self):
        mock_post_data = {
            "maturity_date": "2025-03-01",
            "reference_rate": "SOFR",
            "rate_floor": 0.02,
            "rate_ceiling": 0.10,
            "rate_spread": 0.02,
        }
        expected_response = []
        response = self.client.post("/forward_rates", json=mock_post_data)
        assert response.status_code == 200
        assert response.json() == expected_response

    def test_forward_rates_no_maturity_date(self):
        mock_post_data = {
            "reference_rate": "SOFR",
            "rate_floor": 0.02,
            "rate_ceiling": 0.10,
            "rate_spread": 0.02
        }
        response = self.client.post("/forward_rates", json=mock_post_data)
        assert response.status_code == 422

    def test_forward_rates_no_maturity_rate_spread(self):
        mock_post_data = {
            "maturity_date": "2025-03-01",
            "reference_rate": "SOFR",
            "rate_floor": 0.02,
            "rate_ceiling": 0.10,
        }
        response = self.client.post("/forward_rates", json=mock_post_data)
        assert response.status_code == 422

    def test_forward_rates_maturity_in_the_past(self):
        mock_forward_curve = [
            ForwardCurve(
                index=0,
                reset_date=date(year=2025, month=1, day=1),
                market_expectations=0.015,
            ),
            ForwardCurve(
                index=1,
                reset_date=date(year=2025, month=2, day=1),
                market_expectations=0.0175,
            ),
            ForwardCurve(
                index=2,
                reset_date=date(year=2025, month=3, day=1),
                market_expectations=0.02,
            ),
        ]
        mock_post_data = {
            "maturity_date": "2024-03-01",
            "reference_rate": "SOFR",
            "rate_floor": 0.02,
            "rate_ceiling": 0.10,
            "rate_spread": 0.02,
        }
        expected_response = [
            {"date": "2025-01-01", "rate": "0.035"},
            {"date": "2025-02-01", "rate": "0.0375"},
        ]
        session.add_all(mock_forward_curve)
        session.commit()
        response = self.client.post("/forward_rates", json=mock_post_data)
        expected_response = []
        assert response.status_code == 200
        assert response.json() == expected_response