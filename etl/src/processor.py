import pandas as pd
import openpyxl
import requests

class PensfordProcessor:
    data = None

    def __init__(self, config):
        raw_data = self.load()
        self.data = self.proccess(raw_data)

    def load(self):
        pass

    def process(self):
        pass
