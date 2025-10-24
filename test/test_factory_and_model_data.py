import os

import pytest

from transport.context import ModelData
from transport.factory import ModelDataFactory


PATH = os.path.abspath(__file__)


class TestFactoryAndModelData:
    @pytest.fixture(scope="class")
    def model_data(self) -> ModelData:
        return ModelDataFactory.from_json(
            file=PATH + "data/test_data_and_data_factory.json"
        )

    def test_workshops(self, model_data: ModelData) -> None:
        workshop1 = model_data.workshops_by_id["Workshop1"]
        assert workshop1.id_ == "Workshop1"
        assert workshop1.production_capacity == 97.0
        assert workshop1.production_cost == 20.0

        workshop2 = model_data.workshops_by_id["Workshop2"]
        assert workshop2.id_ == "Workshop2"
        assert workshop2.production_capacity == 55.0
        assert workshop2.production_cost == 25.0

        workshop3 = model_data.workshops_by_id["Workshop3"]
        assert workshop3.id_ == "Workshop3"
        assert workshop3.production_capacity == 160.0
        assert workshop3.production_cost == 18.0

    def test_clients(self, model_data: ModelData) -> None:
        client1 = model_data.clients_by_id["Client1"]
        assert client1.id_ == "Client1"
        assert client1.demand == 91.0

        client2 = model_data.clients_by_id["Client2"]
        assert client2.id_ == "Client2"
        assert client2.demand == 63.0

        client3 = model_data.clients_by_id["Client3"]
        assert client3.id_ == "Client3"
        assert client3.demand == 74.0

    def test_routes(self, model_data: ModelData) -> None:
        route11 = model_data.routes_by_id["Route11"]
        assert route11.origin == "Workshop1"
        assert route11.destination == "Client1"
        assert route11.transport_cost == 12.0
        assert route11.transport_capacity == 15.0
        assert route11.is_active

        route12 = model_data.routes_by_id["Route12"]
        assert route12.origin == "Workshop1"
        assert route12.destination == "Client2"
        assert route12.transport_cost == 11.0
        assert route12.transport_capacity == 16.0
        assert not (route12.is_active)

        route13 = model_data.routes_by_id["Route13"]
        assert route13.origin == "Workshop1"
        assert route13.destination == "Client3"
        assert route13.transport_cost == 14.0
        assert route13.transport_capacity == 17.0
        assert route13.is_active

        route21 = model_data.routes_by_id["Route21"]
        assert route21.origin == "Workshop2"
        assert route21.destination == "Client1"
        assert route21.transport_cost == 15.0
        assert route21.transport_capacity == 10.0
        assert not (route21.is_active)

        route22 = model_data.routes_by_id["Route22"]
        assert route22.origin == "Workshop2"
        assert route22.destination == "Client2"
        assert route22.transport_cost == 12.0
        assert route22.transport_capacity == 17.0
        assert route22.is_active

        route23 = model_data.routes_by_id["Route23"]
        assert route23.origin == "Workshop2"
        assert route23.destination == "Client3"
        assert route23.transport_cost == 12.0
        assert route23.transport_capacity == 17.0
        assert route23.is_active

        route31 = model_data.routes_by_id["Route31"]
        assert route31.origin == "Workshop3"
        assert route31.destination == "Client1"
        assert route31.transport_cost == 9.0
        assert route31.transport_capacity == 14.0
        assert not (route31.is_active)

        route32 = model_data.routes_by_id["Route32"]
        assert route32.origin == "Workshop3"
        assert route32.destination == "Client2"
        assert route32.transport_cost == 18.0
        assert route32.transport_capacity == 19.0
        assert route32.is_active

        route33 = model_data.routes_by_id["Route33"]
        assert route33.origin == "Workshop3"
        assert route33.destination == "Client3"
        assert route33.transport_cost == 17.0
        assert route33.transport_capacity == 14.0
        assert route33.is_active
