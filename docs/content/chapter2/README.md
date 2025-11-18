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
\text{Lio}_t = (\mathbf{V}_t,\ G_t,\ \Theta_t,\ \mathbf{U}_t,\ \mathbf{Y}_t).
$$

The vector $$\mathbf{V}_t$$ is the internal binary state (or memory) of the Neo:
$$
\mathbf{V}_t \in \mathbb{B}^{n_t},
$$
where $$n_t$$ is the number of internal nodes at tick $$t$$. Each coordinate of $$\mathbf{V}_t$$ corresponds to the state of a single node in the Neo’s computational graph.

The graph structure itself is captured by
$$
G_t = (\mathcal{N}_t,\ E_t),
$$
where $$\mathcal{N}_t = \{1,\dots,n_t\}$$ is the set of node indices and $$E_t \subseteq \mathcal{N}_t \times \mathcal{N}_t$$ is the set of directed edges between nodes. We do not impose any topological restriction: $$G_t$$ may be feedforward, recurrent, or contain cycles. This flexibility allows the Neo to evolve arbitrary computational motifs, including those that resemble neural networks, finite-state machines, or more complex dynamical systems.

Each node $$i \in \mathcal{N}_t$$ is associated with a continuous parameter vector
$$
\theta_i \in \mathbb{R}^{k_i},
$$
which determines how that node processes its inputs. We collect all node parameters at tick $$t$$ into
$$
\Theta_t = \{\theta_i : i \in \mathcal{N}_t\}.
$$
These parameters will be used in Section 2.4 to define the node-local update rules that map incoming binary signals to new node states.

The interface between Lio and the NeoVerse is given by the input and output vectors
$$
\mathbf{U}_t \in \mathbb{B}^{m_t}, \qquad
\mathbf{Y}_t \in \mathbb{B}^{p_t}.
$$
The input $$\mathbf{U}_t$$ is the percept at tick $$t$$ defined by the projection in Section 2.2. The output $$\mathbf{Y}_t$$ is produced by a designated subset of nodes, and will later be interpreted as a prediction about future percepts. The dimensions $$m_t$$ and $$p_t$$ may change over time as the Neo gains or loses input and output nodes through structural mutation.

In summary, Lio at tick $$t$$ is an evolving binary graph with continuous parameters, equipped with a binary input and output interface. The pair $$(G_t,\ \Theta_t)$$ specifies *what* computational structure exists, while $$(\mathbf{V}_t,\ \mathbf{U}_t,\ \mathbf{Y}_t)$$ specifies the current binary activity flowing through that structure.

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


## 2.4 Local Computation (Lex and Node Updates)

## 2.5 Mutation Primitives and Structural Updates

## 2.6 The Cycle (Operational Semantics)

## 2.7 Performance Measure: NeoQuotient


