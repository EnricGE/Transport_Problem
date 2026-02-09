# ⛽ Gas Transport Planning — Decision Under Network Constraints

**Network optimisation, cost–feasibility trade-offs, and operational plan selection**

---

## 1. Context & Motivation

Gas distribution decisions are rarely about finding *a* feasible routing.  
They are about **choosing an operational plan** that balances:

- production and transport cost  
- feasibility under hard infrastructure constraints  
- utilisation of limited network capacity  
- exposure to bottlenecks and operational rigidity  

This project studies a **gas transport planning problem under network capacity constraints**, using deterministic optimisation to support **transparent and defensible routing decisions**.

The goal is not to build a generic transport solver, but to answer:

> *“Given strict infrastructure limits, how should gas be routed from production sites to clients — and what trade-offs does this imply?”*

---

## 2. Decision Problem

A gas distribution operator must plan operations for a single planning period.

The system consists of:
- production sites with limited capacity  
- clients with fixed demand  
- a network of conduits with hard capacity limits  

Routing decisions:
- determine which production sites supply which clients  
- define how capacity is allocated across the network  

All constraints are **hard and always enforced**: infeasible plans are not acceptable.

The decision-maker must choose **one routing and production plan**.

---

## 3. Operational Policies Considered

Each feasible solution corresponds to an **implicit operational policy**, defined by:

- production levels at each workshop  
- activated transport routes  
- flow quantities assigned to each route  

Different policies reflect different strategic choices, such as:
- concentrating production on low-cost sites  
- spreading flows to reduce saturation  
- activating or deactivating specific routes  

---

## 4. Modelling & Evaluation Approach

The problem is formulated as a **network flow optimisation model**:

- Continuous variables for production and transported quantities  
- Optional binary variables for route activation  
- Linear cost structure  
- Flow conservation and capacity constraints  

Key characteristics:
- Single-period, deterministic decision  
- No demand relaxation or penalty terms  
- No probabilistic assumptions  

Each candidate policy is evaluated purely on:
- feasibility  
- total operational cost  

---

## 5. Decision Variables & Constraints

### Decision Variables
- Production quantity at each workshop  
- Transported quantity on each route  
- Optional route activation decisions  

### Hard Constraints
- Full demand satisfaction at all clients  
- Production capacity limits  
- Route capacity limits  
- Minimum flow requirements (when specified)  
- Route availability and activation logic  

These constraints define the **feasible decision space**.

---

## 6. Objective Function

The decision criterion is:

```
Minimise total operational cost
= production cost + transport cost (+ optional activation cost)
```

This objective identifies the **lowest-cost feasible operational policy** under the imposed constraints.

---

## 7. Decision Insights

Typical questions this model helps answer:

- Which production sites are actually used, and why?  
- Which routes become binding bottlenecks?  
- Where does cost optimality conflict with network rigidity?  
- How sensitive feasibility is to capacity reductions or outages?  

The value lies in **understanding the structure of the optimal decision**, not just computing it.

---

## 8. Decision Recommendation

For a given scenario, the recommended decision is:

> **The feasible routing and production plan with the lowest total cost, fully respecting all production, demand, and network constraints.**

Because all assumptions are explicit and constraints are hard, the recommendation is:
- transparent  
- reproducible  
- auditable  

---

## 9. Limitations & Extensions

This is a **deliberately static, single-period model**.

Not included (yet):
- demand uncertainty or scenarios  
- soft constraints or penalty-based relaxations  
- route outage probabilities  
- shadow price or sensitivity analysis  

These extensions would allow richer risk-aware decisions.

---

## 10. Takeaway

> **The value of network optimisation lies not in computing flows, but in revealing how infrastructure constraints shape feasible and defensible operational decisions.**

This project demonstrates how optimisation can be used as a **Decision Intelligence tool** to justify routing policies under strict physical constraints.
