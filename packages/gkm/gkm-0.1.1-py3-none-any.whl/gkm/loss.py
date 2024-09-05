import numpy as np


class Loss:
    def __call__(self, y, t):
        raise NotImplementedError()

    def deriv(self, y, t):
        raise NotImplementedError()

    def deriv2(self, y, t):
        raise NotImplementedError()

    def param2mean(self, t):
        return t

    def dparam2mean(self, t):
        return np.ones_like(t)

    def mean2param(self, mu):
        return mu

    def dmean2param(self, mu):
        t = self.mean2param(mu)
        return 1.0 / self.dparam2mean(t)


def compute(y, t, loss, derivative=False):
    ell = loss(y, t)
    if not derivative:
        return ell
    dell = loss.deriv(y, t)
    ddell = loss.deriv2(y, t)
    return ell, dell, ddell
