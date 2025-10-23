from transport.context.model_data import ModelData
from transport.context.objects import Workshop, Client, Route
from transport.factory.types import DataDict, WorkshopRow, ClientRow, RouteRow

from transport.factory.model_data_converter import Converter


class ModelDataFactory:
    def __init__(self):
        pass

    @staticmethod
    def from_json(file: str) -> ModelData:
        return ModelDataFactory()._create_model_data(Converter.from_json(file))
    
    @staticmethod
    def from_excel(file: str) -> ModelData:
        return ModelDataFactory()._create_model_data(Converter.from_excel(file))
    
    def _create_model_data(self, data_dict: DataDict) -> ModelData:

        model_data = ModelData()

        model_data.workshops = self._create_workshops(data_dict)
        model_data.clients = self._create_clients(data_dict)
        model_data.routes = self._create_routes(data_dict)

        return model_data

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
                    is_active=route_dict["is_active"],
                )
            )
        return routes
