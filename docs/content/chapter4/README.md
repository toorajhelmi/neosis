# Chapter 4 — Neo's Learnability

This chapter analyzes a central question in Neosis: to what extent can a Neo, whose internal structure is a self-modifying binary graph driven purely by mutation and energy constraints, develop the ability to learn? Learning is not explicitly built into the Neo architecture. There is no predefined synaptic plasticity rule, no weight-update mechanism, and no gradient-based training. Instead, all changes to a Neo's computational capacity arise through the mutation primitives introduced in Chapter 2.

Despite the absence of explicit learning rules, Neos can nonetheless evolve behaviors that function as learning. We call this property **learnability**: the capacity of a Neo to acquire, through evolutionary processes alone, internal circuitry whose dynamics adapt to experience within a lifetime. In this chapter, we formalize what learnability means for Neos, describe the mechanisms through which it can emerge, and explain why the Neo substrate is sufficient for both learning and meta-learning to arise spontaneously.

## 4.1 Learning Without Explicit Learning Rules

Traditional learning systems rely on explicit local update laws (e.g., Hebbian plasticity) or global optimization (e.g., gradient descent). Neos have neither. The internal state evolves only by:

- the deterministic and stochastic node update rule
  $$
  \mathbf{V}_{t+1}[i] = H(w_i^\top \mathbf{z}_i(t) + \alpha_i \eta_i(t) + b_i)
  $$
- changes in structure and parameters induced by Evo through mutation
- energy feedback from predictive success

Thus a Neo cannot directly modify its parameters within a lifetime. Nevertheless, Neos can develop internal recurrent circuitry whose behavior adapts to experience. The key observation is that learning need not be implemented as parameter updates: it can be implemented as changes in the internal attractor landscape of a recurrent stochastic dynamical system.

**Definition (Implicit Learning).** A Neo exhibits implicit learning if its future responses to identical percepts differ depending on its past trajectory, even though its parameters $$\Theta_t$$ remain fixed within a lifetime.

Because Neos can evolve recurrent structures, memory loops, and modulatory subgraphs, implicit learning is not only possible but expected under evolutionary pressure.

## 4.2 Structural Features Enabling Learnability

Learnability requires that the Neo's structure support representations that change based on experience. Three ingredients of the Neo architecture enable this:

### 4.2.1 Recurrent Graph Dynamics

Any directed cycle in $$E_t$$ yields an internal stateful subsystem. For a cycle
$$
i_1 \to i_2 \to \dots \to i_k \to i_1,
$$
the activity of the nodes depends on their joint history. Such cycles act as memory elements. When combined with threshold nonlinearities, these cycles define basins of attraction that shift as new percepts arrive.

Evolution can discover cycles that selectively stabilize useful perceptual patterns, effectively implementing memory formation and context-dependent behavior.

### 4.2.2 Stochastic Modulation

Each node receives an intrinsic random bit $$\eta_i(t)$$ weighted by $$\alpha_i$$. This makes the global dynamics stochastic. Evolution can exploit this stochasticity to create gating effects, where certain internal states become more or less likely depending on prediction error.

The stochastic term is therefore a catalyst for exploration and symmetry breaking. It enables evolution to create motifs that behave like neuromodulators: internal nodes whose output controls the sensitivity of other nodes to incoming activity.

### 4.2.3 Evolution of Input–Output Surfaces

Chapter 2 introduced the output index set $$O_t$$. Because output mutation is allowed, Neos can evolve which internal nodes represent predictions. This ability to reassign outputs lets evolution discover specialized decoder motifs—subgraphs that reliably summarize internal state into accurate predictions. As these motifs shift in response to environmental challenges, output evolution becomes a mechanism for adaptive restructuring of representational surfaces.

## 4.3 Emergence of Learning Through Evolution

Although parameters do not change within a lifetime, Evo can mutate structure and parameters selectively based on accumulated energy. This creates a two-timescale adaptation process:

- **Fast timescale:** state dynamics $$(\mathbf{V}_t)$$ implement implicit learning via recurrent computation.
- **Slow timescale:** Evo shapes $$(E_t, \Theta_t, O_t)$$ through mutation, selecting structures that support more flexible and adaptive fast-timescale behavior.

This mirrors biological organization: neural activity (fast) and synaptic refinement or development (slow).

### 4.3.1 Evolution of Error-Sensitive Circuits

To predict well, a Neo must detect when its guesses $$\mathbf{Y}_t = \mathbf{V}_t[O_t]$$ are wrong. Although the reward signal $$R(\mathbf{Y}_t, \mathbf{U}_{t+1})$$ is external, evolution can create internal subgraphs that correlate internal activity with the observed reward sequence, effectively building an internal error signal.

Neos with such motifs incur mutations in parameter directions that improve prediction. Over generations, these motifs are reinforced, producing circuits that behave, operationally, like error-driven learners—even in the absence of parameter updates.

### 4.3.2 Emergent Plasticity and Meta-Learning

Meta-learning arises when evolution shapes not only predictive circuits but also circuits that modulate how those circuits behave over time. Typical patterns include:

- nodes that detect volatility and gate internal noise levels
- nodes whose activity triggers more frequent beneficial mutations
- recurrent modules that reconfigure themselves based on long-term trends in input

These structures amount to an **evolution of plasticity**. The Neo acquires circuitry that adjusts its own attractor landscape in ways that mimic synaptic plasticity, despite no explicit plasticity mechanism being present.

## 4.4 Formalizing Learnability

We now give a precise definition of learnability for Neos. Let $$\mathbf{V}_t$$ denote the internal binary state and $$O_t$$ the output set. Consider two trajectories starting from identical initial states and identical parameters:

$$
(\mathbf{V}_0, E_0, \Theta_0, O_0) = (\mathbf{V}'_0, E'_0, \Theta'_0, O'_0).
$$

A Neo is said to be learnable if there exists an environment process $$\{\mathbf{U}_t\}$$ such that

$$
\mathbf{Y}_t = \mathbf{V}_t[O_t] \quad \text{and} \quad \mathbf{Y}'_t = \mathbf{V}'_t[O_t]
$$

diverge over time as a function of differing perceptual histories, without requiring mutations during that interval.

**Interpretation.** Learnability is achieved when the internal dynamics are sensitive to experience.

## 4.5 When Does Learnability Emerge?

Learnability does not require any new primitives; it emerges automatically when:

1. edge$$^+$$ and edge$$^-$$ mutations produce recurrent loops,
2. node$$^+$$ and node$$^-$$ create modulatory subgraphs,
3. stochastic inputs are leveraged by evolution as conditional gates,
4. output$$^+$$ and output$$^-$$ mutations allow adaptive readout of internal representations,
5. energy-based selection rewards structures that respond flexibly to environmental variation.

Under these conditions, evolution discovers Neo architectures that:

- adapt their internal state based on past inputs,
- condition future predictions on internal memory,
- alter internal computational modes based on external volatility,
- restructure the effective functional layout of the graph.

These properties collectively constitute learning and meta-learning.

## 4.6 Summary

Although Neos lack built-in learning rules, the Neo substrate naturally supports the evolution of systems whose fast-timescale dynamics encode experience-dependent behavior. Learnability arises from the combination of recurrent computation, stochastic modulation, evolving input–output surfaces, and energy-driven evolutionary selection.

This chapter establishes that learning need not be inserted into Neosis; it is an emergent property of the architecture itself. The next chapters build on this by analyzing how populations of Neos develop increasingly sophisticated adaptive behaviors through evolutionary pressure.
