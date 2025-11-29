"""Simulation configuration definitions.

This file contains example simulation configurations. You can define
Neos of any size and structure by creating SimulationConfig objects.
Each config can optionally include a neo_factory function to customize
the Neo structure.
"""

from src.config import (
    SimulationConfig, NeoConfig, NeoVerseConfig, 
    LioConfig, EvoConfig, NeoVerseType
)
from src.global_config import GlobalConfig
from src.lio import Lio
from src.types import Node, NodeType, Edge, Lex, MutationType


def _create_minimal_lio_structure(lio: Lio) -> Lio:
    """Helper to build minimal Lio structure (3 nodes: input, memory with self-loop, output)."""
    lio.nodes = {}
    lio.edges = []
    # Input node
    lio.nodes[0] = Node(node_id=0, node_type=NodeType.INPUT, value=0)
    # Memory node with NOT operation (self-toggling)
    lex = Lex(arity=1)
    lex.table[(0,)] = 1  # NOT 0 = 1
    lex.table[(1,)] = 0  # NOT 1 = 0
    lio.nodes[2] = Node(node_id=2, node_type=NodeType.MEMORY, lex=lex, value=0)
    # Output node
    lio.nodes[1] = Node(node_id=1, node_type=NodeType.OUTPUT, value=0)
    # Edges: Memory -> Memory (self-loop), Memory -> Output
    lio.edges = [
        Edge(source_id=2, target_id=2),
        Edge(source_id=2, target_id=1)
    ]
    lio._build_adjacency()
    return lio


# List of simulation configurations
# Each config can have its own neo_factory if needed
SIMULATION_CONFIGS = [
    # ===== No mutations (baseline) =====
    SimulationConfig(
        name="MinimalNeo_no_mutations",
        neo=NeoConfig(n=1, memory=[0], energy=30, input_node_id=0, output_node_id=1),
        neoverse=NeoVerseConfig(neoverse_type=NeoVerseType.RANDOM, seed=42),
        lio=None,
        evo=None,
        run_cost=GlobalConfig.DEFAULT_RUN_COST,
        num_ticks=GlobalConfig.DEFAULT_NUM_TICKS,
        neo_factory=_create_minimal_lio_structure
    ),
    
    # ===== Lex mutations only =====
    SimulationConfig(
        name="MinimalNeo_lex_only",
        neo=NeoConfig(n=1, memory=[0], energy=30, input_node_id=0, output_node_id=1),
        neoverse=NeoVerseConfig(neoverse_type=NeoVerseType.RANDOM, seed=42),
        lio=LioConfig(
            bit_add_cost=999,  # Disable by making very expensive
            bit_remove_cost=999,
            edge_add_cost=999,
            edge_remove_cost=999,
            lex_flip_cost=GlobalConfig.MUTATION_COSTS[MutationType.LEX_FLIP]
        ),
        evo=EvoConfig(
            mutation_probability=GlobalConfig.DEFAULT_MUTATION_PROBABILITY,
            max_mutations_per_event=GlobalConfig.DEFAULT_MAX_MUTATIONS_PER_EVENT
        ),
        run_cost=GlobalConfig.DEFAULT_RUN_COST,
        num_ticks=GlobalConfig.DEFAULT_NUM_TICKS,
        neo_factory=_create_minimal_lio_structure
    ),
    
    # ===== Edge mutations only =====
    SimulationConfig(
        name="MinimalNeo_edges_only",
        neo=NeoConfig(n=1, memory=[0], energy=30, input_node_id=0, output_node_id=1),
        neoverse=NeoVerseConfig(neoverse_type=NeoVerseType.RANDOM, seed=42),
        lio=LioConfig(
            bit_add_cost=999,
            bit_remove_cost=999,
            edge_add_cost=GlobalConfig.MUTATION_COSTS[MutationType.EDGE_ADD],
            edge_remove_cost=GlobalConfig.MUTATION_COSTS[MutationType.EDGE_REMOVE],
            lex_flip_cost=999
        ),
        evo=EvoConfig(
            mutation_probability=GlobalConfig.DEFAULT_MUTATION_PROBABILITY,
            max_mutations_per_event=GlobalConfig.DEFAULT_MAX_MUTATIONS_PER_EVENT
        ),
        run_cost=GlobalConfig.DEFAULT_RUN_COST,
        num_ticks=GlobalConfig.DEFAULT_NUM_TICKS,
        neo_factory=_create_minimal_lio_structure
    ),
    
    # ===== Node mutations only =====
    SimulationConfig(
        name="MinimalNeo_nodes_only",
        neo=NeoConfig(n=1, memory=[0], energy=30, input_node_id=0, output_node_id=1),
        neoverse=NeoVerseConfig(neoverse_type=NeoVerseType.RANDOM, seed=42),
        lio=LioConfig(
            bit_add_cost=GlobalConfig.MUTATION_COSTS[MutationType.BIT_ADD],
            bit_remove_cost=GlobalConfig.MUTATION_COSTS[MutationType.BIT_REMOVE],
            edge_add_cost=999,
            edge_remove_cost=999,
            lex_flip_cost=999
        ),
        evo=EvoConfig(
            mutation_probability=GlobalConfig.DEFAULT_MUTATION_PROBABILITY,
            max_mutations_per_event=GlobalConfig.DEFAULT_MAX_MUTATIONS_PER_EVENT
        ),
        run_cost=GlobalConfig.DEFAULT_RUN_COST,
        num_ticks=GlobalConfig.DEFAULT_NUM_TICKS,
        neo_factory=_create_minimal_lio_structure
    ),
    
    # ===== All mutations =====
    SimulationConfig(
        name="MinimalNeo_all_mutations_balanced",
        neo=NeoConfig(n=1, memory=[0], energy=30, input_node_id=0, output_node_id=1),
        neoverse=NeoVerseConfig(neoverse_type=NeoVerseType.RANDOM, seed=42),
        lio=LioConfig(
            bit_add_cost=GlobalConfig.MUTATION_COSTS[MutationType.BIT_ADD],
            bit_remove_cost=GlobalConfig.MUTATION_COSTS[MutationType.BIT_REMOVE],
            edge_add_cost=GlobalConfig.MUTATION_COSTS[MutationType.EDGE_ADD],
            edge_remove_cost=GlobalConfig.MUTATION_COSTS[MutationType.EDGE_REMOVE],
            lex_flip_cost=GlobalConfig.MUTATION_COSTS[MutationType.LEX_FLIP]
        ),
        evo=EvoConfig(
            mutation_probability=GlobalConfig.DEFAULT_MUTATION_PROBABILITY,
            max_mutations_per_event=GlobalConfig.DEFAULT_MAX_MUTATIONS_PER_EVENT
        ),
        run_cost=GlobalConfig.DEFAULT_RUN_COST,
        num_ticks=GlobalConfig.DEFAULT_NUM_TICKS,
        neo_factory=_create_minimal_lio_structure
    ),
    
]


def get_example_simulation_configs() -> list[SimulationConfig]:
    """
    Get example simulation configurations.
    
    Returns the list of predefined configurations.
    You can modify SIMULATION_CONFIGS or create your own list.
    """
    return SIMULATION_CONFIGS

