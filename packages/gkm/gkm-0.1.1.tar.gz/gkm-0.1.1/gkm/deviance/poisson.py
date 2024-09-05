import numpy as np
from scipy.special import xlogy
from .base import Deviance


class Poisson(Deviance):
    def log_density(self, y, t):
        return y * t - np.exp(t)

    def __call__(self, y, t):
        return -self.log_density(y, t) - (y - xlogy(y, y))

    def param2mean(self, t):
        return np.exp(t)

    def dparam2mean(self, t):
        return np.exp(t)

    def mean2param(self, mu):
        return np.log(mu)

    def dmean2param(self, mu):
        return 1.0 / mu
