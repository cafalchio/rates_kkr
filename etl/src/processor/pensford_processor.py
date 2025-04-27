import pandas as pd
import requests
import logging
from config.config_parser import config

logger = logging.getLogger(__name__)


class DownloadDataError(Exception):
    pass


class PensfordProcessor:
    data = None

    def __init__(self):
        raw_data = self._load()
        self.data = self._process(raw_data)

    def _load(self):
        logger.info("Download data from Pensford")
        try:
            requested = requests.get(config.get("PENSFORD_URL"), allow_redirects=True)
        except requests.HTTPError:
            raise DownloadDataError("Error downloading data from Pensford")
        logger.info(f"Response: {requested.status_code}")
        requested.raise_for_status()
        return requested.content

    def _process(self, raw_data):
        logger.info("Processing data")
        df = pd.read_excel(raw_data, skiprows=2, date_format="%d/%m/%YYYY")
        df = df.dropna(axis="columns", how="all")
        df = df.dropna(axis="rows", how="all")
        df = df[[col for col in df.columns if "Unnamed" not in col]]
        df.columns = df.columns.str.replace(" ", "_").str.lower()
        return df.iloc[:, :2]

    def save_data(self):
        with config.db_engine.connect() as conn:
            # TODO: Fix to not block read, perhaps create the model?
            self.data.to_sql(name="forward_curve", con=conn, if_exists="replace")
            logger.info("Data saved to database")
