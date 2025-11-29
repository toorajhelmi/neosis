"""Evo: Applies mutations to Lio based on available energy."""

from typing import List, Optional, Dict
import random

from .lio import Lio
from .types import Mutation, MutationType, Edge, Node, NodeType, Lex


class Evo:
    """Evo applies mutations to Lio. Can apply multiple mutations per cycle based on available energy."""
    
    def __init__(self, mutation_probability: float = 0.1, max_mutations_per_event: int = 3, costs: Optional[Dict[MutationType, int]] = None):
        """
        Initialize Evo.
        
        Args:
            mutation_probability: Probability of attempting mutations in a given tick (0.0 = never, 1.0 = every tick)
            max_mutations_per_event: Maximum number of mutations to apply per mutation event
            costs: Dictionary of mutation costs (uses Lio's costs if None)
        """
        self.mutation_probability = mutation_probability
        self.max_mutations_per_event = max_mutations_per_event
        self.costs = costs  # If None, will use Lio's costs
    
    def apply_mutations(self, lio: Lio, available_energy: int) -> List[Mutation]:
        """
        Apply mutations to Lio based on available energy.
        Only attempts mutations with probability mutation_probability.
        Uniform random selection of mutation types.
        Continues until energy runs out or no more mutations can be applied.
        
        Args:
            lio: Lio to mutate
            available_energy: Available energy in Nex
            
        Returns:
            List of mutations that were applied
        """
        applied = []
        
        # Check if we should attempt mutations this tick
        if random.random() > self.mutation_probability:
            return applied  # Skip mutations this tick
        
        remaining_energy = available_energy
        
        # Use Lio's costs if Evo doesn't have its own
        costs = self.costs if self.costs else lio.costs
        
        # Keep applying mutations while we have energy
        # Try up to a reasonable number of attempts to avoid infinite loops
        max_attempts = 100
        attempts = 0
        
        # Filter to only affordable mutation types to avoid wasted attempts
        affordable_types = [
            mt for mt in MutationType 
            if costs.get(mt, 0) > 0 and costs.get(mt, 0) <= remaining_energy
        ]
        
        if not affordable_types:
            return applied  # No affordable mutations
        
        while remaining_energy > 0 and attempts < max_attempts and len(applied) < self.max_mutations_per_event:
            attempts += 1
            
            # Uniform random selection from affordable mutation types only
            mutation_type = random.choice(affordable_types)
            cost = costs.get(mutation_type, 0)
            
            # Generate mutation
            mutation = self._generate_mutation(lio, mutation_type)
            if mutation is None:
                continue  # Can't generate this mutation (e.g., no edges to remove), try another type
            
            # Apply mutation
            if self._apply_mutation(lio, mutation):
                applied.append(mutation)
                remaining_energy -= cost
                attempts = 0  # Reset attempts counter on success
                # Update affordable types based on remaining energy
                affordable_types = [
                    mt for mt in MutationType 
                    if costs.get(mt, 0) > 0 and costs.get(mt, 0) <= remaining_energy
                ]
                if not affordable_types:
                    break  # No more affordable mutations
            # If failed to apply, try another mutation type
        
        return applied
    
    def _generate_mutation(self, lio: Lio, mutation_type: MutationType) -> Optional[Mutation]:
        """Generate a mutation of the given type."""
        if mutation_type == MutationType.BIT_ADD:
            return Mutation(
                mutation_type=MutationType.BIT_ADD,
                additional_params={"new_bit_value": 0}
            )
        elif mutation_type == MutationType.BIT_REMOVE:
            if lio.n <= 0:
                return None
            return Mutation(
                mutation_type=MutationType.BIT_REMOVE,
                additional_params={"bit_index": random.randint(0, lio.n - 1)}
            )
        elif mutation_type == MutationType.EDGE_ADD:
            node_ids = list(lio.nodes.keys())
            if len(node_ids) < 2:
                return None
            source_id = random.choice(node_ids)
            target_id = random.choice(node_ids)
            if source_id == target_id:
                return None
            # Check if edge already exists
            for edge in lio.edges:
                if edge.source_id == source_id and edge.target_id == target_id:
                    return None
            return Mutation(
                mutation_type=MutationType.EDGE_ADD,
                additional_params={"source_id": source_id, "target_id": target_id}
            )
        elif mutation_type == MutationType.EDGE_REMOVE:
            if not lio.edges:
                return None
            edge = random.choice(lio.edges)
            return Mutation(
                mutation_type=MutationType.EDGE_REMOVE,
                additional_params={"source_id": edge.source_id, "target_id": edge.target_id}
            )
        elif mutation_type == MutationType.LEX_FLIP:
            computational_nodes = [
                node_id for node_id, node in lio.nodes.items()
                if (node.node_type == NodeType.COMPUTATIONAL or 
                    (node.node_type == NodeType.MEMORY and node.lex)) and node.lex
            ]
            if not computational_nodes:
                return None
            node_id = random.choice(computational_nodes)
            node = lio.nodes[node_id]
            if not node.lex or not node.lex.table:
                return None
            inputs = random.choice(list(node.lex.table.keys()))
            return Mutation(
                mutation_type=MutationType.LEX_FLIP,
                target_id=node_id,
                additional_params={"inputs": inputs}
            )
        return None
    
    def _apply_mutation(self, lio: Lio, mutation: Mutation) -> bool:
        """Apply a mutation to Lio. Returns True if successful."""
        if mutation.mutation_type == MutationType.BIT_ADD:
            new_bit_value = mutation.additional_params.get("new_bit_value", 0)
            lio.n += 1
            lio.memory.append(new_bit_value)
            new_node_id = lio.get_next_node_id()
            lio.nodes[new_node_id] = Node(
                node_id=new_node_id,
                node_type=NodeType.MEMORY,
                value=new_bit_value
            )
            
            # Automatically connect new node with an incoming edge from a random existing node
            # This makes the node immediately useful (cost is still 1, not 2)
            existing_node_ids = [nid for nid in lio.nodes.keys() if nid != new_node_id]
            if existing_node_ids:
                source_id = random.choice(existing_node_ids)
                # Don't create self-loops for the new node (it has no lex yet)
                # Create edge from existing node to new node
                new_edge = Edge(source_id=source_id, target_id=new_node_id)
                lio.edges.append(new_edge)
            
            lio._build_adjacency()
            
            # Update new node's lex arity if needed (it will need a lex for computation)
            if new_node_id in lio.nodes:
                node = lio.nodes[new_node_id]
                if node.node_type == NodeType.MEMORY:
                    # Create a default lex for the new memory node based on incoming edges
                    incoming_count = len(lio.incoming_edges.get(new_node_id, []))
                    if incoming_count > 0:
                        # Create a default lex (all zeros) - mutations can change it later
                        node.lex = Lex(arity=incoming_count)
            
            return True
        
        elif mutation.mutation_type == MutationType.BIT_REMOVE:
            if lio.n <= 0:
                return False
            bit_index = mutation.additional_params.get("bit_index", 0)
            if bit_index < len(lio.memory):
                lio.memory.pop(bit_index)
                lio.n -= 1
                memory_nodes = [
                    node_id for node_id, node in lio.nodes.items()
                    if node.node_type == NodeType.MEMORY
                ]
                if memory_nodes:
                    node_to_remove = memory_nodes[min(bit_index, len(memory_nodes) - 1)]
                    lio.edges = [
                        e for e in lio.edges
                        if e.source_id != node_to_remove and e.target_id != node_to_remove
                    ]
                    del lio.nodes[node_to_remove]
                    lio._build_adjacency()
                return True
            return False
        
        elif mutation.mutation_type == MutationType.EDGE_ADD:
            source_id = mutation.additional_params.get("source_id")
            target_id = mutation.additional_params.get("target_id")
            if source_id is None or target_id is None:
                return False
            if source_id not in lio.nodes or target_id not in lio.nodes:
                return False
            # Check if edge already exists
            for edge in lio.edges:
                if edge.source_id == source_id and edge.target_id == target_id:
                    return False
            new_edge = Edge(source_id=source_id, target_id=target_id)
            lio.edges.append(new_edge)
            lio._build_adjacency()
            # Update target node's lex arity if needed
            if target_id in lio.nodes:
                node = lio.nodes[target_id]
                if node.lex:
                    new_arity = len(lio.incoming_edges[target_id])
                    old_arity = node.lex.arity
                    if new_arity != old_arity:
                        # When arity increases, combine old function with new input using AND
                        # This makes the new input actually matter
                        old_table = dict(node.lex.table)
                        new_table = {}
                        
                        # Generate all possible input combinations for new arity
                        for i in range(2 ** new_arity):
                            new_inputs = tuple((i >> j) & 1 for j in range(new_arity - 1, -1, -1))
                            
                            if old_arity > 0:
                                # Use first old_arity inputs to compute old function
                                old_inputs = new_inputs[:old_arity]
                                old_output = old_table.get(old_inputs, 0)
                                
                                # Combine with new input(s) using AND
                                # For each new input beyond old_arity, AND it with the old output
                                combined_output = old_output
                                for j in range(old_arity, new_arity):
                                    combined_output = combined_output & new_inputs[j]
                                
                                new_table[new_inputs] = combined_output
                            else:
                                # No old function, default to 0
                                new_table[new_inputs] = 0
                        
                        # Create new lex with combined table
                        node.lex = Lex(arity=new_arity, table=new_table)
            return True
        
        elif mutation.mutation_type == MutationType.EDGE_REMOVE:
            source_id = mutation.additional_params.get("source_id")
            target_id = mutation.additional_params.get("target_id")
            if source_id is None or target_id is None:
                return False
            lio.edges = [
                e for e in lio.edges
                if not (e.source_id == source_id and e.target_id == target_id)
            ]
            lio._build_adjacency()
            # Update target node's lex arity if needed
            if target_id in lio.nodes:
                node = lio.nodes[target_id]
                if node.lex:
                    new_arity = len(lio.incoming_edges[target_id])
                    old_arity = node.lex.arity
                    if new_arity != old_arity:
                        # Preserve old behavior: project the old truth table
                        # Use the first k inputs (where k = new_arity) from the old function
                        old_table = dict(node.lex.table)
                        new_table = {}
                        
                        # Generate all possible input combinations for new arity
                        for i in range(2 ** new_arity):
                            new_inputs = tuple((i >> j) & 1 for j in range(new_arity - 1, -1, -1))
                            # Extend to old arity by padding with zeros (or use first k inputs)
                            # We'll use the first k inputs and pad with zeros if needed
                            if new_arity <= old_arity:
                                # Project: use first new_arity inputs, pad with zeros
                                old_inputs = new_inputs + tuple([0] * (old_arity - new_arity))
                            else:
                                # This shouldn't happen (removing edge reduces arity)
                                old_inputs = new_inputs[:old_arity]
                            
                            # Get output from old table (default to 0 if not found)
                            output = old_table.get(old_inputs, 0)
                            new_table[new_inputs] = output
                        
                        # Create new lex with projected table
                        node.lex = Lex(arity=new_arity, table=new_table)
            return True
        
        elif mutation.mutation_type == MutationType.LEX_FLIP:
            node_id = mutation.target_id
            if node_id is None or node_id not in lio.nodes:
                return False
            node = lio.nodes[node_id]
            if node.lex is None:
                return False
            inputs = mutation.additional_params.get("inputs")
            if inputs is None:
                return False
            if not isinstance(inputs, tuple):
                inputs = tuple(inputs)
            node.lex.flip(inputs)
            return True
        
        return False

