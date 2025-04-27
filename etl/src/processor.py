import pandas as pd
import requests
from src.config.config_parser import config

class PensfordProcessor:
    data = None

    def __init__(self):
        raw_data = self.load()
        self.data = self.process(raw_data)

    def load(self):
        requested = requests.get(config.get("PENSFORD_URL"), allow_redirects=True)
        requested.raise_for_status()
        return requested.content

    def process(self, raw_data):
        df = pd.read_excel(raw_data, skiprows=2, date_format="%d/%m/%YYYY")
        df = df.dropna(axis="columns", how="all")
        df = df.dropna(axis="rows", how="all")
        df = df[[col for col in df.columns if "Unnamed" not in col]]
        df.columns = df.columns.str.replace(" ", "_").str.lower()
        return df.iloc[:, :2]

if __name__ == "__main__":
    p = PensfordProcessor()