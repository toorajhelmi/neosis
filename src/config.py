"""Configuration classes for Neosis simulations."""

from typing import Optional, Dict, Any, Callable
from pydantic import BaseModel, Field
from enum import Enum

from .neoverse import NeoVerse, RandomNeoVerse, AlternatingNeoVerse, BlockPatternNeoVerse
from .neo import Neo


class NeoVerseType(str, Enum):
    """Types of NeoVerse environments."""
    RANDOM = "random"
    ALTERNATING = "alternating"
    BLOCK = "block"


class NeoConfig(BaseModel):
    """Configuration for creating a Neo."""
    n: int = Field(default=1, description="Number of memory bits")
    memory: Optional[list[int]] = Field(default=None, description="Initial memory state")
    energy: int = Field(default=10, description="Initial energy in Nex")
    input_node_id: int = Field(default=0, description="Input node ID")
    output_node_id: int = Field(default=1, description="Output node ID")
    # For custom Neo structures, can provide nodes and edges
    nodes: Optional[Dict[int, Any]] = Field(default=None, description="Custom nodes (advanced)")
    edges: Optional[list[Any]] = Field(default=None, description="Custom edges (advanced)")


class LioConfig(BaseModel):
    """Configuration for Lio (computational structure)."""
    # Mutation costs (used by Evo when applying mutations)
    bit_add_cost: int = Field(default=2, description="Cost to add a memory bit")
    bit_remove_cost: int = Field(default=1, description="Cost to remove a memory bit")
    edge_add_cost: int = Field(default=1, description="Cost to add an edge")
    edge_remove_cost: int = Field(default=1, description="Cost to remove an edge")
    lex_flip_cost: int = Field(default=1, description="Cost to flip a lex entry")


class EvoConfig(BaseModel):
    """Configuration for Evo (applies mutations to Lio)."""
    mutation_probability: float = Field(
        default=0.1, 
        ge=0.0, 
        le=1.0, 
        description="Probability of attempting mutations in a given tick (0.0 = never, 1.0 = every tick)"
    )
    max_mutations_per_event: int = Field(
        default=2,
        ge=1,
        description="Maximum number of mutations to apply per mutation event"
    )
    # Can optionally override mutation costs (uses Lio's costs if not provided)


class NeoVerseConfig(BaseModel):
    """Configuration for NeoVerse environment."""
    neoverse_type: NeoVerseType = Field(description="Type of NeoVerse")
    seed: Optional[int] = Field(default=None, description="Random seed (for random NeoVerse)")


class SimulationConfig(BaseModel):
    """Complete configuration for a simulation run."""
    name: str = Field(description="Name of the simulation")
    neo: NeoConfig = Field(description="Neo configuration")
    neoverse: NeoVerseConfig = Field(description="NeoVerse configuration")
    lio: Optional[LioConfig] = Field(default=None, description="Lio configuration (None to disable)")
    evo: Optional[EvoConfig] = Field(default=None, description="Evo configuration (None to disable)")
    run_cost: int = Field(default=1, description="Cost per node per tick")
    num_ticks: int = Field(default=100, description="Number of ticks to simulate")
    enable_offspring: bool = Field(default=True, description="Enable offspring creation on mutation (if False, mutations apply directly to Neo)")
    neo_factory: Optional[Callable] = Field(
        default=None, 
        description="Optional factory function to customize Lio structure after creation (takes Lio, returns Lio)"
    )
    
    class Config:
        arbitrary_types_allowed = True  # Allow callable types
    
    def create_neoverse(self) -> NeoVerse:
        """Create a NeoVerse instance from configuration."""
        if self.neoverse.neoverse_type == NeoVerseType.RANDOM:
            return RandomNeoVerse(seed=self.neoverse.seed)
        elif self.neoverse.neoverse_type == NeoVerseType.ALTERNATING:
            return AlternatingNeoVerse()
        elif self.neoverse.neoverse_type == NeoVerseType.BLOCK:
            return BlockPatternNeoVerse()
        else:
            raise ValueError(f"Unknown NeoVerse type: {self.neoverse.neoverse_type}")

