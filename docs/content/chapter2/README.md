# Chapter 2 — Neosis Axioms and Formal Model

## 2.1 Primitive Ingredients and State

Neosis is defined on top of a small collection of primitive ingredients that will be reused throughout the chapter. In this section, the goal is not to describe the full internal structure of a Neo, but to fix the basic objects and types—time, binary state, energy, and continuous parameters—that later sections will assemble into a complete formal model.

### 2.1.1 Time

All dynamics unfold in discrete time. We index ticks by
$$t \in \mathbb{N} = \{0,1,2,\dots\}$$,
with $$t = 0$$ denoting the initial configuration of the system. Each application of the update rules (perception, internal computation, reward, and mutation) advances the system from tick $$t$$ to tick $$t+1$$. Throughout the chapter, we will describe the behavior of Neos and the NeoVerse by specifying how relevant quantities change as a function of this tick index.

### 2.1.2 Binary State Substrate

The underlying state substrate of Neosis is binary. We write $$\mathbb{B} = \{0,1\}$$ for individual bits, and $$\mathbb{B}^n$$ for length-$$n$$ bit vectors. At any tick $$t$$, the internal memory of a Neo, its perceptual input, and its output will all be represented as elements of $$\mathbb{B}^n$$ for some finite $$n$$. The dimensionality $$n$$ is not fixed once and for all: it may change over time as the Neo gains or loses nodes through structural mutation. This choice keeps the local state space simple, while still allowing the overall system to grow in representational capacity.

### 2.1.3 Energy (Nex)

Each Neo maintains an energy budget, called Nex, which constrains its computation and evolution. At tick $$t$$, the energy of a given Neo is denoted by
$$
N_t \in \mathbb{R}_{\ge 0}.
$$
Running computations and performing structural mutations both consume energy, while successful prediction of the NeoVerse yields energy in the form of rewards (Sparks). All such costs and rewards are measured in the same units as Nex, so that energy evolves by simple additive updates of the form
$$
N_{t+1} = N_t + \text{(reward at } t\text{)} - \text{(cost at } t\text{)}.
$$
Once $$N_t$$ reaches zero, the Neo becomes inert: it can no longer perform internal computation or apply mutations, and its trajectory effectively terminates.

### 2.1.4 Continuous Parameters and Discrete Structure

A central modeling choice in Neosis is to separate *structure* from *parameters*. The structure of a Neo—its set of nodes, edges, and connectivity pattern—will be discrete and graph-like. However, each structural unit carries continuous parameters. For node $$i$$, we write
$$
\theta_i \in \mathbb{R}^{k_i},
$$
where $$k_i$$ is the parameter dimensionality associated with that node. These parameters control the local computation performed at the node (for example, weights, thresholds, or other coefficients), and they may change over time through learning mechanisms or mutation.

This separation between discrete structure (which nodes exist and how they are connected) and continuous parameters $$\theta_i$$ (how each node computes) is deliberate. It allows Neos to evolve by changing their topology in a combinatorial way, while still supporting rich, smooth families of local computations at each node. Later sections will make this distinction explicit when we define the internal graph of a Neo and the node-local update functions.

### 2.1.5 Global State at Tick $$t$$

At each tick $$t$$, we conceptually distinguish between the internal state of a Neo and the state of the surrounding world. We write
$$
\text{World}_t
$$
for the (possibly high-dimensional) state of the NeoVerse at tick $$t$$, and
$$
\text{Neo}_t
$$
for the complete internal state of a single Neo at the same tick, including its binary memory, graph structure, parameters, and energy. In this chapter we will focus on formalizing $$\text{Neo}_t$$; the NeoVerse state $$\text{World}_t$$ will be treated abstractly and will be accessed only through a projection function introduced in Section 2.2.

## 2.2 The NeoVerse and Perception

Neos do not exist in isolation. They operate inside an external world, called the NeoVerse, whose dynamics generate the signals that Neos attempt to predict. In this section we keep the NeoVerse deliberately abstract. The aim is not to model the entire environment in detail, but to specify how it interfaces with a Neo through perception.

At each tick $$t$$, the NeoVerse has a state
$$
\text{World}_t,
$$
which may be arbitrarily complex and high-dimensional. We do not constrain how $$\text{World}_t$$ evolves over time; it may follow a deterministic or stochastic rule, and it may or may not depend on the past behavior of Neos. For the purposes of this chapter, it is sufficient to regard $$\{\text{World}_t\}_{t \ge 0}$$ as an exogenous process that generates the raw conditions under which Neos must operate.

A Neo does not have direct access to $$\text{World}_t$$. Instead, it perceives only a projection of the NeoVerse through a perceptual interface. Formally, we introduce a projection function
$$
\Phi_t : \text{World}_t \longrightarrow \mathbb{B}^{m_t},
$$
and define the perceptual input at tick $$t$$ as
$$
\mathbf{U}_t = \Phi_t(\text{World}_t) \in \mathbb{B}^{m_t}.
$$
The dimensionality $$m_t$$ represents the number of binary channels the Neo can currently observe. This dimensionality is not fixed: as the Neo gains or loses input nodes through structural mutation, its perceptual capacity can change, and the corresponding projection $$\Phi_t$$ can be updated to match.

In the simplest cases, $$\mathbf{U}_t$$ may consist of a single bit, expressing a minimal signal about the NeoVerse. More generally, $$\mathbf{U}_t$$ can be a vector of bits encoding multiple aspects of $$\text{World}_t$$. The exact semantics of each bit are not specified at this level; they depend on the particular environment and experimental setup. What matters for the formal model is that all percepts are binary vectors, and that perception is always mediated by some projection $$\Phi_t$$ from $$\text{World}_t$$ into the Neo's current input space.

This view makes the Neo's situation explicitly partially observable. The Neo must form internal representations and predictions on the basis of $$\mathbf{U}_t$$ rather than on the full underlying state $$\text{World}_t$$. In later sections, we will define the output $$\mathbf{Y}_t$$ of a Neo as a prediction about future percepts $$\mathbf{U}_{t+1}$$, and we will use the accuracy of these predictions to determine the Neo's energy gain or loss.

## 2.3 The Neo: Internal Structure

We now turn from the external NeoVerse to the internal organization of a Neo. At a high level, the state of a single Neo at tick $$t$$ consists of two coupled subsystems:

- **Lio**, the Learner, which carries the Neo’s computational graph, internal memory, parameters, and input–output interface.
- **Evo**, the Evolver, which controls how the structure and parameters of Lio change over time.

For the purposes of this chapter, we focus on specifying the static structure of these subsystems at a given tick $$t$$. The dynamics that update them from $$t$$ to $$t+1$$ will be introduced in later sections.

We write the overall internal state of a Neo at tick $$t$$ as
$$
\text{Neo}_t = (\text{Lio}_t,\ \text{Evo}_t,\ N_t),
$$
where $$N_t$$ is the energy (Nex) introduced in Section 2.1.

### 2.3.1 Lio as an Evolving Binary Graph

Lio contains all components directly involved in perception, internal computation, and prediction. At tick $$t$$, we represent it as
$$
\text{Lio}_t = (\mathbf{V}_t,\ G_t,\ \Theta_t,\ \mathbf{U}_t,\ O_t),
$$

The vector $$\mathbf{V}_t$$ is the internal binary state (or memory) of the Neo:
$$
\mathbf{V}_t \in \mathbb{B}^{n_t},
$$
where $$n_t$$ is the number of internal nodes at tick $$t$$. Each coordinate $$\mathbf{V}_t[i]$$ corresponds to the state of a single node. We will use indices
$$
i \in \{1,\dots,n_t\}
$$
to refer to nodes, so there is no separate symbol for the node set.

The graph structure is captured by
$$
G_t = E_t,
$$
where $$E_t \subseteq \{1,\dots,n_t\} \times \{1,\dots,n_t\}$$ is the set of directed edges between nodes. We do not impose any topological restriction: $$E_t$$ may describe a feedforward, recurrent, or cyclic graph. This flexibility allows the Neo to evolve arbitrary computational motifs, including those that resemble neural networks, finite-state machines, or more complex dynamical systems.

Each node $$i \in \{1,\dots,n_t\}$$ is associated with a continuous parameter vector
$$
\theta_i \in \mathbb{R}^{k_i},
$$
which determines how that node processes its inputs. We collect all node parameters at tick $$t$$ into
$$
\Theta_t = \{\theta_i : i = 1,\dots,n_t\}.
$$
These parameters will be used in Section 2.4 to define the node-local update rules that map incoming binary signals to new node states.

The interface between Lio and the NeoVerse is given by the input vector
$$
\mathbf{U}_t \in \mathbb{B}^{m_t}.
$$
The input $$\mathbf{U}_t$$ is the percept at tick $$t$$ defined by the projection in Section 2.2. The output $$\mathbf{Y}_t$$ is defined as a direct readout of the internal state at the output indices:
$$
\mathbf{Y}_t = \mathbf{V}_t[O_t] \in \mathbb{B}^{p_t},
$$
where $$O_t$$ is the set of output node indices stored in $$\text{Lio}_t$$. Since $$\mathbf{Y}_t$$ is always a direct readout of $$\mathbf{V}_t$$ at indices $$O_t$$, it carries no independent state beyond what is already encoded in $$\mathbf{V}_t$$ and $$O_t$$. The dimensions $$m_t$$ and $$p_t$$ may change over time as the Neo gains or loses input and output nodes through structural mutation.

In summary, Lio at tick $$t$$ is an evolving binary graph with continuous parameters, equipped with a binary input interface. The pair $$(E_t,\ \Theta_t)$$ specifies *what* computational structure exists, while $$(\mathbf{V}_t,\ \mathbf{U}_t)$$ specifies the current binary activity flowing through that structure. The output $$\mathbf{Y}_t$$ is derived from $$\mathbf{V}_t$$ via the output index set $$O_t$$.

### 2.3.2 Evo as a Meta-Level Mutation Controller

Evo operates at a meta level: it does not directly process percepts from the NeoVerse, but instead governs how Lio’s structure and parameters change over time. At tick $$t$$, we keep Evo abstract and write
$$
\text{Evo}_t = (\Psi_t,\ \Xi_t),
$$
where $$\Psi_t$$ denotes any internal variables Evo maintains (for example, mutation rates or exploration preferences), and $$\Xi_t$$ denotes a mutation policy.

Conceptually, the mutation policy $$\Xi_t$$ is a rule that can inspect the current state of the Neo and propose structural or parametric changes to Lio. In later sections, these changes will be formalized as mutation primitives (adding or removing nodes and edges, or perturbing parameters) with associated energy costs. For the present chapter, it is enough to note that Evo:

- has access to $$\text{Lio}_t$$ and $$N_t$$,
- can decide which mutations to attempt at each tick, and
- must respect the available energy when doing so.

This separation between Lio (which computes and predicts) and Evo (which decides how Lio itself should change) is central to Neosis. It mirrors the distinction, in biological systems, between fast neural dynamics and slower evolutionary or developmental processes that shape the underlying circuitry.

### 2.4.1 Node Inputs

At tick $$t$$, the internal state of the Neo is
$$
\mathbf{V}_t \in \mathbb{B}^{n_t},
$$
and the current percept is
$$
\mathbf{U}_t \in \mathbb{B}^{m_t}.
$$

The directed edge set $$E_t \subseteq \{1,\dots,n_t\} \times \{1,\dots,n_t\}$$ specifies how internal nodes read from one another. To allow nodes to also depend on perceptual inputs, we conceptually extend the set of possible inputs by treating components of $$\mathbf{U}_t$$ as additional sources.

For each node index $$i \in \{1,\dots,n_t\}$$, we define a finite index set
$$
\mathcal{I}_t(i) \subseteq \{1,\dots,n_t\} \cup \{\text{input indices}\},
$$
which lists the internal and input coordinates that feed into node $$i$$ at tick $$t$$. From this set we form an input vector
$$
\mathbf{z}_i(t) \in \mathbb{B}^{k_i},
$$
by collecting the corresponding bits from $$\mathbf{V}_t$$ and $$\mathbf{U}_t$$ in a fixed order, where $$k_i = |\mathcal{I}_t(i)|$$. As before, $$k_i$$ may change over time as edges or inputs are added or removed.

In addition to these deterministic inputs, each node also receives a stochastic binary input
$$
\eta_i(t) \sim \text{Bernoulli}(0.5),
$$
independent across nodes and ticks unless otherwise specified. This random bit allows local computations to be intrinsically stochastic even when $$\mathbf{V}_t$$ and $$\mathbf{U}_t$$ are fixed.

### 2.4.2 Parametric Local Update Rule (Stochastic Lex)

Each node $$i$$ carries a continuous parameter vector
$$
\theta_i \in \mathbb{R}^{k_i + 2},
$$
which we interpret as a concatenation of weights and a bias:
$$
\theta_i = (w_i, \alpha_i, b_i),
$$
where
$$
w_i \in \mathbb{R}^{k_i}, \qquad \alpha_i \in \mathbb{R}, \qquad b_i \in \mathbb{R}.
$$

Given the binary input vector $$\mathbf{z}_i(t) \in \mathbb{B}^{k_i}$$ and the stochastic bit $$\eta_i(t) \in \mathbb{B}$$, the node first computes a real-valued activation
$$
a_i(t) = w_i^\top \mathbf{z}_i(t) + \alpha_i\, \eta_i(t) + b_i,
$$
and then applies a threshold to obtain the new binary state:
$$
\mathbf{V}_{t+1}[i]
= \text{Lex}_i\big(\mathbf{z}_i(t), \eta_i(t), \theta_i\big)
= H\big(a_i(t)\big),
$$
with the Heaviside step function
$$
H(x) =
\begin{cases}
1, & x \ge 0,\\
0, & x < 0.
\end{cases}
$$

This definition preserves the properties we want:

- **Locality**: each update depends only on $$\mathbf{z}_i(t)$$, $$\eta_i(t)$$, and $$\theta_i$$.  
- **Binary state**: outputs stay in $$\mathbb{B}$$.  
- **Stochasticity**: even with fixed $$\mathbf{V}_t$$ and $$\mathbf{U}_t$$, the next state can vary due to $$\eta_i(t)$$.  
- **Structural robustness**: when $$k_i$$ changes, we only resize $$w_i$$ and the construction of $$\mathbf{z}_i(t)$$; $$\alpha_i$$ and $$b_i$$ remain single scalars.

Snapshot semantics remain as before: all nodes read $$\mathbf{V}_t$$, $$\mathbf{U}_t$$, and their own $$\eta_i(t)$$ at the beginning of tick $$t$$, then update in parallel to produce $$\mathbf{V}_{t+1}$$.

## 2.5 Mutation Primitives and Structural Updates

A defining property of a Neo is that its internal structure is not fixed. Both the topology of
its computational graph and the interpretation of its outputs may change over time through
discrete mutation events. These mutations are proposed by Evo's mutation policy $$\Xi_t$$
and applied during the Mutation Phase of each Cycle, subject to available energy.

We introduce a unified set of mutation primitives:

$$
A_{\text{mut}}
=
\{
\texttt{node},\;
\texttt{edge},\;
\texttt{param}^f,\;
\texttt{output}
\},
$$

where each primitive includes multiple subtypes (addition, removal, or reassignment)
defined below. Each mutation type $$a \in A_{\text{mut}}$$ has an associated energy cost
$$C_{\text{mut}}(a) \ge 0$$.

All mutations operate locally on the tuple
$$
(V_t, E_t, \Theta_t, U_t, O_t),
$$
and produce an updated structure consistent with the rules of the Neo's internal graph.

### 2.5.1 Node Mutation (node)

Node mutations modify the number of internal nodes. A node mutation consists of either
adding a new node or removing an existing one.

#### Node Addition (node$$^+$$)

A node-addition mutation introduces a new internal node and increases the dimensionality
of the state vector from $$n_t$$ to $$n_t+1$$.
Formally,

$$
V'_t \in \mathbb{B}^{n_t+1}, \qquad
\Theta'_t = \Theta_t \cup \{\theta_{n_t+1}\},
$$

where $$V'_t[n_t+1]$$ is initialized to 0 and the new parameter vector $$\theta_{n_t+1}$$ is drawn
from an initialization distribution over $$\mathbb{R}^{k_{n_t+1}+2}$$.

Optionally, Evo may introduce new edges involving the new node:
$$
E'_t = E_t \cup E_{\text{new}}.
$$

All index sets and parameter vectors are resized accordingly.

#### Node Removal (node$$^-$$)

A node-removal mutation selects an index $$i \in \{1,\dots,n_t\}$$ and deletes it. The
updated dimensionality becomes $$n'_t = n_t - 1$$. All edges incident to $$i$$ are removed:

$$
E'_t = \{ (j,k) \in E_t : j \neq i,\; k \neq i \}.
$$

The corresponding state coordinate and parameter vector are removed, and remaining node
indices are re-labeled to maintain a contiguous index set. If $$i \in O_t$$, it is also removed
from the output set.

Node removal may disconnect the graph; the result is still considered valid.

### 2.5.2 Edge Mutation (edge)

Edge mutations change information flow by adding or removing directed edges.

#### Edge Addition (edge$$^+$$)

Select a pair $$(j,k)$$ with $$j \neq k$$. The edge is added:

$$
E'_t = E_t \cup \{(j,k)\}.
$$

This increases the input dimensionality of node $$k$$ by one, requiring expansion of its weight
vector $$w_k$$ by appending a new weight drawn from an initialization distribution.

#### Edge Removal (edge$$^-$$)

Select an existing edge $$(j,k) \in E_t$$ and delete it:

$$
E'_t = E_t \setminus \{(j,k)\}.
$$

The corresponding coordinate is removed from $$w_k$$, decreasing its input dimensionality.

### 2.5.3 Parameter Perturbation (param$$^f$$)

A parameter-perturbation mutation updates the continuous parameters of a single node
without altering the graph structure. For a selected node $$i$$:

$$
\theta_i \leftarrow \theta_i + \Delta_i,
$$

where $$\Delta_i$$ is drawn from a zero-mean perturbation distribution on
$$\mathbb{R}^{k_i+2}$$. All other nodes and edges remain unchanged.

This primitive enables exploration of local computational behaviors.

### 2.5.4 Output Mutation (output)

Output mutations allow the Neo to change which internal nodes contribute to its prediction
vector $$\mathbf{Y}_t = \mathbf{V}_t[O_t]$$. The output index set at tick $$t$$ is

$$
O_t = \{o_1, \dots, o_{p_t}\} \subseteq \{1,\dots,n_t\}.
$$

We introduce two subtypes.

#### Output Addition (output$$^+$$)

Select a node index $$i \in \{1,\dots,n_t\}$$ with $$i \notin O_t$$ and add it to the output set:

$$
O_{t+1} = O_t \cup \{i\}.
$$

This increases the output dimensionality $$p_t \to p_{t+1} = p_t + 1$$.

#### Output Removal (output$$^-$$)

Select $$i \in O_t$$ and remove it:

$$
O_{t+1} = O_t \setminus \{i\},
$$

reducing the output dimensionality $$p_t \to p_{t+1} = p_t - 1$$.

Output mutations allow the Neo to evolve its prediction interface, enabling specialization,
pruning, and reallocation of computational resources.

---

Together, the unified mutation set
$$
A_{\text{mut}} = \{
\texttt{node}^+, \texttt{node}^-,
\texttt{edge}^+, \texttt{edge}^-,
\texttt{param}^f,
\texttt{output}^+, \texttt{output}^- \}
$$
provides a minimal but expressive basis for evolving both the topology and computation of
Lio. By associating each primitive with an energy cost and constraining mutations to be
affordable at tick $$t$$, Evo must balance exploration against the Neo's available energy,
embedding evolutionary pressure directly into the organism's survival dynamics.

## 2.6 The Cycle: Operational Semantics

We now describe how a Neo evolves from tick $$t$$ to tick $$t+1$$. The Cycle specifies the order in which perception, internal computation, reward, energy update, and mutation occur. All quantities are understood to be conditioned on the current internal state
$$
\text{Neo}_t = (\text{Lio}_t,\ \text{Evo}_t,\ N_t)
$$
and the external world state $$\text{World}_t$$.

For readability, we keep the description at a single-Neo level; in later chapters, populations of Neos will be handled by applying the same rules to each individual.

### 2.6.1 Perception

At the beginning of tick $$t$$, the Neo perceives the NeoVerse through the projection function introduced in Section 2.2. The world is in state $$\text{World}_t$$, and the percept is
$$
\mathbf{U}_t = \Phi_t(\text{World}_t) \in \mathbb{B}^{m_t}.
$$

This value is written into Lio's input component, so that
$$
\text{Lio}_t = (\mathbf{V}_t,\ E_t,\ \Theta_t,\ \mathbf{U}_t,\ O_t),
$$
with $$\mathbf{U}_t$$ matching the current projection of the NeoVerse.

### 2.6.2 Internal Computation and Output

Given $$\mathbf{V}_t$$, $$\mathbf{U}_t$$, the edge set $$E_t$$, and parameters $$\Theta_t$$, Lio updates its internal state and produces an output.

For each node index $$i = 1,\dots,n_t$$:

1. Construct the input index set $$\mathcal{I}_t(i)$$ and the corresponding binary vector
   $$
   \mathbf{z}_i(t) \in \mathbb{B}^{k_i}
   $$
   by reading from $$\mathbf{V}_t$$ and $$\mathbf{U}_t$$.

2. Sample a stochastic bit
   $$
   \eta_i(t) \sim \text{Bernoulli}(0.5).
   $$

3. Compute the activation using the node’s parameters $$\theta_i = (w_i, \alpha_i, b_i)$$:
   $$
   a_i(t) = w_i^\top \mathbf{z}_i(t) + \alpha_i\, \eta_i(t) + b_i.
   $$

4. Update the node’s binary state using the local rule
   $$
   \mathbf{V}_{t+1}[i]
     = \text{Lex}_i\big(\mathbf{z}_i(t), \eta_i(t), \theta_i\big)
     = H\big(a_i(t)\big),
   $$
   where $$H(\cdot)$$ is the Heaviside step function.

We adopt snapshot semantics: all nodes read $$\mathbf{V}_t$$ and $$\mathbf{U}_t$$ and their own $$\eta_i(t)$$ at the start of tick $$t$$, and all updates to $$\mathbf{V}_{t+1}$$ are conceptually applied in parallel.

The output vector $$\mathbf{Y}_t \in \mathbb{B}^{p_t}$$ is defined as a direct readout of the internal state at the output indices:
$$
\mathbf{Y}_t = \mathbf{V}_t[O_t],
$$

Thus at tick $$t$$, the Neo produces a prediction $$\mathbf{Y}_t$$ based on its internal state and the current percept, while its internal memory is updated to $$\mathbf{V}_{t+1}$$ for use at the next tick.

### 2.6.3 Running Cost and Energy Deduction

Executing the internal computation incurs a running cost that depends on the size of the Neo’s active structure. We introduce a cost function
$$
C_{\text{run}} : \mathbb{N}^2 \to \mathbb{R}_{\ge 0},
$$
which may, for example, depend on the number of internal nodes and input bits. A simple choice is
$$
C_{\text{run}}(n_t, m_t)
  = c_{\text{node}}\, n_t + c_{\text{in}}\, m_t,
$$
with non-negative constants $$c_{\text{node}}, c_{\text{in}}$$.
$$
N_t' = N_t - C_{\text{run}}(n_t, m_t).
$$

If $$N_t' \le 0$$, the Neo has exhausted its energy and becomes inert; its trajectory terminates, and no further computation or mutation occurs.

### 2.6.4 Reward (Spark) and Energy Update

After Lio has produced $$\mathbf{Y}_t$$ and updated its internal state, the NeoVerse advances to the next tick. The world transitions to $$\text{World}_{t+1}$$ according to its own dynamics, and the Neo receives a new percept
$$
\mathbf{U}_{t+1} = \Phi_{t+1}(\text{World}_{t+1}).
$$

The quality of the Neo’s prediction is assessed by a reward function
$$
R : \mathbb{B}^{p_t} \times \mathbb{B}^{m_{t+1}} \to \mathbb{R},
$$
which compares $$\mathbf{Y}_t$$ to $$\mathbf{U}_{t+1}$$. We write the resulting reward (Spark) as
$$
S_t = R(\mathbf{Y}_t,\ \mathbf{U}_{t+1}).
$$
The Neo’s energy is then updated to
$$
N_t'' = N_t' + S_t.
$$

The specific form of $$R$$ can vary with the environment; in many examples it will reward accurate prediction of selected components of $$\mathbf{U}_{t+1}$$ and penalize systematic errors. For the formal model, it is enough to assume that $$R$$ is well-defined and can be evaluated from $$\mathbf{Y}_t$$ and $$\mathbf{U}_{t+1}$$.

### 2.6.5 Mutation Phase

If $$N_t'' > 0$$, Evo may attempt to modify Lio’s structure or parameters. At tick $$t$$, Evo’s policy $$\Xi_t$$ can inspect the current internal state and energy
$$
(\text{Lio}_t,\ N_t'')
$$
and select a (possibly empty) finite sequence of mutation primitives
$$
(a_{t,1}, a_{t,2}, \dots, a_{t,K_t}), \qquad a_{t,k} \in \mathcal{A}_{\text{mut}},
$$
to be applied to $$(\mathbf{V}_{t+1}, E_t, \Theta_t, \mathbf{U}_{t+1}, O_t)$$.

Each mutation type $$a \in \mathcal{A}_{\text{mut}}$$ has an associated non-negative energy cost
$$
C_{\text{mut}}(a) \in \mathbb{R}_{\ge 0}.
$$
Let
$$
C_{\text{mut,total}}(t)
= \sum_{k=1}^{K_t} C_{\text{mut}}(a_{t,k})
$$
be the total cost of the proposed mutations. Evo can only apply mutations up to the available energy. Formally, the sequence of mutations is truncated, if necessary, at the largest prefix that satisfies
$$
N_t'' - \sum_{k=1}^{k^\ast} C_{\text{mut}}(a_{t,k}) > 0.
$$
The truncated prefix is then applied in order, yielding updated structural and parametric components (which we still denote by $$E_{t+1}$$, $$\Theta_{t+1}$$, and $$O_{t+1}$$ for simplicity). All bookkeeping on $$\mathbf{V}_{t+1}$$ and $$\mathbf{U}_{t+1}$$ required to maintain consistency with the new structure is treated as part of the mutation operation.

The final energy after mutation is
$$
N_{t+1}
  = N_t'' - \sum_{k=1}^{k^\ast} C_{\text{mut}}(a_{t,k}),
$$
and the Neo's internal state at tick $$t+1$$ is
$$
\text{Lio}_{t+1} = (\mathbf{V}_{t+1}, E_{t+1}, \Theta_{t+1}, \mathbf{U}_{t+1}, O_{t+1}),
$$
where $$\mathbf{Y}_{t+1}$$ will be derived from $$\mathbf{V}_{t+1}$$ via $$O_{t+1}$$ at the next computation step.

### 2.6.6 Summary of One Cycle

Putting the pieces together, one full Cycle from tick $$t$$ to tick $$t+1$$ consists of:

1. **Perception**: observe $$\mathbf{U}_t = \Phi_t(\text{World}_t)$$.  
2. **Computation**: update $$\mathbf{V}_{t+1}$$ and produce $$\mathbf{Y}_t$$ via local node rules.  
3. **Running cost**: deduct $$C_{\text{run}}(n_t, m_t, p_t)$$ to obtain $$N_t'$$.  
4. **World update and reward**: compute $$\mathbf{U}_{t+1}$$ and reward $$S_t = R(\mathbf{Y}_t,\ \mathbf{U}_{t+1})$$, yielding energy $$N_t''$$.  
5. **Mutation** (optional): Evo selects and applies affordable mutations from $$\mathcal{A}_{\text{mut}}$$, updating $$(E_t, \Theta_t)$$ to $$(E_{t+1}, \Theta_{t+1})$$ and reducing energy to $$N_{t+1}$$.  
6. **Termination check**: if $$N_{t+1} \le 0$$, the Neo becomes inert; otherwise, the Cycle repeats.

This operational definition provides a complete, minimal description of how a single Neo interacts with the NeoVerse, computes, earns or loses energy, and modifies its own structure over time. In the next section, we introduce a performance measure that summarizes how efficiently a Neo converts structure and energy into predictive success.

## 2.7 Performance Measures: Lifetime and Vitality

The formal model of Neosis defines a complete energy trajectory
$$
N_0, N_1, N_2, \dots
$$
for each Neo interacting with a given NeoVerse. This trajectory already combines prediction rewards and structural costs, so we do not introduce an additional ratio of “reward over cost.” Instead, we summarize performance with two simple quantities that capture how long a Neo remains alive and how much energy it manages to accumulate during its existence.

### 2.7.1 Lifetime

A Neo is considered alive at tick $$t$$ if its energy is strictly positive, $$N_t > 0$$. Once its energy reaches zero, it becomes inert and can no longer compute or mutate. We define the **lifetime**
$$
\tau = \max\{t \ge 0 : N_t > 0\},
$$
as the last tick at which the Neo is still alive. A longer lifetime indicates that the Neo is better at maintaining a positive energy budget in the given environment, either by predicting well, using a frugal structure, or both.

### 2.7.2 Vitality

While lifetime measures how long a Neo survives, we also want to quantify how energetically “alive” it becomes during that period. We define the **Vitality** of a Neo as the maximum energy it attains over its lifetime:
$$
\text{Vitality} = \max_{0 \le t \le \tau} N_t.
$$
A high Vitality means that the Neo was able to build up a substantial energy reserve at some point in its life, reflecting a strong match between its internal structure and the statistics of the NeoVerse. A low Vitality indicates that the Neo never accumulated much energy and remained close to the brink of exhaustion.

In most analyses, we will consider the pair $$(\tau,\ \text{Vitality})$$ as the basic summary of a Neo’s performance in a given environment. This pair captures both endurance (how long the Neo survives) and energetic strength (how “alive” it becomes) without introducing additional normalizations or heuristic ratios. More refined metrics can be derived from the full trajectory $$\{N_t\}$$ when needed in later chapters, but lifetime and Vitality are sufficient for the core formal model developed here.

## 2.8 Rationale for the Neo Structure

The formal model above makes a specific set of design choices: a Neo is an evolving directed graph over binary node states, with continuous local parameters, one stochastic bit per node, and an explicit separation between fast computation (Lio) and slower structural change (Evo). In this section we briefly justify these choices and relate them to both artificial neural networks and biological synapses.

### 2.8.1 Relation to Neurons and Synapses

At the level of a single node, the update rule
$$
\mathbf{V}_{t+1}[i]
  = H\big(w_i^\top \mathbf{z}_i(t) + \alpha_i \eta_i(t) + b_i\big)
$$
is deliberately close to a threshold neuron: it combines a weighted sum of inputs with a bias and then applies a nonlinearity. The directed edges $$E_t$$ play the role of synapses, determining which nodes can influence which others, and the continuous parameters $$\theta_i = (w_i, \alpha_i, b_i)$$ determine the strength and sign of those influences.

The key differences from a standard artificial neuron are:

- **Binary internal state**: node outputs live in $$\mathbb{B}$$, making the local state space as simple as possible while still allowing rich global dynamics through the network.
- **Evolving topology**: the edge set $$E_t$$ is not fixed. Nodes and edges can be added or removed, unlike conventional ANNs where the graph is chosen once and trained only in weight space.
- **Explicit energy accounting**: each run and mutation is charged against $$N_t$$, tying “synaptic complexity” and structural changes directly to survival.

This makes each node loosely analogous to a neuron with a discrete firing state and continuously tunable synaptic efficacy, while Evo provides a separate mechanism more reminiscent of developmental or evolutionary processes acting on circuitry over longer timescales.

### 2.8.2 Why Stochasticity at Each Node?

The inclusion of a stochastic bit $$\eta_i(t) \sim \text{Bernoulli}(0.5)$$ per node is intentional rather than cosmetic. Even with binary inputs $$\mathbf{z}_i(t)$$ fixed, the activation
$$
a_i(t) = w_i^\top \mathbf{z}_i(t) + \alpha_i \eta_i(t) + b_i
$$
can change from tick to tick through $$\eta_i(t)$$, and thus the output can fluctuate.

This local randomness serves several purposes:

- **Exploration in parameter and structure space**: stochastic node outputs can cause different sequences of rewards $$S_t$$ under the same environment, which in turn biases Evo’s choices of mutations. This provides an intrinsic exploration mechanism without needing an additional external noise process at the level of Evo.
- **Symmetry breaking**: in purely deterministic systems, structurally identical Neos placed in identical environments would follow identical trajectories. The per-node stochasticity allows initially identical Neos to diverge, supporting richer population-level dynamics without complicating the deterministic part of the update rule.
- **Modeling stochastic environments**: many NeoVerses are inherently noisy. Allowing internal computations to incorporate randomness makes it easier for Neos to represent and approximate stochastic mappings from past percepts to future outcomes, rather than being restricted to deterministic input–output relationships.

Crucially, the stochasticity is added in the simplest possible way: a single Bernoulli bit enters linearly with weight $$\alpha_i$$. This keeps the local rule analytically tractable while still providing a source of randomness that can be up- or down-weighted by evolution (through changes in $$\alpha_i$$).

### 2.8.3 Minimality and Extensibility

The overall structure of a Neo is chosen to be minimal but extensible:

- **Minimal substrate**: all observable states (internal, input, output) are binary, and all structure is encoded in a finite directed graph $$E_t$$ and parameter set $$\Theta_t$$. This keeps the state space simple and makes it easy to reason about limits such as small-Neo behavior or single-node dynamics.
- **Continuous parameters with discrete structure**: separating discrete topology from continuous parameters allows us to treat structural mutations (node$$^+$$, node$$^-$$, edge$$^+$$, edge$$^-$$) and local parametric changes (param$$^f$$) within a single framework. Conventional ANNs appear as a special case where $$E_t$$ is fixed and only parameter updates are allowed.
- **Clean energy coupling**: by charging both running cost and mutation cost directly to $$N_t$$, every aspect of the Neo’s complexity—depth, width, connectivity, and rate of structural change—becomes subject to selection pressure through Lifetime and Vitality. There is no separate, ad hoc regularizer.
- **Straightforward generalizations**: the current node rule is threshold-based, but replacing $$H(\cdot)$$ by another nonlinearity, or allowing continuous-valued node states, requires only local modifications to Section 2.4. The rest of the framework (structure, energy, mutation, Cycle) remains unchanged.

In summary, the chosen Neo structure sits deliberately between biological inspiration and mathematical simplicity. It is close enough to a network of stochastic threshold neurons with evolving synapses to be cognitively meaningful, yet minimal enough to support precise analysis of survival, evolution, and emergent computation in the subsequent chapters.