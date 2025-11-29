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

We start with one of the simplest—and most revealing—motifs: a "copy Neo" interacting with an $$m$$-bit Markov NeoVerse projection. Despite its simplicity, this setup already exhibits clear trade-offs between environmental noise, task dimensionality, and reward structure. We will derive closed forms for $$\Xi$$ under two reward regimes: one where Sparks are granted only when the entire prediction vector is correct, and one where Sparks are proportional to the fraction of correctly predicted bits. In the second case, the Neo retains the last $$L$$ percepts, producing an $$L$$-dimensional internal state that evolves as a shift register. Its stationary distribution becomes non-trivial, reflecting the joint structure induced by noise, temporal aggregation, and the Lex update rule.

### 4.3.1 m-Bit Markov NeoVerse and the Copy Neo 

We consider an $$m$$-bit NeoVerse (NV) projection $$U_t = (U_t(1), \ldots, U_t(m)) \in \{0,1\}^m$$, where each coordinate evolves as an independent binary Markov chain with flip probability $$\alpha \in [0,1]$$:

$$P(U_{t+1}(j) \neq U_t(j)) = \alpha, \quad P(U_{t+1}(j) = U_t(j)) = 1 - \alpha.$$

Each coordinate is symmetric, so in its stationary regime

$$P(U_t(j) = 0) = P(U_t(j) = 1) = \frac{1}{2}.$$

A copy Neo directly stores the current NV projection, so its internal state is $$X_t = U_t$$, and its output is the readout $$Y_t = g(X_t) = X_t$$.

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

Using Bayes' rule,

$$P(U^+ = u' \mid Y = y) = \frac{P(U^+ = u', \, Y = y)}{P(Y = y)} = \prod_{j=1}^m \left[(1-\alpha) \mathbb{1}\{u'_j = y_j\} + \alpha \, \mathbb{1}\{u'_j \neq y_j\}\right].$$

The most likely next NV is obtained by maximizing this expression; the maximizing pattern is $$u' = y$$. Hence the optimal decoder is

$$\hat{u}(y) = y.$$

#### Prediction Accuracy

The accuracy is

$$\text{Acc} = P(\hat{u}(Y) = U^+) = \sum_{y \in \{0,1\}^m} P(Y = y) \, P(U^+ = y \mid Y = y).$$

Using $$P(Y = y) = 2^{-m}$$ and

$$P(U^+ = y \mid Y = y) = \prod_{j=1}^m (1-\alpha) = (1-\alpha)^m,$$

we obtain

$$\text{Acc} = (1-\alpha)^m.$$

#### Energy Drift and Variance

At each tick,

$$\Delta E_t = r \, \mathbb{1}\{\hat{u}(Y_t) = U^+\} - c_\ell.$$

Since correctness is Bernoulli with success probability $$\text{Acc}$$,

$$\mu = \mathbb{E}[\Delta E_t] = r \, \text{Acc} - c_\ell = r(1-\alpha)^m - c_\ell,$$

$$\sigma^2 = \text{Var}(\Delta E_t) = r^2 \, \text{Acc}(1 - \text{Acc}) = r^2 (1-\alpha)^m [1 - (1-\alpha)^m].$$

#### Survivability

Let $$E_t$$ evolve as

$$E_{t+1} = E_t + \Delta E_t, \quad E_0 > 0,$$

with absorption at $$E_t = 0$$. Using the diffusion approximation,

$$\Xi = 0 \quad \text{if } r \, \text{Acc} \leq c_\ell,$$

and otherwise

$$\Xi \approx 1 - \exp\left(-\frac{2\mu E_0}{\sigma^2}\right) = 1 - \exp\left(-\frac{2E_0}{r^2 (1-\alpha)^m [1 - (1-\alpha)^m]} (r(1-\alpha)^m - c_\ell)\right).$$

### 4.3.2 Majority-over-3 Neo

We now consider a Neo whose internal state consists of the last three observations of a 1-bit NeoVerse (NV). The NV is a symmetric binary Markov chain $$U_t \in \{0,1\}$$ with $$P(U_{t+1} \neq U_t) = \alpha$$ and $$P(U_{t+1} = U_t) = 1 - \alpha$$. In stationarity, $$P(U_t = 0) = P(U_t = 1) = \frac{1}{2}$$.

The Neo stores the last three NV values $$X_t = (U_t, U_{t-1}, U_{t-2}) \in \{0,1\}^3$$, and outputs the majority of these three bits, $$Y_t = g(X_t) = \text{Maj}(X_t) \in \{0,1\}$$. As a predictor, the Neo uses the simple rule $$\hat{u}(Y_t) = Y_t$$, i.e., it predicts that the next NV bit $$U_{t+1}$$ will equal the majority of the last three observations.

#### Joint Stationary Distribution $$\pi(x, u)$$

We analyze the joint process $$(X_t, U_t)$$ in its stationary regime. The joint stationary distribution is

$$\pi(x, u) = \lim_{t \to \infty} P(X_t = x, \, U_t = u),$$

with the constraint that the first coordinate of $$x$$ must equal the current NV state: $$x = (x_0, x_1, x_2)$$, $$x_0 = U_t = u$$. Hence $$\pi(x, u) = 0$$ if $$x_0 \neq u$$, and

$$\pi(x, u) = \pi_3(x) \, \mathbb{1}\{x_0 = u\},$$

where $$\pi_3(x) = P(X_t = x)$$ is the stationary distribution over 3-bit windows.

To compute $$\pi_3(x)$$, interpret $$x_0 = U_t$$, $$x_1 = U_{t-1}$$, $$x_2 = U_{t-2}$$. In stationarity,

$$\pi_3(x) = P(U_{t-2} = x_2) \, P(U_{t-1} = x_1 \mid U_{t-2} = x_2) \, P(U_t = x_0 \mid U_{t-1} = x_1).$$

The base term is $$P(U_{t-2} = x_2) = \frac{1}{2}$$. The Markov transitions are

$$P(U_{s+1} = a \mid U_s = b) = \begin{cases} 1-\alpha, & a = b, \\ \alpha, & a \neq b. \end{cases}$$

Define the number of flips inside the 3-bit pattern

$$\Delta(x) = \mathbb{1}\{x_1 \neq x_0\} + \mathbb{1}\{x_2 \neq x_1\} \in \{0,1,2\}.$$

Then the number of non-flips is $$2 - \Delta(x)$$. The stationary probability of a given pattern is

$$\pi_3(x) = \frac{1}{2} (1-\alpha)^{2-\Delta(x)} \alpha^{\Delta(x)}.$$

Thus the joint SD is

$$\pi(x, u) = \frac{1}{2} (1-\alpha)^{2-\Delta(x)} \alpha^{\Delta(x)} \, \mathbb{1}\{x_0 = u\}.$$

#### Accuracy of the Majority-3 Predictor

We now compute the prediction accuracy

$$\text{Acc}_3 = P(\hat{u}(Y_t) = U_{t+1}) = P(Y_t = U_{t+1}).$$

Because $$Y_t = g(X_t) = \text{Maj}(X_t)$$ and $$U_{t+1}$$ depends only on $$U_t = x_0$$, we can write

$$\text{Acc}_3 = \sum_{x, u} \pi(x, u) \, P(U_{t+1} = g(x) \mid U_t = u).$$

Using $$\pi(x, u) = \pi_3(x) \, \mathbb{1}\{x_0 = u\}$$,

$$\text{Acc}_3 = \sum_x \pi_3(x) \, P(U_{t+1} = \text{Maj}(x) \mid U_t = x_0).$$

The NV transition rule gives

$$P(U_{t+1} = \text{Maj}(x) \mid U_t = x_0) = \begin{cases} 1-\alpha, & \text{Maj}(x) = x_0, \\ \alpha, & \text{Maj}(x) \neq x_0. \end{cases}$$

Define $$m(x) = \text{Maj}(x)$$, $$A = \{x : m(x) = x_0\}$$. Then

$$\text{Acc}_3 = \sum_{x \in A} \pi_3(x) (1-\alpha) + \sum_{x \notin A} \pi_3(x) \alpha = (1-\alpha) \sum_{x \in A} \pi_3(x) + \alpha \left(1 - \sum_{x \in A} \pi_3(x)\right).$$

Let

$$q_3 := \sum_{x \in A} \pi_3(x) = P(m(X_t) = U_t),$$

the probability that the majority of the last three bits agrees with the current bit. Then

$$\text{Acc}_3 = \alpha + (1-2\alpha) q_3.$$

It remains to compute $$q_3$$ under $$\pi_3$$. We enumerate the eight patterns $$x = (x_0, x_1, x_2) \in \{0,1\}^3$$, their $$\Delta(x)$$, and whether $$m(x) = x_0$$:

- **000**: $$\Delta = 0$$, $$m(x) = 0 = x_0$$ (in $$A$$).
- **001**: $$\Delta = 1$$, $$m(x) = 0 = x_0$$ (in $$A$$).
- **010**: $$\Delta = 2$$, $$m(x) = 0 = x_0$$ (in $$A$$).
- **011**: $$\Delta = 1$$, $$m(x) = 1 \neq x_0$$ (not in $$A$$).
- **100**: $$\Delta = 1$$, $$m(x) = 0 \neq x_0$$ (not in $$A$$).
- **101**: $$\Delta = 2$$, $$m(x) = 1 = x_0$$ (in $$A$$).
- **110**: $$\Delta = 1$$, $$m(x) = 1 = x_0$$ (in $$A$$).
- **111**: $$\Delta = 0$$, $$m(x) = 1 = x_0$$ (in $$A$$).

So the patterns in $$A$$ are: **000, 001, 010, 101, 110, 111**.

Using $$\pi_3(x) = \frac{1}{2} (1-\alpha)^{2-\Delta(x)} \alpha^{\Delta(x)}$$, group them by $$\Delta(x)$$:

- **$$\Delta = 0$$**: patterns **000, 111**: contribution $$2 \cdot \frac{1}{2} (1-\alpha)^2 = (1-\alpha)^2$$.
- **$$\Delta = 1$$**: patterns **001, 110**: contribution $$2 \cdot \frac{1}{2} (1-\alpha)\alpha = (1-\alpha)\alpha$$.
- **$$\Delta = 2$$**: patterns **010, 101**: contribution $$2 \cdot \frac{1}{2} \alpha^2 = \alpha^2$$.

Thus

$$q_3 = (1-\alpha)^2 + (1-\alpha)\alpha + \alpha^2.$$

Expanding, $$(1-\alpha)^2 = 1 - 2\alpha + \alpha^2$$, so

$$q_3 = 1 - 2\alpha + \alpha^2 + \alpha - \alpha^2 + \alpha^2 = 1 - \alpha + \alpha^2.$$

Hence $$q_3 = 1 - \alpha + \alpha^2$$.

Substituting into $$\text{Acc}_3 = \alpha + (1-2\alpha) q_3$$ and simplifying,

$$\text{Acc}_3 = \alpha + (1-2\alpha)(1-\alpha+\alpha^2) = 1 - 2\alpha + 3\alpha^2 - 2\alpha^3.$$

Thus the prediction accuracy of the majority-over-3 Neo is

$$\text{Acc}_3 = 1 - 2\alpha + 3\alpha^2 - 2\alpha^3.$$

#### Energy Drift, Variance, and Survivability

As before, let the Neo gain $$r > 0$$ Nex units when the prediction is correct and pay a living cost $$c_\ell > 0$$ every tick. The per-tick energy increment is

$$\Delta E_t = r \, \mathbb{1}\{\hat{u}(Y_t) = U_{t+1}\} - c_\ell.$$

Under stationarity, correctness is Bernoulli with success probability $$\text{Acc}_3$$. Therefore

$$\mu = \mathbb{E}[\Delta E_t] = r \, \text{Acc}_3 - c_\ell = r(1-2\alpha+3\alpha^2-2\alpha^3) - c_\ell,$$

$$\sigma^2 = \text{Var}(\Delta E_t) = r^2 \text{Acc}_3 (1 - \text{Acc}_3) = r^2 (1-2\alpha+3\alpha^2-2\alpha^3) [1 - (1-2\alpha+3\alpha^2-2\alpha^3)].$$

Let $$E_t$$ evolve as

$$E_{t+1} = E_t + \Delta E_t, \quad E_0 > 0,$$

with absorption at $$E_t = 0$$. Using the same diffusion approximation as before, the survivability $$\Xi_3$$ satisfies

$$\Xi_3 = 0 \quad \text{if } r \, \text{Acc}_3 \leq c_\ell,$$

and when $$r \, \text{Acc}_3 > c_\ell$$,

$$\Xi_3 \approx 1 - \exp\left(-\frac{2(r \, \text{Acc}_3 - c_\ell) E_0}{r^2 \text{Acc}_3 (1 - \text{Acc}_3)}\right),$$

with $$\text{Acc}_3 = 1 - 2\alpha + 3\alpha^2 - 2\alpha^3$$.

This completes the SD-based derivation of the majority-over-3 Neo.

### 4.3.3 Structural Motif for Majority-over-3 Neo

The stationary distribution derived for the Majority-over-3 Neo is not arbitrary: it is a direct mathematical consequence of a specific Neo structure capable of representing a temporal window of recent inputs and applying a deterministic majority Lex transformation over that window. It is therefore important to understand what minimal structural motif yields such a stationary process.

The central requirement is that the Neo must internally store the previous values of the NeoVerse (NV) input $$X_t \in \{0,1\}$$, so that its output at tick $$t$$ can compute $$\text{Maj}(X_t, X_{t-1}, X_{t-2})$$. Since a Neo does not have direct access to past values of $$X_t$$, the temporal window must be constructed inside the Neo's internal state through its Lex updates. This is achieved by a simple chain of memory nodes that act as a shift register, automatically producing the internal state whose stationary distribution we derived earlier.
