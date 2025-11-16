from typing import TypedDict, NotRequired


class WorkshopRow(TypedDict):
    id: str
    production_capacity: float
    production_cost: float


class ClientRow(TypedDict):
    id: str
    demand: float


class RouteRow(TypedDict):
    origin: str
    destination: str
    transport_cost: float
    transport_capacity: float
    is_active: bool
    id: NotRequired[str]  # if sometimes present


class DataDict(TypedDict):
    workshops: list[WorkshopRow]
    clients: list[ClientRow]
    routes: list[RouteRow]
