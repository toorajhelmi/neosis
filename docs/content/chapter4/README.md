# Chapter 4 — Micro Analysis of a Single Neo

## 4.1 Scope and Objectives

This chapter analyzes the behavior of an individual Neo at the smallest structural scales. We focus on nodes, edges, Lex, stochasticity, energy transitions, mutation effects, and In-Life learning rules, independent of population-level dynamics.

## 4.2 Minimal Neo Structures

## 4.2.1 Zero-Node and Degenerate Cases

**Purpose:** Characterize Neos with no internal nodes.  

**Expectation:** Show they have no representational capacity and follow trivial energy trajectories.

A zero-node Neo has no internal state:

$$V(t) = \varnothing.$$

There is exactly one state. Call it state 0.

### Transition Matrix

State space: {0}

$$P = \begin{bmatrix} 1 \end{bmatrix}.$$

### Stationary Distribution

Let $$\pi = [\pi_0]$$ with the normalization constraint $$\pi_0 = 1$$.

Stationarity:

$$\pi P = \pi$$

is trivially satisfied.

### Result

$$\boxed{\pi = [1]}$$

No representational power; trivial dynamics.

---

## 4.2.2 Single-Node Neo

**Purpose:** Analyze the simplest functional unit governed by Lex.  

**Expectation:** Evaluate deterministic, stochastic, and memory-like behavior.

Diagram:

```
    U(t)
     |
     v
   +-----+
   | V1  |
   +-----+
     |
     v
   Y(t)=V1(t)
```

We use a minimal Lex update:

$$a(t) = a\,U(t) + b + \alpha\,\eta(t),$$

with noise:

$$\eta(t)\in\{-1,+1\},\quad \mathbb{P}(\eta=\pm1)=\tfrac12.$$

State update:

$$V(t+1) = H(a(t)).$$

To obtain a homogeneous Markov chain, fix $$U(t)=u$$.

---

### Numerical Example

Pick parameters:

$$a = 1.2,\quad b = -0.4,\quad \alpha = 0.8.$$

Thus:

$$a(t) = 1.2u - 0.4 + 0.8\eta(t).$$

Let

$$s = 1.2u - 0.4.$$

Compute probabilities:

Case u = 0:

- s = -0.4  
- a_+ = -0.4 + 0.8 = 0.4  → H(a_+) = 1  
- a_- = -0.4 - 0.8 = -1.2 → H(a_-) = 0  

Thus:

$$P(V'=1\mid u=0)=0.5.$$

Case u = 1:

- s = 0.8  
- a_+ = 0.8 + 0.8 = 1.6 → 1  
- a_- = 0.8 - 0.8 = 0 → 1  

Thus:

$$P(V'=1\mid u=1)=1.$$

---

### Transition Matrices

State ordering: [0, 1].

#### For u = 0:

$$P_{u=0} = \begin{bmatrix} 0.5 & 0.5 \\ 0.5 & 0.5 \end{bmatrix}.$$

#### For u = 1:

$$P_{u=1} = \begin{bmatrix} 0 & 1 \\ 0 & 1 \end{bmatrix}.$$

---

### Stationary Distribution

Solve $$\pi P = \pi$$.

#### u = 0:

Equations:

$$\pi_0 = 0.5(\pi_0+\pi_1),\quad \pi_1=0.5(\pi_0+\pi_1)$$

Normalization $$\pi_0+\pi_1=1$$ forces

$$\pi_0=\pi_1=\tfrac12.$$

#### u = 1:

State 1 is absorbing.

$$\pi = (0,1).$$

---

### Result Summary

- For u=0: $$\pi = (0.5, 0.5)$$  
- For u=1: $$\pi = (0, 1)$$

A single-node Neo already supports deterministic and stochastic modes and 1-bit memory.

---

## 4.2.3 Two-Node Neo

**Purpose:** Introduce the simplest interacting system.  

**Expectation:** Show how feedforward, parallel, and feedback structures produce richer micro-dynamics.

Let

$$V(t) = (V_1(t), V_2(t)) \in \{0,1\}^2.$$

State ordering:  

1 = (0,0),  

2 = (0,1),  

3 = (1,0),  

4 = (1,1).

---

# === CASE A — FEEDFORWARD (U→V1→V2) ===

Diagram:

```
    U
    |
    v
 +-----+      +-----+
 | V1  | ---> | V2  |
 +-----+      +-----+
```

Choose parameters:

Node 1:

$$V_1' = H(1.0 U - 0.2 + 0.7\eta_1).$$

Node 2:

$$V_2' = H(1.4 V_1 - 0.1 + 0.9\eta_2).$$

Noise variables independent.

Fix input u.

---

### Numerical Behavior

For u = 0:

- $$P(V_1'=1) = 0.5.$$
- If $$V_1'=0$$, then $$P(V_2'=1)=0.5$$.
- If $$V_1'=1$$, then $$P(V_2'=1)=1$$.

Thus:

$$P(V_2'=1\mid u=0) = 0.5(0.5) + 0.5(1) = 0.75.$$

For u = 1:

- $$P(V_1'=1)=1.$$
- Thus $$P(V_2'=1)=1.$$

---

### Transition Matrix for u = 0

Using independence:

$$P_{u=0}^{FF} = \begin{bmatrix} 0.25 & 0.25 & 0.25 & 0.25 \\ 0.25 & 0.25 & 0.25 & 0.25 \\ 0    & 0.5  & 0    & 0.5  \\ 0    & 0.5  & 0    & 0.5 \end{bmatrix}.$$

### Stationary Distribution (u = 0)

Use symmetry:

Let $$\pi_1=\pi_3=a,\; \pi_2=\pi_4=b,$$  

with $$a+b=\tfrac12$$.

From the first row:

$$a = 0.25(a+b),$$

so

$$a = 0.25\cdot \tfrac12 = \tfrac18, \qquad b = \tfrac38.$$

Final:

$$\pi = \Big(\tfrac18,\tfrac38,\tfrac18,\tfrac38\Big).$$

### Transition Matrix for u = 1

$$P_{u=1}^{FF} = \begin{bmatrix} 0 & 0 & 0.5 & 0.5 \\ 0 & 0 & 0.5 & 0.5 \\ 0 & 0 & 0   & 1   \\ 0 & 0 & 0   & 1 \end{bmatrix}.$$

### Stationary Distribution (u = 1)

State 4 = (1,1) is absorbing.

$$\pi = (0,0,0,1).$$

---

# === CASE B — PARALLEL (U→V1 and U→V2) ===

Diagram:

```
          U
         / \
        v   v
     +-----+ +-----+
     | V1  | | V2  |
     +-----+ +-----+
```

Let each node behave like the single-node example.

Thus for u = 0:

$$P(V_1'=1)=0.5,\quad P(V_2'=1)=0.5.$$

Joint distribution:

$$P(V_1',V_2' \mid u=0)=\frac14 \text{ for all 4 states}.$$

Transition matrix (independent of previous state):

$$P_{u=0}^{PAR} = \begin{bmatrix} 0.25 & 0.25 & 0.25 & 0.25 \\ 0.25 & 0.25 & 0.25 & 0.25 \\ 0.25 & 0.25 & 0.25 & 0.25 \\ 0.25 & 0.25 & 0.25 & 0.25 \end{bmatrix}.$$

Stationary distribution:

$$\pi = (0.25,0.25,0.25,0.25).$$

For u = 1:

$$V_1'=1,\quad V_2'=1$$

⇒ the absorbing state (1,1).

$$\pi=(0,0,0,1).$$

---

# === CASE C — FEEDBACK (V1 ↔ V2) ===

Diagram:

```
         U
        / \
       v   v
    +-----+ <-----+
    | V1  |       |
    +-----+       |
      ^           |
       \          |
        \         v
         \      +-----+
          ------| V2  |
                +-----+
```

Choose parameters:

Node 1:

$$V_1' = H(0.7U + 1.0V_2 - 0.5 + 0.6\eta_1).$$

Node 2:

$$V_2' = H(-0.4U + 1.5V_1 - 0.2 + 0.7\eta_2).$$

---

### Transition Matrix for u = 0

From the derivation:

$$P_{u=0}^{FB} = \begin{bmatrix} 0.25 & 0.25 & 0.25 & 0.25 \\ 0.25 & 0.25 & 0.25 & 0.25 \\ 0    & 0.5  & 0    & 0.5  \\ 0    & 0.5  & 0    & 0.5 \end{bmatrix}.$$

This is identical to feedforward u=0 under this numeric choice.

### Stationary Distribution (u = 0)

Same solution:

$$\pi = \Big(\tfrac18,\tfrac38,\tfrac18,\tfrac38\Big).$$

---

### Transition Matrix for u = 1

$$P_{u=1}^{FB} = \begin{bmatrix} 0.25 & 0.25 & 0.25 & 0.25 \\ 0    & 0    & 0.5  & 0.5  \\ 0    & 0.5  & 0    & 0.5  \\ 0    & 0    & 0    & 1 \end{bmatrix}.$$

State (1,1) is absorbing.

### Stationary Distribution (u = 1)

$$\pi = (0,0,0,1).$$

---

# Summary of Results

| Case | Input u | Transition Matrix | Stationary Distribution |
|------|---------|-------------------|-------------------------|
| Zero-node | any | [1] | [1] |
| Single-node | 0 | [[0.5 0.5],[0.5 0.5]] | (0.5,0.5) |
| Single-node | 1 | [[0 1],[0 1]] | (0,1) |
| FF 2-node | 0 | as above | (1/8,3/8,1/8,3/8) |
| FF 2-node | 1 | absorbing | (0,0,0,1) |
| PAR 2-node | 0 | fully uniform | (1/4,1/4,1/4,1/4) |
| PAR 2-node | 1 | absorbing | (0,0,0,1) |
| FB 2-node | 0 | same as FF u=0 | (1/8,3/8,1/8,3/8) |
| FB 2-node | 1 | absorbing | (0,0,0,1) |

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
