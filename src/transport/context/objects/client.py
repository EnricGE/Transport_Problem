from typing_extensions import override, cast

from pydantic import BaseModel, ValidationInfo, field_validator

from transport.context.objects.validation_utils import check_value_in_range


class Client(BaseModel):
    """
    Client class

    Attributes
    ----------
    id_ : str
        Unique identifier of the class instance.
    demand: float
        Product quantity demand of the product by the client.
    """

    id_: str
    demand: float

    @override
    def __str__(self) -> str:
        return self.id_

    @override
    def __repr__(self) -> str:
        return self.id_

    @field_validator("demand")
    @classmethod
    def validate_demand(cls, value: float, info: ValidationInfo) -> None:
        min_range = 0.0
        max_range = None
        id_ = cast(str, "Client[" + info.data.get("id_", "unknown") + "]")
        check_value_in_range(value, min_range, max_range, id_)
