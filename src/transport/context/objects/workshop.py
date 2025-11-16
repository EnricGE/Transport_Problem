from typing_extensions import override, cast

from pydantic import BaseModel, ValidationInfo, field_validator

from transport.context.objects.validation_utils import check_value_in_range


class Workshop(BaseModel):
    """
    Workshop class

    Attributes
    ----------
    id_ : str
        Unique identifier of the class instance.
    production_capacity: float
        Maximum production of the product by the workshop.
    production_cost: float
        Production cost of the product by the workshop.
    """
    
    id_: str
    production_capacity: float
    production_cost: float

    @override
    def __str__(self) -> str:
        return self.id_

    @override
    def __repr__(self) -> str:
        return self.id_
        
    @field_validator("id_")
    @classmethod
    def id_not_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Workshop.id_ cannot be empty")
        return value
        
    @field_validator("production_capacity")
    @classmethod
    def validate_production_capacity(cls, value: float, info: ValidationInfo) -> float:
        min_range = 0.0
        max_range = None
        id_ = cast(str, "Workshop[" + info.data.get("id_", "unknown") + "]")
        check_value_in_range(value, min_range, max_range, id_)
        return value
        
    @field_validator("production_cost")
    @classmethod
    def validate_production_cost(cls, value: float, info: ValidationInfo) -> float:
        min_range = 0.0
        max_range = None
        id_ = cast(str, "Workshop[" + info.data.get("id_", "unknown") + "]")
        check_value_in_range(value, min_range, max_range, id_)
        return value
