from dataclasses import dataclass

@dataclass(frozen=True)
class SolveResult:
    status: str
    objective: float
    transport_quantity: dict[str, float]  # route_id -> quantity
    solver: str