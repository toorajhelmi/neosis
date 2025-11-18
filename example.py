"""Simple example of using Neosis framework."""

from src.neo import Neo
from src.neoverse import AlternatingNeoVerse
from src.simulation import NeoCycle

def main():
    """Run a simple example simulation."""
    print("Creating a simple Neo...")
    
    # Create a Neo with 1 memory bit and 10 Nex energy
    neo = Neo(n=1, memory=[0], energy=10)
    
    # Create an alternating NeoVerse environment
    neoverse = AlternatingNeoVerse()
    
    # Create simulation cycle (mutations disabled for simplicity)
    cycle = NeoCycle(neo=neo, neoverse=neoverse, enable_mutations=False, run_cost=1)
    
    print("Running simulation for 20 ticks...")
    result = cycle.run(num_ticks=20)
    
    print("\nResults:")
    print(f"  Final energy: {result.energy_history[-1]} Nex")
    print(f"  Final accuracy: {result.accuracy_history[-1]:.3f}")
    print(f"  Total rewards: {sum(result.rewards)}")
    print(f"\nFirst 10 predictions vs actuals:")
    for i in range(min(10, len(result.predictions))):
        pred = result.predictions[i]
        actual = result.actuals[i]
        match = "✓" if pred == actual else "✗"
        print(f"  Tick {i+1}: predicted {pred}, actual {actual} {match}")
    
    print("\nNote: To regenerate the N_0 figures, run:")
    print("  python -m simulations.n0_simulation")

if __name__ == "__main__":
    main()

