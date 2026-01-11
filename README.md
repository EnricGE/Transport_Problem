# Transport Problem – Production & Transportation Optimization

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Optimization](https://img.shields.io/badge/optimization-Pyomo-green)
![Status](https://img.shields.io/badge/status-active-success)

A Python project that solves a **production + transportation optimization problem** using mathematical programming.

The goal is to determine how much to produce at each workshop and how much to transport along each route in order to **minimize total cost**, while satisfying capacity, demand, and operational constraints.

---

## Problem Overview

- Workshops have limited production capacity and a unit production cost  
- Clients require a fixed demand  
- Routes connect workshops to clients with:
  - transport cost
  - capacity limits
  - optional minimum shipment constraints
- Some routes may be inactive

The model finds the **lowest-cost feasible transport plan** that satisfies all constraints.

---

## Key Features

- Clean domain models with validation (Pydantic)
- Deterministic optimization model (LP / MILP)
- Production capacity constraints
- Exact demand satisfaction
- Route capacity & minimum shipment constraints
- Binary route activation variables
- Multiple solver support:
  - CBC (open-source)
  - Gurobi (commercial)
  - Hexaly (WIP)

---

## Tech Stack

- **Python 3.10+**
- **Pyomo** – optimization modeling
- **Pydantic** – data validation
- **CBC / Gurobi** – solvers

---

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Make sure a Pyomo-compatible solver is installed and accessible in your PATH.

---

## Project Structure

```
TransportProblem/
├── src/transport/
│   ├── engine/        # Optimization engines
│   ├── factory/       # Data loading & conversion
│   ├── context/       # Domain models
│   └── run.py         # Example runner
├── test/              # Unit tests & test data
└── README.md
```

---

## Usage

### Run example

From the project root:

```bash
python -m transport.run
```

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

## Input Data Format

Input is provided as JSON with three sections:

- **workshops**
  - `id`
  - `production_capacity`
  - `production_cost`
- **clients**
  - `id`
  - `demand`
- **routes**
  - `origin`
  - `destination`
  - `transport_cost`
  - `transport_capacity`
  - `min_transport_quantity`
  - `is_active`

---

## Output

The solver returns a `SolveResult` containing:

- solver termination status
- total objective value
- transported quantity per route

This explicit result object makes the model easy to test, extend, and integrate.

---

## Roadmap

- Add CLI interface (`transport-solve`)
- Soft demand constraints with penalty variables
- Infeasibility diagnostics
- Result export to CSV / JSON
- Continuous Integration (GitHub Actions)

---

## License

MIT License
