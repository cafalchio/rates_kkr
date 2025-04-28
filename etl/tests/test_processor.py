from unittest.mock import patch
import pandas as pd


from processor.pensford_processor import PensfordProcessor


class mockResponse:
    status_code = 200
    content = "dummy_data"

    def raise_for_status(self):
        return self.status_code


def mocked_get_request(*args, **kwargs):
    return mockResponse()


def mock_pd_read_excel(*args, **kwargs):
    dummy_data = pd.DataFrame(
        columns=["Unnamed", "dummy1", "dummy2"],
        data=[[None, "2/10/2020", "1"], [None, None, None]],
    )
    return dummy_data


@patch("processor.pensford_processor.requests.get", mocked_get_request)
@patch("processor.pensford_processor.pd.read_excel", mock_pd_read_excel)
def test_pensford_processor_load():
    expected_df = pd.DataFrame(
        columns=["dummy1", "dummy2"],
        data=[["2/10/2020", "1"]],
    )
    processor = PensfordProcessor()
    pd.testing.assert_frame_equal(left=expected_df, right=processor.data)
