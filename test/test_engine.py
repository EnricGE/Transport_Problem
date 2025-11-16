from pathlib import Path

from transport.context import ModelData
from transport.factory import ModelDataFactory
from transport.engine import Engine


PATH = Path(__file__).parent


class TestEngine:
    
    def create_model_data(self, test_path: str) -> ModelData:
        return ModelDataFactory.from_json(
            PATH / "data/test_engine" / test_path
        )

    def test_engine_constr_client_demand(self) -> None:
        """
        Descripció del test, què es lo que limita i quina seria la solució si no estigués la restricció
        """
        model_data = self.create_model_data("test_engine_constr_client_demand.json")
        Engine(model_data, "cbc").run()
        
        route = model_data.routes_by_id["Workshop1,Client1"]
        
        assert model_data.transport_quantity[route] == 10.0
        
        
        