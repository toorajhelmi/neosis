# Chapter 7 — Related Theories and Neosis in Context

Over the past fifty years, multiple scientific communities have attempted to construct systems capable of evolving their computational structure, adapting to their environment, and developing new capabilities over time. Early work in the 1970s and 1980s explored evolutionary algorithms and genetic programming as mechanisms for open-ended problem solving [@holland1975adaption]. These systems demonstrated that mutation and selection could navigate immense design spaces, but the resulting artifacts were static: once deployed, their structures no longer changed within their lifetime.

During the 1990s and 2000s, Artificial Life (ALife) platforms such as Tierra and Avida [@ray1991tierra; @adami1998introduction] produced digital organisms that replicated, competed, and diversified under evolutionary pressures. These environments achieved open-ended population dynamics but failed to produce agents with rich internal models or capacity for structural reorganization within a lifetime. Evolution optimized replication, not adaptive cognition.

Parallel developments in neural networks and reinforcement learning [@lecun2015deep; @sutton2018reinforcement] yielded powerful functional systems operating over fixed network architectures. Neuroevolution methods such as NEAT and HyperNEAT [@stanley2002evolving; @stanley2009hyperneat] introduced structural evolution, but only across generations, not as part of an individual agent's adaptive cycle.

Recent work—neural cellular automata [@mordvintsev2020growing], hypernetworks [@ha2016hypernetworks], meta-learning, and developmental cognitive architectures—introduces forms of plasticity and structure manipulation. Yet none unifies *in-lifetime* structural change, *survival-based* objectives, and *energy-constrained* mutation into a single organismal model. Neosis aims to fill precisely this gap.

To situate Neosis clearly, this chapter presents:

1. A conceptual diagram mapping theoretical traditions into a three-axis space.  

2. A categorical table comparing frameworks by structural adaptation, objectives, and development.  

3. A review of **theoretical frameworks**, organized into conceptual categories.  

4. A review of **systems and projects**, organized into mechanistic categories.

---

## Conceptual Placement of Neosis

**Figure 7.1 — Conceptual Cube Diagram (Placeholder)**  

(A diagram to be inserted.)

---

## Table 7.1 — Three-Axis Mapping of Frameworks

| Theory Family | Structural Adaptation | Objective Source | Developmental Regime |
|---------------|----------------------|------------------|-----------------------|
| Artificial Neural Networks | Fixed | External loss | Static |
| Spiking Neural Networks | Fixed | External loss | Static |
| Reinforcement Learning | Fixed | External reward | Static |
| Neuroevolution | Generational | External task fitness | Generational |
| Artificial Life (Tierra, Avida) | Generational | Replication fitness | Generational |
| Predictive Processing / FEP | Fixed hierarchy | Free-energy minimization | Static |
| Developmental Systems Theory | Developmental | Biological fitness | Scaffolded |
| Dynamical Systems Theory | Fixed attractor landscape | Emergent | Continuous |
| Embodied/Enactive Cognition | Structural coupling | Viability | Developmental |
| Reservoir Computing | Fixed | External training | Static |
| Neural Architecture Search | Generational/Meta | External loss | Static |
| Neural Cellular Automata | Local rules | External constraints | Pattern-growth |
| Hypernetworks / Meta-learning | Fixed meta-topology | External loss | Static |
| **Neosis** | **In-lifetime self-modifying** | **Internal survival energy** | **Open-ended** |

---

# 7.1 Theoretical Frameworks

Theoretical traditions can be grouped into categories based on the **goal or approach** shaping each field. These categories clarify how each tradition attempts to answer a subset of the problem Neosis addresses.

---

## 7.1.1 Category A — **Learning-Based Theories**  
### *Goal: Improve performance through parameter adaptation while assuming a fixed architecture.*

This category includes artificial neural networks, reinforcement learning, and predictive processing.  

Artificial neural networks [@rumelhart1986learning; @lecun2015deep] use gradient-based updates to refine numerical parameters on static computation graphs. Reinforcement learning [@sutton2018reinforcement] optimizes expected reward by adjusting policy or value function parameters based on experience. Predictive processing and the Free Energy Principle [@friston2010free] treat cognition as hierarchical prediction-error minimization.

Despite their strengths, these learning-based theories rely on fixed structures and externally defined tasks. Their adaptation occurs exclusively through differentiable updates rather than through structural mutation. Because they do not couple prediction, reward, and structural change within a single organismal cycle, they lack the unified energy economy and continuous self-modification that characterize Neosis.

---

## 7.1.2 Category B — **Evolution-Based Theories**  
### *Goal: Discover functional structures through mutation and selection across generations.*

Evolutionary computation [@holland1975adaption], genetic programming [@koza1992genetic], and neuroevolution methods such as NEAT and HyperNEAT [@stanley2002evolving; @stanley2009hyperneat] search vast design spaces through generational mutation and selection. Artificial Life environments such as Tierra and Avida [@ray1991tierra; @adami1998introduction] demonstrate open-ended population dynamics and developmental divergence.

Although these systems generate novelty and support domain-general search, they do not allow *in-lifetime* structural change. Adaptation is tied to replication fitness rather than predictive survival. Internal cognitive complexity remains limited because there is no mechanism linking computation, reward, and structural modification inside the organism's operational cycle. Neosis unifies learning and evolution in a way these frameworks do not.

---

## 7.1.3 Category C — **Developmental and Cognitive Theories**  
### *Goal: Explain how cognition emerges from developmental processes, modularity, and environmental interaction.*

Computational cognitive science [@anderson2007integrated; @newell1994unified] models cognition through specialized modules and multi-timescale adaptation. Developmental systems theory [@oyama2000ontogeny] emphasizes gene–environment coupling and emergent developmental trajectories. Embodied and enactive cognition [@varela1991embodied; @clark1997being] argue that cognition arises from tight coupling between organism and environment.

These theories articulate powerful principles describing natural cognition, yet they are interpretive rather than constructive: they explain biological systems rather than define a minimal computational substrate for synthetic organisms. Because they lack explicit mutation mechanisms or survival-based internal objectives, they do not exhibit the energy-constrained structural evolution that Neosis supports.

---

## 7.1.4 Category D — **Self-Organizing and Dynamical Theories**  
### *Goal: Reveal how complex behavior emerges from simple local interactions and intrinsic system dynamics.*

Dynamical systems theory [@kelso1995dynamic] models cognition and behavior as trajectories through attractor landscapes shaped by system interactions. Reservoir computing [@jaeger2001echo] uses fixed recurrent dynamics to produce rich transformations, relying on trained readouts. Neural cellular automata [@mordvintsev2020growing] demonstrate pattern formation and self-repair based on local update rules.

Although these systems produce rich emergent dynamics, they provide no survival objective and no mechanism for energy-regulated mutation. Most operate on fixed architectures or predetermined update laws. Without a unified operational cycle linking prediction, reward, structural change, and survival, their adaptability remains fundamentally limited compared to Neosis.

---

# 7.2 Systems and Projects

Systems and projects differ from theoretical frameworks in that they implement working platforms. These can likewise be grouped into categories based on their underlying **mechanistic approach**.

---

## 7.2.1 Category E — **Evolutionary ALife Platforms**  
### *Approach: Create digital ecosystems where organisms mutate, replicate, and compete.*

Platforms such as Tierra [@ray1991tierra], Avida [@adami1998introduction], Polyworld [@yaeger1994computational], and Lenia [@chan2019lenia] explore ecological competition, mutation, and population-level adaptation. These systems showcase open-ended dynamics, spontaneous diversification, and ecosystem-level complexity.

Yet despite their ecological richness, these systems rarely develop sophisticated internal predictive models or meaningful within-lifetime structural adaptation. Their objectives remain tied to replication rather than survival-based computation, and mutation affects only generational change, not continuous structural reorganization. Neosis's integration of prediction, energy, and mutation within a single organism sets it apart.

---

## 7.2.2 Category F — **Adaptive Neural Systems**  
### *Approach: Enhance neural models with auxiliary mechanisms for dynamic parameterization or meta-level adaptation.*

Hypernetworks [@ha2016hypernetworks], meta-learning architectures, differentiable architecture search, and morphological computation [@pfeifer2007self] provide additional flexibility beyond fixed neural parameters. They introduce mechanisms that generate weights dynamically or reconfigure computational pathways.

However, these systems maintain fixed meta-structures and rely on external, differentiable losses to govern adaptation. They do not incorporate intrinsic survival-based objectives or unified energy economies that regulate structural mutation. Consequently, they lack the open-ended structural growth that Neosis enables within a single lifetime.

---

## 7.2.3 Category G — **Self-Modifying Neural or Graph Systems**  
### *Approach: Allow networks to alter their topology or computation rules during operation.*

Neural cellular automata [@mordvintsev2020growing], continual topology-adapting networks [@stanley2003continual], and modular neural architectures introduce forms of structural plasticity that operate during computation. These approaches explore the frontier between fixed computation graphs and flexible, evolving structures.

Despite exploring structural change, these systems lack a survival-based internal energy model that ties structural mutation to adaptive success. Structural modifications are typically driven by heuristics, external training signals, or rule-based mechanisms rather than a unified organismal loop linking prediction, reward, and survival. As such, they do not achieve the open-ended cognitive development central to Neosis.

---

# 7.3 Why These Comparisons Matter

The traditions reviewed above illuminate crucial aspects of adaptive behavior—learning, mutation, development, ecological interaction, and self-organization. However, each occupies only a portion of a broader conceptual space defined by:

1. The locus of structural adaptation (fixed, generational, developmental, in-lifetime).  

2. The origin of objectives (external loss, external reward, replication fitness, internal survival).  

3. The developmental regime (static, generational, scaffolded, open-ended).

Neosis is distinguished by integrating all three dimensions: in-lifetime self-modification, survival-driven internal energy objectives, and open-ended representational expansion. This makes Neosis categorically distinct—not superior—from existing approaches.

---

# 7.4 Summary

Neosis draws from decades of research in neural computation, Artificial Life, evolutionary algorithms, cognitive science, and self-organizing systems. Prior efforts focused on learning without structural evolution, evolution without cognition, or development without energy constraints. Neosis unifies these principles into a single minimal computational framework linking prediction, energy, structure, and survival. This positions Neosis not as an incremental extension of prior systems, but as a foundation for open-ended, self-modifying digital organisms.
