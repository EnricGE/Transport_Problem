from pydantic import BaseModel, ValidationInfo, field_validator, model_validator
from typing_extensions import cast, override

from transport.context.objects.validation_utils import check_value_in_range


class Route(BaseModel):
    """
    Route class

    Attributes
    ----------
    origin : str
        Origin Workshop of the route.
    destination : str
        Destination Workshop of the route.
    transport_cost: float
        Cost to transport the product through the route.
    transport_capacity: float
        Maximum product capacity to transport through the route.
    min_transport_quantity: float
        Minimum product quantity to transport through the route.
    is_active: bool
         Boolean indicating whether the route is active.
    """

    origin: str
    destination: str
    transport_cost: float
    transport_capacity: float
    min_transport_quantity: float
    is_active: bool

    @property
    def id_(self) -> str:
        return self.origin + "," + self.destination

    @override
    def __str__(self) -> str:
        return self.id_

    @override
    def __repr__(self) -> str:
        return self.id_

    def __hash__(self) -> int:
        """Make Route hashable so it can be used as dictionary key"""
        return hash((self.origin, self.destination))

    def __eq__(self, other: object) -> bool:
        """Define equality based on origin and destination"""
        if not isinstance(other, Route):
            return False
        return self.origin == other.origin and self.destination == other.destination

    @field_validator("origin")
    @classmethod
    def origin_not_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Route.origin cannot be empty")
        return value

    @field_validator("destination")
    @classmethod
    def destination_not_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Route.destination cannot be empty")
        return value

    @field_validator("transport_cost")
    @classmethod
    def validate_transport_cost(cls, value: float, info: ValidationInfo) -> float:
        min_range = 0.0
        max_range = None
        id_ = cast(str, "Route[" + info.data.get("id_", "unknown") + "]")
        check_value_in_range(value, min_range, max_range, id_)
        return value

    @field_validator("transport_capacity")
    @classmethod
    def validate_transport_capacity(cls, value: float, info: ValidationInfo) -> float:
        min_range = 0.0
        max_range = None
        id_ = cast(str, "Route[" + info.data.get("id_", "unknown") + "]")
        check_value_in_range(value, min_range, max_range, id_)
        return value
        
    @field_validator("min_transport_quantity")
    @classmethod
    def validate_min_transport_quantity(cls, value: float, info: ValidationInfo) -> float:
        min_range = 0.0
        max_range = info.data.get("transport_capacity") #cls.transport_capacity
        id_ = cast(str, "Route[" + info.data.get("id_", "unknown") + "]")
        check_value_in_range(value, min_range, max_range, id_)
        return value

    @model_validator(mode="after")
    def validate_different_endpoints(self) -> "Route":
        if self.origin == self.destination:
            raise ValueError(
                f"Route origin and destination must be different, got: {self.origin}"
            )
        return self
