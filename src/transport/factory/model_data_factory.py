from __future__ import annotations

from pathlib import Path

from transport.context.model_data import ModelData
from transport.context.objects import Client, Route, Workshop
from transport.factory.model_data_converter import Converter, DataDict
from transport.factory.types import ClientRow, RouteRow, WorkshopRow


class ModelDataFactory:
    def __init__(self):
        pass

    @staticmethod
    def from_json(file: str | "Path") -> ModelData:
        return ModelDataFactory()._create_model_data(Converter.from_json(file))

    @staticmethod
    def from_excel(file: str) -> ModelData:
        return ModelDataFactory()._create_model_data(Converter.from_excel(file))

    def _create_model_data(self, data_dict: DataDict) -> ModelData:
        workshops = [
            Workshop(
                id_=w["id"],
                production_capacity=float(w["production_capacity"]),
                production_cost=float(w["production_cost"]),
            )
            for w in data_dict.get("workshops", [])
        ]

        clients = [
            Client(
                id_=c["id"],
                demand=float(c["demand"]),
            )
            for c in data_dict.get("clients", [])
        ]

        routes = [
            Route(
                # id_=r["id"],
                origin=r["origin"],
                destination=r["destination"],
                transport_cost=float(r["transport_cost"]),
                transport_capacity=float(r["transport_capacity"]),
                min_transport_quantity=float(r["min_transport_quantity"]),
                is_active=bool(r.get("is_active", True)),
            )
            for r in data_dict.get("routes", [])
        ]

        return ModelData(workshops=workshops, clients=clients, routes=routes)

    def _create_workshops(self, data_dict: DataDict) -> list[Workshop]:
        workshop_dicts_list: list[WorkshopRow] = data_dict["Workshops"]
        workshops: list[Workshop] = []
        for workshop_dict in workshop_dicts_list:
            workshops.append(
                Workshop(
                    id_=workshop_dict["id"],
                    production_capacity=workshop_dict["production_capacity"],
                    production_cost=workshop_dict["production_cost"],
                )
            )
        return workshops

    def _create_clients(self, data_dict: DataDict) -> list[Client]:
        client_dicts_list: list[ClientRow] = data_dict["Clients"]
        clients: list[Client] = []
        for client_dict in client_dicts_list:
            clients.append(
                Client(
                    id_=client_dict["id"],
                    demand=client_dict["demand"],
                )
            )
        return clients

    def _create_routes(self, data_dict: DataDict) -> list[Route]:
        route_dicts_list: list[RouteRow] = data_dict["Routes"]
        routes: list[Route] = []
        for route_dict in route_dicts_list:
            routes.append(
                Route(
                    origin=route_dict["origin"],
                    destination=route_dict["destination"],
                    transport_cost=route_dict["transport_cost"],
                    transport_capacity=route_dict["transport_capacity"],
                    min_transport_quantity=route_dict["min_transport_quantity"],
                    is_active=route_dict["is_active"],
                )
            )
        return routes
