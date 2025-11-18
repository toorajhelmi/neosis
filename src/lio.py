"""Lio: The learner containing nodes, edges, memory, and lex (computational structure)."""

from typing import Dict, List, Optional, Tuple
from collections import defaultdict
import copy
import random

from .types import Node, NodeType, Edge, Lex, Mutation, MutationType
from .global_config import GlobalConfig


class Lio:
    """Lio is the learner - contains the computational structure (nodes, edges, memory, lex)."""
    
    def __init__(
        self,
        n: int = 1,
        memory: Optional[List[int]] = None,
        nodes: Optional[Dict[int, Node]] = None,
        edges: Optional[List[Edge]] = None,
        input_node_id: int = 0,
        output_node_id: int = 1,
        costs: Optional[Dict[MutationType, int]] = None
    ):
        """
        Initialize Lio with computational structure.
        
        Args:
            n: Number of memory bits
            memory: Initial memory state (defaults to all zeros)
            nodes: Dictionary of node_id -> Node (will create default if None)
            edges: List of edges (will create default if None)
            input_node_id: ID of the input node
            output_node_id: ID of the output node
            costs: Dictionary of mutation costs
        """
        self.n = n
        self.memory = memory if memory is not None else [0] * n
        self.input_node_id = input_node_id
        self.output_node_id = output_node_id
        
        # Initialize nodes if not provided
        if nodes is None:
            self.nodes = self._create_default_nodes()
        else:
            self.nodes = nodes
        
        # Initialize edges if not provided
        if edges is None:
            self.edges = self._create_default_edges()
        else:
            self.edges = edges
        
        # Build adjacency lists for efficient computation
        self._build_adjacency()
        
        # Mutation costs (use global defaults if not provided)
        self.costs = costs or GlobalConfig.get_mutation_costs()
    
    def _create_default_nodes(self) -> Dict[int, Node]:
        """Create default node structure for a minimal Lio."""
        nodes = {}
        
        # Input node
        nodes[self.input_node_id] = Node(
            node_id=self.input_node_id,
            node_type=NodeType.INPUT,
            value=0
        )
        
        # Memory node (if we have memory)
        if self.n > 0:
            memory_node_id = 2
            nodes[memory_node_id] = Node(
                node_id=memory_node_id,
                node_type=NodeType.MEMORY,
                value=self.memory[0] if self.memory else 0
            )
        
        # Computational node
        comp_node_id = 3
        lex = Lex(arity=1)
        lex.table[(0,)] = 1
        lex.table[(1,)] = 0
        nodes[comp_node_id] = Node(
            node_id=comp_node_id,
            node_type=NodeType.COMPUTATIONAL,
            lex=lex,
            value=0
        )
        
        # Output node
        nodes[self.output_node_id] = Node(
            node_id=self.output_node_id,
            node_type=NodeType.OUTPUT,
            value=0
        )
        
        return nodes
    
    def _create_default_edges(self) -> List[Edge]:
        """Create default edge structure for a minimal Lio."""
        edges = []
        
        # Connect input to computational node
        if self.input_node_id in self.nodes and 3 in self.nodes:
            edges.append(Edge(source_id=self.input_node_id, target_id=3))
        
        # Connect memory to computational node
        if 2 in self.nodes and 3 in self.nodes:
            edges.append(Edge(source_id=2, target_id=3))
        
        # Connect computational node to output
        if 3 in self.nodes and self.output_node_id in self.nodes:
            edges.append(Edge(source_id=3, target_id=self.output_node_id))
        
        return edges
    
    def _build_adjacency(self):
        """Build adjacency lists for efficient graph traversal."""
        self.incoming_edges: Dict[int, List[int]] = defaultdict(list)
        self.outgoing_edges: Dict[int, List[int]] = defaultdict(list)
        
        for edge in self.edges:
            self.incoming_edges[edge.target_id].append(edge.source_id)
            self.outgoing_edges[edge.source_id].append(edge.target_id)
    
    def get_next_node_id(self) -> int:
        """Get the next available node ID."""
        return max(self.nodes.keys(), default=-1) + 1
    
    def receive_input(self, u_t: int):
        """Receive perceptual input from NeoVerse."""
        if self.input_node_id in self.nodes:
            self.nodes[self.input_node_id].value = u_t
    
    def compute(self):
        """Perform one computation step using snapshot semantics."""
        # Create snapshot of current values
        snapshot = {node_id: node.value for node_id, node in self.nodes.items()}
        
        # Topological sort for computation order
        computation_order = self._topological_sort()
        
        # Compute each node in topological order
        for node_id in computation_order:
            node = self.nodes[node_id]
            
            if node.node_type == NodeType.INPUT:
                continue
            
            if node.node_type == NodeType.MEMORY:
                if node.lex:
                    input_values = []
                    for source_id in self.incoming_edges[node_id]:
                        input_values.append(snapshot[source_id])
                    if not input_values:
                        input_values = [snapshot[node_id]]
                    if len(input_values) == node.lex.arity:
                        inputs_tuple = tuple(input_values)
                        node.value = node.lex.compute(inputs_tuple)
                continue
            
            if node.node_type == NodeType.COMPUTATIONAL:
                input_values = []
                for source_id in self.incoming_edges[node_id]:
                    input_values.append(snapshot[source_id])
                if node.lex and len(input_values) == node.lex.arity:
                    inputs_tuple = tuple(input_values)
                    node.value = node.lex.compute(inputs_tuple)
                continue
            
            if node.node_type == NodeType.OUTPUT:
                if self.incoming_edges[node_id]:
                    source_id = self.incoming_edges[node_id][0]
                    # Use the current computed value, not the snapshot
                    # (since we compute in topological order, source is already computed)
                    node.value = self.nodes[source_id].value
                continue
        
        # Update memory nodes after computation (only if they don't have lex)
        for node_id, node in self.nodes.items():
            if node.node_type == NodeType.MEMORY and not node.lex:
                for source_id in self.incoming_edges[node_id]:
                    if source_id in self.nodes:
                        node.value = self.nodes[source_id].value
                        break
    
    def _topological_sort(self) -> List[int]:
        """Topological sort of nodes for computation order."""
        visited = set()
        result = []
        
        def visit(node_id: int):
            if node_id in visited:
                return
            visited.add(node_id)
            for source_id in self.incoming_edges[node_id]:
                visit(source_id)
            result.append(node_id)
        
        for node_id in self.nodes.keys():
            if node_id not in visited:
                visit(node_id)
        
        return result
    
    def get_output(self) -> int:
        """Get the current output prediction."""
        if self.output_node_id in self.nodes:
            return self.nodes[self.output_node_id].value
        return 0
    
    def update_memory(self):
        """Update memory bits from memory nodes."""
        memory_node_ids = [
            node_id for node_id, node in self.nodes.items()
            if node.node_type == NodeType.MEMORY
        ]
        for i, node_id in enumerate(memory_node_ids[:self.n]):
            if i < len(self.memory):
                self.memory[i] = self.nodes[node_id].value
    
    def get_size(self) -> int:
        """Get the number of nodes."""
        return len(self.nodes)
    
    def get_mutation_cost(self, mutation_type: MutationType) -> int:
        """Get the cost for a mutation type."""
        return self.costs.get(mutation_type, 0)
    
    def copy(self) -> 'Lio':
        """Create a deep copy of this Lio."""
        # Deep copy nodes
        new_nodes = {}
        for node_id, node in self.nodes.items():
            # Copy node with all its attributes
            new_lex = None
            if node.lex:
                new_lex = Lex(arity=node.lex.arity, table=dict(node.lex.table))
            new_nodes[node_id] = Node(
                node_id=node.node_id,
                node_type=node.node_type,
                value=node.value,
                lex=new_lex
            )
        
        # Deep copy edges
        new_edges = [Edge(source_id=e.source_id, target_id=e.target_id) for e in self.edges]
        
        # Create new Lio with copied structure
        new_lio = Lio(
            n=self.n,
            memory=list(self.memory),  # Copy memory list
            nodes=new_nodes,
            edges=new_edges,
            input_node_id=self.input_node_id,
            output_node_id=self.output_node_id,
            costs=dict(self.costs)  # Copy costs
        )
        
        # Rebuild adjacency lists
        new_lio._build_adjacency()
        
        return new_lio

