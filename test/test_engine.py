from pathlib import Path

from transport.context import ModelData
from transport.engine import Engine
from transport.factory import ModelDataFactory

PATH = Path(__file__).parent


class TestEngine:
    def create_model_data(self, test_path: str) -> ModelData:
        return ModelDataFactory.from_json(PATH / "data/test_engine" / test_path)

    def test_engine_constr_workshop_capacity(self) -> None:
        """
        Test that the engine respects workshop capacity constraints.

        The test verifies that total transported from workshop doesn't exceed capacity.
        Expected result: 50.0 to Client1 + 50.0 to Client2 = 100.0 total
        """
        model_data = self.create_model_data("test_engine_constr_workshop_capacity.json")
        Engine(model_data, "cbc").run()

        # Get total transported from Workshop1
        total_from_workshop1 = sum(
            qty
            for route, qty in model_data.transport_quantity.items()
            if route.origin == "Workshop1"
        )

        # Total should equal workshop capacity (100.0)
        assert total_from_workshop1 == 100.0

        # Also verify individual routes meet client demands
        route1 = model_data.routes_by_id["Workshop1,Client1"]
        route2 = model_data.routes_by_id["Workshop1,Client2"]
        assert model_data.transport_quantity[route1] == 50.0
        assert model_data.transport_quantity[route2] == 50.0

    def test_engine_workshop_capacity_respected(self) -> None:
        """
        Test that workshop capacity is respected across multiple routes.

        Workshop1 has capacity 100, but 2 routes each capable of 100.
        Total transported should be <= 100, not 200.
        """
        model_data = self.create_model_data("test_engine_constr_workshop_capacity.json")
        Engine(model_data, "cbc").run()

        # Get total transported from Workshop1
        total_from_workshop1 = sum(
            qty
            for route, qty in model_data.transport_quantity.items()
            if route.origin == "Workshop1"
        )

        # Should be <= workshop capacity
        assert total_from_workshop1 <= 100.0, (
            f"Workshop1 produced {total_from_workshop1} exceeding capacity of 100.0"
        )

    def test_engine_constr_client_demand(self) -> None:
        """
        Test that the engine respects client demand constraints.

        The test verifies that transported quantity does not exceed client demand.
        Expected result: transport_quantity = 10.0 (matching client demand)
        """
        model_data = self.create_model_data("test_engine_constr_client_demand.json")
        Engine(model_data, "cbc").run()

        route = model_data.routes_by_id["Workshop1,Client1"]

        assert model_data.transport_quantity[route] == 10.0





