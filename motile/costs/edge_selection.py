from __future__ import annotations

from typing import TYPE_CHECKING

from ..variables import EdgeSelected
from .cost import Cost
from .weight import Weight

if TYPE_CHECKING:
    from motile.solver import Solver


class EdgeSelection(Cost):
    """Cost for :class:`~motile.variables.EdgeSelected` variables.

    Args:
        weight:
            The weight to apply to the cost given by the provided attribute of
            each edge. Default is ``1.0``.

        attribute:
            The name of the edge attribute to use to look up cost. Default is
            None, which means only a constant cost is used.

        constant:
            A constant cost for each selected edge. Default is ``0.0``.
    """

    def __init__(
        self, weight: float = 1, attribute: str | None = None, constant: float = 0.0
    ) -> None:
        self.weight = Weight(weight)
        self.constant = Weight(constant)
        self.attribute = attribute

    def apply(self, solver: Solver) -> None:
        edge_variables = solver.get_variables(EdgeSelected)

        for edge, index in edge_variables.items():
            if self.attribute is not None:
                solver.add_variable_cost(
                    index, solver.graph.edges[edge][self.attribute], self.weight
                )
            solver.add_variable_cost(index, 1.0, self.constant)
