"""Global configuration values for Neosis simulations."""

from typing import Dict
from .types import MutationType


class GlobalConfig:
    """Global configuration values used across simulations."""
    
    # Mutation costs (in Nex)
    MUTATION_COSTS: Dict[MutationType, int] = {
        MutationType.BIT_ADD: 1,
        MutationType.BIT_REMOVE: 1,
        MutationType.EDGE_ADD: 1,
        MutationType.EDGE_REMOVE: 1,
        MutationType.LEX_FLIP: 1,
    }
    
    # Default mutation probability for Evo
    DEFAULT_MUTATION_PROBABILITY: float = 0.15
    
    # Default max mutations per event
    DEFAULT_MAX_MUTATIONS_PER_EVENT: int = 2
    
    # Default run cost per node per tick
    DEFAULT_RUN_COST: int = 1
    
    # Default number of ticks
    DEFAULT_NUM_TICKS: int = 100
    
    @classmethod
    def get_mutation_costs(cls) -> Dict[MutationType, int]:
        """Get the global mutation costs."""
        return cls.MUTATION_COSTS.copy()
    
    @classmethod
    def set_mutation_cost(cls, mutation_type: MutationType, cost: int):
        """Set the cost for a specific mutation type."""
        cls.MUTATION_COSTS[mutation_type] = cost
    
    @classmethod
    def set_all_mutation_costs(cls, cost: int):
        """Set all mutation costs to the same value."""
        for mutation_type in MutationType:
            cls.MUTATION_COSTS[mutation_type] = cost


