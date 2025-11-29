# Chapter {CH} — Micro Static Analysis of a Single Neo

A Neo survives by predicting the NeoVerse (NV). At every tick, it receives a small snapshot of the world—$$m$$ binary inputs $$U_t \in \{0,1\}^m$$—and updates its internal state according to the Lex rule. From this updated state it produces an output vector $$Y_t$$, interpreted as its prediction of the next NV state $$U_{t+1}$$. Correct predictions generate Sparks, which increase the Neo's Nex. Regardless of correctness, each update consumes a fixed amount of Nex simply to remain alive.

In the broader Neosis framework, a Neo may improve its predictive ability through in-life plasticity or through evolutionary processes. However, this chapter focuses on the static case, where the Neo's structure and parameters are fixed. In this setting, the Neo does not adjust its weights or topology; it behaves exactly according to the computation encoded in its architecture at birth.

Because the computation is fixed, the Neo eventually settles into a long-run statistical pattern determined entirely by its structure and by the statistics of the NV. Its internal states, its outputs, and their relationship to NV inputs become time-invariant. This is the stationary regime of a Neo, and understanding this regime is the central goal of micro analysis.

The purpose of this chapter is to determine how much predictive ability a fixed Neo possesses purely from its stationary behavior. By characterizing how its stationary output relates to the NV's stationary dynamics, we can determine its expected Nex gain, its expected Nex loss, and ultimately whether it will survive.

## {CH}.1 Neo as a Predictive System

Prediction is only meaningful when the environment exhibits stable statistical structure. If the NeoVerse changed its distribution over time—drifting, aging, or altering its transition rules—then a static Neo could not maintain predictive accuracy. Even though learning-capable Neos will be treated later, the static Neo analyzed here can only exploit whatever statistical regularities are already present. Its predictive power depends entirely on whether the relationship between $$U_t$$ and $$U_{t+1}$$ remains consistent over time.

For this reason, we assume that the projection of the NeoVerse that a Neo perceives is a stationary stochastic process. As discussed in earlier chapters, a Neo does not experience the full NeoVerse; it only receives a limited projection of it through its m-bit input channel. It is this projected process, not the full NV, that must exhibit stable statistics. Stationarity does not require periodicity. A process may vary dramatically from moment to moment and still be stationary if its probability distribution does not change over time. What matters is that

$$P(U_t = u) = P(U_{t+1} = u) \quad \text{and} \quad P(U_{t+1} \mid U_t) \text{ is independent of } t.$$

Under this assumption, the joint distribution of the Neo's internal state and the current NV input,

$$\pi(x, u) = \lim_{t \to \infty} P(X_t = x, \, U_t = u),$$

converges to a well-defined stationary distribution. All predictive properties of the Neo derive from this object. Its output distribution is obtained by marginalizing the internal state, and its predictive performance is obtained by examining how its stationary output relates to the NV's next state.

A stationary NV therefore makes micro analysis possible: it ensures that a fixed Neo has a well-defined, time-invariant predictive relationship with the environment.

## {CH}.2 Neo's Survivability

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
