import numpy as np
from scipy.special import xlogy
from .base import Deviance


class Binomial(Deviance):
    def __init__(self, n=1):
        super().__init__()
        self.n = n

    def log_density(self, y, t):
        return y * t - self.n * np.log(1.0 + np.exp(t))

    def __call__(self, y, t):
        ell = -self.log_density(y, t)
        ell -= xlogy(self.n, self.n) - xlogy(y, y) - xlogy(self.n - y, self.n - y)
        return ell

    def param2mean(self, t):
        return self.n / (1.0 + np.exp(-t))

    def dparam2mean(self, t):
        ent = np.exp(-t)
        return self.n / (1.0 + ent) ** 2 * ent

    def mean2param(self, mu):
        return -np.log(self.n / mu - 1.0)

    def dmean2param(self, mu):
        return 1.0 / mu + 1.0 / (self.n - mu)
