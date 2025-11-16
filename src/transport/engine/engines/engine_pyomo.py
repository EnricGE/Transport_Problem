from typing_extensions import override

import pyomo.environ as pyo

from transport.context import ModelData
from transport.context.objects import Route, Client
from transport.engine.engines.abstract_engine import AbstractEngine


class EnginePyomo(AbstractEngine):
    def __init__(self, model_data: ModelData) -> None:
        super().__init__(model_data)

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
            route: pyo.value(value) 
            for (route, value) in self.model.var_transport_quantity.items()
        }

    def _build_sets(self) -> None:
        # [Workshop]
        self.model.workshops = pyo.Set(dimen=1, initialize=self.data.workshops)
        # [Clients]
        self.model.clients = pyo.Set(dimen=1, initialize=self.data.clients)
        # [Routes]
        self.model.routes = pyo.Set(dimen=1, initialize=self.data.active_routes)

    def _build_variables(self) -> None:
        self.model.var_transport_quantity = pyo.Var(
            self.model.routes, within=pyo.NonNegativeReals
        )

    def _build_expressions(self) -> None:
        self.model.expression_routes_cost = pyo.Expression(
            self.model.routes, rule=self._expr_routes_cost
        )

    def _build_constraints(self) -> None:
        self.model.constraint_workshop_capacity = pyo.Constraint(
            self.model.routes, rule=self._const_workshop_capacity
        )

        self.model.constraint_client_demand = pyo.Constraint(
            self.model.clients, rule=self._const_client_demand
        )

        self.model.constraint_route_capacity = pyo.Constraint(
            self.model.routes, rule=self._const_route_capacity
        )

    def _build_objective(self) -> None:
        self.model.objective = pyo.Objective(
            rule=self._objective_function, sense=pyo.maximize
        )
    
    def _expr_routes_cost(self, _: pyo.ConcreteModel, route: Route) -> float:
        return self.model.var_transport_quantity[route] * route.transport_cost

    def _const_workshop_capacity(self, _: pyo.ConcreteModel, route: Route) -> bool:
        route_workshop = self.data.workshops_by_id[route.origin]
        return (
            self.model.var_transport_quantity[route]
            <= route_workshop.production_capacity
        )

    def _const_client_demand(self, _: pyo.ConcreteModel, client: Client) -> bool:
        return (
            sum(
                self.model.var_transport_quantity[route]
                for route in self.model.routes
                if route.destination == client.id
            )
            <= client.demand
        )

    def _const_route_capacity(self, _: pyo.ConcreteModel, route: Route) -> bool:
        return self.model.var_transport_quantity[route] <= route.transport_capacity
    
    def _objective_function(self, _: pyo.ConcreteModel) -> float:
        return sum(self.expression_routes_cost[route] for route in self.model.routes)

    def _check_solution_status(self):
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
