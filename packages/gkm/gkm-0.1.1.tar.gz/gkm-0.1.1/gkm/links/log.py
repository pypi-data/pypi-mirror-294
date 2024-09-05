import numpy as np
from .base import Link


class Log(Link):
    def _clean(self, x):
        return np.clip(x, np.finfo(float).eps, np.inf)

    def __call__(self, mu):
        mu = self._clean(mu)
        return np.log(mu)

    def deriv(self, mu):
        mu = self._clean(mu)
        return 1.0 / mu

    def deriv2(self, mu):
        mu = self._clean(mu)
        return -1.0 / mu**2

    def inverse(self, t):
        t = np.clip(t, -709.78, 709.78)
        return np.exp(t)

    def inverse_deriv(self, t):
        t = np.clip(t, -709.78, 709.78)
        return np.exp(t)

    def inverse_deriv2(self, t):
        t = np.clip(t, -709.78, 709.78)
        return np.exp(t)
