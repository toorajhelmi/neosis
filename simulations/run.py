"""Main entry point for running simulations and plotting results."""

from typing import Dict, List, Optional, Tuple
from collections import Counter
import json
import os
from datetime import datetime
try:
    import matplotlib.pyplot as plt
    from matplotlib.ticker import MaxNLocator
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    MaxNLocator = None

from src.simulation import SimulationResult, NeoLineage, run_simulations_from_configs
from src.config import SimulationConfig
from .configs import get_example_simulation_configs


def lineage_to_dict(lineage: NeoLineage) -> dict:
    """Convert NeoLineage to a dictionary for JSON serialization."""
    return {
        "lineage_id": lineage.lineage_id,
        "parent_id": lineage.parent_id,
        "birth_tick": lineage.birth_tick,
        "death_tick": lineage.death_tick,
        "energy_history": lineage.energy_history,
        "accuracy_history": lineage.accuracy_history,
        "predictions": lineage.predictions,
        "actuals": lineage.actuals,
        "rewards": lineage.rewards,
        "size_history": lineage.size_history,
        "mutations_applied": lineage.mutations_applied
    }


def result_to_dict(result: SimulationResult) -> dict:
    """Convert SimulationResult to a dictionary for JSON serialization."""
    return {
        "energy_history": result.energy_history,
        "accuracy_history": result.accuracy_history,
        "predictions": result.predictions,
        "actuals": result.actuals,
        "rewards": result.rewards,
        "size_history": result.size_history,
        "mutations_applied": result.mutations_applied,
        "lineages": [lineage_to_dict(l) for l in result.lineages]
    }


def config_to_dict(config: SimulationConfig) -> dict:
    """Convert SimulationConfig to a dictionary for JSON serialization."""
    config_dict = {
        "name": config.name,
        "neo": {
            "n": config.neo.n,
            "energy": config.neo.energy,
            "input_node_id": config.neo.input_node_id,
            "output_node_id": config.neo.output_node_id,
            "memory": config.neo.memory
        },
        "neoverse": {
            "neoverse_type": config.neoverse.neoverse_type.value,
            "seed": config.neoverse.seed
        },
        "run_cost": config.run_cost,
        "num_ticks": config.num_ticks
    }
    
    if config.lio:
        config_dict["lio"] = {
            "bit_add_cost": config.lio.bit_add_cost,
            "bit_remove_cost": config.lio.bit_remove_cost,
            "edge_add_cost": config.lio.edge_add_cost,
            "edge_remove_cost": config.lio.edge_remove_cost,
            "lex_flip_cost": config.lio.lex_flip_cost
        }
    else:
        config_dict["lio"] = None
    
    if config.evo:
        config_dict["evo"] = {}  # EvoConfig is empty now
    else:
        config_dict["evo"] = None
    
    return config_dict


def generate_filename_from_configs(configs: List[SimulationConfig]) -> str:
    """
    Generate a descriptive filename from configuration values.
    
    Args:
        configs: List of simulation configurations
        
    Returns:
        Filename prefix based on config values
    """
    if not configs:
        return "simulation"
    
    # Use the first config as representative (assuming all configs share key parameters)
    config = configs[0]
    
    parts = []
    
    # Neo configuration
    parts.append(f"n{config.neo.n}")  # Number of memory bits
    parts.append(f"E{config.neo.energy}")  # Initial energy
    
    # Lio configuration
    if config.lio:
        parts.append("lio")
    else:
        parts.append("nolio")
    
    # Evo configuration
    if config.evo:
        parts.append("evo")
    else:
        parts.append("noevo")
    
    # NeoVerse type
    parts.append(config.neoverse.neoverse_type.value)
    
    # Run cost
    parts.append(f"cost{config.run_cost}")
    
    return "_".join(parts)


def log_results(results: Dict[str, SimulationResult], configs: List[SimulationConfig], 
                output_dir: str = "logs") -> str:
    """
    Log simulation results to a JSON file with timestamp-based filename.
    
    Args:
        results: Dictionary mapping simulation name to SimulationResult
        configs: List of configurations used
        output_dir: Directory to save log files (default: "logs")
        
    Returns:
        Path to the saved log file
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Generate config-based filename component
    config_prefix = generate_filename_from_configs(configs)
    
    # Create filename: timestamp_configprefix_results.json
    filename = f"{timestamp}_{config_prefix}_results.json"
    filepath = os.path.join(output_dir, filename)
    
    # Prepare data for logging
    log_data = {
        "timestamp": timestamp,
        "config_summary": config_prefix,
        "num_configs": len(configs),
        "configs": [config_to_dict(config) for config in configs],
        "results": {
            name: {
                "config_name": name,
                "result": result_to_dict(result),
                "summary": {
                    "final_energy": result.energy_history[-1] if result.energy_history else 0,
                    "final_accuracy": result.accuracy_history[-1] if result.accuracy_history else 0.0,
                    "num_ticks_run": len(result.accuracy_history),
                    "total_mutations": len(result.mutations_applied),
                    "max_energy": max(result.energy_history) if result.energy_history else 0,
                    "min_energy": min(result.energy_history) if result.energy_history else 0,
                    "max_accuracy": max(result.accuracy_history) if result.accuracy_history else 0.0,
                    "final_size": result.size_history[-1] if result.size_history else 0
                }
            }
            for name, result in results.items()
        }
    }
    
    # Write to file
    with open(filepath, 'w') as f:
        json.dump(log_data, f, indent=2)
    
    return filepath


def load_results_from_log(filepath: str) -> Tuple[Dict[str, SimulationResult], Dict]:
    """
    Load simulation results from a log file.
    
    Args:
        filepath: Path to the JSON log file
        
    Returns:
        Tuple of (results_dict, metadata_dict) where:
        - results_dict: Dictionary mapping config name to SimulationResult
        - metadata_dict: Dictionary with timestamp, config_summary, etc.
    """
    with open(filepath, 'r') as f:
        log_data = json.load(f)
    
    # Reconstruct results
    results = {}
    for name, data in log_data["results"].items():
        result_data = data["result"]
        results[name] = SimulationResult(
            energy_history=result_data["energy_history"],
            accuracy_history=result_data["accuracy_history"],
            predictions=result_data["predictions"],
            actuals=result_data["actuals"],
            rewards=result_data["rewards"],
            size_history=result_data["size_history"],
            mutations_applied=result_data["mutations_applied"]
        )
    
    # Extract metadata
    metadata = {
        "timestamp": log_data["timestamp"],
        "config_summary": log_data["config_summary"],
        "num_configs": log_data["num_configs"],
        "configs": log_data["configs"]
    }
    
    return results, metadata


def format_label(sim_name: str) -> str:
    """Format simulation name into a cleaner label for plots."""
    # Remove "MinimalNeo_" prefix if present
    label = sim_name.replace("MinimalNeo_", "")
    # Replace underscores with spaces
    label = label.replace("_", " ")
    # Capitalize first letter of each word
    label = " ".join(word.capitalize() for word in label.split())
    return label


def print_lineage_tree(result: SimulationResult, sim_name: str = ""):
    """Print a tree visualization of Neo lineages."""
    if not result.lineages:
        print(f"{sim_name}: No lineages found")
        return
    
    print(f"\n{'='*80}")
    print(f"Lineage Tree for: {sim_name}")
    print(f"{'='*80}")
    
    # Build parent-child mapping
    children_map = {}
    root_lineage = None
    for lineage in result.lineages:
        if lineage.parent_id is None:
            root_lineage = lineage
        else:
            if lineage.parent_id not in children_map:
                children_map[lineage.parent_id] = []
            children_map[lineage.parent_id].append(lineage)
    
    def print_lineage(lineage: NeoLineage, indent: int = 0, prefix: str = ""):
        """Recursively print lineage tree."""
        indent_str = "  " * indent
        death_str = f" (died at tick {lineage.death_tick})" if lineage.death_tick is not None else " (alive)"
        mutations_str = f", {len(lineage.mutations_applied)} mutations" if lineage.mutations_applied else ", no mutations"
        final_acc = lineage.accuracy_history[-1] if lineage.accuracy_history else 0.0
        ticks_alive = len(lineage.predictions)
        
        print(f"{indent_str}{prefix}Lineage {lineage.lineage_id}: "
              f"birth={lineage.birth_tick}{death_str}, "
              f"ticks={ticks_alive}, "
              f"final_acc={final_acc:.3f}{mutations_str}")
        
        if lineage.mutations_applied:
            for mut in lineage.mutations_applied[:3]:  # Show first 3 mutations
                print(f"{indent_str}  └─ {mut}")
            if len(lineage.mutations_applied) > 3:
                print(f"{indent_str}  └─ ... ({len(lineage.mutations_applied) - 3} more)")
        
        # Print children
        if lineage.lineage_id in children_map:
            children = sorted(children_map[lineage.lineage_id], key=lambda x: x.lineage_id)
            for i, child in enumerate(children):
                is_last = i == len(children) - 1
                child_prefix = "└─ " if is_last else "├─ "
                print_lineage(child, indent + 1, child_prefix)
    
    if root_lineage:
        print_lineage(root_lineage)
    else:
        # Fallback: print all lineages
        for lineage in sorted(result.lineages, key=lambda x: x.lineage_id):
            print_lineage(lineage)
    
    print(f"\nTotal lineages: {len(result.lineages)}")
    print(f"{'='*80}\n")


def print_lineage_summary(results: Dict[str, SimulationResult]):
    """Print summary of lineage information for all simulations."""
    print("\n" + "="*80)
    print("LINEAGE SUMMARY")
    print("="*80)
    
    for sim_name, result in results.items():
        if not result.lineages:
            continue
        
        total_lineages = len(result.lineages)
        max_depth = 0
        max_children = 0
        
        # Build parent-child mapping to calculate depth
        children_map = {}
        for lineage in result.lineages:
            if lineage.parent_id is not None:
                if lineage.parent_id not in children_map:
                    children_map[lineage.parent_id] = []
                children_map[lineage.parent_id].append(lineage)
        
        # Calculate max depth
        def get_depth(lineage_id: int, visited: set = None) -> int:
            if visited is None:
                visited = set()
            if lineage_id in visited:
                return 0
            visited.add(lineage_id)
            if lineage_id not in children_map:
                return 1
            return 1 + max([get_depth(c.lineage_id, visited) for c in children_map[lineage_id]], default=0)
        
        root_lineage = next((l for l in result.lineages if l.parent_id is None), None)
        if root_lineage:
            max_depth = get_depth(root_lineage.lineage_id)
        
        max_children = max([len(children_map.get(l.lineage_id, [])) for l in result.lineages], default=0)
        
        avg_lifespan = sum([len(l.predictions) for l in result.lineages]) / total_lineages if total_lineages > 0 else 0
        total_mutations = sum([len(l.mutations_applied) for l in result.lineages])
        
        print(f"\n{sim_name}:")
        print(f"  Total lineages: {total_lineages}")
        print(f"  Max tree depth: {max_depth}")
        print(f"  Max children per parent: {max_children}")
        print(f"  Average lifespan: {avg_lifespan:.1f} ticks")
        print(f"  Total mutations across all lineages: {total_mutations}")


def plot_results(results: Dict[str, SimulationResult], configs: Optional[List[SimulationConfig]] = None, 
                 output_dir: str = "figures", title_prefix: str = ""):
    """
    Plot results for simulations.
    
    Args:
        results: Dictionary mapping simulation name to SimulationResult
        configs: Optional list of configurations to generate filename from
        output_dir: Directory to save plots
        title_prefix: Optional prefix for plot titles
    """
    if not HAS_MATPLOTLIB:
        print("Warning: matplotlib not available, skipping plots")
        return
    
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate filename from configs if provided
    if configs:
        filename_prefix = generate_filename_from_configs(configs)
    else:
        filename_prefix = "simulation"
    
    # Plot energy trajectories
    plt.figure(figsize=(12, 7))
    ax = plt.gca()
    plotted_count = 0
    # Use solid lines only, different markers and colors to distinguish curves
    markers = ['o', 's', '^', 'v', 'D', 'p', '*', 'h']
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']
    
    for idx, (sim_name, result) in enumerate(results.items()):
        # Check if we have multiple lineages (offspring enabled)
        has_offspring = hasattr(result, 'lineages') and result.lineages and len(result.lineages) > 1
        
        if has_offspring:
            # Plot each lineage separately, with offspring using parent's color
            # Build parent-child mapping and assign colors
            lineage_colors = {}
            root_lineage = None
            
            for lineage in result.lineages:
                if lineage.parent_id is None:
                    root_lineage = lineage
                    # Root gets the simulation's color
                    lineage_colors[lineage.lineage_id] = colors[idx % len(colors)]
                else:
                    # Offspring uses parent's color
                    lineage_colors[lineage.lineage_id] = lineage_colors.get(lineage.parent_id, colors[idx % len(colors)])
            
            # Plot each lineage
            for lineage in sorted(result.lineages, key=lambda x: x.lineage_id):
                if len(lineage.energy_history) > 0:
                    # Adjust ticks: offspring starts at birth_tick
                    if lineage.birth_tick > 0:
                        # Offspring: shift ticks to absolute timeline
                        ticks = list(range(lineage.birth_tick, lineage.birth_tick + len(lineage.energy_history)))
                    else:
                        # Root: use normal ticks
                        ticks = list(range(len(lineage.energy_history)))
                    
                    color = lineage_colors[lineage.lineage_id]
                    marker = markers[lineage.lineage_id % len(markers)]
                    
                    # Label: show lineage info for offspring
                    if lineage.lineage_id == 0:
                        label = format_label(sim_name)
                    else:
                        label = f"{format_label(sim_name)} (L{lineage.lineage_id})"
                    
                    markevery = max(1, len(ticks) // 15) if len(ticks) > 15 else 1
                    plt.plot(ticks, lineage.energy_history, label=label, linewidth=2.5, 
                            linestyle='-', marker=marker, markersize=7, color=color, 
                            markevery=markevery, alpha=0.9)
                    
                    plotted_count += 1
            
            # Add mutation markers for offspring lineages
            for lineage in result.lineages:
                if len(lineage.energy_history) == 0:
                    continue
                
                color = lineage_colors.get(lineage.lineage_id, colors[idx % len(colors)])
                
                # Collect mutations for this lineage
                for mut_str in lineage.mutations_applied:
                    try:
                        parts = mut_str.split(':')
                        tick_str = parts[0].split('=')[1].strip()
                        absolute_tick = int(tick_str)  # Mutation tick is already absolute
                        mut_type = parts[1].strip() if len(parts) > 1 else "?"
                        
                        # Get energy value at this tick
                        # For offspring: energy_history[0] is at birth_tick, so we need to calculate the index
                        if lineage.birth_tick > 0:
                            # Offspring: energy_history[0] corresponds to birth_tick
                            # So energy_history[i] corresponds to birth_tick + i
                            # For mutation at absolute_tick, index = absolute_tick - birth_tick
                            energy_idx = absolute_tick - lineage.birth_tick
                            if 0 <= energy_idx < len(lineage.energy_history):
                                energy_val = lineage.energy_history[energy_idx]
                            else:
                                continue
                        else:
                            # Root: energy_history[0] is initial energy, energy_history[1] is after tick 0
                            # So energy_history[i] corresponds to tick i - 1
                            # For mutation at absolute_tick, index = absolute_tick + 1
                            energy_idx = absolute_tick + 1
                            if 0 <= energy_idx < len(lineage.energy_history):
                                energy_val = lineage.energy_history[energy_idx]
                            else:
                                continue
                        
                        # Plot mutation marker
                        plt.scatter(absolute_tick, energy_val, marker='*', s=250, color=color, 
                                  edgecolors='black', linewidths=2, zorder=5, alpha=0.9, label='_nolegend_')
                        
                        # Add annotation
                        offset_y = 15 if absolute_tick % 2 == 0 else -20
                        plt.annotate(mut_type, xy=(absolute_tick, energy_val), 
                                   xytext=(8, offset_y), textcoords='offset points',
                                   fontsize=7, color='black', alpha=0.9,
                                   bbox=dict(boxstyle='round,pad=0.4', facecolor='yellow', 
                                           edgecolor=color, linewidth=1.5, alpha=0.85),
                                   arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.1',
                                                 color=color, lw=1.2, alpha=0.6))
                    except (ValueError, IndexError):
                        continue
        else:
            # No offspring: plot root lineage only
            if len(result.energy_history) > 0:
                ticks = list(range(len(result.energy_history)))
                label = format_label(sim_name)
                marker = markers[idx % len(markers)]
                color = colors[idx % len(colors)]
                
                markevery = max(1, len(ticks) // 15) if len(ticks) > 15 else 1
                plt.plot(ticks, result.energy_history, label=label, linewidth=2.5, 
                        linestyle='-', marker=marker, markersize=7, color=color, 
                        markevery=markevery, alpha=0.9)
                
                # Add mutation markers for root curve (no offspring case)
                mutation_ticks = {}
                for mut_str in result.mutations_applied:
                    try:
                        parts = mut_str.split(':')
                        tick_str = parts[0].split('=')[1].strip()
                        absolute_tick = int(tick_str)  # Mutation tick is already absolute
                        mut_type = parts[1].strip() if len(parts) > 1 else "?"
                        # Root: energy_history[0] is initial, energy_history[1] is after tick 0
                        # So energy_history[i] corresponds to tick i - 1
                        # For mutation at absolute_tick, index = absolute_tick + 1
                        energy_idx = absolute_tick + 1
                        if 0 <= energy_idx < len(result.energy_history):
                            if absolute_tick not in mutation_ticks:
                                mutation_ticks[absolute_tick] = []
                            mutation_ticks[absolute_tick].append(mut_type)
                    except (ValueError, IndexError):
                        continue
                
                # Plot mutation markers
                for absolute_tick, mut_types in mutation_ticks.items():
                    energy_idx = absolute_tick + 1
                    if 0 <= energy_idx < len(result.energy_history):
                        energy_val = result.energy_history[energy_idx]
                        plt.scatter(absolute_tick, energy_val, marker='*', s=250, color=color, 
                                  edgecolors='black', linewidths=2, zorder=5, alpha=0.9, label='_nolegend_')
                        
                        # Create compact mutation label
                        mut_counts = Counter(mut_types)
                        mut_parts = []
                        for mut_type, count in mut_counts.items():
                            if count > 1:
                                mut_parts.append(f"{mut_type}×{count}")
                            else:
                                mut_parts.append(mut_type)
                        mut_label = ', '.join(mut_parts[:3])
                        if len(mut_parts) > 3:
                            mut_label += f" (+{len(mut_parts)-3})"
                        
                        offset_y = 15 if absolute_tick % 2 == 0 else -20
                        plt.annotate(mut_label, xy=(absolute_tick, energy_val), 
                                   xytext=(8, offset_y), textcoords='offset points',
                                   fontsize=7, color='black', alpha=0.9,
                                   bbox=dict(boxstyle='round,pad=0.4', facecolor='yellow', 
                                           edgecolor=color, linewidth=1.5, alpha=0.85),
                                   arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.1',
                                                 color=color, lw=1.2, alpha=0.6))
                
                plotted_count += 1
            else:
                print(f"Warning: {sim_name} has no energy history data")
    print(f"Plotted {plotted_count} energy curves out of {len(results)} results")
    plt.xlabel("Tick", fontsize=12)
    plt.ylabel("Energy (Nex)", fontsize=12)
    title = f"{title_prefix}Energy Trajectory" if title_prefix else "Energy Trajectory"
    plt.title(title, fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)
    # Set y-axis to explicitly include 0 and show full range
    min_energy = min([min(r.energy_history) for r in results.values()])
    max_energy = max([max(r.energy_history) for r in results.values()])
    plt.ylim(bottom=min(0, min_energy), top=max_energy * 1.05)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    # Set axes to cross at origin
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    # Ensure y-axis ticks include 0
    ax.set_yticks([0] + list(ax.get_yticks()))
    plt.tight_layout()
    filename = f"{filename_prefix}_energy.pdf"
    plt.savefig(f"{output_dir}/{filename}")
    plt.close()
    
    # Plot accuracy trajectories
    plt.figure(figsize=(12, 7))
    ax = plt.gca()
    plotted_count = 0
    # Use solid lines only, different markers and colors to distinguish curves
    markers = ['o', 's', '^', 'v', 'D', 'p', '*', 'h']
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']
    
    for idx, (sim_name, result) in enumerate(results.items()):
        # Check if we have multiple lineages (offspring enabled)
        has_offspring = hasattr(result, 'lineages') and result.lineages and len(result.lineages) > 1
        
        if has_offspring:
            # Plot each lineage separately, with offspring using parent's color
            # Build parent-child mapping and assign colors
            lineage_colors = {}
            root_lineage = None
            
            for lineage in result.lineages:
                if lineage.parent_id is None:
                    root_lineage = lineage
                    lineage_colors[lineage.lineage_id] = colors[idx % len(colors)]
                else:
                    lineage_colors[lineage.lineage_id] = lineage_colors.get(lineage.parent_id, colors[idx % len(colors)])
            
            # Plot each lineage
            for lineage in sorted(result.lineages, key=lambda x: x.lineage_id):
                if len(lineage.accuracy_history) > 0:
                    # Adjust ticks: offspring starts at birth_tick (not birth_tick + 1)
                    # This ensures continuity with parent's curve
                    if lineage.birth_tick > 0:
                        ticks = list(range(lineage.birth_tick, lineage.birth_tick + len(lineage.accuracy_history)))
                    else:
                        ticks = list(range(1, len(lineage.accuracy_history) + 1))
                    
                    color = lineage_colors[lineage.lineage_id]
                    marker = markers[lineage.lineage_id % len(markers)]
                    
                    # Label: show lineage info for offspring
                    if lineage.lineage_id == 0:
                        label = format_label(sim_name)
                    else:
                        label = f"{format_label(sim_name)} (L{lineage.lineage_id})"
                    
                    markevery = max(1, len(ticks) // 15) if len(ticks) > 15 else 1
                    plt.plot(ticks, lineage.accuracy_history, label=label, linewidth=2.5,
                            linestyle='-', marker=marker, markersize=7, color=color,
                            markevery=markevery, alpha=0.9)
                    plotted_count += 1
            
            # Add mutation markers for offspring lineages
            for lineage in result.lineages:
                if len(lineage.accuracy_history) == 0:
                    continue
                
                color = lineage_colors.get(lineage.lineage_id, colors[idx % len(colors)])
                
                # Collect mutations for this lineage
                for mut_str in lineage.mutations_applied:
                    try:
                        parts = mut_str.split(':')
                        tick_str = parts[0].split('=')[1].strip()
                        absolute_tick = int(tick_str)  # Mutation tick is already absolute
                        mut_type = parts[1].strip() if len(parts) > 1 else "?"
                        
                        # Get accuracy value at this tick
                        # For offspring: accuracy_history[0] is at birth_tick, so we need to calculate the index
                        if lineage.birth_tick > 0:
                            # Offspring: accuracy_history[0] corresponds to birth_tick
                            # So accuracy_history[i] corresponds to birth_tick + i
                            # For mutation at absolute_tick, index = absolute_tick - birth_tick
                            acc_idx = absolute_tick - lineage.birth_tick
                            if 0 <= acc_idx < len(lineage.accuracy_history):
                                accuracy_val = lineage.accuracy_history[acc_idx]
                            else:
                                continue
                        else:
                            # Root: accuracy_history[0] corresponds to tick 1
                            # So accuracy_history[i] corresponds to tick i + 1
                            # For mutation at absolute_tick, index = absolute_tick - 1
                            acc_idx = absolute_tick - 1
                            if 0 <= acc_idx < len(lineage.accuracy_history):
                                accuracy_val = lineage.accuracy_history[acc_idx]
                            else:
                                continue
                        
                        # Plot mutation marker
                        plt.scatter(absolute_tick, accuracy_val, marker='*', s=250, color=color, 
                                  edgecolors='black', linewidths=2, zorder=5, alpha=0.9, label='_nolegend_')
                        
                        # Add annotation
                        offset_y = 15 if absolute_tick % 2 == 0 else -20
                        plt.annotate(mut_type, xy=(absolute_tick, accuracy_val), 
                                   xytext=(8, offset_y), textcoords='offset points',
                                   fontsize=7, color='black', alpha=0.9,
                                   bbox=dict(boxstyle='round,pad=0.4', facecolor='yellow', 
                                           edgecolor=color, linewidth=1.5, alpha=0.85),
                                   arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.1',
                                                 color=color, lw=1.2, alpha=0.6))
                    except (ValueError, IndexError):
                        continue
        else:
            # No offspring: plot root lineage only
            if len(result.accuracy_history) > 0:
                ticks = list(range(1, len(result.accuracy_history) + 1))
                label = format_label(sim_name)
                marker = markers[idx % len(markers)]
                color = colors[idx % len(colors)]
                
                markevery = max(1, len(ticks) // 15) if len(ticks) > 15 else 1
                plt.plot(ticks, result.accuracy_history, label=label, linewidth=2.5,
                        linestyle='-', marker=marker, markersize=7, color=color,
                        markevery=markevery, alpha=0.9)
                
                # Add mutation markers for root curve (no offspring case)
                mutation_ticks = {}
                for mut_str in result.mutations_applied:
                    try:
                        parts = mut_str.split(':')
                        tick_str = parts[0].split('=')[1].strip()
                        tick = int(tick_str)
                        mut_type = parts[1].strip() if len(parts) > 1 else "?"
                        if 1 <= tick <= len(result.accuracy_history):
                            if tick not in mutation_ticks:
                                mutation_ticks[tick] = []
                            mutation_ticks[tick].append(mut_type)
                    except (ValueError, IndexError):
                        continue
                
                # Plot mutation markers
                for tick, mut_types in mutation_ticks.items():
                    if 1 <= tick <= len(result.accuracy_history):
                        acc_idx = tick - 1
                        accuracy_val = result.accuracy_history[acc_idx]
                        plt.scatter(tick, accuracy_val, marker='*', s=250, color=color, 
                                  edgecolors='black', linewidths=2, zorder=5, alpha=0.9, label='_nolegend_')
                        
                        # Create compact mutation label
                        mut_counts = Counter(mut_types)
                        mut_parts = []
                        for mut_type, count in mut_counts.items():
                            if count > 1:
                                mut_parts.append(f"{mut_type}×{count}")
                            else:
                                mut_parts.append(mut_type)
                        mut_label = ', '.join(mut_parts[:3])
                        if len(mut_parts) > 3:
                            mut_label += f" (+{len(mut_parts)-3})"
                        
                        offset_y = 15 if tick % 2 == 0 else -20
                        plt.annotate(mut_label, xy=(tick, accuracy_val), 
                                   xytext=(8, offset_y), textcoords='offset points',
                                   fontsize=7, color='black', alpha=0.9,
                                   bbox=dict(boxstyle='round,pad=0.4', facecolor='yellow', 
                                           edgecolor=color, linewidth=1.5, alpha=0.85),
                                   arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.1',
                                                 color=color, lw=1.2, alpha=0.6))
                
                plotted_count += 1
            else:
                print(f"Warning: {sim_name} has no accuracy history data (energy_history length: {len(result.energy_history)})")
    print(f"Plotted {plotted_count} accuracy curves out of {len(results)} results")
    plt.xlabel("Tick", fontsize=12)
    plt.ylabel("Prediction Accuracy", fontsize=12)
    title = f"{title_prefix}Prediction Accuracy Over Time" if title_prefix else "Prediction Accuracy Over Time"
    plt.title(title, fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.ylim(0, 1.1)
    # Set x-axis to start from 0 to show the full range
    plt.xlim(left=0)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    # Set axes to cross at origin
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    plt.tight_layout()
    filename = f"{filename_prefix}_accuracy.pdf"
    plt.savefig(f"{output_dir}/{filename}")
    plt.close()


def main(enable_offspring: Optional[bool] = None, config_name: Optional[str] = None):
    """
    Run example simulations.
    
    Args:
        enable_offspring: If provided, override enable_offspring for all configs.
                         If None, use each config's enable_offspring setting.
        config_name: If provided, only run configs matching this name (case-insensitive partial match).
                     If None, run all configs.
    """
    import sys
    import argparse
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Run Neosis simulations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m simulations.run                           # Run all configs
  python -m simulations.run --config edges_only       # Run only edges_only config
  python -m simulations.run --config MinimalNeo       # Run all MinimalNeo configs
  python -m simulations.run --no-offspring            # Disable offspring for all
  python -m simulations.run --config edges_only --offspring  # Run edges_only with offspring
  python -m simulations.run --list                    # List all available configs
        """
    )
    
    # Use mutually exclusive group for offspring flags
    offspring_group = parser.add_mutually_exclusive_group()
    offspring_group.add_argument(
        '--offspring', '--with-offspring', '--lineage', '--with-lineage',
        action='store_true',
        dest='enable_offspring',
        help='Enable offspring creation (override config settings)'
    )
    offspring_group.add_argument(
        '--no-offspring', '--without-offspring', '--no-lineage', '--without-lineage',
        action='store_false',
        dest='enable_offspring',
        help='Disable offspring creation (override config settings)'
    )
    
    parser.add_argument(
        '--config', '-c',
        type=str,
        default=None,
        help='Run only configs matching this name (case-insensitive partial match)'
    )
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='List all available configuration names and exit'
    )
    
    args = parser.parse_args()
    
    # List configs if requested
    if args.list:
        all_configs = get_example_simulation_configs()
        print("Available configurations:")
        print("-" * 60)
        for i, config in enumerate(all_configs):
            print(f"  {i}: {config.name}")
        return
    
    # Use command line args if provided, otherwise use function parameters
    # Check if offspring flag was explicitly provided
    offspring_flags = ['--offspring', '--with-offspring', '--lineage', '--with-lineage',
                       '--no-offspring', '--without-offspring', '--no-lineage', '--without-lineage']
    if any(flag in sys.argv for flag in offspring_flags):
        if any(flag in sys.argv for flag in ['--offspring', '--with-offspring', '--lineage', '--with-lineage']):
            enable_offspring = True
        else:
            enable_offspring = False
    if args.config is not None:
        config_name = args.config
    
    print("Running simulations...")
    if enable_offspring is not None:
        print(f"Offspring mode: {'ENABLED' if enable_offspring else 'DISABLED'} (override)")
    else:
        print("Offspring mode: Using config settings")
    
    # Get configurations (you can replace this with your own configs)
    all_configs = get_example_simulation_configs()
    
    # Filter configs if config_name is specified
    if config_name:
        config_name_lower = config_name.lower()
        configs = [c for c in all_configs if config_name_lower in c.name.lower()]
        if not configs:
            print(f"Error: No configurations found matching '{config_name}'")
            print("\nAvailable configurations:")
            for i, config in enumerate(all_configs):
                print(f"  {i}: {config.name}")
            return
        print(f"Filtered to {len(configs)} config(s) matching '{config_name}':")
        for config in configs:
            print(f"  - {config.name}")
    else:
        configs = all_configs
    
    # Override enable_offspring if specified
    if enable_offspring is not None:
        for config in configs:
            config.enable_offspring = enable_offspring
    
    # Run simulations
    print(f"\nRunning {len(configs)} simulation(s)...")
    for config in configs:
        offspring_status = "with offspring" if config.enable_offspring else "without offspring"
        print(f"  Running {config.name} ({offspring_status})...")
    results = run_simulations_from_configs(configs)
    print(f"Completed {len(results)}/{len(configs)} simulations successfully")
    
    # Print summary
    print("\nSimulation Summary:")
    print("-" * 60)
    for sim_name, result in results.items():
        final_energy = result.energy_history[-1] if result.energy_history else 0
        final_accuracy = result.accuracy_history[-1] if result.accuracy_history else 0.0
        num_ticks_run = len(result.accuracy_history)
        num_lineages = len(result.lineages) if hasattr(result, 'lineages') else 0
        print(f"{sim_name:30s} | Energy: {final_energy:4d} | Accuracy: {final_accuracy:.3f} | Ticks: {num_ticks_run} | Lineages: {num_lineages}")
        if result.energy_history:
            print(f"  Last 5 energy values: {result.energy_history[-5:]}")
    
    # Print lineage information
    print_lineage_summary(results)
    
    # Print detailed lineage trees for simulations with mutations
    print("\n" + "="*80)
    print("DETAILED LINEAGE TREES")
    print("="*80)
    for sim_name, result in results.items():
        if hasattr(result, 'lineages') and result.lineages and len(result.lineages) > 1:
            print_lineage_tree(result, sim_name)
    
    # Log results to file
    print("\nLogging results to file...")
    log_filepath = log_results(results, configs, output_dir="logs")
    print(f"Results logged to: {log_filepath}")
    
    # Plot results
    print("\nGenerating plots...")
    plot_results(results, configs=configs, title_prefix="")
    print(f"Plots saved to figures/ directory")
    print(f"  Filename prefix: {generate_filename_from_configs(configs)}")
    
    return results


if __name__ == "__main__":
    main()

