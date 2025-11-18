# Chapter 2 — Neosis Axioms and Formal Model

## 2.1 Primitive Ingredients and State

Neosis is defined on top of a small collection of primitive ingredients that will be reused throughout the chapter. In this section, the goal is not to describe the full internal structure of a Neo, but to fix the basic objects and types—time, binary state, energy, and continuous parameters—that later sections will assemble into a complete formal model.

### 2.1.1 Time

All dynamics unfold in discrete time. We index ticks by
$t \in \mathbb{N} = \{0,1,2,\dots\}$,
with $t = 0$ denoting the initial configuration of the system. Each application of the update rules (perception, internal computation, reward, and mutation) advances the system from tick $t$ to tick $t+1$. Throughout the chapter, we will describe the behavior of Neos and the NeoVerse by specifying how relevant quantities change as a function of this tick index.

### 2.1.2 Binary State Substrate

The underlying state substrate of Neosis is binary. We write
$\mathbb{B} = \{0,1\}$
for individual bits, and $\mathbb{B}^n$ for length-$n$ bit vectors. At any tick $t$, the internal memory of a Neo, its perceptual input, and its output will all be represented as elements of $\mathbb{B}^n$ for some finite $n$. The dimensionality $n$ is not fixed once and for all: it may change over time as the Neo gains or loses nodes through structural mutation. This choice keeps the local state space simple, while still allowing the overall system to grow in representational capacity.

### 2.1.3 Energy (Nex)

Each Neo maintains an energy budget, called Nex, which constrains its computation and evolution. At tick $t$, the energy of a given Neo is denoted by
$$
N_t \in \mathbb{R}_{\ge 0}.
$$
Running computations and performing structural mutations both consume energy, while successful prediction of the NeoVerse yields energy in the form of rewards (Sparks). All such costs and rewards are measured in the same units as Nex, so that energy evolves by simple additive updates of the form
$$
N_{t+1} = N_t + \text{(reward at } t\text{)} - \text{(cost at } t\text{)}.
$$
Once $N_t$ reaches zero, the Neo becomes inert: it can no longer perform internal computation or apply mutations, and its trajectory effectively terminates.

### 2.1.4 Continuous Parameters and Discrete Structure

A central modeling choice in Neosis is to separate *structure* from *parameters*. The structure of a Neo—its set of nodes, edges, and connectivity pattern—will be discrete and graph-like. However, each structural unit carries continuous parameters. For node $i$, we write
$$
\theta_i \in \mathbb{R}^{k_i},
$$
where $k_i$ is the parameter dimensionality associated with that node. These parameters control the local computation performed at the node (for example, weights, thresholds, or other coefficients), and they may change over time through learning mechanisms or mutation.

This separation between discrete structure (which nodes exist and how they are connected) and continuous parameters $\theta_i$ (how each node computes) is deliberate. It allows Neos to evolve by changing their topology in a combinatorial way, while still supporting rich, smooth families of local computations at each node. Later sections will make this distinction explicit when we define the internal graph of a Neo and the node-local update functions.

### 2.1.5 Global State at Tick \(t\)

At each tick $t$, we conceptually distinguish between the internal state of a Neo and the state of the surrounding world. We write
$$
\text{World}_t
$$
for the (possibly high-dimensional) state of the NeoVerse at tick $t$, and
$$
\text{Neo}_t
$$
for the complete internal state of a single Neo at the same tick, including its binary memory, graph structure, parameters, and energy. In this chapter we will focus on formalizing $\text{Neo}_t$; the NeoVerse state $\text{World}_t$ will be treated abstractly and will be accessed only through a projection function introduced in Section 2.2.

## 2.2 The NeoVerse and Perception
- World state
- Projection Φ to U_t

## 2.3 The Neo: Internal Structure
- Lio: (V_t, G_t, Lex, U_t, Y_t)
- Evo: mutation policy and parameters

## 2.4 Local Computation (Lex and Node Updates)

## 2.5 Mutation Primitives and Structural Updates

## 2.6 The Cycle (Operational Semantics)

## 2.7 Performance Measure: NeoQuotient


