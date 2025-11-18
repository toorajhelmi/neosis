"""NeoCycle: The main simulation loop for Neosis."""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field

from .neo import Neo
from .lio import Lio
from .evo import Evo
from .neoverse import NeoVerse
from .types import Mutation, MutationType, Edge, Node, NodeType, Lex
from .config import SimulationConfig


@dataclass
class NeoLineage:
    """Results for a single Neo lineage (parent and its descendants)."""
    lineage_id: int
    parent_id: Optional[int]  # None for root
    energy_history: List[int]
    accuracy_history: List[float]
    predictions: List[int]
    actuals: List[int]
    rewards: List[int]
    size_history: List[int]
    mutations_applied: List[str]
    birth_tick: int  # When this lineage was created
    death_tick: Optional[int]  # When this lineage died (None if still alive)


@dataclass
class SimulationResult:
    """Results from a simulation run."""
    energy_history: List[int]
    accuracy_history: List[float]
    predictions: List[int]
    actuals: List[int]
    rewards: List[int]
    size_history: List[int]
    mutations_applied: List[str]
    lineages: List[NeoLineage]  # All Neo lineages (offsprings)


class NeoCycle:
    """The main simulation loop for Neosis."""
    
    def __init__(
        self,
        neo: Neo,
        neoverse: NeoVerse,
        run_cost: int = 1
    ):
        """
        Initialize NeoCycle.
        
        Args:
            neo: The Neo to simulate (contains Lio and optionally Evo)
            neoverse: The NeoVerse environment
            run_cost: Cost per node per tick
        """
        self.neo = neo
        self.neoverse = neoverse
        self.run_cost = run_cost
    
    def run(self, num_ticks: int, enable_offspring: bool = True) -> SimulationResult:
        """
        Run the simulation for a specified number of ticks.
        
        Args:
            num_ticks: Number of ticks to simulate
            enable_offspring: If True, when a mutation happens, the parent stops mutating 
                            and creates an offspring. If False, mutations apply directly 
                            to the Neo (original behavior).
            
        Returns:
            SimulationResult with history of the simulation and all lineages
        """
        # Track active Neos: (neo, lineage_id, parent_id, birth_tick, history)
        active_neos: List[Tuple[Neo, int, Optional[int], int, Dict]] = [
            (self.neo, 0, None, 0, {
                'energy_history': [self.neo.energy],
                'accuracy_history': [],
                'predictions': [],
                'actuals': [],
                'rewards': [],
                'size_history': [self.neo.get_size()],
                'mutations_applied': []
            })
        ]
        
        next_lineage_id = 1
        all_lineages: List[NeoLineage] = []
        
        for t in range(num_ticks):
            new_offsprings = []
            dead_lineages = []
            
            # Process each active Neo
            for neo, lineage_id, parent_id, birth_tick, history in active_neos:
                # Check if Neo has enough energy
                required_cost = self.run_cost * neo.lio.get_size()
                
                if neo.energy < required_cost:
                    # Neo dies - record final state
                    history['energy_history'].append(neo.energy)
                    all_lineages.append(NeoLineage(
                        lineage_id=lineage_id,
                        parent_id=parent_id,
                        energy_history=history['energy_history'],
                        accuracy_history=history['accuracy_history'],
                        predictions=history['predictions'],
                        actuals=history['actuals'],
                        rewards=history['rewards'],
                        size_history=history['size_history'],
                        mutations_applied=history['mutations_applied'],
                        birth_tick=birth_tick,
                        death_tick=t
                    ))
                    dead_lineages.append((neo, lineage_id))
                    continue
                
                # Step 1: Receive input
                u_t = self.neoverse.get_input(t)
                neo.lio.receive_input(u_t)
                
                # Step 2: Compute
                neo.lio.compute()
                
                # Step 3: Get prediction
                y_t = neo.lio.get_output()
                history['predictions'].append(y_t)
                
                # Step 4: Pay run cost
                neo.pay_energy(required_cost)
                
                # Step 5: Get next input and compute reward
                u_t_plus_1 = self.neoverse.get_input(t + 1)
                history['actuals'].append(u_t_plus_1)
                reward = self.neoverse.compute_reward(y_t, u_t_plus_1, num_nodes=neo.lio.get_size())
                history['rewards'].append(reward)
                
                # Step 6: Receive reward
                neo.receive_reward(reward)
                history['energy_history'].append(neo.energy)
                
                # Step 7: Update accuracy (per-lineage)
                correct_in_lineage = sum(1 for i, p in enumerate(history['predictions']) 
                                        if i < len(history['actuals']) and p == history['actuals'][i])
                total_in_lineage = len(history['predictions'])
                accuracy = correct_in_lineage / total_in_lineage if total_in_lineage > 0 else 0.0
                history['accuracy_history'].append(accuracy)
                
                # Step 8: Check for mutations (only if Evo exists and hasn't been disabled)
                if neo.evo:
                    next_tick_run_cost = self.run_cost * neo.lio.get_size()
                    safety_buffer = max(1, next_tick_run_cost // 2)
                    reserved_energy = next_tick_run_cost + safety_buffer
                    available_for_mutations = max(0, neo.energy - reserved_energy)
                    
                    if available_for_mutations > 0:
                        applied_mutations = neo.evo.apply_mutations(neo.lio, available_for_mutations)
                        
                        if applied_mutations:
                            # Record mutations and pay costs
                            for mutation in applied_mutations:
                                cost = neo.lio.get_mutation_cost(mutation.mutation_type)
                                neo.pay_energy(cost)
                                history['mutations_applied'].append(f"t={t}: {mutation.mutation_type.value}")
                            
                            if enable_offspring:
                                # Create offspring with mutated state
                                offspring = neo.create_offspring()
                                
                                # Inherit parent's history up to current tick (t)
                                # At the time of offspring creation (after step 7), the parent has:
                                # - Made t+1 predictions (indices 0 to t, including the one just made at tick t)
                                # - Received t+1 actuals (indices 0 to t, including the one just received at tick t)
                                # - Has t+1 accuracy values (indices 0 to t)
                                # We want to inherit exactly t predictions and t actuals (up to but not including tick t)
                                # This matches what the parent had at the END of tick t-1, which is what we want
                                parent_predictions = list(history['predictions'][:t])  # First t predictions (indices 0 to t-1)
                                parent_actuals = list(history['actuals'][:t])  # First t actuals (indices 0 to t-1)
                                
                                # Use parent's accuracy at tick t (the last accuracy, which is the current tick's accuracy)
                                # This is the accuracy the parent had at the end of tick t, which is what we want to inherit
                                parent_accuracy = history['accuracy_history'][-1] if history['accuracy_history'] else 0.0
                                
                                new_offsprings.append((offspring, next_lineage_id, lineage_id, t + 1, {
                                    'energy_history': [offspring.energy],
                                    'accuracy_history': [parent_accuracy],  # Start with parent's accuracy at tick t-1
                                    'predictions': parent_predictions,  # Inherit parent's prediction history up to tick t-1
                                    'actuals': parent_actuals,  # Inherit parent's actual history up to tick t-1
                                    'rewards': list(history['rewards'][:t]),  # Inherit parent's reward history up to tick t-1
                                    'size_history': [offspring.get_size()],
                                    'mutations_applied': []
                                }))
                                next_lineage_id += 1
                                
                                # Disable mutations on parent (remove Evo)
                                neo.evo = None
                            # If enable_offspring=False, mutations apply directly and Neo continues mutating
                
                # Step 9: Update memory
                neo.lio.update_memory()
                history['size_history'].append(neo.get_size())
            
            # Remove dead lineages
            active_neos = [(n, lid, pid, bt, h) for n, lid, pid, bt, h in active_neos 
                          if (n, lid) not in dead_lineages]
            
            # Add new offsprings
            active_neos.extend(new_offsprings)
            
            # If no active Neos, simulation ends
            if not active_neos:
                break
        
        # Record remaining active lineages
        for neo, lineage_id, parent_id, birth_tick, history in active_neos:
            all_lineages.append(NeoLineage(
                lineage_id=lineage_id,
                parent_id=parent_id,
                energy_history=history['energy_history'],
                accuracy_history=history['accuracy_history'],
                predictions=history['predictions'],
                actuals=history['actuals'],
                rewards=history['rewards'],
                size_history=history['size_history'],
                mutations_applied=history['mutations_applied'],
                birth_tick=birth_tick,
                death_tick=None  # Still alive
            ))
        
        # For backward compatibility, use the root lineage (lineage_id=0) for main results
        root_lineage = next((l for l in all_lineages if l.lineage_id == 0), None)
        if root_lineage:
            return SimulationResult(
                energy_history=root_lineage.energy_history,
                accuracy_history=root_lineage.accuracy_history,
                predictions=root_lineage.predictions,
                actuals=root_lineage.actuals,
                rewards=root_lineage.rewards,
                size_history=root_lineage.size_history,
                mutations_applied=root_lineage.mutations_applied,
                lineages=all_lineages
            )
        else:
            # Fallback if no root lineage
            return SimulationResult(
                energy_history=[],
                accuracy_history=[],
                predictions=[],
                actuals=[],
                rewards=[],
                size_history=[],
                mutations_applied=[],
                lineages=all_lineages
            )
    


# Configuration-based simulation runner functions

def create_neo_from_config(config: SimulationConfig, lio_factory=None) -> Neo:
    """
    Create a Neo instance from configuration.
    
    Args:
        config: Simulation configuration
        lio_factory: Optional function to customize Lio after creation
                    (e.g., for custom node structures)
    """
    # Create Lio with computational structure
    costs = None
    if config.lio:
        costs = {
            MutationType.BIT_ADD: config.lio.bit_add_cost,
            MutationType.BIT_REMOVE: config.lio.bit_remove_cost,
            MutationType.EDGE_ADD: config.lio.edge_add_cost,
            MutationType.EDGE_REMOVE: config.lio.edge_remove_cost,
            MutationType.LEX_FLIP: config.lio.lex_flip_cost,
        }
    
    lio = Lio(
        n=config.neo.n,
        memory=config.neo.memory,
        nodes=config.neo.nodes,
        edges=config.neo.edges,
        input_node_id=config.neo.input_node_id,
        output_node_id=config.neo.output_node_id,
        costs=costs
    )
    
    # Apply custom factory if provided
    if lio_factory is not None:
        lio = lio_factory(lio)
    
    # Create Evo if configured
    evo = None
    if config.evo:
        evo_costs = {
            MutationType.BIT_ADD: config.lio.bit_add_cost if config.lio else 2,
            MutationType.BIT_REMOVE: config.lio.bit_remove_cost if config.lio else 1,
            MutationType.EDGE_ADD: config.lio.edge_add_cost if config.lio else 1,
            MutationType.EDGE_REMOVE: config.lio.edge_remove_cost if config.lio else 1,
            MutationType.LEX_FLIP: config.lio.lex_flip_cost if config.lio else 1,
        }
        evo = Evo(
            mutation_probability=config.evo.mutation_probability,
            max_mutations_per_event=config.evo.max_mutations_per_event,
            costs=evo_costs
        )
    
    # Create Neo as container
    neo = Neo(
        lio=lio,
        evo=evo,
        energy=config.neo.energy
    )
    
    return neo




def run_simulation(config: SimulationConfig, enable_offspring: Optional[bool] = None) -> SimulationResult:
    """
    Run a simulation from a configuration object.
    
    Args:
        config: Simulation configuration (includes neo_factory if needed)
        enable_offspring: Override config.enable_offspring if provided (None = use config value)
        
    Returns:
        SimulationResult
    """
    # Create Neo (use factory from config if provided)
    neo = create_neo_from_config(config, lio_factory=config.neo_factory)
    
    # Create NeoVerse
    neoverse = config.create_neoverse()
    
    # Use parameter override or config value
    use_offspring = enable_offspring if enable_offspring is not None else config.enable_offspring
    
    # Create and run simulation
    cycle = NeoCycle(
        neo=neo,
        neoverse=neoverse,
        run_cost=config.run_cost
    )
    
    result = cycle.run(config.num_ticks, enable_offspring=use_offspring)
    return result


def run_simulations_from_configs(configs: List[SimulationConfig]) -> Dict[str, SimulationResult]:
    """
    Run multiple simulations from configuration objects.
    
    Args:
        configs: List of SimulationConfig objects (each can have its own neo_factory)
        
    Returns:
        Dictionary mapping simulation name to SimulationResult
    """
    results = {}
    for config in configs:
        try:
            result = run_simulation(config)
            results[config.name] = result
        except Exception as e:
            print(f"Error running simulation {config.name}: {e}")
            import traceback
            traceback.print_exc()
            # Continue with other simulations
    return results

