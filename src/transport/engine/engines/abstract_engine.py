from abc import ABC, abstractmethod

from transport.context import ModelData


class AbstractEngine(ABC):
    
    def __init__(self, model_data: ModelData) -> None:
        self.data: ModelData = model_data
    
    @abstractmethod
    def run(self, solver: str) -> None:
        pass
