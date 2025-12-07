# Chapter 4 — Micro Static Analysis of a Single Neo

A Neo survives by predicting the NeoVerse (NV). At every tick, it receives a small snapshot of the world—$$m$$ binary inputs $$U_t \in \{0,1\}^m$$—and updates its internal state according to the Lex rule. From this updated state it produces an output vector $$Y_t$$, interpreted as its prediction of the next NV state $$U_{t+1}$$. Correct predictions generate Sparks, which increase the Neo's Nex. Regardless of correctness, each update consumes a fixed amount of Nex simply to remain alive.

In the broader Neosis framework, a Neo may improve its predictive ability through in-life plasticity or through evolutionary processes. However, this chapter focuses on the static case, where the Neo's structure and parameters are fixed. In this setting, the Neo does not adjust its weights or topology; it behaves exactly according to the computation encoded in its architecture at birth.

Because the computation is fixed, the Neo eventually settles into a long-run statistical pattern determined entirely by its structure and by the statistics of the NV. Its internal states, its outputs, and their relationship to NV inputs become time-invariant. This is the stationary regime of a Neo, and understanding this regime is the central goal of micro analysis.

The purpose of this chapter is to determine how much predictive ability a fixed Neo possesses purely from its stationary behavior. By characterizing how its stationary output relates to the NV's stationary dynamics, we can determine its expected Nex gain, its expected Nex loss, and ultimately whether it will survive.

## 4.1 Neo as a Predictive System

Prediction is only meaningful when the environment exhibits stable statistical structure. If the NeoVerse changed its distribution over time—drifting, aging, or altering its transition rules—then a static Neo could not maintain predictive accuracy. Even though learning-capable Neos will be treated later, the static Neo analyzed here can only exploit whatever statistical regularities are already present. Its predictive power depends entirely on whether the relationship between $$U_t$$ and $$U_{t+1}$$ remains consistent over time.

For this reason, we assume that the projection of the NeoVerse that a Neo perceives is a stationary stochastic process. As discussed in earlier chapters, a Neo does not experience the full NeoVerse; it only receives a limited projection of it through its m-bit input channel. It is this projected process, not the full NV, that must exhibit stable statistics. Stationarity does not require periodicity. A process may vary dramatically from moment to moment and still be stationary if its probability distribution does not change over time. What matters is that

$$P(U_t = u) = P(U_{t+1} = u) \quad \text{and} \quad P(U_{t+1} \mid U_t) \text{ is independent of } t.$$

Under this assumption, the joint distribution of the Neo's internal state and the current NV input,

$$\pi(x, u) = \lim_{t \to \infty} P(X_t = x, \, U_t = u),$$

converges to a well-defined stationary distribution. All predictive properties of the Neo derive from this object. Its output distribution is obtained by marginalizing the internal state, and its predictive performance is obtained by examining how its stationary output relates to the NV's next state.

A stationary NV therefore makes micro analysis possible: it ensures that a fixed Neo has a well-defined, time-invariant predictive relationship with the environment.

## 4.2 Neo's Survivability

Once the Neo and the perceived NeoVerse (NV) projection settle into their joint stationary regime, their long-run behavior is captured by the stationary distribution

$$\pi(x, u) = \lim_{t \to \infty} P(X_t = x, \, U_t = u),$$

where $$X_t$$ is the Neo's internal state and $$U_t \in \{0,1\}^m$$ is the $$m$$-bit NV projection it sees at time $$t$$. The Neo's output is a fixed readout of its state,

$$Y_t = g(X_t),$$

and the NV projection evolves according to a time-invariant transition law

$$P(U^+ = u' \mid U = u),$$

where $$U^+ = U_{t+1}$$ denotes the next NV projection the Neo is trying to predict.

Starting from $$\pi(x, u)$$, the distribution of outputs in the stationary regime is obtained by marginalizing over the internal state and input:

$$P(Y = y) = \sum_{x, u} \pi(x, u) \, \mathbb{1}\{g(x) = y\}.$$

To measure prediction, we need the joint behavior of the Neo's output and the next NV projection. This is given by

$$P(U^+ = u', \, Y = y) = \sum_{x, u} P(U^+ = u' \mid U = u) \, \pi(x, u) \, \mathbb{1}\{g(x) = y\}.$$

From this joint distribution we recover the conditional distribution the Neo is implicitly using for prediction:

$$P(U^+ = u' \mid Y = y) = \frac{P(U^+ = u', \, Y = y)}{P(Y = y)}.$$

In the stationary regime, an ideal observer that has access to $$Y$$ and knows these probabilities can construct the optimal decoder

$$\hat{u}(y) \in \arg\max_{u'} P(U^+ = u' \mid Y = y),$$

which chooses, for each output pattern $$y$$, the most likely next NV pattern. The corresponding prediction accuracy is

$$\text{Acc} = P(\hat{u}(Y) = U^+) = \sum_y P(Y = y) \, \max_{u'} P(U^+ = u' \mid Y = y).$$

This accuracy is a pure functional of $$\pi(x, u)$$, the readout $$g$$, and the NV transition $$P(U^+ \mid U)$$; no additional assumptions are needed.

To connect this to survival, we model the Neo's Nex over time. At each tick, if the prediction is correct, the Neo gains $$r > 0$$ Nex units as a Spark reward; regardless of correctness, it pays a living cost $$c_\ell > 0$$ Nex to maintain its state and perform the Lex update. The per-tick change in energy can therefore be written as

$$\Delta E_t = r \, \mathbb{1}\{\hat{u}(Y_t) = U^+\} - c_\ell.$$

Under stationarity, the event "prediction is correct" is Bernoulli with success probability $$\text{Acc}$$, so $$\Delta E_t$$ takes the two values

$$\Delta E_t = \begin{cases} r - c_\ell, & \text{with probability Acc}, \\ -c_\ell, & \text{with probability } 1 - \text{Acc}. \end{cases}$$

From this two-point distribution we obtain the mean energy drift

$$\mu = \mathbb{E}[\Delta E_t] = r \, \text{Acc} - c_\ell,$$

and the variance

$$\sigma^2 = \text{Var}(\Delta E_t) = r^2 \, \text{Acc}(1 - \text{Acc}).$$

Let $$E_t$$ denote the Neo's Nex at tick $$t$$, starting from some initial energy $$E_0 > 0$$, and evolving as

$$E_{t+1} = E_t + \Delta E_t,$$

with an absorbing boundary at $$E_t = 0$$ (death). This is a biased random walk in energy space. Using a standard diffusion approximation for such a process with drift $$\mu$$ and variance $$\sigma^2$$, we can express the Neo's survivability—its probability of never hitting zero energy—as a function of these quantities.

We denote survivability by $$\Xi$$. When the drift is non-positive, $$r \, \text{Acc} \leq c_\ell$$, the Neo eventually dies with probability one, so $$\Xi = 0$$. When the drift is positive, $$r \, \text{Acc} > c_\ell$$, the diffusion approximation yields

$$\Xi \approx 1 - \exp\left(-\frac{2\mu}{\sigma^2} E_0\right) = 1 - \exp\left(-\frac{2E_0}{r^2 \, \text{Acc}(1 - \text{Acc})} (r \, \text{Acc} - c_\ell)\right).$$

Putting these pieces together, survivability is fully determined by the Neo's stationary interaction with the NeoVerse projection:

$$\Xi = \Xi(\pi(x, u), \, g, \, P(U^+ \mid U), \, r, \, c_\ell, \, E_0).$$

The stationary distribution $$\pi(x, u)$$ encodes how the Neo's internal state co-varies with its perceived environment; the output mapping $$g$$ and NV dynamics $$P(U^+ \mid U)$$ determine prediction accuracy; and the Spark reward $$r$$, living cost $$c_\ell$$, and initial Nex $$E_0$$ translate predictive performance into a concrete survival probability.

## 4.3 Neo Motifs and Analytical Examples

So far we have treated the Neo in full generality, expressing survivability $$\Xi$$ in terms of its stationary interaction with the NeoVerse projection. In practice, however, it is rarely possible to write down the stationary distribution $$\pi(x, u)$$ in closed form for an arbitrary topology. To make progress, we analyze Neo motifs: small, structurally simple Neos embedded in simple but nontrivial NeoVerse models. These motifs give us concrete, interpretable examples where we can compute both the stationary behavior and the resulting survivability analytically.

The analytical approach depends on the complexity of the Neo's internal dynamics. For simple cases where the Neo's behavior can be characterized directly without feedback loops, we can use maximum likelihood methods to determine optimal predictions and compute survivability. However, when the Neo contains internal feedback loops that create complex temporal dependencies, the analysis requires computing the stationary distribution of the joint Markov chain over internal states and NeoVerse inputs. From this stationary distribution, we can derive prediction accuracy and ultimately survivability.

We present two cases that illustrate these different analytical approaches. The first case considers a simple "copy Neo" that directly stores the current NeoVerse projection without internal feedback. This allows us to use maximum likelihood estimation to find the optimal decoder and compute accuracy directly. The second case examines a more complex "p-estimator Neo" with internal feedback loops that create memory and temporal dependencies. For this case, we must compute the stationary distribution of the internal state Markov chain to determine prediction accuracy and survivability.

### 4.3.1 m-Bit Markov NeoVerse and the Copy Neo

We consider an $$m$$-bit NeoVerse (NV) projection

$$U_t = (U_t(1), \ldots, U_t(m)) \in \{0,1\}^m,$$

where each coordinate evolves as an independent binary Markov chain with flip probability $$\alpha \in [0,1]$$:

$$P(U_{t+1}(j) \neq U_t(j)) = \alpha, \quad P(U_{t+1}(j) = U_t(j)) = 1 - \alpha.$$

A copy Neo directly stores the current NV projection,

$$X_t = U_t,$$

and its output is

$$Y_t = g(X_t) = X_t.$$

#### Joint Stationary Distribution $$\pi(x, u)$$

The Neo and NV settle into a joint stationary regime described by

$$\pi(x, u) = \lim_{t \to \infty} P(X_t = x, \, U_t = u).$$

Because $$X_t = U_t$$ deterministically, $$\pi(x, u) = 0$$ if $$x \neq u$$, and when $$x = u$$, $$\pi(u, u) = P(U_t = u)$$ in stationarity. Since the $$m$$ coordinates are independent and each has marginal $$(\frac{1}{2}, \frac{1}{2})$$, the stationary distribution of $$U_t$$ is uniform:

$$P(U_t = u) = 2^{-m}, \quad u \in \{0,1\}^m.$$

Thus,

$$\pi(x, u) = 2^{-m} \, \mathbb{1}\{x = u\}.$$

#### Output Distribution

Marginalizing over $$\pi$$,

$$P(Y = y) = \sum_{x, u} \pi(x, u) \, \mathbb{1}\{g(x) = y\} = \sum_u 2^{-m} \mathbb{1}\{u = y\} = 2^{-m}.$$

Hence, $$P(Y = y) = 2^{-m}$$.

#### Joint Law of $$(U^+, Y)$$

Let $$U^+ = U_{t+1}$$. The stationary joint distribution is

$$P(U^+ = u', \, Y = y) = \sum_{x, u} P(U^+ = u' \mid U = u) \, \pi(x, u) \, \mathbb{1}\{g(x) = y\}.$$

Substituting $$\pi(x, u) = 2^{-m} \mathbb{1}\{x = u\}$$ and $$g(x) = x$$,

$$P(U^+ = u', \, Y = y) = 2^{-m} \, P(U_{t+1} = u' \mid U_t = y).$$

Because the NV transition kernel factorizes across bits,

$$P(U_{t+1} = u' \mid U_t = y) = \prod_{j=1}^m \left[(1-\alpha) \mathbb{1}\{u'_j = y_j\} + \alpha \, \mathbb{1}\{u'_j \neq y_j\}\right].$$

Thus,

$$P(U^+ = u', \, Y = y) = 2^{-m} \prod_{j=1}^m \left[(1-\alpha) \mathbb{1}\{u'_j = y_j\} + \alpha \, \mathbb{1}\{u'_j \neq y_j\}\right].$$

#### Conditional Prediction Law

Since $$Y_t = U_t$$,

$$P(U_{t+1} = u' \mid Y_t = y) = P(U_{t+1} = u' \mid U_t = y).$$

Each bit evolves independently, so

$$P(U_{t+1}(j) = u'_j \mid U_t(j) = y_j) = \begin{cases} 1-\alpha, & u'_j = y_j, \\ \alpha, & u'_j \neq y_j. \end{cases}$$

Thus,

$$P(U_{t+1} = u' \mid Y_t = y) = \prod_{j=1}^m \left[(1-\alpha) \mathbb{1}\{u'_j = y_j\} + \alpha \, \mathbb{1}\{u'_j \neq y_j\}\right].$$

#### Optimal Decoder

To choose the most likely next vector $$u'$$, we maximize the above product over all $$u' \in \{0,1\}^m$$.

Each bit contributes either:
- a factor $$1-\alpha$$ if we match the current bit $$y_j$$,
- a factor $$\alpha$$ if we flip it.

When $$\alpha < 0.5$$, matching gives the larger factor. Because bits are independent, maximizing the full product means maximizing each factor individually, giving

$$\hat{u}(y) = y.$$

(If $$\alpha > 0.5$$, the maximizing bitwise choice would be $$1-y$$; at $$\alpha = 0.5$$ all predictions are equally likely.)

In the predictive regime $$\alpha < 0.5$$, the optimal decoder is therefore

$$\hat{u}(Y_t) = Y_t.$$

#### Prediction Accuracy

Accuracy is

$$\text{Acc} = P(\hat{u}(Y_t) = U_{t+1}) = P(U_{t+1} = U_t).$$

Since each bit stays the same with probability $$1-\alpha$$,

$$P(U_{t+1} = U_t) = (1-\alpha)^m.$$

Thus

$$\text{Acc} = (1-\alpha)^m.$$

#### Energy Drift and Variance

Energy changes according to

$$\Delta E_t = r \, \mathbb{1}\{\hat{u}(Y_t) = U_{t+1}\} - c_\ell.$$

Let

$$Z_t = \mathbb{1}\{\hat{u}(Y_t) = U_{t+1}\},$$

so $$Z_t \sim \text{Bernoulli}(\text{Acc})$$.

Mean drift:

$$\mu = \mathbb{E}[\Delta E_t] = r(1-\alpha)^m - c_\ell.$$

Variance:

$$\sigma^2 = r^2 \, \text{Acc}(1 - \text{Acc}) = r^2 (1-\alpha)^m [1 - (1-\alpha)^m].$$

#### Survivability

Let

$$E_{t+1} = E_t + \Delta E_t, \quad E_0 > 0,$$

with absorption at $$E_t = 0$$.

From the diffusion approximation:

$$\Xi = 0 \quad \text{if } r(1-\alpha)^m \leq c_\ell,$$

and for $$r(1-\alpha)^m > c_\ell$$,

$$\Xi \approx 1 - \exp\left(-\frac{2E_0 (r(1-\alpha)^m - c_\ell)}{r^2 (1-\alpha)^m [1 - (1-\alpha)^m]}\right).$$

### 4.3.2 p-Estimator Neo: Full Derivation

We now consider a more complex case where the Neo contains internal feedback loops that create temporal dependencies. This requires computing the stationary distribution of the internal state Markov chain to determine prediction accuracy and survivability.

#### 4.3.2.1 Setting and Goal

The NeoVerse emits a binary percept stream

$$U_t \sim \text{Bernoulli}(p), \quad t = 0,1,2,\ldots$$

independently over time, with an unknown parameter $$p \in (0,1)$$. The Neo does not receive $$p$$; it only observes the bits $$U_t$$.

We consider a small Neo whose job is to:

1. Run its internal Lex dynamics driven by the input stream $$\{U_t\}$$.
2. Produce a prediction for the next percept using node $$A$$: $$\hat{U}_{t+1} = A(t+1)$$.
3. Achieve high next-bit prediction accuracy $$\text{Acc}(p) = P\big(A(t+1) = U(t+1)\big)$$, in the long run (stationary regime).
4. Use its internal stationary behavior as an implicit estimate of the bias $$p$$.

Because the stream is i.i.d. Bernoulli, the theoretical optimal predictor (with true $$p$$) is "always predict the majority bit," with accuracy

$$\text{Acc}^*(p) = \max\{p, 1-p\}.$$

So this Neo cannot ever reach 100% accuracy unless $$p \in \{0,1\}$$; the interesting question is how its architecture + feedback shape its stationary prediction accuracy and its implicit representation of $$p$$.

#### 4.3.2.2 Architecture of the p-Estimator Neo

The Neo has two internal nodes:

* **Node $$A$$** — the predictor node. Its state drives the output.
* **Node $$B$$** — a memory node that tracks recent behavior of $$A$$.

Node states are binary:

$$A(t), B(t) \in \{0,1\}.$$

We disable intrinsic node noise ($$\alpha_A = \alpha_B = 0$$) to isolate the effect of weights and feedback.

**Node $$A$$ (Predictor)**

Inputs to $$A$$:

* $$U_t$$: current percept
* $$A(t)$$: self-feedback
* $$B(t)$$: input from memory node

Lex update:

$$A(t+1) = H\big(2U_t + 1\cdot A(t) - 2\cdot B(t) - 1\big),$$

where $$H(x) = 1$$ if $$x \geq 0$$ and $$0$$ otherwise.

**Node $$B$$ (Memory)**

Inputs to $$B$$:

* $$A(t)$$: previous predictor state

Lex update:

$$B(t+1) = H\big(A(t) - 0.5\big).$$

So $$B(t+1) = 1$$ iff $$A(t) = 1$$; otherwise $$B(t+1) = 0$$.

In words: $$B$$ copies $$A$$ with a one-tick delay, providing a crude memory of whether $$A$$ was recently active.

**Prediction Rule**

At time $$t$$:

1. The Neo observes $$U_t$$.
2. It updates $$A(t+1), B(t+1)$$ via the rules above.
3. It uses $$\hat{U}_{t+1} = A(t+1)$$ as its prediction for the next percept $$U_{t+1}$$.

We then measure

$$\text{Acc}(p) = P\big(A(t+1) = U(t+1)\big)$$

in the stationary regime.

#### 4.3.2.3 Markov Chain over Internal States

Define the internal state:

$$S_t = (A(t), B(t)) \in \{0,1\}^2.$$

There are four possible internal states:

$$s_0 = (0,0), \quad s_1 = (0,1), \quad s_2 = (1,0), \quad s_3 = (1,1).$$

At each tick, given $$S_t$$ and $$U_t$$, the next state $$S_{t+1} = (A(t+1), B(t+1))$$ is deterministically defined by the Lex rules. Since $$U_t$$ is random with $$P(U_t = 1) = p$$, the process $$\{S_t\}$$ is a 4-state Markov chain with transition probabilities depending on $$p$$.

We now derive:

1. The state transition map $$(S_t, U_t) \mapsto S_{t+1}$$.
2. The transition matrix $$P(p)$$ over the 4 states.
3. The stationary distribution $$\pi(p)$$.
4. From that, the prediction accuracy $$\text{Acc}(p)$$.

**Deterministic Next State for Each $$S_t$$ and $$U_t$$**

We explicitly compute $$S_{t+1} = (A(t+1),B(t+1))$$ for all four states and both values of $$U_t$$.

Recall:

$$\begin{aligned} A(t+1) &= H(2U_t + A(t) - 2B(t) - 1),\\ B(t+1) &= H(A(t) - 0.5). \end{aligned}$$

**Case 1:** $$S_t = s_0 = (A,B)=(0,0)$$

* If $$U_t = 0$$: $$a_A = 2\cdot 0 + 0 - 2\cdot 0 - 1 = -1 \Rightarrow A(t+1)=0$$, $$a_B = 0 - 0.5 = -0.5 \Rightarrow B(t+1)=0$$. So $$S_{t+1} = (0,0) = s_0$$.
* If $$U_t = 1$$: $$a_A = 2\cdot 1 + 0 - 0 - 1 = 1 \Rightarrow A(t+1)=1$$, $$a_B = 0 - 0.5 = -0.5 \Rightarrow B(t+1)=0$$. So $$S_{t+1} = (1,0) = s_2$$.

**Case 2:** $$S_t = s_1 = (0,1)$$

* If $$U_t = 0$$: $$a_A = 0 + 0 - 2\cdot 1 - 1 = -3 \Rightarrow A(t+1)=0$$, $$a_B = 0 - 0.5 = -0.5 \Rightarrow B(t+1)=0$$. So $$S_{t+1} = (0,0) = s_0$$.
* If $$U_t = 1$$: $$a_A = 2\cdot 1 + 0 - 2\cdot 1 - 1 = -1 \Rightarrow A(t+1)=0$$, $$a_B = 0 - 0.5 = -0.5 \Rightarrow B(t+1)=0$$. So $$S_{t+1} = (0,0) = s_0$$.

Thus from $$s_1$$ we always go to $$s_0$$, regardless of $$U_t$$.

**Case 3:** $$S_t = s_2 = (1,0)$$

* If $$U_t = 0$$: $$a_A = 0 + 1 - 0 - 1 = 0 \Rightarrow A(t+1)=1$$, $$a_B = 1 - 0.5 = 0.5 \Rightarrow B(t+1)=1$$. So $$S_{t+1} = (1,1) = s_3$$.
* If $$U_t = 1$$: $$a_A = 2\cdot 1 + 1 - 0 - 1 = 2 \Rightarrow A(t+1)=1$$, $$a_B = 1 - 0.5 = 0.5 \Rightarrow B(t+1)=1$$. So $$S_{t+1} = (1,1) = s_3$$.

From $$s_2$$ we always go to $$s_3$$, regardless of $$U_t$$.

**Case 4:** $$S_t = s_3 = (1,1)$$

* If $$U_t = 0$$: $$a_A = 0 + 1 - 2\cdot 1 - 1 = -2 \Rightarrow A(t+1)=0$$, $$a_B = 1 - 0.5 = 0.5 \Rightarrow B(t+1)=1$$. So $$S_{t+1} = (0,1) = s_1$$.
* If $$U_t = 1$$: $$a_A = 2\cdot 1 + 1 - 2\cdot 1 - 1 = 0 \Rightarrow A(t+1)=1$$, $$a_B = 1 - 0.5 = 0.5 \Rightarrow B(t+1)=1$$. So $$S_{t+1} = (1,1) = s_3$$.

So from $$s_3$$: $$U_t = 0 \Rightarrow s_1$$; $$U_t = 1 \Rightarrow s_3$$.

**Transition Matrix $$P(p)$$**

Now we incorporate the randomness of $$U_t$$. Since $$P(U_t = 1) = p$$, $$P(U_t = 0) = 1-p$$, we can compute the Markov transition probabilities between the 4 states.

Label states in order $$(s_0,s_1,s_2,s_3)$$.

* From $$s_0$$:
    * $$U_t=0$$ (prob $$1-p$$) → $$s_0$$
    * $$U_t=1$$ (prob $$p$$) → $$s_2$$
* Row 0: $$P_{0\rightarrow\cdot} = \big(1-p,\;0,\;p,\;0\big)$$.

* From $$s_1$$:
    * Always goes to $$s_0$$
* Row 1: $$P_{1\rightarrow\cdot} = \big(1,\;0,\;0,\;0\big)$$.

* From $$s_2$$:
    * Always goes to $$s_3$$
* Row 2: $$P_{2\rightarrow\cdot} = \big(0,\;0,\;0,\;1\big)$$.

* From $$s_3$$:
    * $$U_t=0$$ (prob $$1-p$$) → $$s_1$$
    * $$U_t=1$$ (prob $$p$$) → $$s_3$$
* Row 3: $$P_{3\rightarrow\cdot} = \big(0,\;1-p,\;0,\;p\big)$$.

Collecting everything, the transition matrix is

$$P(p) = \begin{pmatrix} 1-p & 0 & p & 0 \\ 1 & 0 & 0 & 0 \\ 0 & 0 & 0 & 1 \\ 0 & 1-p & 0 & p \end{pmatrix}.$$

**Stationary Distribution $$\pi(p)$$**

Let $$\pi(p) = (\pi_0,\pi_1,\pi_2,\pi_3)$$ be the stationary distribution over states $$s_0,\dots,s_3$$. It satisfies:

$$\pi = \pi P(p), \quad \pi_0+\pi_1+\pi_2+\pi_3 = 1.$$

From $$\pi = \pi P$$, we get:

1. Coordinate 0: $$\pi_0 = \pi_0(1-p) + \pi_1$$.
2. Coordinate 1: $$\pi_1 = (1-p)\pi_3$$.
3. Coordinate 2: $$\pi_2 = p\pi_0$$.
4. Coordinate 3: $$\pi_3 = \pi_2 + p\pi_3$$.

We now solve step by step.

From (4):

$$\pi_3 = \pi_2 + p\pi_3 \quad\Rightarrow\quad \pi_3(1-p) = \pi_2 \quad\Rightarrow\quad \pi_3 = \frac{\pi_2}{1-p}.$$

From (3) we know $$\pi_2 = p\pi_0$$, so:

$$\pi_3 = \frac{p\pi_0}{1-p}.$$

From (2):

$$\pi_1 = (1-p)\pi_3 = (1-p)\cdot \frac{p\pi_0}{1-p} = p\pi_0.$$

From (1):

$$\pi_0 = (1-p)\pi_0 + \pi_1 \quad\Rightarrow\quad \pi_0 - (1-p)\pi_0 = \pi_1 \quad\Rightarrow\quad p\pi_0 = \pi_1,$$

which is consistent with what we already got, so no new constraint.

Now apply normalization:

$$\pi_0 + \pi_1 + \pi_2 + \pi_3 = 1.$$

Substitute $$\pi_1 = p\pi_0$$, $$\pi_2 = p\pi_0$$, and $$\pi_3 = \dfrac{p\pi_0}{1-p}$$:

$$\pi_0 + p\pi_0 + p\pi_0 + \frac{p\pi_0}{1-p} = 1.$$

Factor $$\pi_0$$:

$$\pi_0\left(1 + 2p + \frac{p}{1-p}\right) = 1.$$

Compute the bracket:

$$1 + 2p + \frac{p}{1-p} = \frac{(1-p)(1+2p) + p}{1-p} = \frac{1 + 2p - p - 2p^2 + p}{1-p} = \frac{1 + 2p - 2p^2}{1-p}.$$

Define

$$D(p) = 1 + 2p - 2p^2.$$

Then:

$$\pi_0 \cdot \frac{D(p)}{1-p} = 1 \quad\Rightarrow\quad \pi_0 = \frac{1-p}{D(p)}.$$

And therefore:

$$\begin{aligned} \pi_1 &= p \pi_0 = \frac{p(1-p)}{D(p)},\\[4pt] \pi_2 &= p \pi_0 = \frac{p(1-p)}{D(p)},\\[4pt] \pi_3 &= \frac{p}{1-p}\pi_0 = \frac{p}{1-p}\cdot \frac{1-p}{D(p)} = \frac{p}{D(p)}. \end{aligned}$$

So the stationary distribution is:

$$\boxed{ \pi(p) = \left( \frac{1-p}{1+2p-2p^2},\; \frac{p(1-p)}{1+2p-2p^2},\; \frac{p(1-p)}{1+2p-2p^2},\; \frac{p}{1+2p-2p^2} \right). }$$

**Stationary Probability that $$A = 1$$**

The prediction node $$A$$ is 1 in states $$s_2 = (1,0)$$ and $$s_3 = (1,1)$$. Thus:

$$P_\pi(A(t) = 1) = \pi_2 + \pi_3 = \frac{p(1-p)}{D(p)} + \frac{p}{D(p)} = \frac{p(2-p)}{D(p)},$$

where $$D(p) = 1 + 2p - 2p^2$$.

So:

$$\boxed{ P_\pi(A=1) = \frac{p(2-p)}{1+2p-2p^2}. }$$

Since the chain is stationary, this is also the distribution of $$A(t+1)$$, $$A(t+2)$$, etc.

**Prediction Accuracy $$\text{Acc}(p)$$**

We now derive $$\text{Acc}(p) = P\big(A(t+1) = U(t+1)\big)$$ in closed form.

Key points:

* $$U_{t+1}$$ is independent of $$(S_t, U_t)$$ and has distribution $$\text{Bernoulli}(p)$$.
* Under stationarity, the marginal distribution of $$A(t+1)$$ is the same as that of $$A(t)$$, i.e., $$P(A(t+1)=1) = P_\pi(A=1) = q(p) = \frac{p(2-p)}{D(p)}$$. So $$P(A(t+1)=0) = 1 - q(p)$$.

Given these, we can write:

$$\begin{aligned} \text{Acc}(p) &= P(A(t+1)=1, U_{t+1}=1) + P(A(t+1)=0, U_{t+1}=0)\\ &= P(A(t+1)=1)\,P(U_{t+1}=1) + P(A(t+1)=0)\,P(U_{t+1}=0)\\ &= q(p)\cdot p + (1-q(p))\cdot (1-p). \end{aligned}$$

Plug $$q(p) = \dfrac{p(2-p)}{D(p)}$$:

$$\text{Acc}(p) = \frac{p(2-p)}{D(p)}\cdot p + \left(1 - \frac{p(2-p)}{D(p)}\right)\cdot (1-p).$$

Using the alternative form:

$$\text{Acc}(p) = (1-p) + (2p-1)\,q(p) = (1-p) + (2p-1)\frac{p(2-p)}{D(p)}.$$

Computing the numerator explicitly:

Let $$\text{Acc}(p) = \frac{N(p)}{D(p)}$$.

Then

$$N(p) = (1-p)D(p) + (2p-1)p(2-p).$$

First term:

$$(1-p)D(p) = (1-p)(1+2p-2p^2) = 1 + 2p - 2p^2 - p -2p^2 + 2p^3 = 1 + p - 4p^2 + 2p^3.$$

Second term:

$$(2p-1)p(2-p) = p(2p-1)(2-p).$$

Compute $$(2p-1)(2-p)$$:

$$(2p-1)(2-p) = 4p - 2p^2 - 2 + p = -2 + 5p - 2p^2.$$

Multiply by $$p$$:

$$(2p-1)p(2-p) = -2p + 5p^2 - 2p^3.$$

Add both contributions:

$$\begin{aligned} N(p) &= \big(1 + p - 4p^2 + 2p^3\big) + \big(-2p + 5p^2 - 2p^3\big)\\ &= 1 + (p - 2p) + (-4p^2 + 5p^2) + (2p^3 - 2p^3)\\ &= 1 - p + p^2. \end{aligned}$$

Therefore,

$$\boxed{ \text{Acc}(p) = \frac{1 - p + p^2}{1 + 2p - 2p^2}. }$$

For sanity checks:

* $$p = 0.5$$: Numerator $$= 1 - 0.5 + 0.25 = 0.75$$, Denominator $$= 1 + 1 - 0.5 = 1.5$$, $$\text{Acc}(0.5) = 0.75/1.5 = 0.5$$ (chance level, as expected).
* $$p = 0.2$$: Numerator $$= 1 - 0.2 + 0.04 = 0.84$$, Denominator $$= 1 + 0.4 - 0.08 = 1.32$$, $$\text{Acc}(0.2) \approx 0.636$$.
* $$p = 0.8$$: Numerator $$= 1 - 0.8 + 0.64 = 0.84$$, Denominator $$= 1 + 1.6 - 1.28 = 1.32$$, $$\text{Acc}(0.8) \approx 0.636$$.

Note that $$\text{Acc}(p) \leq \max(p,1-p)$$ for all $$p \in (0,1)$$; the Neo does not reach the Bayes limit.

#### 4.3.2.4 Simulation Results (Next-Bit Prediction)

We simulate the Neo for $$T = 200{,}000$$ ticks for each $$p \in \{0.2,0.5,0.8\}$$.

Procedure:

1. Sample $$U_0, \dots, U_T$$ i.i.d. $$\text{Bernoulli}(p)$$.
2. Initialize $$A(0)=B(0)=0$$.
3. For $$t = 0,\dots,T-1$$:
    * Update $$A(t+1),B(t+1)$$ using the Lex rules.
    * Use $$A(t+1)$$ as prediction for $$U_{t+1}$$.
4. Compute empirical accuracy $$\hat{\text{Acc}}(p) = \frac{1}{T}\sum_{t=0}^{T-1} \mathbf{1}\{A(t+1)=U_{t+1}\}$$.

Sample outcomes ($$T$$ large):

| $$p$$ | Theoretical $$\text{Acc}(p)$$ | Empirical $$\hat{\text{Acc}}(p)$$ (example) |
|-------|------------------------------|---------------------------------------------|
| 0.2   | $$\approx 0.636$$             | $$\approx 0.638$$                           |
| 0.5   | $$0.5$$                       | $$\approx 0.501$$                           |
| 0.8   | $$\approx 0.636$$             | $$\approx 0.634$$                           |

