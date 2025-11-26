# Chapter 4 — Micro Analysis of a Single Neo

## 4.1 Scope and Objectives

This chapter analyzes the behavior of an individual Neo at the smallest structural scales. We focus on nodes, edges, Lex, stochasticity, energy transitions, mutation effects, and In-Life learning rules, independent of population-level dynamics.

## 4.2 Minimal Neo Structures

Before analyzing general Neo behavior or introducing simulation-based and macro-level analytical tools, it is essential to understand the smallest possible Neo configurations in full mathematical detail. These minimal structures allow us to introduce the exact formal treatment used throughout this chapter—state evolution, transition matrices, and stationary distributions—while also revealing the fundamental building blocks of Neo dynamics. Even the simplest Neos already display the core mechanisms of computation, stochasticity, memory, and stability that will later reappear in more complex systems.

The goal of this section is twofold. First, we provide concrete numerical examples that make the Lex update rule, noise-driven stochasticity, and state transitions completely explicit. Second, by deriving transition matrices and stationary distributions for each small case, we establish the analytical vocabulary that will be necessary for larger-scale reasoning. These elementary analyses form the conceptual bridge between the micro-level Neo defined earlier and the simulation- or macro-level treatments that follow in later chapters.

A Neo, being a finite-state stochastic dynamical system, evolves according to a Markov process once the input is fixed. At any time step, the internal state determines the distribution of the next state. For small Neos, this process can be expressed exactly through a **transition matrix**, which is a table containing all probabilities of moving from any current state to any future state in one time step. Formally, if the Neo has $$K$$ possible internal configurations, the transition matrix is a $$K \times K$$ matrix

$$P(i,j) = P(X(t+1)=j \mid X(t)=i),$$

where $$X(t)$$ denotes the internal state at time $$t$$. The transition matrix completely determines the dynamics of the Neo under fixed external input and fixed parameters.

Once we have the transition matrix, we can study the **stationary distribution**, which is the long-run probability with which the Neo occupies each state. A stationary distribution is any probability vector $$\pi$$ satisfying

$$\pi P = \pi, \quad \sum_i \pi_i = 1.$$

This equation expresses the idea that the distribution does not change over time when the system is already in its long-run regime. If the Markov chain is irreducible (all states eventually communicate) and aperiodic, the stationary distribution is unique and describes the asymptotic behavior of the Neo independent of its initial condition. In simple configurations, the stationary distribution reveals whether the Neo stabilizes on a particular state, oscillates between several states, or continuously explores the entire state space.

Understanding transition matrices and stationary distributions at the micro-level is important for three reasons. First, these quantities provide exact insight into how Lex, stochasticity, and basic topology produce deterministic or probabilistic behaviors. Second, they allow us to characterize stability and long-run predictability of small Neo motifs before introducing more complex structures. Third, they form the analytical template we will later generalize using simulation, approximation, and macro-level mathematical tools, especially when direct computation becomes infeasible due to the exponential size of the state space.

Before diving into the detailed cases, a few conceptual points should be kept in mind:

1. **Minimal Neos are not trivial.**  

   Even a single node can exhibit stochastic switching, memory, and asymmetric transition behavior. Two-node networks can display feedforward computation, parallel processing, and recurrent feedback loops.

2. **Stochasticity is inherent, not optional.**  

   The Rademacher noise term $$\eta(t)\in\{-1,+1\}$$ plays a critical role in creating probabilistic transitions. Later chapters will relate this to exploration, robustness, and evolutionary variability.

3. **Topology matters dramatically.**  

   Feedforward, parallel, and feedback structures behave fundamentally differently, even in their minimal 2-node forms. Studying these prototypes builds intuition for larger Neo graphs.

4. **Transition matrices grow exponentially.**  

   A Neo with $$N$$ binary nodes has $$2^N$$ possible states. By explicitly analyzing the smallest cases, we understand why analytical solutions rapidly become infeasible and why simulation and macro analysis are required later.

5. **Stationary distributions compress long-term behavior.**  

   Although individual transitions may be noisy, the stationary distribution summarizes the global tendencies of a Neo. It reveals absorbing states, dominant motifs, or persistent stochastic wandering—all of which matter for energy dynamics, representational power, and evolutionary fitness.

With these foundations, the next subsection analyzes a two-node recurrent Neo structure in detail, including a numerical example, the complete derivation of transition probabilities, the full transition matrix, and the stationary distribution. Additional minimal Neo cases (zero-node, single-node, and other two-node topologies) are provided in Appendix A.

---

### 4.2.1 Two-Node Recurrent Neo (Feedback: Node1 ↔ Node2)

We now analyze a minimal recurrent Neo consisting of two binary nodes that feed back into each other while both receive the same external input bit. This gives the simplest nontrivial closed micro-dynamics that can already exhibit stability, oscillation, and noise-driven switching, and it will later serve as a canonical building block for larger Neos. The construction here is consistent with the general Neo definition given in Chapter 2 of the main document.

At tick $$t$$, the internal state of this two-node Neo is the binary pair

$$X_t = (V_t(1), V_t(2)) \in \{0,1\}^2,$$

and the external percept is a single bit

$$U_t \in \{0,1\}.$$

Node 1 receives $$U_t$$ and the current state of Node 2, while Node 2 receives $$U_t$$ and the current state of Node 1. The resulting graph is:

```
           ┌──────────────┐
           │   U_t (input)│
           └───────┬──────┘
                   │
         ┌─────────┴─────────┐
         │                   │
   ┌───────────┐       ┌───────────┐
   │  Node 1   │<----->│  Node 2   │
   │  V_t(1)   │       │  V_t(2)   │
   └─────┬─────┘       └─────┬─────┘
         │                   │
      z₁(t)               z₂(t)
```

Node 1's local input vector is

$$z_1(t) = [U_t, V_t(2)],$$

and Node 2's local input vector is

$$z_2(t) = [U_t, V_t(1)].$$

Each node follows the same stochastic threshold rule used in the general Neo model. For node $$i \in \{1,2\}$$, with weight vector $$w_i$$, bias $$b_i$$, and noise scale $$\alpha_i$$, we define the deterministic pre-activation

$$s_i = w_i^\top z_i(t) + b_i,$$

and the noisy activation

$$a_i(t) = s_i + \alpha_i \eta_i(t),$$

where $$\eta_i(t)$$ is a Bernoulli noise term. The updated node state is

$$V_{t+1}(i) = H(a_i(t)),$$

with $$H(\cdot)$$ the Heaviside step. In the simplified piecewise-probabilistic form we use here, the noise is summarized by a "soft band" around zero: when $$s_i$$ is outside this band the node behaves almost deterministically, and when $$s_i$$ lies inside it, the node fires with probability one half. Concretely, the firing probabilities are

$$p_1(u, v_2) = \begin{cases} 1, & s_1 \geq \alpha_1, \\ 0, & s_1 \leq -\alpha_1, \\ \frac{1}{2}, & -\alpha_1 < s_1 < \alpha_1, \end{cases}$$

$$p_2(u, v_1) = \begin{cases} 1, & s_2 \geq \alpha_2, \\ 0, & s_2 \leq -\alpha_2, \\ \frac{1}{2}, & -\alpha_2 < s_2 < \alpha_2, \end{cases}$$

where $$s_1$$ and $$s_2$$ are evaluated at the corresponding inputs.

#### 4.2.1.1 Dynamics with Concrete Parameters

To make these abstract rules concrete, we now choose explicit parameters and examine how the two-node Neo behaves step by step. Let the weight vectors and biases be

$$w_1 = [1.2, -0.8], \quad b_1 = -0.3, \quad \alpha_1 = 0.4,$$

$$w_2 = [0.6, 1.1], \quad b_2 = -0.2, \quad \alpha_2 = 0.3.$$

Recall that the inputs are ordered as

$$z_1(t) = [U_t, V_t(2)], \quad z_2(t) = [U_t, V_t(1)].$$

We consider a fixed external input $$U_t = 1$$, and an initial internal state

$$V_t(1) = 0, \quad V_t(2) = 1.$$

For this tick, suppose the noise samples are $$\eta_1(t) = 1$$ and $$\eta_2(t) = 0$$. Node 1 computes

$$s_1 = 1.2 \cdot U_t - 0.8 \cdot V_t(2) + b_1 = 1.2 \cdot 1 - 0.8 \cdot 1 - 0.3 = 0.1,$$

and then

$$a_1(t) = s_1 + \alpha_1 \eta_1(t) = 0.1 + 0.4 \cdot 1 = 0.5.$$

Since $$a_1(t) \geq 0$$, Node 1 switches to the ON state,

$$V_{t+1}(1) = 1.$$

Node 2, with the same input but a different feedback term, computes

$$s_2 = 0.6 \cdot U_t + 1.1 \cdot V_t(1) + b_2 = 0.6 \cdot 1 + 1.1 \cdot 0 - 0.2 = 0.4,$$

and

$$a_2(t) = s_2 + \alpha_2 \eta_2(t) = 0.4 + 0.3 \cdot 0 = 0.4.$$

Again $$a_2(t) \geq 0$$, so Node 2 is also ON:

$$V_{t+1}(2) = 1.$$

In this example the feedback and shared input quickly drive the system to the joint ON state

$$X_{t+1} = (V_{t+1}(1), V_{t+1}(2)) = (1, 1),$$

with randomness playing a decisive role only for Node 1 through the positive noise spike. As we now show, once the parameters are fixed we can summarize all such updates by a four-state Markov chain and compute its stationary distribution.

#### 4.2.1.2 Computing Transition Probabilities

We now fix the external input permanently to $$U_t = 1$$ for all $$t$$. Under this assumption, the system becomes a homogeneous Markov chain on the four states

$$(0,0), (0,1), (1,0), (1,1),$$

which we abbreviate as $$00, 01, 10, 11$$. For any current state $$(v_1, v_2)$$ we set

$$z_1 = [1, v_2], \quad z_2 = [1, v_1],$$

and compute the deterministic parts

$$s_1(1, v_2) = 1.2 \cdot 1 - 0.8 v_2 - 0.3,$$

$$s_2(1, v_1) = 0.6 \cdot 1 + 1.1 v_1 - 0.2.$$

For our chosen parameters the resulting values are

$$s_1(1, 0) = 0.9, \quad s_1(1, 1) = 0.1,$$

$$s_2(1, 0) = 0.4, \quad s_2(1, 1) = 1.5.$$

With $$\alpha_1 = 0.4$$ and $$\alpha_2 = 0.3$$, we see that

$$s_1(1, 0) = 0.9 \geq \alpha_1 \Rightarrow p_1(1, 0) = 1,$$

$$s_1(1, 1) = 0.1 \in (-\alpha_1, \alpha_1) = (-0.4, 0.4) \Rightarrow p_1(1, 1) = \frac{1}{2},$$

$$s_2(1, 0) = 0.4 \geq \alpha_2 \Rightarrow p_2(1, 0) = 1,$$

$$s_2(1, 1) = 1.5 \geq \alpha_2 \Rightarrow p_2(1, 1) = 1.$$

Thus, for this specific two-node Neo under constant input $$U_t = 1$$, Node 2 is effectively deterministic and always fires, while Node 1 is deterministic when $$V_t(2) = 0$$ and probabilistic when $$V_t(2) = 1$$.

Given $$p_1(u, v_2)$$ and $$p_2(u, v_1)$$, the joint transition probability factorizes because the local noises are independent:

$$P(X_{t+1} = (v_1', v_2') \mid X_t = (v_1, v_2), U_t = 1) = P(V_{t+1}(1) = v_1' \mid v_2, 1) \cdot P(V_{t+1}(2) = v_2' \mid v_1, 1).$$

Using the usual Bernoulli splitting, this expands to

$$P(X_{t+1} = (1, 1) \mid v_1, v_2) = p_1(1, v_2) \cdot p_2(1, v_1),$$

$$P(X_{t+1} = (1, 0) \mid v_1, v_2) = p_1(1, v_2) \cdot (1 - p_2(1, v_1)),$$

$$P(X_{t+1} = (0, 1) \mid v_1, v_2) = (1 - p_1(1, v_2)) \cdot p_2(1, v_1),$$

$$P(X_{t+1} = (0, 0) \mid v_1, v_2) = (1 - p_1(1, v_2)) \cdot (1 - p_2(1, v_1)).$$

With the numeric values for $$p_1$$ and $$p_2$$, we can now write the full transition matrix.

#### 4.2.1.3 The 4×4 Transition Matrix

We order the states as $$00, 01, 10, 11$$. For each row, we plug the appropriate $$p_1(1, v_2)$$ and $$p_2(1, v_1)$$ into the expressions above.

**From 00** we have $$v_1 = 0$$, $$v_2 = 0$$, thus $$p_1 = p_1(1, 0) = 1$$ and $$p_2 = p_2(1, 0) = 1$$. The next state is deterministically $$11$$:

$$P(00 \to 11) = 1, \quad P(00 \to 00) = P(00 \to 01) = P(00 \to 10) = 0.$$

**From 01** we have $$v_1 = 0$$, $$v_2 = 1$$, so $$p_1 = p_1(1, 1) = \frac{1}{2}$$ and $$p_2 = p_2(1, 0) = 1$$. Hence

$$P(01 \to 11) = p_1 p_2 = \frac{1}{2},$$

$$P(01 \to 01) = (1 - p_1) p_2 = \frac{1}{2},$$

and transitions to $$00$$ and $$10$$ have probability zero.

**From 10** we have $$v_1 = 1$$, $$v_2 = 0$$, hence $$p_1 = p_1(1, 0) = 1$$ and $$p_2 = p_2(1, 1) = 1$$. Again the next state is deterministically $$11$$:

$$P(10 \to 11) = 1,$$

all other outcomes zero.

**From 11** we have $$v_1 = 1$$, $$v_2 = 1$$, so $$p_1 = p_1(1, 1) = \frac{1}{2}$$ and $$p_2 = p_2(1, 1) = 1$$. This is analogous to the $$01$$ case:

$$P(11 \to 11) = p_1 p_2 = \frac{1}{2}, \quad P(11 \to 01) = (1 - p_1) p_2 = \frac{1}{2},$$

with all other transitions zero.

Collecting these results, the transition matrix $$P$$ in the state order $$[00, 01, 10, 11]$$ is

$$P = \begin{pmatrix} 0 & 0 & 0 & 1 \\ 0 & 1/2 & 0 & 1/2 \\ 0 & 0 & 0 & 1 \\ 0 & 1/2 & 0 & 1/2 \end{pmatrix}.$$

States $$00$$ and $$10$$ are transient: both flow deterministically into $$11$$ and can never be revisited. The long-run behavior is confined to the two-state subsystem $$\{01, 11\}$$.

#### 4.2.1.4 Stationary Distribution for Fixed Input

The stationary distribution $$\pi$$ for this Markov chain satisfies

$$\pi = \pi P, \quad \sum_{x \in \{00, 01, 10, 11\}} \pi_x = 1,$$

where $$\pi_x = P(X_t = x)$$ in the long-run equilibrium. Because the first and third columns of $$P$$ are identically zero, any stationary distribution must have

$$\pi_{00} = \pi_{10} = 0.$$

Hence the stationary mass lives entirely on $$01$$ and $$11$$. Let

$$\pi_{01} = x, \quad \pi_{11} = 1 - x.$$

We only need to enforce the stationarity condition on these two states. For state $$01$$ we have

$$\pi_{01} = \pi_{01} P(01 \to 01) + \pi_{11} P(11 \to 01) = x \cdot \frac{1}{2} + (1 - x) \cdot \frac{1}{2} = \frac{1}{2}.$$

This immediately gives $$x = \frac{1}{2}$$. The probability of state $$11$$ then follows from normalization:

$$\pi_{11} = 1 - \pi_{01} = \frac{1}{2}.$$

Thus the unique stationary distribution for this two-node Neo under constant input $$U_t = 1$$ is

$$\boxed{\pi_{00} = 0, \quad \pi_{01} = \frac{1}{2}, \quad \pi_{10} = 0, \quad \pi_{11} = \frac{1}{2}.}$$

In other words, in the long run the Neo spends half of its time in the partially active configuration $$(0, 1)$$ and half of its time fully active in $$(1, 1)$$. The OFF–OFF and mixed $$(1, 0)$$ states are only visited transiently, on the way into this two-state attractor. Even this minimal recurrent Neo therefore exhibits a nontrivial equilibrium structure: sustained stochastic switching between a "semi-on" and a "fully-on" configuration, shaped jointly by feedback and local noise. This equilibrium behavior will later connect directly to macro-level notions such as stationary distributions over larger Neo populations and the emergence of stable computational motifs.

---

### 4.2.2 Canonical Micro-Motifs

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

---

## Appendix A: Additional Minimal Neo Structures

This appendix provides detailed analysis of additional minimal Neo configurations that complement the two-node recurrent Neo presented in Section 4.2.1.

### A.1 Zero-Node and Degenerate Cases

A zero-node Neo has no internal state. Formally, its state vector is empty:

$$V(t) = \varnothing.$$

There is only one possible configuration, which we call state 0. No Lex update is applied, because there are no nodes and therefore no activations to compute. The system can only emit a fixed output or some externally defined constant, and it cannot store any information about past inputs.

Because there is only one state, the internal dynamics form a trivial Markov chain with a single state.

#### Transition matrix

Let the state space be

$$\mathcal{S} = \{0\}.$$

The one-step transition matrix is

$$P = \begin{bmatrix} 1 \end{bmatrix},$$

meaning that if the system is in state 0 at time $$t$$, it remains in state 0 at time $$t+1$$ with probability 1.

#### Stationary distribution

The stationary distribution is a row vector

$$\pi = [\pi_0],$$

with normalization

$$\pi_0 = 1.$$

The stationarity condition

$$\pi P = \pi$$

expands to

$$[\pi_0] \begin{bmatrix} 1 \end{bmatrix} = [\pi_0],$$

which is satisfied for $$\pi_0 = 1$$. Thus the unique stationary distribution is

$$\boxed{\pi = [1].}$$

This confirms that a zero-node Neo has no representational capacity and its internal dynamics are trivial: there is a single state that is always occupied.

---

### A.2 Single-Node Neo

We now consider the smallest non-degenerate Neo: a single internal state node. This Neo can already pass through deterministic and stochastic regimes and store a single bit of memory. The output is always taken directly from the state node:

$$Y(t) = V(t).$$

We model Lex for a single node using a linear activation perturbed by symmetric noise. Let the input $$U(t) \in \{0,1\}$$ be fixed to a constant value $$u$$ so that the resulting Markov chain is time-homogeneous.

The activation is

$$a(t) = a_U\,U(t) + a_V\,V(t) + b + \alpha\,\eta(t),$$

where:

- $$a_U$$ is the weight from the external input,
- $$a_V$$ is the self-connection weight (memory term),
- $$b$$ is a bias,
- $$\alpha$$ scales the stochastic perturbation,
- $$\eta(t) \in \{-1, +1\}$$ is a Rademacher noise variable with

  $$\mathbb{P}(\eta(t) = +1) = \mathbb{P}(\eta(t) = -1) = \tfrac12.$$

The state update is

$$V(t+1) = H(a(t)),$$

where $$H(x) = 1$$ if $$x \ge 0$$ and $$0$$ otherwise. The output is simply

$$Y(t) = V(t).$$

To obtain a concrete Markov chain and show how the probabilities are derived, we fix the input to $$U(t) = 1$$ and choose specific parameter values.

#### Numerical Lex specification

Choose:

$$a_U = 1,\quad a_V = 1,\quad b = -0.7,\quad \alpha = 1.0,\quad U(t) = 1 \text{ for all } t.$$

Then the deterministic part of the activation is

$$s(V(t)) = a_U\,U(t) + a_V\,V(t) + b = 1\cdot 1 + 1\cdot V(t) - 0.7 = 0.3 + V(t).$$

So we have:

- If $$V(t) = 0$$, then

  $$s_0 = 0.3.$$

- If $$V(t) = 1$$, then

  $$s_1 = 1.3.$$

The full activation for each case is

$$a(t) = s(V(t)) + \alpha\,\eta(t) = s(V(t)) + 1.0 \cdot \eta(t).$$

We now compute the transition probabilities explicitly.

#### Computing transition probabilities

We want $$P(V(t+1) = 1 \mid V(t) = v)$$ for $$v \in \{0,1\}$$.

Because $$\eta(t) \in \{-1, +1\}$$ with equal probability, we can write:

$$P(V(t+1)=1 \mid V(t) = v) = P(H(a(t))=1 \mid V(t)=v) = P(a(t) \ge 0 \mid V(t)=v)$$

$$= P(s(v) + \eta(t) \ge 0) = \tfrac12 \mathbb{1}\{s(v) + 1 \ge 0\} + \tfrac12 \mathbb{1}\{s(v) - 1 \ge 0\},$$

where $$\mathbb{1}\{\cdot\}$$ is the indicator function.

We apply this to each state.

**Case 1: $$V(t) = 0$$.**

Here $$s_0 = 0.3$$. The two possible activations are:

$$a_+ = s_0 + 1 = 0.3 + 1 = 1.3,\quad a_- = s_0 - 1 = 0.3 - 1 = -0.7.$$

So:

- $$a_+ \ge 0 \Rightarrow H(a_+) = 1$$,
- $$a_- < 0 \Rightarrow H(a_-) = 0$$.

Thus:

$$P(V(t+1)=1 \mid V(t)=0) = \tfrac12 \cdot 1 + \tfrac12 \cdot 0 = \tfrac12.$$

Similarly,

$$P(V(t+1)=0 \mid V(t)=0) = 1 - \tfrac12 = \tfrac12.$$

**Case 2: $$V(t) = 1$$.**

Here $$s_1 = 1.3$$. The two possible activations are:

$$a_+ = s_1 + 1 = 1.3 + 1 = 2.3,\quad a_- = s_1 - 1 = 1.3 - 1 = 0.3.$$

Both are nonnegative, so:

- $$H(a_+) = 1$$,
- $$H(a_-) = 1$$.

Therefore:

$$P(V(t+1)=1 \mid V(t)=1) = \tfrac12 \cdot 1 + \tfrac12 \cdot 1 = 1,$$

and

$$P(V(t+1)=0 \mid V(t)=1) = 0.$$

#### Transition matrix

Order the states as $$[0, 1]$$. The transition matrix $$P^{(1)}$$ has entries

$$P^{(1)}_{ij} = P(V(t+1) = j \mid V(t) = i).$$

From the probabilities we derived:

- From state 0:

  $$P(0\to 0) = 0.5,\quad P(0\to 1) = 0.5.$$

- From state 1:

  $$P(1\to 0) = 0,\quad P(1\to 1) = 1.$$

Thus

$$P^{(1)} = \begin{bmatrix} 0.5 & 0.5 \\ 0   & 1 \end{bmatrix}.$$

#### Stationary distribution

Let the stationary distribution be

$$\pi = [\pi_0, \pi_1],$$

with

$$\pi_0 + \pi_1 = 1.$$

The stationarity condition is

$$\pi P^{(1)} = \pi.$$

Compute the left-hand side:

$$\pi P^{(1)} = [\pi_0, \pi_1] \begin{bmatrix} 0.5 & 0.5 \\ 0   & 1 \end{bmatrix} = [\pi_0 \cdot 0.5 + \pi_1 \cdot 0,\; \pi_0 \cdot 0.5 + \pi_1 \cdot 1] = [0.5\pi_0,\; 0.5\pi_0 + \pi_1].$$

Setting this equal to $$[\pi_0, \pi_1]$$ yields:

1. For the first component:

   $$0.5\pi_0 = \pi_0 \;\Rightarrow\; 0.5\pi_0 = 0 \;\Rightarrow\; \pi_0 = 0.$$

2. Normalization then forces:

   $$\pi_1 = 1.$$

So the unique stationary distribution is

$$\boxed{\pi = (0, 1).}$$

In words, under this Lex and fixed input, the single-node Neo eventually spends almost all its time in the state $$V=1$$: once it flips to 1 it never returns to 0. The stochasticity only affects the transient path from 0 to 1.

---

### A.3 Two-Node Neo: Feedforward Topology

We analyze a two-node feedforward motif where $$V_1$$ depends only on the external input $$U$$ and noise, and $$V_2$$ depends only on $$V_1$$ and noise.

Diagram:

```text
    U
    |
    v
 +-----+      +-----+
 | V1  | ---> | V2  |
 +-----+      +-----+
```

We fix the input to a constant value $$U(t) = u$$ to obtain a time-homogeneous Markov chain.

##### Lex specification

Node 1 activation:

$$a_1(t) = 1.0 \cdot U(t) - 0.2 + 0.7 \cdot \eta_1(t),$$

with $$\eta_1(t)\in\{-1,+1\}$$ and $$\mathbb{P}(\eta_1=\pm1)=\tfrac12$$.

Node 2 activation:

$$a_2(t) = 1.4 \cdot V_1(t) - 0.1 + 0.9 \cdot \eta_2(t),$$

with $$\eta_2(t)\in\{-1,+1\}$$ independent of $$\eta_1(t)$$.

The state updates are

$$V_1(t+1) = H(a_1(t)),\quad V_2(t+1) = H(a_2(t)).$$

##### Case u = 0

For node 1, the deterministic part is $$s_1 = -0.2$$, giving $$P(V_1'=1 \mid U=0) = 0.5$$.

For node 2: if $$V_1=0$$, $$P(V_2'=1)=0.5$$; if $$V_1=1$$, $$P(V_2'=1)=1$$.

The transition matrix is:

$$P^{FF}_{u=0} = \begin{bmatrix} 0.25 & 0.25 & 0.25 & 0.25 \\ 0.25 & 0.25 & 0.25 & 0.25 \\ 0    & 0.5  & 0    & 0.5  \\ 0    & 0.5  & 0    & 0.5 \end{bmatrix}.$$

The stationary distribution is:

$$\boxed{\pi^{FF}_{u=0} = \Big(\tfrac18, \tfrac38, \tfrac18, \tfrac38\Big).}$$

##### Case u = 1

Under $$U=1$$, $$P(V_1'=1) = 1$$. The transition matrix becomes:

$$P^{FF}_{u=1} = \begin{bmatrix} 0 & 0 & 0.5 & 0.5 \\ 0 & 0 & 0.5 & 0.5 \\ 0 & 0 & 0   & 1   \\ 0 & 0 & 0   & 1 \end{bmatrix}.$$

The stationary distribution is:

$$\boxed{\pi^{FF}_{u=1} = (0,0,0,1).}$$

---

### A.4 Two-Node Neo: Parallel Topology

Both nodes receive the same input but do not directly interact.

Diagram:

```text
          U
         / \
        v   v
     +-----+ +-----+
     | V1  | | V2  |
     +-----+ +-----+
```

For $$U(t)=0$$ with symmetric parameters, each node has $$P(V_i'=1) = 0.5$$ independently.

The transition matrix is:

$$P^{PAR}_{u=0} = \begin{bmatrix} 0.25 & 0.25 & 0.25 & 0.25 \\ 0.25 & 0.25 & 0.25 & 0.25 \\ 0.25 & 0.25 & 0.25 & 0.25 \\ 0.25 & 0.25 & 0.25 & 0.25 \end{bmatrix}.$$

The stationary distribution is:

$$\boxed{\pi^{PAR}_{u=0} = (0.25, 0.25, 0.25, 0.25).}$$

For $$U(t)=1$$, both nodes deterministically go to state 1:

$$\pi^{PAR}_{u=1} = (0,0,0,1).$$
