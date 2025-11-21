# Chapter 7 — Related Theories and Neosis in Context

This chapter situates Neosis within the broader landscape of computational, cognitive, and evolutionary frameworks. Rather than treating Neosis as an extension of any single prior approach, we organize the landscape along three categorical axes: (1) the locus of structural adaptation, (2) the origin and nature of objectives, and (3) the developmental regime governing representational growth. These axes define a conceptual space in which different theoretical traditions occupy distinct regions. Neosis emerges not as an extreme point, but as a category that lies outside the intersections of existing paradigms.

A diagram illustrating this three-axis taxonomy is shown in Figure 7.1.

<!-- GITBOOK_ONLY -->
![Figure 7.1: Conceptual Placement of Theoretical Frameworks](assets/neosis-cube-diagram.svg)
<!-- END_GITBOOK_ONLY -->

```latex
\begin{figure}[h]
\centering
\begin{tikzpicture}[x={(1cm,0cm)}, y={(0.5cm,0.866cm)}, z={(0cm,1cm)}]
% Cube edges
\draw[thick] (0,0,0) -- (4,0,0) -- (4,4,0) -- (0,4,0) -- cycle;
\draw[thick] (0,0,4) -- (4,0,4) -- (4,4,4) -- (0,4,4) -- cycle;
\draw[thick] (0,0,0) -- (0,0,4);
\draw[thick] (4,0,0) -- (4,0,4);
\draw[thick] (4,4,0) -- (4,4,4);
\draw[thick] (0,4,0) -- (0,4,4);
% Axis labels
\node[below] at (2,0,0) {Locus of Structural Adaptation};
\node[right] at (4,2,0) {Origin of Objectives};
\node[above] at (0,4,2) {Developmental Regime};
% Representative theories
\node at (3.5,0.5,0.5) {ANN / SNN};
\node at (3.5,3.5,0.5) {Neuroevolution};
\node at (0.5,3.5,0.5) {ALife};
\node at (0.5,0.5,3.5) {CCS / DST};
\node at (3.5,0.5,3.5) {Reservoir / NAS};
\node[font=\bfseries] at (2,2,3.5) {Neosis};
\end{tikzpicture}
\caption{Conceptual placement of major theoretical families in a three-axis space.}
\label{fig:neosis-cube}
\end{figure}
```

<!-- GITBOOK_ONLY -->
**Figure 7.1:** Conceptual placement of major theoretical families in a three-axis space. The three axes represent: (1) **Locus of Structural Adaptation** (X-axis): Fixed, generational, developmental, or in-lifetime; (2) **Origin of Objectives** (Y-axis): External loss, external reinforcement, replication fitness, or internal energy survival; (3) **Developmental Regime** (Z-axis): Static capacity, generationally expandable, biologically scaffolded, or self-expanding. Neosis occupies a distinct region characterized by in-lifetime self-modification, internal energy survival objectives, and open-ended developmental growth.
<!-- END_GITBOOK_ONLY -->

<!-- GITBOOK_ONLY -->
| Theory Family | Structural Adaptation | Objective Source | Developmental Regime |
|---------------|----------------------|-----------------|---------------------|
| Artificial Neural Networks | Fixed | External loss | Static |
| Spiking Neural Networks | Fixed | External loss | Static |
| Reinforcement Learning | Fixed | External reward | Static |
| Neuroevolution (NEAT, HyperNEAT) | Generational | External task fitness | Generational |
| Artificial Life (Tierra, Avida) | Generational | Replication fitness | Generational |
| Predictive Processing / FEP | Fixed hierarchy | Variational free energy | Static |
| Developmental Systems Theory | Developmental | Biological fitness | Scaffolding |
| Dynamical Systems Theory | Fixed attractor landscape | None / emergent | Continuous |
| Embodied/Enactive Cognition | Structural coupling | Viability | Developmental |
| Reservoir Computing | Fixed | External training | Static |
| Neural Architecture Search | Generational/Meta | External loss | Static |
| Liquid State Machines | Fixed | External training | Static |
| Hypernetworks / Meta-learning | Fixed meta-topology | External loss | Static |
| **Neosis** | **In-lifetime self-modifying** | **Internal energy survival** | **Open-ended** |
<!-- END_GITBOOK_ONLY -->

```latex
\begin{table}[h]
\centering
\begin{tabular}{lccc}
\toprule
\textbf{Theory Family} & \textbf{Structural Adaptation} & \textbf{Objective Source} & \textbf{Developmental Regime} \\
\midrule
Artificial Neural Networks & Fixed & External loss & Static \\
Spiking Neural Networks & Fixed & External loss & Static \\
Reinforcement Learning & Fixed & External reward & Static \\
Neuroevolution (NEAT, HyperNEAT) & Generational & External task fitness & Generational \\
Artificial Life (Tierra, Avida) & Generational & Replication fitness & Generational \\
Predictive Processing / FEP & Fixed hierarchy & Variational free energy & Static \\
Developmental Systems Theory & Developmental & Biological fitness & Scaffolding \\
Dynamical Systems Theory & Fixed attractor landscape & None / emergent & Continuous \\
Embodied/Enactive Cognition & Structural coupling & Viability & Developmental \\
Reservoir Computing & Fixed & External training & Static \\
Neural Architecture Search & Generational/Meta & External loss & Static \\
Liquid State Machines & Fixed & External training & Static \\
Hypernetworks / Meta-learning & Fixed meta-topology & External loss & Static \\
\textbf{Neosis} & \textbf{In-lifetime self-modifying} & \textbf{Internal energy survival} & \textbf{Open-ended} \\
\bottomrule
\end{tabular}
\caption{Comprehensive mapping of theoretical frameworks to the three categorical axes.}
\end{table}
```

<!-- GITBOOK_ONLY -->
**Table 7.1:** Comprehensive mapping of theoretical frameworks to the three categorical axes.
<!-- END_GITBOOK_ONLY -->

The following sections review major theoretical traditions that share conceptual territory with Neosis. For each, we highlight connections, distinctions, and key insights that motivate the need for a unified, energy-based, self-modifying computational framework.

## 7.1 Artificial Neural Networks

Artificial neural networks (ANNs) model computation as transformations over fixed graph structures trained through gradient-based optimization (Rumelhart et al., 1986; LeCun et al., 2015). They provide expressive supervised and unsupervised learning machinery, but architectures are static once chosen.

**Relation to Neosis.** Both ANNs and Neosis process information on directed graphs with continuous parameters. The local Lex rule resembles threshold neurons with stochastic effects.

**Differences.**

- ANNs rely on backpropagation and require differentiability; Neosis operates on binary substrates and local rules without gradient flow.
- ANN topology is fixed; Neosis uses in-lifetime structural mutation (node$$^+$$, node$$^-$$, edge$$^+$$, edge$$^-$$).
- ANNs optimize externally defined loss; Neosis optimizes internal survival via its energy economy.

## 7.2 Reinforcement Learning

Reinforcement learning (RL) models reward-driven behavior optimization (Sutton & Barto, 2018). Agents update policies or value functions to maximize expected cumulative reward.

**Relation to Neosis.** Neosis also receives reward signals (Sparks) based on predictive success.

**Differences.**

- RL updates parameters, not structure; Neosis modifies both structure and parameters.
- RL's reward is external; Neosis converts reward into energy that directly restricts future computation and mutation.
- RL optimizes expected returns; Neosis optimizes survival (lifetime and Vitality).

## 7.3 Evolutionary Computation and Genetic Programming

Evolutionary computation explores solution spaces via mutation, selection, and crossover (Holland, 1975; Koza, 1992). Genetic programming evolves programs themselves.

**Relation to Neosis.** Neosis adopts mutation and selection dynamics, including structural operators analogous to genetic primitives.

**Differences.**

- Evolutionary computation evolves static artifacts; Neos evolve *while alive*.
- Fitness functions are fixed; Neosis uses energy-based environmental coupling.
- Typical evolutionary systems separate learning from evolution; Neosis unifies them.

## 7.4 Neuroevolution

Neuroevolution evolves neural architectures and weights (Stanley & Miikkulainen, 2002; Stanley et al., 2009). Techniques include NEAT and HyperNEAT.

**Relation to Neosis.** Both explore topology–parameter spaces.

**Differences.**

- Neuroevolution modifies structure across generations; Neosis modifies structure across *ticks*.
- Neuroevolution optimizes task performance; Neosis evolves for long-term survival and resource management.

## 7.5 Artificial Life and Digital Organisms

Artificial Life (ALife) simulates digital organisms with mutation, self-replication, and competition (Ray, 1991; Adami, 1998). Systems such as Tierra and Avida define instruction-based organisms evolving under resource constraints.

**Relation to Neosis.** Neosis shares core ALife concepts: resource-limited computation, mutation-driven variation, and survival-based selection.

**Differences.**

- ALife organisms often evolve replication efficiency; Neosis evolves cognitive structure.
- ALife typically uses linear instruction sequences; Neosis uses evolving directed graphs.
- ALife focuses on population-level evolution; Neosis integrates computational dynamics and evolution in each individual.

## 7.6 Computational Cognitive Science

Computational cognitive science (CCS) studies heterogeneous cognitive architectures, development, and multi-timescale adaptation (Anderson, 2007; Newell, 1994).

**Relation to Neosis.** Neosis is inspired by CCS: specialization, modularity, and adaptive heterogeneity arise naturally through structural mutation.

**Differences.**

- CCS models are hand-designed; Neosis structures arise through self-modification.
- CCS focuses on biological explanation; Neosis provides a computational substrate for synthetic cognition.

## 7.7 Developmental and Dynamical Systems Theories

Developmental systems theory emphasizes gene–environment interaction and emergent development (Oyama, 2000). Dynamical systems approaches to cognition treat mind–brain–environment coupling as continuous self-organization (Kelso, 1995).

**Relation to Neosis.** Neosis similarly couples structure and environment, with adaptive capacity emerging through interaction.

**Differences.**

- These theories describe biological systems; Neosis provides a formal computational model.
- Neosis uses discrete binary dynamics and explicit energy accounting.

## 7.8 Reservoir Computing and Liquid State Machines

Reservoir computing uses fixed recurrent networks with trainable readouts (Jaeger, 2001; Maass et al., 2002). The internal reservoir is rich but unmodifiable.

**Relation to Neosis.** Neosis can evolve subgraphs with reservoir-like dynamics.

**Differences.**

- Reservoir topology is static; Neosis modifies topology continuously.
- Reservoir computing trains only readout weights; Neosis adapts nodes, edges, and interfaces.

## 7.9 Spiking Neural Networks

Spiking neural networks (SNNs) model neurons as temporal spiking units (Gerstner & Kistler, 2002). They incorporate temporal coding and biological detail.

**Relation to Neosis.** Both operate with discrete events and dynamic internal states.

**Differences.**

- SNNs aim for biological plausibility; Neosis prioritizes evolvability.
- SNN structure is fixed; Neosis structure evolves.

## 7.10 Embodied Cognition and Enactivism

Embodied cognition emphasizes the role of sensorimotor coupling and physical grounding (Varela et al., 1991; Clark, 1997).

**Relation to Neosis.** Neos perceive only through their projection $$\Phi_t$$ and act only through prediction, giving them an implicit minimal embodiment.

**Differences.**

- Embodied cognition requires physical or simulated bodies; Neosis abstracts embodiment into a binary interface.
- Enactivism emphasizes lived experience; Neosis emphasizes computational evolution.

## 7.11 Free Energy Principle and Predictive Processing

The Free Energy Principle (FEP) proposes that biological systems minimize variational free energy to maintain homeostasis (Friston, 2010). Predictive processing models cognition as hierarchical prediction-error minimization.

**Relation to Neosis.** Both involve prediction as a survival mechanism.

**Differences.**

- FEP uses differentiable optimization; Neosis uses non-differentiable mutation and energy costs.
- FEP assumes fixed hierarchical structure; Neosis permits structural self-modification.

## 7.12 Why These Comparisons Matter

These theories illuminate complementary aspects of computation, cognition, and evolution. Each dominates a different region of a three-axis categorical space:

1. **Locus of Structural Adaptation:** fixed, generational, developmental, or in-lifetime.
2. **Origin of Objectives:** external loss, external reinforcement, replication fitness, or internal energy survival.
3. **Developmental Regime:** static capacity, generationally expandable, biologically scaffolded, or self-expanding.

Neosis occupies a region characterized by:

- *in-lifetime structural self-modification*,
- *survival-based internal energy objectives*,
- and *open-ended representational growth*.

This location is not superior but categorically distinct. Existing theories emphasize computation, learning, or evolution separately. Neosis unifies these components into a single operational framework grounded in the energy dynamics defined in Chapter 2.

## 7.13 Summary

Neosis draws upon principles from neural computation, reinforcement learning, artificial life, evolutionary algorithms, dynamical systems, cognitive architectures, and predictive theories. However, none of these frameworks integrates computation, learning, evolution, and energy economics within a single self-modifying organism. This chapter clarifies the conceptual landscape and positions Neosis as a novel theoretical framework aimed at open-ended cognitive evolution.
