from collections.abc import Collection

from pydantic import BaseModel, ValidationInfo, field_validator, model_validator

from transport.context.objects import Client, Route, Workshop
from transport.context.objects.validation_utils import (
    HasId,
    check_unique_ids,
    assert_min_count,
    assert_min_active_routes,
    assert_route_endpoints_exist,
    assert_unique_route_pairs,
)


class ModelData(BaseModel):
    def __init__(self) -> None:
        super().__init__()
        self.__workshops: list[Workshop] = list()
        self.__workshops_by_id: dict[str, Workshop] = dict()
        self.__clients: list[Client] = list()
        self.__clients_by_id: dict[str, Client] = dict()
        self.__routes: list[Route] = list()
        self.__routes_by_id: dict[str, Route] = dict()

    @property
    def workshops(self) -> list[Workshop]:
        return self.__workshops

    @workshops.setter
    def workshops(self, workshops: list[Workshop]) -> None:
        self.__workshops = workshops
        self.__workshops_by_id = {workshop.id_: workshop for workshop in self.workshops}

    @property
    def workshops_by_id(self) -> dict[str, Workshop]:
        return self.__workshops_by_id

    @property
    def clients(self) -> list[Client]:
        return self.__clients

    @clients.setter
    def clients(self, clients: list[Client]) -> None:
        self.__clients = clients
        self.__clients_by_id = {client.id_: client for client in self.clients}

    @property
    def clients_by_id(self) -> dict[str, Client]:
        return self.__clients_by_id

    @property
    def routes(self) -> list[Route]:
        return self.__routes

    @routes.setter
    def routes(self, routes: list[Route]) -> None:
        self.__routes = routes
        self.__routes_by_id = {route.id_: route for route in self.routes}

    @property
    def routes_by_id(self) -> dict[str, Route]:
        return self.__routes_by_id

    @field_validator("workshops", "clients", "routes")
    def no_duplicate_ids(cls, objects_with_id: Collection[HasId], info: ValidationInfo):
        check_unique_ids(objects_with_id, info.field_name or "unknown")
        return objects_with_id

    @model_validator(mode="after")
    def cross_checks(self):
        # existence
        assert_min_count(self.workshops, "workshop")
        assert_min_count(self.clients, "client")
        assert_min_active_routes(self.routes, 1)

        # references & duplicates across routes
        w_ids = {w.id_ for w in self.workshops}
        c_ids = {c.id_ for c in self.clients}
        assert_route_endpoints_exist(self.routes, w_ids, c_ids)
        assert_unique_route_pairs(self.routes)

        return self
