# Neosis

A computational framework for simulating computational organisms called "Neos" that evolve through energy-constrained computation and self-modification.

## Overview

Neosis is a minimal framework where computational organisms (Neos) exist within an environment (NeoVerse) and attempt to predict future sensory signals. The accuracy of predictions determines energy rewards, while all computation and structural modifications consume energy. This creates a direct link between intelligence and survival.

## Installation

```bash
pip install -r requirements.txt
```

## Project Structure

```
Neosis/
├── src/                    # Core Neosis framework
│   ├── types.py           # Pydantic models and types
│   ├── config.py          # Configuration classes
│   ├── neo.py             # Neo class (computational organism)
│   ├── lio.py             # Lio mutator (self-modification)
│   ├── evo.py             # Evo meta-mutator
│   ├── neoverse.py        # NeoVerse environments
│   └── simulation.py      # NeoCycle simulation loop + config-based runner
├── simulations/           # Simulation configurations and runner
│   ├── configs.py         # Simulation configurations (define any Neo size/structure)
│   └── run.py             # Main simulation runner and plotting
├── tests/                 # Test files
└── requirements.txt       # Python dependencies
```

## Quick Start

Run simulations:

```bash
python -m simulations.run
```

This will:
1. Run N_0 in three different NeoVerse environments (Random, Alternating, Block Pattern)
2. Generate plots showing energy trajectories and prediction accuracy
3. Save plots to the `figures/` directory

## Core Concepts

### Neo
The fundamental computational organism containing:
- Memory bits
- Nodes (input, memory, computational, output)
- Graph structure (edges between nodes)
- Lex (truth tables) for computation
- Energy (Nex)

### Lio
The embedded mutator that proposes structural changes:
- `bit+`: Add memory bit
- `bit-`: Remove memory bit
- `edge+`: Add edge
- `edge-`: Remove edge
- `lexflip`: Flip lex entry

### Evo
The meta-level mutator that modifies Lio itself, shaping how evolution proceeds.

### NeoVerse
The environment providing sensory signals. Implementations include:
- `RandomNeoVerse`: Random binary inputs
- `AlternatingNeoVerse`: Pattern 01010101...
- `BlockPatternNeoVerse`: Pattern 00110011...

### NeoCycle
The main simulation loop that:
1. Receives input from NeoVerse
2. Computes predictions
3. Pays run costs
4. Receives rewards based on prediction accuracy
5. Applies mutations (if enabled)
6. Updates energy and state

## Example Usage

```python
from src.neo import Neo
from src.neoverse import AlternatingNeoVerse
from src.simulation import NeoCycle

# Create a Neo
neo = Neo(n=1, energy=10)

# Create a NeoVerse
neoverse = AlternatingNeoVerse()

# Create and run simulation
cycle = NeoCycle(neo=neo, neoverse=neoverse, enable_mutations=False)
result = cycle.run(num_ticks=100)

# Access results
print(f"Final energy: {result.energy_history[-1]}")
print(f"Final accuracy: {result.accuracy_history[-1]}")
```

## Axioms

Neosis is built on eight axioms:
1. **Binary Substrate**: All values are binary (0 or 1)
2. **Energetic Cost**: All actions require energy
3. **Local Computation**: State changes through local lex computations
4. **Snapshot Semantics**: Computation uses previous tick's values
5. **Perception**: Neo receives perceptual signals from NeoVerse
6. **Prediction and Reward**: Predictions are rewarded based on accuracy
7. **Self-Modification via Lio**: Lio proposes mutations subject to energy
8. **Meta-Modification via Evo**: Evo can modify Lio itself

## License

This is a research framework for exploring computational intelligence and evolution.

