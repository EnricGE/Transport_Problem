# ⛽ Gas Transport Planning — Routing Under Network Constraints

Optimal production and delivery routing for gas networks, where infrastructure limits — not just cost — determine what is operationally possible.

The goal is to select the lowest-cost feasible plan for routing gas from production sites to clients in order to:
- Respect hard capacity limits across every production site, conduit, and delivery point
- Guarantee full demand satisfaction with no relaxations or penalties
- Make the cost–feasibility trade-off explicit and auditable

## Problem Overview

Without a structured optimisation approach, operators risk:
- Routing plans that violate physical network capacity and are therefore infeasible
- Suboptimal cost allocation — activating expensive sites or routes when cheaper alternatives exist
- Invisible bottlenecks that constrain future network decisions without being identified
- Decisions that are difficult to justify or reproduce across planning cycles

## What the Model Does

- Enforces all hard constraints simultaneously: production capacity, client demand, route throughput, and minimum flow requirements
- Identifies which production sites are activated and at what output level
- Allocates flow across the network to minimise total production and transport cost
- Reveals binding bottlenecks — routes or sites where capacity limits the feasible decision space
- Produces a single, transparent recommendation: the **lowest-cost feasible routing plan**

## Approaches

- **Exact solver (CBC / Gurobi)** — Mixed-integer linear programme guaranteeing an optimal solution; used as the primary method and benchmark
- **Combinatorial solver (Hexaly)** — Alternative engine for large-scale or complex network configurations where exact methods become slow

## Purpose

This project demonstrates:
- Formulating a real infrastructure planning problem as a constrained optimisation model
- Enforcing hard constraints with no slack — infeasible plans are rejected, not penalised
- Using binary route-activation logic to model all-or-nothing operational decisions
- Designing a solver-agnostic architecture that supports multiple optimisation backends
- Building a transparent decision tool where every constraint and cost assumption is explicit and auditable
