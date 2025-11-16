from typing_extensions import override

from transport.context import ModelData
from transport.engine.engines.abstract_engine import AbstractEngine


class EngineHexaly(AbstractEngine):
    
    def __init__(self, model_data: ModelData) -> None:
        super().__init__(model_data)

    @override
    def run(self, solver: str) -> None:
        raise NotImplementedError
