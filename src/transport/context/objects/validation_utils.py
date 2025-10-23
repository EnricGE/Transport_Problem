from collections import Counter
from collections.abc import Collection, Iterable
from typing import Protocol


class HasId(Protocol):
    id_: str


class RouteProtocol(Protocol):
    origin: str
    destination: str
    transport_capacity: int | float
    transport_cost: int | float
    is_active: bool


def check_unique_ids(values: Collection[HasId], field_name: str) -> None:
    ids = [v.id_ for v in values]
    dup_ids = [i for i, c in Counter(ids).items() if c > 1]
    if dup_ids:
        dup_ids.sort()
        raise ValueError(
            (f"There cannot be repeated ids on ModelData.{field_name}: ({dup_ids})")
        )


def assert_min_count(values: Iterable[object], name: str, min_count: int = 1) -> None:
    n = sum(1 for _ in values)
    if n < min_count:
        raise ValueError(
            f"ModelData must contain at least {min_count} {name} (found {n})."
        )


def assert_min_active_routes(
    routes: Iterable[RouteProtocol], min_active: int = 1
) -> None:
    active = sum(1 for r in routes if r.is_active)
    if active < min_active:
        raise ValueError(
            (
                f"ModelData must contain at least {min_active} "
                f"active route (found {active})."
            )
        )


def check_value_in_range(
    value: int | float,
    min_range: int | float | None,
    max_range: int | float | None,
    id_: str,
) -> None:
    if min_range is not None:
        if value < min_range:
            raise ValueError(
                (f"Value {value} is below minimum range {min_range} for object {id_}")
            )
    if max_range is not None:
        if value > max_range:
            raise ValueError(
                (f"Value {value} is above maximum range {max_range} for object {id_}")
            )


def assert_route_endpoints_exist(
    routes: Iterable[RouteProtocol],
    workshop_ids: set[str],
    client_ids: set[str],
) -> None:
    missing_origins = sorted({r.origin for r in routes} - workshop_ids)
    missing_destinations = sorted({r.destination for r in routes} - client_ids)
    problems: list[str] = []
    if missing_origins:
        problems.append(f"unknown workshop ids in routes.origin: {missing_origins}")
    if missing_destinations:
        problems.append(
            f"unknown client ids in routes.destination: {missing_destinations}"
        )
    if problems:
        raise ValueError("Referential integrity error: " + "; ".join(problems))


def assert_unique_route_pairs(routes: Iterable[RouteProtocol]) -> None:
    seen: set[tuple[str, str]] = set()
    dups: set[tuple[str, str]] = set()
    for r in routes:
        key = (r.origin, r.destination)
        if key in seen and key not in dups:
            dups.add(key)
        seen.add(key)
    if dups:
        raise ValueError(f"Duplicate (origin, destination) routes: {sorted(dups)}")
