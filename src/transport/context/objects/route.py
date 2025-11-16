from typing_extensions import override, cast

from pydantic import BaseModel, ValidationInfo, field_validator

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
    is_active: bool
         Boolean indicating whether the route is active.
    """

    origin: str
    destination: str
    transport_cost: float
    transport_capacity: float
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

    @field_validator("origin")
    @classmethod
    def origin_not_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Route.origin cannot be empty")
        return value

    @field_validator("destination")
    @classmethod
    def destinationnot_empty(cls, value: str) -> str:
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
