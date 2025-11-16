from __future__ import annotations

from collections.abc import Collection
from typing import List

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationInfo,
    field_validator,
    model_validator,
)

from transport.context.objects import Client, Route, Workshop
from transport.context.objects.validation_utils import (
    HasId,
    assert_min_active_routes,
    assert_min_count,
    assert_route_endpoints_exist,
    assert_unique_route_pairs,
    check_unique_ids,
)


class ModelData(BaseModel):
    # re-validate when assigning to fields after creation (useful in tests)
    model_config = ConfigDict(validate_assignment=True)

    # --- real pydantic fields ---
    workshops: List[Workshop] = Field(default_factory=list)
    clients: List[Client] = Field(default_factory=list)
    routes: List[Route] = Field(default_factory=list)
    transport_quantity: dict[Route, float] = Field(default_factory=dict)

    # --- derived views (computed on access; no sync issues) ---
    @property
    def workshops_by_id(self) -> dict[str, Workshop]:
        return {w.id_: w for w in self.workshops}

    @property
    def clients_by_id(self) -> dict[str, Client]:
        return {c.id_: c for c in self.clients}

    @property
    def routes_by_id(self) -> dict[str, Route]:
        return {r.id_: r for r in self.routes}

    @property
    def active_routes(self) -> list[Route]:
        return [r for r in self.routes if getattr(r, "is_active", False)]

    @field_validator("workshops", "clients", "routes")
    @classmethod
    def no_duplicate_ids(cls, values: Collection[HasId], info: ValidationInfo):
        """
        per-field validation: no duplicate ids in each list
        """
        # info.field_name is guaranteed here because these are real fields
        check_unique_ids(values, info.field_name or "unknown")
        return list(values)

    @model_validator(mode="after")
    def cross_checks(self) -> "ModelData":
        """
        cross-field validation
        """
        # existence
        assert_min_count(self.workshops, "workshop")
        assert_min_count(self.clients, "client")
        assert_min_active_routes(self.routes, 1)

        # references & duplicates across routes
        w_ids = {w.id_ for w in self.workshops}
        c_ids = {c.id_ for c in self.clients}
        assert_route_endpoints_exist(self.routes, w_ids, c_ids)
        assert_unique_route_pairs(self.routes)

        return self
