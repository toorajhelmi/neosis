# Chapter 4 — Micro Analysis of a Single Neo

## 4.1 Scope and Objectives

This chapter analyzes the behavior of an individual Neo at the smallest structural scales. We focus on nodes, edges, Lex, stochasticity, energy transitions, mutation effects, and In-Life learning rules, independent of population-level dynamics.

## 4.2 Minimal Neo Structures

### 4.2.1 Zero-Node and Degenerate Cases

**Purpose:** Characterize Neos with no internal nodes.

**Expectation:** Show they have no representational capacity and follow trivial energy trajectories.

### 4.2.2 Single-Node Neo

**Purpose:** Analyze the simplest functional unit governed by Lex.

**Expectation:** Evaluate deterministic, stochastic, and memory-like behavior for minimal structures.

### 4.2.3 Two-Node Neo

**Purpose:** Introduce the simplest interacting system.

**Expectation:** Demonstrate how feedforward, recurrent, and parallel pairs yield richer micro-dynamics.

### 4.2.4 Canonical Micro-Motifs

**Purpose:** Identify recurring low-level patterns.

**Expectation:** Use chains, fan-in, fan-out, and loops as computational building blocks for larger Neos.

## 4.3 Lex and Local Computation

### 4.3.1 Lex Dynamics

**Purpose:** Formalize deterministic and stochastic transitions induced by the Lex rule.

**Expectation:** Analyze the influence of weights, bias, and the stochastic term on node updates.

### 4.3.2 Effect of Stochasticity

**Purpose:** Study how randomness modifies micro-scale behavior.

**Expectation:** Show variability, exploration, and divergence across identical initialized Neos.

### 4.3.3 Micro-Level Expressive Capacity

**Purpose:** Assess the representational power of small fixed structures.

**Expectation:** Describe the deterministic and stochastic input–output mappings achievable by one- and two-node Neos.

## 4.4 Energy Trajectories at Micro Scale

### 4.4.1 Tick-Level Energy Flow

**Purpose:** Examine energy changes during a single cycle.

**Expectation:** Detail computation cost, reward acquisition, and the resulting energy update.

### 4.4.2 Lifetime and Vitality in Simple Structures

**Purpose:** Quantify survival properties of minimal Neos.

**Expectation:** Compare deterministic, stochastic, and recurrent motifs in terms of energy trajectories and survival.

## 4.5 Micro-Level Mutation Experiments

### 4.5.1 Isolated Mutation Types

**Purpose:** Analyze the effect of each mutation primitive separately.

**Expectation:** Show structural and behavioral results for node$$^+$$, node$$^-$$, edge$$^+$$, edge$$^-$$, and param$$^f$$.

### 4.5.2 Mutation Cost and Trade-Offs

**Purpose:** Relate mutation outcomes to energy budget.

**Expectation:** Demonstrate scenarios where beneficial mutations fail due to cost and scenarios where small modifications outperform structural changes.

### 4.5.3 Comparative Mutation Strategies

**Purpose:** Compare alternative mutation strategies on identical initial conditions.

**Expectation:** Identify strategies that maximize accuracy, stability, or survival at the micro scale.

## 4.6 In-Life Learning at the Micro Level

### 4.6.1 In-Life Learning vs Mutation

**Purpose:** Clarify conceptual separation between In-Life learning rules and evolutionary mutation.

**Expectation:** Show why In-Life learning must be pattern-triggered rather than error-driven.

### 4.6.2 Minimal In-Life Learning Schemes

**Purpose:** Introduce simple local In-Life learning mechanisms.

**Expectation:** Propose conditional param adjustments and evaluate their behavior in one- and two-node systems.

### 4.6.3 Effects of In-Life Learning on Micro Dynamics

**Purpose:** Analyze situations where In-Life learning helps or harms.

**Expectation:** Present simulations illustrating successful adaptation versus destabilizing drift.

## 4.7 Role of Stochasticity in Micro Evolution

### 4.7.1 Fixed-Structure Stochastic Behavior

**Purpose:** Understand the influence of noise on stable structures.

**Expectation:** Demonstrate divergence in predictions and internal states across runs.

### 4.7.2 Stochasticity as Exploration Under Mutation

**Purpose:** Show how noise facilitates discovery of structural variations.

**Expectation:** Illustrate how stochasticity interacts with Evo to produce divergent evolutionary paths.

## 4.8 Summary of Micro-Level Insights

**Purpose:** Consolidate micro-scale results.

**Expectation:** Summarize patterns in structural motifs, mutation tendencies, In-Life learning interactions, and the role of stochasticity.
