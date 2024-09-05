import numpy as np
from .base import Link


class Identity(Link):
    def __call__(self, mu):
        return mu

    def deriv(self, mu):
        return np.ones_like(mu)

    def deriv2(self, mu):
        return np.zeros_like(mu)

    def inverse(self, t):
        return t

    def inverse_deriv(self, t):
        return np.ones_like(t)

    def inverse_deriv2(self, t):
        return np.zeros_like(t)
