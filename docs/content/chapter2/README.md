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

The interface between Lio and the NeoVerse is given by the input and output vectors
$$
\mathbf{U}_t \in \mathbb{B}^{m_t}, \qquad
\mathbf{Y}_t \in \mathbb{B}^{p_t}.
$$
The input $$\mathbf{U}_t$$ is the percept at tick $$t$$ defined by the projection in Section 2.2. The output $$\mathbf{Y}_t$$ is produced by a designated subset of nodes, and will later be interpreted as a prediction about future percepts. The dimensions $$m_t$$ and $$p_t$$ may change over time as the Neo gains or loses input and output nodes through structural mutation.

In summary, Lio at tick $$t$$ is an evolving binary graph with continuous parameters, equipped with a binary input and output interface. The pair $$(E_t,\ \Theta_t)$$ specifies *what* computational structure exists, while $$(\mathbf{V}_t,\ \mathbf{U}_t,\ \mathbf{Y}_t)$$ specifies the current binary activity flowing through that structure.

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

## 2.4 Local Computation: Node Inputs and Updates

Having specified the structural components of a Neo, we now describe how internal binary states are updated from one tick to the next. The basic idea is that each node reads a subset of internal and perceptual bits, combines them according to its parameters, and produces a new binary state through a simple local rule.

### 2.4.1 Node Inputs

At tick $$t$$, the internal state of the Neo is given by
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
by collecting the corresponding bits from $$\mathbf{V}_t$$ and $$\mathbf{U}_t$$ in a fixed order. The integer $$k_i$$ is therefore the number of binary inputs that node $$i$$ currently receives. It may change over time as edges are added or removed, or as the Neo gains or loses input channels.

### 2.4.2 Parametric Local Update Rule

Each node $$i$$ carries a continuous parameter vector
$$
\theta_i \in \mathbb{R}^{k_i + 1},
$$
which we interpret as a concatenation of weights and a bias:
$$
\theta_i = (w_i, b_i), \qquad w_i \in \mathbb{R}^{k_i},\ b_i \in \mathbb{R}.
$$
Given the binary input vector $$\mathbf{z}_i(t) \in \mathbb{B}^{k_i}$$, the node computes a real-valued activation
$$
a_i(t) = w_i^\top \mathbf{z}_i(t) + b_i,
$$
and then applies a threshold to obtain the new binary state. In the simplest deterministic version, the update rule is
$$
\mathbf{V}_{t+1}[i] = \text{Lex}_i\big(\mathbf{z}_i(t), \theta_i\big)
= H\big(a_i(t)\big),
$$
where $$H(\cdot)$$ is the Heaviside step function
$$
H(x) =
\begin{cases}
1, & x \ge 0,\\
0, & x < 0.
\end{cases}
$$

This local rule has several useful properties:

- It depends only on the node’s current inputs $$\mathbf{z}_i(t)$$ and parameters $$\theta_i$$.
- It is compatible with the binary state substrate, since the output is always in $$\mathbb{B}$$.
- It remains well-defined as $$k_i$$ changes; adding or removing inputs simply changes the dimensionality of $$w_i$$ and the construction of $$\mathbf{z}_i(t)$$.

The collection of all node updates defines a global state transition from $$\mathbf{V}_t$$ to $$\mathbf{V}_{t+1}$$. We adopt snapshot semantics: all nodes read $$\mathbf{V}_t$$ and $$\mathbf{U}_t$$ as they were at the beginning of tick $$t$$, compute their activations and outputs in parallel, and write their new values into $$\mathbf{V}_{t+1}$$.

### 2.4.3 Outputs as Designated Nodes

The Neo’s output at tick $$t$$ is a binary vector
$$
\mathbf{Y}_t \in \mathbb{B}^{p_t},
$$
defined by a designated set of output indices
$$
\mathcal{O}_t \subseteq \{1,\dots,n_t\}, \qquad |\mathcal{O}_t| = p_t.
$$
We enumerate $$\mathcal{O}_t = \{o_1,\dots,o_{p_t}\}$$ and set
$$
\mathbf{Y}_t[j] = \mathbf{V}_t[o_j], \qquad j = 1,\dots,p_t.
$$
Thus outputs are not special nodes with different internal rules; they are ordinary nodes whose current states are simply read out as the Neo’s prediction vector. As with inputs, the cardinality $$p_t$$ may change over time as the Neo gains or loses output nodes.

Taken together, the constructions above specify how a Neo transforms percepts and internal states at tick $$t$$ into a new internal state $$\mathbf{V}_{t+1}$$ and an output $$\mathbf{Y}_t$$, using only local node computations controlled by continuous parameters. In the next sections, we will describe how these structures can change over time through mutation, and how the resulting predictions feed into the energy dynamics that govern survival.

## 2.5 Mutation Primitives and Structural Updates

## 2.6 The Cycle (Operational Semantics)

## 2.7 Performance Measure: NeoQuotient


