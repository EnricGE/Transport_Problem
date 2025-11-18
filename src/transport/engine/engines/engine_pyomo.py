import pyomo.environ as pyo
from typing_extensions import override

from transport.context import ModelData

# from transport.context.objects import Route, Client
from transport.engine.engines.abstract_engine import AbstractEngine


class EnginePyomo(AbstractEngine):
    def __init__(self, model_data: ModelData) -> None:
        super().__init__(model_data)
        self.BIG_M = 1e6

    @override
    def run(self, solver: str) -> None:
        self._build_model()
        self._solve_model(solver)
        self._build_solution()

    def _build_model(self) -> None:
        self.model = pyo.ConcreteModel()

        self._build_sets()
        self._build_variables()
        self._build_expressions()
        self._build_constraints()
        self._build_objective()

    def _solve_model(self, solver: str) -> None:
        solver = pyo.SolverFactory(solver)
        self.solution = solver.solve(self.model, tee=True)
        self._check_solution_status()

    def _build_solution(self) -> None:
        self.data.transport_quantity = {
            self.data.routes_by_id[route_id]: float(pyo.value(value))
            for route_id, value in self.model.var_transport_quantity.items()
        }

    def _build_sets(self) -> None:
        # [Workshop]
        self.model.workshops = pyo.Set(
            dimen=1,
            initialize=[w.id_ for w in self.data.workshops],
        )
        # [Clients]
        self.model.clients = pyo.Set(
            dimen=1,
            initialize=[c.id_ for c in self.data.clients],
        )
        # [Routes]
        self.model.routes = pyo.Set(
            dimen=1,
            initialize=[r.id_ for r in self.data.routes],
        )

    def _build_variables(self) -> None:
        self.model.var_transport_quantity = pyo.Var(
            self.model.routes, within=pyo.NonNegativeReals
        )
        self.model.var_is_route_used = pyo.Var(self.model.routes, within=pyo.Binary)

    def _build_expressions(self) -> None:
        self.model.expression_routes_cost = pyo.Expression(
            self.model.routes, rule=self._expr_routes_cost
        )

    def _build_constraints(self) -> None:
        self.model.constraint_workshop_capacity = pyo.Constraint(
            self.model.workshops, rule=self._const_workshop_capacity
        )

        self.model.constraint_client_demand = pyo.Constraint(
            self.model.clients, rule=self._const_client_demand
        )

        self.model.constraint_route_capacity = pyo.Constraint(
            self.model.routes, rule=self._const_route_capacity
        )

        self.model.constraint_min_transport_quantity_1 = pyo.Constraint(
            self.model.routes, rule=self._const_min_transport_quantity_1
        )

        self.model.constraint_min_transport_quantity_2 = pyo.Constraint(
            self.model.routes, rule=self._const_min_transport_quantity_2
        )

    def _build_objective(self) -> None:
        self.model.objective = pyo.Objective(
            rule=self._objective_function, sense=pyo.minimize
        )

    def _expr_routes_cost(self, _: pyo.ConcreteModel, route_id: str):
        route = self.data.routes_by_id[route_id]
        return self.model.var_transport_quantity[route_id] * route.transport_cost

    def _const_workshop_capacity(self, _: pyo.ConcreteModel, workshop_id: str):
        workshop = self.data.workshops_by_id[workshop_id]
        return (
            sum(
                self.model.var_transport_quantity[route_id]
                for route_id in self.model.routes
                if self.data.routes_by_id[route_id].origin == workshop_id
            )
            <= workshop.production_capacity
        )

    def _const_client_demand(self, _: pyo.ConcreteModel, client_id: str):
        client = self.data.clients_by_id[client_id]
        return (
            sum(
                self.model.var_transport_quantity[route_id]
                for route_id in self.model.routes
                if self.data.routes_by_id[route_id].destination == client.id_
            )
            >= client.demand
        )

    def _const_route_capacity(self, _: pyo.ConcreteModel, route_id: str):
        route = self.data.routes_by_id[route_id]
        return self.model.var_transport_quantity[route_id] <= route.transport_capacity

    def _const_min_transport_quantity_1(self, _: pyo.ConcreteModel, route_id: str):
        route = self.data.routes_by_id[route_id]
        return (
            self.model.var_transport_quantity[route_id]
            <= self.model.var_is_route_used[route_id] * self.BIG_M
        )

    def _const_min_transport_quantity_2(self, _: pyo.ConcreteModel, route_id: str):
        route = self.data.routes_by_id[route_id]
        return (
            self.model.var_transport_quantity[route_id]
            >= self.model.var_is_route_used[route_id] * route.min_transport_quantity
        )

    def _objective_function(self, _: pyo.ConcreteModel) -> float:
        return sum(
            self.model.expression_routes_cost[route_id]
            for route_id in self.model.routes
        )

    def _check_solution_status(self) -> None:
        status = self.solution.solver.status
        termination_cause = self.solution.solver.termination_condition
        cause_termination_is_time = (
            termination_cause == pyo.TerminationCondition.maxTimeLimit
        )
        feasible = (
            termination_cause == pyo.TerminationCondition.optimal
            or termination_cause == pyo.TerminationCondition.feasible
        )
        solution_status = (
            (status == pyo.SolverStatus.ok and feasible)
            or (status == pyo.SolverStatus.aborted and cause_termination_is_time)
            or (status == pyo.SolverStatus.ok and cause_termination_is_time)
        )
        if not solution_status:
            raise Exception("Solver failed to find a solution.")
