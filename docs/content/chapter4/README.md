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

With these foundations, the next subsections analyze zero-node, single-node, and two-node Neo structures in detail. Each case includes a numerical example, the complete derivation of transition probabilities, the full transition matrix, and the stationary distribution. These minimal Neos serve as the mathematical base cases for understanding how more complex Neo behaviors emerge from combinations of simple stochastic units.

---

### 4.2.1 Zero-Node and Degenerate Cases

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

### 4.2.2 Single-Node Neo

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

### 4.2.3 Two-Node Neo

We now consider the simplest interacting Neo: two binary state nodes

$$V(t) = (V_1(t), V_2(t)) \in \{0,1\}^2.$$

We will analyze three basic topologies:

1. Feedforward: $$V_1 \to V_2$$.
2. Parallel: both nodes driven independently by the same input.
3. Feedback: $$V_1 \leftrightarrow V_2$$.

In each case, we specify Lex for both nodes using simple numeric parameters and derive the full transition matrix over the four states, followed by the stationary distribution.

We order the joint states as:

$$1 \equiv (0,0),\quad 2 \equiv (0,1),\quad 3 \equiv (1,0),\quad 4 \equiv (1,1).$$

---

#### 4.2.3.A Feedforward (V1 → V2)

We first analyze a two-node feedforward motif where $$V_1$$ depends only on the external input $$U$$ and noise, and $$V_2$$ depends only on $$V_1$$ and noise. This already yields richer dynamics than the single-node case.

Diagram:

```text
    U
    |
    v
 +-----+      +-----+
 | V1  | ---> | V2  |
 +-----+      +-----+
```

We again fix the input to a constant value $$U(t) = u$$ to obtain a time-homogeneous Markov chain. The randomness then comes solely from internal noise.

##### Lex specification

Node 1 activation:

$$a_1(t) = 1.0 \cdot U(t) - 0.2 + 0.7 \cdot \eta_1(t),$$

with $$\eta_1(t)\in\{-1,+1\}$$ and $$\mathbb{P}(\eta_1=\pm1)=\tfrac12$$.

Node 2 activation:

$$a_2(t) = 1.4 \cdot V_1(t) - 0.1 + 0.9 \cdot \eta_2(t),$$

with $$\eta_2(t)\in\{-1,+1\}$$ independent of $$\eta_1(t)$$.

The state updates are

$$V_1(t+1) = H(a_1(t)),\quad V_2(t+1) = H(a_2(t)).$$

We will compute the transition matrix for two fixed inputs: $$u=0$$ and $$u=1$$.

---

##### Case u = 0: computing node-wise probabilities

Set $$U(t)=0$$.

For node 1, the deterministic part is:

$$s_1 = 1.0\cdot 0 - 0.2 = -0.2.$$

The two activations are:

$$a_{1,+} = s_1 + 0.7 = -0.2 + 0.7 = 0.5, \quad a_{1,-} = s_1 - 0.7 = -0.2 - 0.7 = -0.9.$$

So:

* $$H(a_{1,+}) = 1$$,
* $$H(a_{1,-}) = 0$$,

and

$$P(V_1(t+1)=1 \mid U=0) = \tfrac12\cdot 1 + \tfrac12\cdot 0 = 0.5.$$

Thus

$$P(V_1' = 1 \mid U=0) = 0.5,\quad P(V_1'=0 \mid U=0)=0.5.$$

For node 2, the deterministic part depends on $$V_1(t)$$:

$$s_2(V_1) = 1.4\cdot V_1 - 0.1.$$

If $$V_1(t)=0$$:

$$s_2(0) = -0.1,$$

so

$$a_{2,+} = -0.1 + 0.9 = 0.8,\quad a_{2,-} = -0.1 - 0.9 = -1.0.$$

Hence:

* $$H(a_{2,+})=1$$,
* $$H(a_{2,-})=0$$,

and

$$P(V_2(t+1) = 1 \mid V_1(t)=0) = \tfrac12.$$

If $$V_1(t)=1$$:

$$s_2(1) = 1.4 - 0.1 = 1.3,$$

so

$$a_{2,+} = 1.3 + 0.9 = 2.2,\quad a_{2,-} = 1.3 - 0.9 = 0.4.$$

Both are nonnegative, so

$$P(V_2(t+1) = 1 \mid V_1(t)=1) = 1.$$

In summary (for $$u=0$$):

$$P(V_1'=1) = 0.5,\quad P(V_1'=0) = 0.5,$$

$$P(V_2'=1 \mid V_1=0) = 0.5,\quad P(V_2'=1 \mid V_1=1) = 1.$$

We now build the 4-state transition matrix.

##### Transition probabilities for each joint state (u = 0)

Let $$X(t) = (V_1(t), V_2(t))$$. Because $$V_1'$$ depends only on $$U$$ and $$V_2'$$ depends only on $$V_1(t)$$ and noise, and noise for node 1 and 2 are independent, we have

$$P(X(t+1) = (v_1', v_2') \mid X(t) = (v_1, v_2), U=0) = P(V_1' = v_1' \mid U=0) \cdot P(V_2' = v_2' \mid V_1=v_1).$$

We compute row by row.

**Row 1: current state (0,0).**

Here $$V_1=0$$, but note that $$P(V_1' \mid U=0)$$ does not depend on the current state. We have:

$$P(V_1'=0)=0.5,\quad P(V_1'=1)=0.5.$$

For $$V_2'$$:

* If $$V_1=0$$, then $$P(V_2'=1)=0.5$$, $$P(V_2'=0)=0.5$$.

Therefore:

* $$P((0,0)\to(0,0)) = P(V_1'=0) \cdot P(V_2'=0\mid V_1=0) = 0.5 \cdot 0.5 = 0.25,$$
* $$P((0,0)\to(0,1)) = 0.5 \cdot 0.5 = 0.25,$$
* $$P((0,0)\to(1,0)) = P(V_1'=1) \cdot P(V_2'=0\mid V_1=0) = 0.5 \cdot 0.5 = 0.25,$$
* $$P((0,0)\to(1,1)) = 0.5 \cdot 0.5 = 0.25.$$

The row sums to 1.

**Row 2: current state (0,1).**

The current value of $$V_2$$ does not influence $$V_1'$$ or $$V_2'$$ (which depends on $$V_1$$, not $$V_2$$). So the same reasoning applies:

$$P((0,1)\to j) = P((0,0)\to j)$$

for each joint next state $$j$$. So the second row is identical to the first:

$$(0.25, 0.25, 0.25, 0.25).$$

**Row 3: current state (1,0).**

Now $$V_1=1$$. The distribution of $$V_1'$$ is still independent of the current state and remains

$$P(V_1'=0) = 0.5,\quad P(V_1'=1)=0.5.$$

However, $$V_2'$$ conditional probabilities change because they depend on $$V_1(t)$$, which is 1 here:

$$P(V_2'=1 \mid V_1=1) = 1,\quad P(V_2'=0\mid V_1=1)=0.$$

Thus:

* $$P((1,0)\to(0,0)) = P(V_1'=0) \cdot P(V_2'=0\mid V_1=1) = 0.5 \cdot 0 = 0,$$
* $$P((1,0)\to(0,1)) = 0.5 \cdot 1 = 0.5,$$
* $$P((1,0)\to(1,0)) = P(V_1'=1) \cdot P(V_2'=0\mid V_1=1) = 0.5 \cdot 0 = 0,$$
* $$P((1,0)\to(1,1)) = 0.5 \cdot 1 = 0.5.$$

So the third row is:

$$(0, 0.5, 0, 0.5).$$

**Row 4: current state (1,1).**

Same as row 3, because $$V_1=1$$ and $$V_2$$ is irrelevant to $$V_1'$$ and $$V_2'$$:

$$(0, 0.5, 0, 0.5).$$

##### Transition matrix (u = 0)

Collecting all rows:

$$P^{FF}_{u=0} = \begin{bmatrix} 0.25 & 0.25 & 0.25 & 0.25 \\ 0.25 & 0.25 & 0.25 & 0.25 \\ 0    & 0.5  & 0    & 0.5  \\ 0    & 0.5  & 0    & 0.5 \end{bmatrix}.$$

##### Stationary distribution (u = 0)

Let the stationary distribution be

$$\pi = (\pi_1, \pi_2, \pi_3, \pi_4),$$

with

$$\pi_1 + \pi_2 + \pi_3 + \pi_4 = 1.$$

By symmetry of rows (1 and 2 identical; 3 and 4 identical) and columns, it is natural to look for a solution with

$$\pi_1 = \pi_3 = a,\quad \pi_2 = \pi_4 = b,\quad a + b = \tfrac12.$$

We now impose stationarity on, say, $$\pi_1$$:

$$\pi_1' = \pi_1 = \sum_{i=1}^4 \pi_i P^{FF}_{u=0}(i,1) = \pi_1 \cdot 0.25 + \pi_2 \cdot 0.25 + \pi_3 \cdot 0 + \pi_4 \cdot 0.$$

Substitute $$\pi_1=a, \pi_2=b$$:

$$a = 0.25 a + 0.25 b.$$

Using the constraint $$a + b = 0.5$$, we solve:

$$a = 0.25 (a + b) = 0.25 \cdot 0.5 = 0.125 = \tfrac18.$$

Therefore

$$b = 0.5 - a = 0.5 - 0.125 = 0.375 = \tfrac38.$$

Thus

$$\boxed{\pi^{FF}_{u=0} = \Big(\tfrac18, \tfrac38, \tfrac18, \tfrac38\Big).}$$

---

##### Case u = 1

We now set $$U(t) = 1$$.

For node 1, deterministic part:

$$s_1 = 1.0\cdot 1 - 0.2 = 0.8.$$

Then:

$$a_{1,+} = 0.8 + 0.7 = 1.5,\quad a_{1,-} = 0.8 - 0.7 = 0.1.$$

Both nonnegative, so

$$P(V_1'=1 \mid U=1) = 1.$$

For node 2, deterministic part:

$$s_2(V_1) = 1.4 V_1 - 0.1.$$

As before, if $$V_1=0$$, $$P(V_2'=1)=0.5$$, and if $$V_1=1$$, $$P(V_2'=1)=1$$. However, under $$U=1$$, $$V_1'$$ is always 1, so after one step the system will behave as if $$V_1(t)=1$$ at all future times.

To keep the Markov chain defined in terms of current state, we again use:

$$P(X(t+1) = (v_1', v_2') \mid X(t) = (v_1, v_2), U=1) = P(V_1'=v_1' \mid U=1) P(V_2'=v_2' \mid V_1=v_1).$$

But now $$P(V_1'=0)=0$$ and $$P(V_1'=1)=1$$, so transitions can only go to states with $$V_1'=1$$ (i.e., states 3 or 4).

Carrying through the same logic as before yields:

$$P^{FF}_{u=1} = \begin{bmatrix} 0 & 0 & 0.5 & 0.5 \\ 0 & 0 & 0.5 & 0.5 \\ 0 & 0 & 0   & 1   \\ 0 & 0 & 0   & 1 \end{bmatrix}.$$

The last state (1,1) is absorbing, and all other states have a nonzero probability of eventually reaching it. Thus the unique stationary distribution is:

$$\boxed{\pi^{FF}_{u=1} = (0,0,0,1).}$$

---

#### 4.2.3.B Parallel (U → V1 and U → V2)

Now we consider a parallel topology where both nodes receive the same input but do not directly interact. This is the smallest multi-bit output that can still be treated as two independent single-node Neos.

Diagram:

```text
          U
         / \
        v   v
     +-----+ +-----+
     | V1  | | V2  |
     +-----+ +-----+
```

Assume both nodes obey the same single-node Lex rule used in Section 4.2.2, and that their noise processes are independent. For a fixed input $$u$$, each node has the same transition probabilities as the single-node case, and the joint transition matrix is the Kronecker product of the single-node matrix with itself.

For simplicity, consider $$U(t)=0$$ with the single-node parameters chosen so that

$$P(V_i'=1 \mid U=0) = 0.5,\quad i \in \{1,2\}.$$

Then each node at each step is an independent Bernoulli(0.5) random variable, independent of its previous state. The joint distribution over the pair is uniform over the four states.

Thus for any current state,

$$P(X(t+1) = (v_1', v_2')) = 0.25$$

for each of the four configurations.

The transition matrix is therefore:

$$P^{PAR}_{u=0} = \begin{bmatrix} 0.25 & 0.25 & 0.25 & 0.25 \\ 0.25 & 0.25 & 0.25 & 0.25 \\ 0.25 & 0.25 & 0.25 & 0.25 \\ 0.25 & 0.25 & 0.25 & 0.25 \end{bmatrix}.$$

The stationary distribution $$\pi$$ must satisfy $$\pi P^{PAR}_{u=0}=\pi$$. Because every row is identical and uniform, the unique normalized solution is

$$\boxed{\pi^{PAR}_{u=0} = (0.25, 0.25, 0.25, 0.25).}$$

The parallel 2-node Neo under symmetric stochastic input is therefore a uniform random generator over the four joint states.

For $$U(t)=1$$ and our earlier single-node parameters, each node deterministically goes to state 1. Hence (1,1) is absorbing, and the stationary distribution is again

$$\pi^{PAR}_{u=1} = (0,0,0,1).$$

---

#### 4.2.3.C Feedback (V1 ↔ V2)

Finally, we consider a feedback topology where each node depends on the other's previous state. This is the smallest genuine recurrent Neo and can already exhibit nontrivial stochastic dynamics, including concentration on particular states.

Diagram:

```text
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

We again fix $$U(t)=u$$ and choose explicit parameters.

##### Lex specification

Node 1:

$$a_1(t) = 0.7 \cdot U(t) + 1.0 \cdot V_2(t) - 0.5 + 0.6 \cdot \eta_1(t).$$

Node 2:

$$a_2(t) = -0.4 \cdot U(t) + 1.5 \cdot V_1(t) - 0.2 + 0.7 \cdot \eta_2(t).$$

Both noise variables $$\eta_1,\eta_2$$ take values $$\{-1,+1\}$$ with probability 0.5 and are independent.

Updates:

$$V_1(t+1) = H(a_1(t)),\quad V_2(t+1) = H(a_2(t)).$$

We again consider two cases: $$u=0$$ and $$u=1$$.

---

##### Case u = 0

Set $$U(t)=0$$. The deterministic parts are:

$$s_1(V_2) = 0.7\cdot 0 + 1.0 V_2 - 0.5 = V_2 - 0.5,$$

$$s_2(V_1) = -0.4\cdot 0 + 1.5 V_1 - 0.2 = 1.5 V_1 - 0.2.$$

We compute node-wise probabilities.

**Node 1:**

If $$V_2=0$$:

$$s_1(0) = -0.5,$$

so

$$a_{1,+} = -0.5 + 0.6 = 0.1,\quad a_{1,-} = -0.5 - 0.6 = -1.1.$$

Thus

$$P(V_1'=1 \mid V_2=0, U=0) = \tfrac12 \cdot 1 + \tfrac12 \cdot 0 = 0.5.$$

If $$V_2=1$$:

$$s_1(1) = 1 - 0.5 = 0.5,$$

so

$$a_{1,+} = 0.5 + 0.6 = 1.1,\quad a_{1,-} = 0.5 - 0.6 = -0.1.$$

Again,

$$P(V_1'=1 \mid V_2=1,U=0) = 0.5.$$

So for $$u=0$$, node 1 is symmetric:

$$P(V_1'=1 \mid V_2=0) = P(V_1'=1 \mid V_2=1) = 0.5.$$

**Node 2:**

If $$V_1=0$$:

$$s_2(0) = -0.2,$$

$$a_{2,+} = -0.2 + 0.7 = 0.5,\quad a_{2,-} = -0.2 - 0.7 = -0.9.$$

So

$$P(V_2'=1 \mid V_1=0,U=0) = 0.5.$$

If $$V_1=1$$:

$$s_2(1) = 1.5 - 0.2 = 1.3,$$

$$a_{2,+} = 1.3 + 0.7 = 2.0,\quad a_{2,-} = 1.3 - 0.7 = 0.6.$$

Both nonnegative, so

$$P(V_2'=1 \mid V_1=1,U=0) = 1.$$

We now build the transition matrix.

**State (0,0):** here $$V_1=0,V_2=0$$.

* Node1: $$P(V_1'=1 \mid V_2=0) = 0.5$$, $$P(V_1'=0)=0.5$$.
* Node2: $$P(V_2'=1 \mid V_1=0) = 0.5$$, $$P(V_2'=0)=0.5$$.

Joint transitions:

* $$P((0,0)\to(0,0)) = 0.5 \cdot 0.5 = 0.25,$$
* $$P((0,0)\to(0,1)) = 0.5 \cdot 0.5 = 0.25,$$
* $$P((0,0)\to(1,0)) = 0.5 \cdot 0.5 = 0.25,$$
* $$P((0,0)\to(1,1)) = 0.5 \cdot 0.5 = 0.25.$$

**State (0,1):** $$V_1=0,V_2=1$$.

* Node1: $$P(V_1'=1 \mid V_2=1)=0.5$$, $$P(V_1'=0)=0.5$$.
* Node2: $$P(V_2'=1 \mid V_1=0)=0.5$$, $$P(V_2'=0)=0.5$$.

Thus the row is identical to state (0,0):

$$(0.25,0.25,0.25,0.25).$$

**State (1,0):** $$V_1=1,V_2=0$$.

* Node1: $$P(V_1'=1 \mid V_2=0)=0.5$$.
* Node2: $$P(V_2'=1 \mid V_1=1)=1$$, $$P(V_2'=0)=0$$.

So:

* $$P((1,0)\to(0,0)) = P(V_1'=0) \cdot P(V_2'=0\mid V_1=1) = 0.5\cdot 0 = 0,$$
* $$P((1,0)\to(0,1)) = 0.5\cdot 1 = 0.5,$$
* $$P((1,0)\to(1,0)) = 0.5\cdot 0 = 0,$$
* $$P((1,0)\to(1,1)) = 0.5\cdot 1 = 0.5.$$

**State (1,1):** $$V_1=1,V_2=1$$.

* Node1: $$P(V_1'=1 \mid V_2=1)=0.5$$.
* Node2: $$P(V_2'=1 \mid V_1=1)=1$$.

So again:

$$(1,1)\to(0,0) = 0,\quad (1,1)\to(0,1) = 0.5,\quad (1,1)\to(1,0) = 0,\quad (1,1)\to(1,1) = 0.5.$$

Collecting these rows, we obtain:

$$P^{FB}_{u=0} = \begin{bmatrix} 0.25 & 0.25 & 0.25 & 0.25 \\ 0.25 & 0.25 & 0.25 & 0.25 \\ 0    & 0.5  & 0    & 0.5  \\ 0    & 0.5  & 0    & 0.5 \end{bmatrix}.$$

This matrix is identical to the feedforward case with $$u=0$$, so the stationary distribution is again:

$$\boxed{\pi^{FB}_{u=0} = \Big(\tfrac18, \tfrac38, \tfrac18, \tfrac38\Big).}$$

##### Case u = 1 (feedback)

With $$U=1$$, the deterministic parts change, and the Markov chain becomes more biased toward the state (1,1). A similar step-by-step analysis (omitted here to avoid redundancy) yields:

$$P^{FB}_{u=1} = \begin{bmatrix} 0.25 & 0.25 & 0.25 & 0.25 \\ 0    & 0    & 0.5  & 0.5  \\ 0    & 0.5  & 0    & 0.5  \\ 0    & 0    & 0    & 1 \end{bmatrix}.$$

The state (1,1) is absorbing and is reachable from every other state under the dynamics, so the unique stationary distribution is

$$\boxed{\pi^{FB}_{u=1} = (0,0,0,1).}$$

This two-node feedback Neo therefore converges, under this Lex choice, to a fully "activated" state in the long run.

---

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
