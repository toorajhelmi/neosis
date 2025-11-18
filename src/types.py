"""Core types and Pydantic models for Neosis."""

from typing import Dict, List, Tuple, Optional
from enum import Enum
from pydantic import BaseModel, Field


class MutationType(str, Enum):
    """Types of mutations that can be applied to a Neo."""
    BIT_ADD = "bit+"
    BIT_REMOVE = "bit-"
    EDGE_ADD = "edge+"
    EDGE_REMOVE = "edge-"
    LEX_FLIP = "lexflip"


class NodeType(str, Enum):
    """Types of nodes in a Neo."""
    INPUT = "input"
    MEMORY = "memory"
    COMPUTATIONAL = "computational"
    OUTPUT = "output"


class Lex(BaseModel):
    """Lex (truth table) for a node with k inputs."""
    
    arity: int = Field(ge=0, description="Number of inputs (k)")
    table: Dict[Tuple[int, ...], int] = Field(
        default_factory=dict,
        description="Mapping from input tuples to output bits"
    )
    
    def __init__(self, arity: int = 0, table: Optional[Dict[Tuple[int, ...], int]] = None, **kwargs):
        super().__init__(arity=arity, table=table or {}, **kwargs)
        # Initialize all possible input combinations if table is empty
        if not self.table and arity > 0:
            self._initialize_table()
    
    def _initialize_table(self):
        """Initialize lex with all possible input combinations."""
        for i in range(2 ** self.arity):
            inputs = tuple((i >> j) & 1 for j in range(self.arity - 1, -1, -1))
            self.table[inputs] = 0
    
    def compute(self, inputs: Tuple[int, ...]) -> int:
        """Compute output for given inputs."""
        if len(inputs) != self.arity:
            raise ValueError(f"Expected {self.arity} inputs, got {len(inputs)}")
        return self.table.get(inputs, 0)
    
    def flip(self, inputs: Tuple[int, ...]) -> bool:
        """Flip the output for a given input combination. Returns True if successful."""
        if inputs not in self.table:
            return False
        self.table[inputs] = 1 - self.table[inputs]
        return True
    
    def get_all_inputs(self) -> List[Tuple[int, ...]]:
        """Get all possible input combinations."""
        return list(self.table.keys())


class Node(BaseModel):
    """A node in the Neo graph."""
    
    node_id: int = Field(description="Unique identifier for the node")
    node_type: NodeType = Field(description="Type of the node")
    lex: Optional[Lex] = Field(default=None, description="Lex (truth table) for computational nodes")
    value: int = Field(default=0, ge=0, le=1, description="Current value of the node")
    
    class Config:
        frozen = False  # Allow mutation for value updates


class Edge(BaseModel):
    """A directed edge in the Neo graph."""
    
    source_id: int = Field(description="Source node ID")
    target_id: int = Field(description="Target node ID")
    
    class Config:
        frozen = True


class Mutation(BaseModel):
    """A mutation proposal from Lio."""
    
    mutation_type: MutationType = Field(description="Type of mutation")
    target_id: Optional[int] = Field(default=None, description="Target node/edge ID for the mutation")
    additional_params: Dict = Field(default_factory=dict, description="Additional parameters for the mutation")
    
    class Config:
        frozen = True

