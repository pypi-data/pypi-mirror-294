import numpy as np
from .base import Link


class Logit(Link):
    def __init__(self, n):
        self.n = n

    def _clean(self, x):
        return np.clip(x, np.finfo(float).eps, self.n - np.finfo(float).eps)

    def __call__(self, mu):
        mu = self._clean(mu)
        return np.log(mu / (self.n - mu))

    def deriv(self, mu):
        mu = self._clean(mu)
        return self.n / (mu * (self.n - mu))

    def deriv2(self, mu):
        mu = self._clean(mu)
        return (2.0 * mu - self.n) / (mu * (self.n - mu)) ** 2

    def inverse(self, t):
        t = np.clip(t, -709.78, 709.78)
        return self.n / (1.0 + np.exp(-t))

    def inverse_deriv(self, t):
        t = np.clip(t, -709.78, 709.78)
        et = np.exp(t)
        return self.n * et / (1.0 + et) ** 2

    def inverse_deriv2(self, t):
        t = np.clip(t, -709.78, 709.78)
        et = np.exp(t)
        return self.n * et * (1.0 - et) / (1.0 + et) ** 2
