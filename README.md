# Gas Distribution Planning Under Network Capacity Constraints

A Decision Intelligence case study focused on **planning gas distribution flows through a constrained network**.

The project supports decisions on how to route gas from multiple production sites (workshops) to multiple clients through capacity‑limited conduits, **minimizing operational cost while satisfying demand and network constraints**.

This is not a generic transport model: it represents a real industrial decision problem where routing choices have cost, feasibility, and operational consequences.

---

## Decision Context

A gas distribution operator must decide:

- How much gas to produce at each workshop  
- How to route gas through a network of conduits  
- Which routes to activate or limit  

The challenge is to **meet all client demand at minimum cost**, while respecting:

- Production capacity limits  
- Network capacity constraints  
- Operational rules on minimum flows and route availability  

Each feasible routing represents a different operational policy, with clear cost and feasibility trade‑offs.

---

## Problem Framing

**Decision to make**  
Choose a gas routing and production plan that minimizes total cost.

**Alternatives**  
Different flow allocations across the network, using different subsets of routes and production sites.

**Constraints**
- Limited production capacity at workshops  
- Fixed demand at clients  
- Capacity limits on each conduit  
- Optional minimum flow requirements  
- Route availability (active / inactive)  

**Objective**
- Minimize total production and transportation cost  

---

## Modeling Approach

The problem is formulated as a **constrained network flow optimization model**:

- Continuous decision variables for production and transported quantities  
- Linear cost structure  
- Capacity and flow conservation constraints  
- Optional binary variables for route activation  

The model is solved deterministically using linear / mixed‑integer programming.

---

## Key Features

- Clean domain modeling with validation (Pydantic)
- Production + transport cost optimization
- Capacity‑constrained network flow modeling
- Optional minimum shipment constraints
- Route activation logic
- Explicit, testable solve results
- Multiple solver support:
  - CBC (open‑source)
  - Gurobi (commercial)
  - Hexaly (experimental)

---

## Tech Stack

- **Python 3.10+**
- **Pyomo** – optimization modeling
- **Pydantic** – domain validation
- **CBC / Gurobi** – solvers

---

### Python API

```python
from transport.engine.engine import Engine
from transport.factory.model_data_factory import ModelDataFactory

data = ModelDataFactory.from_json(
    "test/data/test_model_data/test_data_and_data_factory.json"
)

engine = Engine(model_data=data, engine_type="cbc")
result = engine.run()

print(result.status)
print(result.objective)
print(result.transport_quantity)
```

---

## Input Data

Input is provided as JSON with three core entities:

### Workshops
- `id`
- `production_capacity`
- `production_cost`

### Clients
- `id`
- `demand`

### Routes
- `origin`
- `destination`
- `transport_cost`
- `transport_capacity`
- `min_transport_quantity`
- `is_active`

---

## Output

The solver returns a structured `SolveResult` containing:

- Solver termination status  
- Total cost  
- Production levels per workshop  
- Transported quantities per route  

This makes the model easy to analyze, test, and extend.

---

## What This Case Demonstrates

- How **physical infrastructure constraints** shape feasible decisions  
- How cost‑optimal solutions emerge from constrained choices  
- How network structure creates trade‑offs between routes and production sites  

This case fits naturally within **Decision Intelligence**, where the goal is not just optimization, but **justified, transparent operational decisions**.

---

## Roadmap

- Demand uncertainty and scenario analysis
- Soft demand constraints with penalties
- Route outage scenarios
- Result export (CSV / JSON)
- CLI interface

---

## License

MIT License
