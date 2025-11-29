import numpy as np


def heaviside(x):
    return 1 if x >= 0 else 0


class DelayMotif:
    def __init__(self,
                 w1_V2=1.0, w1_U=0.0, alpha1=1.0, b1=-1.5, r=0.5,
                 w2=1.0, alpha2=1.0, b2=-1.5, s=0.5):
        """
        Initialize the 2-node delay motif.

        Node 1:
            V1_t = H(w1_V2 * V2_{t-1} + w1_U * U_t + alpha1 * eta1 + b1)
            eta1 ~ Bernoulli(r)

        Node 2:
            V2_t = H(w2 * V1_t + alpha2 * eta2 + b2)
            eta2 ~ Bernoulli(s)

        Y_t = V2_t
        """

        self.w1_V2 = w1_V2
        self.w1_U  = w1_U
        self.alpha1 = alpha1
        self.b1 = b1
        self.r = r  # noise probability for V1

        self.w2 = w2
        self.alpha2 = alpha2
        self.b2 = b2
        self.s = s  # noise probability for V2

        # internal memory state for V2
        self.V2 = 0  # initialize however you want

    def step(self, U_t):
        """Simulate one time step given input U_t."""

        # noise bits
        eta1 = np.random.rand() < self.r
        eta2 = np.random.rand() < self.s

        # compute V1_t
        V1_t = heaviside(
            self.w1_V2 * self.V2
            + self.w1_U * U_t
            + self.alpha1 * eta1
            + self.b1
        )

        # compute V2_t
        V2_t = heaviside(
            self.w2 * V1_t
            + self.alpha2 * eta2
            + self.b2
        )

        # output
        Y_t = V2_t

        # update internal memory
        self.V2 = V2_t

        return V1_t, V2_t, Y_t


# ---------------------------------------------------------
# Example usage
# ---------------------------------------------------------

if __name__ == "__main__":
    motif = DelayMotif(
        w1_V2=1.0,  # weight from V2_{t-1} to V1_t
        w1_U=0.0,   # weight from U_t to V1_t (set nonzero to use U_t)
        alpha1=1.0,
        b1=-1.5,
        r=0.3,      # Bernoulli parameter for V1

        w2=1.0,     # weight from V1_t to V2_t
        alpha2=1.0,
        b2=-1.5,
        s=0.7       # Bernoulli parameter for V2
    )

    # simulate with some input sequence
    inputs = [0,1,1,0,1,0,0,1,1,0]
    print("U_t | V1_t | V2_t (=Y_t)")
    for u in inputs:
        V1, V2, Y = motif.step(u)
        print(f" {u}     {V1}       {V2}")

