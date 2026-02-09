# ⛽ Gas Distribution Planning — Network Flow Optimization

This project implements a **realistic gas distribution planning problem** using **linear / mixed-integer optimization**, under **production, demand, and network capacity constraints**.

The goal is **not just cost minimization**, but to **support justified operational decisions** by exposing how infrastructure constraints, routing choices, and production limits interact.

---

## 1. Problem Overview

Given:

- A set of **gas production sites (workshops)** acting as sources  
- A set of **clients** with fixed demand  
- A network of **capacity-limited conduits (routes)**  
- Production, transport, and activation costs  

We compute a **single-period distribution plan** that:

- Satisfies all client demand  
- Respects production and network capacity limits  
- Enforces operational routing rules  
- Minimizes total operational cost  

All constraints are **hard and always enforced**.  
Each feasible solution represents a **distinct operational policy**.

---

## 2. Data Schema

All input data is JSON-based and validated before optimization.

### `workshops.json`

**Fields**

- `id`: unique identifier  
- `production_capacity`: maximum producible quantity  
- `production_cost`: unit production cost  

Workshops act **only as sources** in the network.

---

### `clients.json`

**Fields**

- `id`: unique identifier  
- `demand`: required gas quantity  

Client demand must be **fully satisfied**.

---

### `routes.json`

**Fields**

- `origin`: source workshop  
- `destination`: client  
- `transport_cost`: unit transport cost  
- `transport_capacity`: maximum transferable quantity  
- `min_transport_quantity`: minimum required flow (hard constraint)  
- `is_active`: route availability flag  

Routes define a **directed distribution network** from workshops to clients.

---

### `scenario.json`

**Fields**

- `allow_route_activation`: enable / disable binary route activation  
- `solver`: selected optimization solver  
- `solver_options`: solver-specific parameters  

---

## 3. Decision Variables

| Variable | Meaning |
|--------|--------|
| `production[w]` | Gas produced at workshop `w` |
| `flow[r]` | Gas transported on route `r` |
| `use_route[r]` | Route activation (binary, optional) |
| `total_cost` | Total production + transport cost |

---

## 4. Constraints

### Hard Constraints

1. **Demand satisfaction**  
   Total incoming flow to each client equals demand.

2. **Production capacity**  
   `production[w] ≤ production_capacity[w]`

3. **Route capacity**  
   `flow[r] ≤ transport_capacity[r]`

4. **Minimum flow requirements**  
   `flow[r] ≥ min_transport_quantity[r]` (when specified)

5. **Route activation logic (optional)**  
   Flow allowed only if route is active.

6. **Flow consistency**  
   Transported quantities originate exclusively from workshops.

All constraints are **strictly enforced** — no penalties, no relaxations.

---

## 5. Objective Function

The solver minimizes:

```
Total production cost
+ Total transport cost
+ Optional route activation cost
```

Formally:

```
min Σ production_cost[w] × production[w]
  + Σ transport_cost[r] × flow[r]
  + Σ activation_cost[r] × use_route[r]
```

This yields the **lowest-cost feasible operational policy**.

---

## 6. How to Run

### Install dependencies

```bash
uv sync
```

### Run the optimization

```bash
python scripts/run_model.py --scenario data/scenarios/base.json
```

---

## 7. Outputs

### Solver result object

The solver returns a structured `SolveResult` containing:

- Solver termination status  
- Total cost  
- Production levels per workshop  
- Transported quantities per route  

---

### Typical decision insights

- Which workshops supply which clients  
- Which routes are saturated or unused  
- Cost trade-offs between production sites  
- Impact of capacity bottlenecks on feasibility  

---

## 8. Design Choices

- **Network flow formulation** chosen for:
  - Transparency
  - Deterministic behavior
  - Strong optimality guarantees
- **Hard constraints only**, reflecting strict industrial requirements
- **Optional MILP structure**, enabling:
  - Pure LP for baseline studies
  - Binary routing logic when operationally required
- Model designed to remain:
  - Auditable
  - Testable
  - Scenario-driven

---

## 9. Possible Extensions

- Demand uncertainty and scenario analysis  
- Soft demand constraints with penalties  
- Route outage scenarios  
- Bottleneck and sensitivity analysis  
- CLI interface and result export (CSV / JSON)  

---

## 10. Author Notes

This project focuses on **decision quality**, not prediction.

It demonstrates how **physical infrastructure constraints** and **network structure** define feasible operational policies, and how optimization can support **transparent, defensible decisions** under real-world constraints.
