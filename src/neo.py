"""Neo: Container for Lio and Evo."""

from typing import Optional

from .lio import Lio
from .evo import Evo


class Neo:
    """Neo is a container that holds Lio (computational structure) and Evo (mutator)."""
    
    def __init__(
        self,
        lio: Lio,
        evo: Optional[Evo] = None,
        energy: int = 10
    ):
        """
        Initialize a Neo.
        
        Args:
            lio: Lio instance (contains nodes, edges, memory - the computational structure)
            evo: Optional Evo instance (applies mutations to Lio)
            energy: Initial energy in Nex
        """
        self.lio = lio
        self.evo = evo
        self.energy = energy
    
    def has_energy(self, amount: int) -> bool:
        """Check if Neo has enough energy."""
        return self.energy >= amount
    
    def pay_energy(self, amount: int) -> int:
        """Pay energy cost. Returns actual amount paid."""
        actual = min(amount, self.energy)
        self.energy -= actual
        return actual
    
    def receive_reward(self, reward: int):
        """Receive energy reward (Spark) from NeoVerse."""
        self.energy += reward
    
    def get_size(self) -> int:
        """Get the number of nodes in Lio."""
        return self.lio.get_size()
    
    def create_offspring(self) -> 'Neo':
        """
        Create an offspring Neo with the same state (energy and structure).
        The offspring can mutate, while the parent should stop mutating.
        
        Returns:
            A new Neo instance with copied Lio and Evo
        """
        # Copy Lio structure
        new_lio = self.lio.copy()
        
        # Copy Evo if it exists (with same mutation probability and settings)
        new_evo = None
        if self.evo:
            from .evo import Evo
            new_evo = Evo(
                mutation_probability=self.evo.mutation_probability,
                max_mutations_per_event=self.evo.max_mutations_per_event,
                costs=dict(self.evo.costs) if self.evo.costs else None
            )
        
        # Create offspring with same energy
        offspring = Neo(
            lio=new_lio,
            evo=new_evo,
            energy=self.energy
        )
        
        return offspring
