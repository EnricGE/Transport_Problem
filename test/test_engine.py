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

    def test_engine_constr_client_demand_multiple_routes(self) -> None:
        """
        Test that the engine respects client demand constraints across multiple routes.

        The test verifies that transported quantity does not exceed client demand.
        Expected result: transport_quantity = 10.0 (matching client demand)
        """
        model_data = self.create_model_data(
            "test_engine_constr_client_demand_multiple_routes.json"
        )
        Engine(model_data, "cbc").run()

        route1 = model_data.routes_by_id["Workshop1,Client1"]
        route2 = model_data.routes_by_id["Workshop1,Client2"]

        assert model_data.transport_quantity[route1] == 10.0
        assert model_data.transport_quantity[route2] == 10.0

    def test_engine_constr_client_demand_multiple_workshops(self) -> None:
        """
        Test that the engine respects client demand constraints across multiple workshops.

        The test verifies that transported quantity does not exceed client demand.
        Expected result: transport_quantity = 10.0 (matching client demand)
        """
        model_data = self.create_model_data(
            "test_engine_constr_client_demand_multiple_workshops.json"
        )
        Engine(model_data, "cbc").run()

        route1 = model_data.routes_by_id["Workshop1,Client1"]
        route2 = model_data.routes_by_id["Workshop2,Client1"]

        assert model_data.transport_quantity[route1] == 20.0
        assert model_data.transport_quantity[route2] == 0.0

    def test_engine_constr_client_demand_multiple_workshops_and_routes(self) -> None:
        """
        Test that the engine respects client demand constraints across multiple workshops and routes.

        The test verifies that transported quantity does not exceed client demand.
        Expected result: transport_quantity = 10.0 (matching client demand)
        """
        model_data = self.create_model_data(
            "test_engine_constr_client_demand_multiple_workshops_and_routes.json"
        )
        Engine(model_data, "cbc").run()

        route1 = model_data.routes_by_id["Workshop1,Client1"]
        route2 = model_data.routes_by_id["Workshop2,Client1"]
        route3 = model_data.routes_by_id["Workshop1,Client2"]

        assert model_data.transport_quantity[route1] == 20.0
        assert model_data.transport_quantity[route2] == 0.0
        assert model_data.transport_quantity[route3] == 10.0

    def test_engine_constr_route_capacity(self) -> None:
        """
        Test that the engine respects route capacity constraints.

        The test verifies that transported quantity does not exceed route capacity.
        Expected result: transport_quantity = 10.0 (matching route capacity)
        """
        model_data = self.create_model_data("test_engine_constr_route_capacity.json")
        Engine(model_data, "cbc").run()

        route1 = model_data.routes_by_id["Workshop1,Client1"]
        route2 = model_data.routes_by_id["Workshop2,Client1"]
        route3 = model_data.routes_by_id["Workshop1,Client2"]

        assert model_data.transport_quantity[route1] == 10.0
        assert model_data.transport_quantity[route2] == 10.0
        assert model_data.transport_quantity[route3] == 10.0

    def test_engine_constr_min_transport_quantity(self) -> None:
        """
        Test that verifies that min transport quantity is respected.
        
        When a route is used (transport_quantity > 0), it must transport at least
        the minimum quantity. If min_transport_quantity is not met, the route
        should not be used at all (transport_quantity = 0).
        
        Expected: Route with min_transport_quantity=5 transports either 0 or >= 5
        """
        model_data = self.create_model_data(
            "test_engine_constr_min_transport_quantity.json"
        )
        Engine(model_data, "cbc").run()
    
        route1 = model_data.routes_by_id["Workshop1,Client1"]
        route2 = model_data.routes_by_id["Workshop2,Client1"]
    
        # Route1 has min_transport_quantity = 5.0
        # If route is used, must transport >= 5.0
        if model_data.transport_quantity[route1] > 0:
            assert model_data.transport_quantity[route1] >= 5.0, (
                f"Route1 transports {model_data.transport_quantity[route1]} "
                f"but min_transport_quantity is 5.0"
            )
        
        # Route2 has min_transport_quantity = 8.0
        # If route is used, must transport >= 8.0
        if model_data.transport_quantity[route2] > 0:
            assert model_data.transport_quantity[route2] >= 8.0, (
                f"Route2 transports {model_data.transport_quantity[route2]} "
                f"but min_transport_quantity is 8.0"
            )
        
        # Verify client demand is still met
        total_to_client = (
            model_data.transport_quantity[route1] + 
            model_data.transport_quantity[route2]
        )
        assert total_to_client >= 10.0, "Client demand must be covered"
    
    def test_engine_objective(self) -> None:
        """
        Test that verifies the objective function minimizes total cost.
        
        Total cost = sum(production_cost * quantity) + sum(transport_cost * quantity)
        
        The optimizer should choose the lowest-cost combination of routes that
        satisfies all constraints.
        """
        model_data = self.create_model_data("test_engine_objective.json")
        Engine(model_data, "cbc").run()
    
        # Calculate total cost manually
        total_cost = 0.0
        
        # Production costs: cost per unit * quantity produced
        for workshop in model_data.workshops:
            # Sum all quantities from this workshop
            produced = sum(
                qty
                for route, qty in model_data.transport_quantity.items()
                if route.origin == workshop.id_
            )
            total_cost += workshop.production_cost * produced
        
        # Transport costs: cost per unit * quantity transported
        for route, quantity in model_data.transport_quantity.items():
            total_cost += route.transport_cost * quantity
        
        # Expected optimal solution:
        # Workshop1 has lower production cost (20 vs 25)
        # Route Workshop1->Client1 has lower transport cost (10 vs 15)
        # So all 30 units should come from Workshop1->Client1
        
        route1 = model_data.routes_by_id["Workshop1,Client1"]
        route2 = model_data.routes_by_id["Workshop2,Client1"]
        
        # Verify optimizer chose the cheapest route
        assert model_data.transport_quantity[route1] == 30.0, (
            "Should use Workshop1->Client1 (cheaper production + transport)"
        )
        assert model_data.transport_quantity[route2] == 0.0, (
            "Should not use Workshop2->Client1 (more expensive)"
        )
        
        # Verify total cost calculation
        expected_cost = (20.0 * 30.0) + (10.0 * 30.0)  # production + transport
        assert abs(total_cost - expected_cost) < 0.01, (
            f"Total cost {total_cost} should equal {expected_cost}"
        )
        
        # Verify it's truly minimized (not using expensive route)
        expensive_cost = (25.0 * 30.0) + (15.0 * 30.0)  # if using Workshop2
        assert total_cost < expensive_cost, (
            "Optimizer should choose cheaper route combination"
        )