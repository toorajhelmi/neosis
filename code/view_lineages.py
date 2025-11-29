#!/usr/bin/env python3
"""Quick script to view lineage information from simulation results."""

import json
import glob
import os
from src.simulation import SimulationResult, NeoLineage
from simulations.run import print_lineage_tree, print_lineage_summary

def load_latest_results():
    """Load the most recent simulation results."""
    log_files = glob.glob("logs/*_results.json")
    if not log_files:
        print("No log files found in logs/ directory")
        print("Run 'python -m simulations.run' first to generate results")
        return None, None
    
    latest = max(log_files, key=os.path.getmtime)
    print(f"Loading results from: {latest}\n")
    
    with open(latest, 'r') as f:
        log_data = json.load(f)
    
    # Reconstruct results with lineages
    results = {}
    for name, data in log_data["results"].items():
        result_data = data["result"]
        lineages = []
        if "lineages" in result_data:
            for lin_data in result_data["lineages"]:
                lineages.append(NeoLineage(
                    lineage_id=lin_data["lineage_id"],
                    parent_id=lin_data["parent_id"],
                    birth_tick=lin_data["birth_tick"],
                    death_tick=lin_data["death_tick"],
                    energy_history=lin_data["energy_history"],
                    accuracy_history=lin_data["accuracy_history"],
                    predictions=lin_data["predictions"],
                    actuals=lin_data["actuals"],
                    rewards=lin_data["rewards"],
                    size_history=lin_data["size_history"],
                    mutations_applied=lin_data["mutations_applied"]
                ))
        
        results[name] = SimulationResult(
            energy_history=result_data["energy_history"],
            accuracy_history=result_data["accuracy_history"],
            predictions=result_data["predictions"],
            actuals=result_data["actuals"],
            rewards=result_data["rewards"],
            size_history=result_data["size_history"],
            mutations_applied=result_data["mutations_applied"],
            lineages=lineages
        )
    
    return results, log_data


def main():
    """View lineage information from latest simulation results."""
    results, log_data = load_latest_results()
    if results is None:
        return
    
    print("="*80)
    print("LINEAGE SUMMARY")
    print("="*80)
    print_lineage_summary(results)
    
    print("\n" + "="*80)
    print("DETAILED LINEAGE TREES")
    print("="*80)
    for sim_name, result in results.items():
        if result.lineages and len(result.lineages) > 1:
            print_lineage_tree(result, sim_name)
        elif result.lineages:
            print(f"\n{sim_name}: Only root lineage (no mutations occurred)")
    
    print("\n" + "="*80)
    print("QUICK STATS")
    print("="*80)
    for sim_name, result in results.items():
        if result.lineages:
            print(f"\n{sim_name}:")
            print(f"  Total lineages: {len(result.lineages)}")
            if len(result.lineages) > 1:
                longest_lived = max(result.lineages, key=lambda x: len(x.predictions))
                most_mutations = max(result.lineages, key=lambda x: len(x.mutations_applied))
                print(f"  Longest lived: Lineage {longest_lived.lineage_id} ({len(longest_lived.predictions)} ticks)")
                print(f"  Most mutations: Lineage {most_mutations.lineage_id} ({len(most_mutations.mutations_applied)} mutations)")


if __name__ == "__main__":
    main()


