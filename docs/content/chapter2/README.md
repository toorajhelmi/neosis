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

So far we have treated the internal structure of a Neo at tick $$t$$ as fixed: Lio is specified by $$(\mathbf{V}_t, E_t, \Theta_t, \mathbf{U}_t, \mathbf{Y}_t)$$ and Evo by $$(\Psi_t, \Xi_t)$$. In Neosis, however, the defining property of a Neo is that this structure can change over time. Structural and parametric changes are not continuous “training steps” on a fixed graph, but discrete mutation events selected and triggered by Evo.

In this section we introduce a minimal set of mutation primitives. Each primitive is a local operation on the tuple $$(\mathbf{V}_t, E_t, \Theta_t, \mathbf{U}_t, \mathbf{Y}_t)$$. Later, in the Cycle definition, we will associate each operation with an energy cost and specify when mutations can occur.

For clarity, we collect all mutation types into a finite set
$$
\mathcal{A}_{\text{mut}}
= \{\text{node}^+,\ \text{node}^-,\ \text{edge}^+,\ \text{edge}^-,\ \text{param}^f\}.
$$

### 2.5.1 Node Addition (node$$^+$$)

A node-addition mutation increases the number of internal nodes from $$n_t$$ to $$n_t + 1$$. Concretely, we extend the state vector and parameter set as
$$
\mathbf{V}_t' \in \mathbb{B}^{n_t+1}, \qquad
\Theta_t' = \Theta_t \cup \{\theta_{n_t+1}\},
$$
where the new coordinate $$\mathbf{V}_t'[n_t+1]$$ is initialized (for example) to zero, and the new parameter vector $$\theta_{n_t+1}$$ is drawn from an initialization distribution over $$\mathbb{R}^{k_{n_t+1}+2}$$. The edge set is extended by optionally adding new edges involving node $$n_t+1$$:
$$
E_t' = E_t \cup E_{\text{new}},
$$
where $$E_{\text{new}} \subseteq \{n_t+1\} \times \{1,\dots,n_t+1\} \cup \{1,\dots,n_t\} \times \{n_t+1\}$$.

The exact choice of $$E_{\text{new}}$$ and the initialization distribution for $$\theta_{n_t+1}$$ are controlled by Evo’s mutation policy $$\Xi_t$$. The definition above only requires that the result be a valid graph and parameter set.

### 2.5.2 Node Removal (node$$^-$$)

A node-removal mutation selects an index $$i \in \{1,\dots,n_t\}$$ and deletes that node. All edges incident to $$i$$ are removed, and the corresponding coordinate is removed from the state vector and parameter set. Formally, we obtain a new dimension $$n_t' = n_t - 1$$ and a new state vector $$\mathbf{V}_t' \in \mathbb{B}^{n_t'}$$ by deleting $$\mathbf{V}_t[i]$$ and re-indexing the remaining coordinates. The parameter set $$\Theta_t$$ is updated in the same way, and the edge set becomes
$$
E_t' = \{(j,k) \in E_t : j \neq i,\ k \neq i\},
$$
with node indices re-labeled to match the new indexing of $$\mathbf{V}_t'$$.

If the removed node belonged to the output set $$\mathcal{O}_t$$, the output index set must also be updated by deleting that index; similarly, if the node played a role in interpreting inputs, the mapping from percept coordinates to internal indices must be updated. These adjustments are local bookkeeping steps that ensure the consistency of $$\mathbf{U}_t$$ and $$\mathbf{Y}_t$$ with the new internal graph.

Node removal can in principle disconnect the graph into multiple components. In this chapter we simply require that $$E_t'$$ defines a valid (possibly disconnected) graph. Whether disconnected components become separate Neos in a population will be specified in later chapters on survival and reproduction.

### 2.5.3 Edge Addition (edge$$^+$$)

An edge-addition mutation selects a pair of node indices $$(j,k)$$ with $$j \neq k$$ and adds a directed edge from $$j$$ to $$k$$:
$$
E_t' = E_t \cup \{(j,k)\}.
$$
This change affects the input index set $$\mathcal{I}_t(k)$$ of node $$k$$ by adding $$j$$ to it, and therefore increases the dimensionality $$k_k$$ of its input vector $$\mathbf{z}_k(t)$$. To keep the local update rule for node $$k$$ well-defined, its parameter vector $$\theta_k = (w_k, \alpha_k, b_k)$$ must be expanded by appending a new weight for the incoming signal from node $$j$$. This can be done by sampling a new weight component from a chosen initialization distribution.

All other nodes, and their parameter vectors, remain unchanged.

### 2.5.4 Edge Removal (edge$$^-$$)

An edge-removal mutation selects an existing edge $$(j,k) \in E_t$$ and deletes it:
$$
E_t' = E_t \setminus \{(j,k)\}.
$$
The input index set $$\mathcal{I}_t(k)$$ of node $$k$$ is updated by removing $$j$$, and the corresponding weight component is removed from $$w_k$$. The dimensionality $$k_k$$ of its input vector decreases by one. As with node removal, the graph may become disconnected; we only require that $$E_t'$$ remains a valid directed graph over the current node indices.

### 2.5.5 Parameter Perturbation (param$$^f$$)

A parameter-perturbation mutation changes the continuous parameters of a single node without altering the graph structure. For some selected node index $$i$$, we replace
$$
\theta_i \leftarrow \theta_i + \Delta_i,
$$
where $$\Delta_i \in \mathbb{R}^{k_i+2}$$ is a random perturbation drawn from a specified distribution (for example, a zero-mean Gaussian with fixed covariance). All other parameters and the edge set remain unchanged.

This primitive allows the Neo to explore nearby computational behaviors while keeping its structure fixed. When combined with node and edge mutations, it provides a simple but expressive mechanism for evolving both the topology and the local computations of Lio.

---

Together, these five primitive operations describe how the structural and parametric components of a Neo can change in discrete steps. Evo’s role is to decide which mutations to attempt, when to apply them, and how to balance structural exploration against the energy costs that will be introduced in the next section.

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

This value is written into Lio’s input component, so that
$$
\text{Lio}_t = (\mathbf{V}_t,\ E_t,\ \Theta_t,\ \mathbf{U}_t,\ \mathbf{Y}_t),
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

The output vector $$\mathbf{Y}_t \in \mathbb{B}^{p_t}$$ is obtained by reading out a designated subset of node states. Let
$$
\mathcal{O}_t = \{o_1,\dots,o_{p_t}\} \subseteq \{1,\dots,n_t\}
$$
be the set of output indices. We define
$$
\mathbf{Y}_t[j] = \mathbf{V}_t[o_j], \qquad j = 1,\dots,p_t.
$$
Thus at tick $$t$$, the Neo produces a prediction $$\mathbf{Y}_t$$ based on its internal state and the current percept, while its internal memory is updated to $$\mathbf{V}_{t+1}$$ for use at the next tick.

### 2.6.3 Running Cost and Energy Deduction

Executing the internal computation incurs a running cost that depends on the size of the Neo’s active structure. We introduce a cost function
$$
C_{\text{run}} : \mathbb{N}^3 \to \mathbb{R}_{\ge 0},
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
to be applied to $$(\mathbf{V}_{t+1}, E_t, \Theta_t, \mathbf{U}_{t+1}, \mathbf{Y}_t)$$.

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
The truncated prefix is then applied in order, yielding updated structural and parametric components (which we still denote by $$E_{t+1}$$ and $$\Theta_{t+1}$$ for simplicity). All bookkeeping on $$\mathbf{V}_{t+1}$$, $$\mathbf{U}_{t+1}$$, and $$\mathbf{Y}_t$$ required to maintain consistency with the new structure is treated as part of the mutation operation.

The final energy after mutation is
$$
N_{t+1}
  = N_t'' - \sum_{k=1}^{k^\ast} C_{\text{mut}}(a_{t,k}),
$$
and the Neo’s internal state at tick $$t+1$$ is
$$
\text{Lio}_{t+1} = (\mathbf{V}_{t+1}, E_{t+1}, \Theta_{t+1}, \mathbf{U}_{t+1}, \mathbf{Y}_{t+1}),
$$
where $$\mathbf{Y}_{t+1}$$ will be determined at the next computation step.

### 2.6.6 Summary of One Cycle

Putting the pieces together, one full Cycle from tick $$t$$ to tick $$t+1$$ consists of:

1. **Perception**: observe $$\mathbf{U}_t = \Phi_t(\text{World}_t)$$.  
2. **Computation**: update $$\mathbf{V}_{t+1}$$ and produce $$\mathbf{Y}_t$$ via local node rules.  
3. **Running cost**: deduct $$C_{\text{run}}(n_t, m_t, p_t)$$ to obtain $$N_t'$$.  
4. **World update and reward**: compute $$\mathbf{U}_{t+1}$$ and reward $$S_t = R(\mathbf{Y}_t,\ \mathbf{U}_{t+1})$$, yielding energy $$N_t''$$.  
5. **Mutation** (optional): Evo selects and applies affordable mutations from $$\mathcal{A}_{\text{mut}}$$, updating $$(E_t, \Theta_t)$$ to $$(E_{t+1}, \Theta_{t+1})$$ and reducing energy to $$N_{t+1}$$.  
6. **Termination check**: if $$N_{t+1} \le 0$$, the Neo becomes inert; otherwise, the Cycle repeats.

This operational definition provides a complete, minimal description of how a single Neo interacts with the NeoVerse, computes, earns or loses energy, and modifies its own structure over time. In the next section, we introduce a performance measure that summarizes how efficiently a Neo converts structure and energy into predictive success.

## 2.7 Performance Measure: NeoQuotient


