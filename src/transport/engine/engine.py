from typing import Literal
from pathlib import Path
from transport.factory.model_data_factory import ModelDataFactory

from transport.engine.result import SolveResult
from transport.context import ModelData
from transport.engine.engines import AbstractEngine, EngineHexaly, EnginePyomo


class Engine:
    
    def __init__(
        self, 
        model_data: ModelData, 
        engine_type: Literal["cbc", "gurobi", "hexaly"]
    ):
        self.data: ModelData = model_data
        self.engine_type: str = engine_type
        
        engines: dict[str, AbstractEngine] = {
            "cbc": EnginePyomo,
            "gurobi": EnginePyomo,
            "hexaly": EngineHexaly,
        }
        
        engine_class: AbstractEngine | None = engines.get(engine_type)
        
        if engine_class is None:
            raise ValueError((
                f"engine_type can only be ['cbc', 'gurobi', 'hexaly'], "
                f"but it is {engine_type}"
            ))
        else:
            self.engine: AbstractEngine = engine_class(self.data)
    
    def run(self) -> SolveResult:
        return self.engine.run(self.engine_type)

