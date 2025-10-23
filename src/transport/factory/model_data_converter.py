import json

from transport.factory.types import DataDict


class Converter:

    def __init__(self):
        pass

    @staticmethod
    def from_json(file: str) -> DataDict:
        with open(file, "r", encoding="utf-8") as f:
            data: DataDict = json.load(f)
        return data

    @staticmethod
    def from_excel(file: str) -> DataDict:
        import pandas as pd

        workshops = pd.read_excel(file, sheet_name="Workshops").to_dict("records")
        clients = pd.read_excel(file, sheet_name="Clients").to_dict("records")
        routes = pd.read_excel(file, sheet_name="Routes").to_dict("records")

        data: DataDict = {
            "Workshops": workshops,
            "Clients": clients,
            "Routes": routes,
        }
        return data
