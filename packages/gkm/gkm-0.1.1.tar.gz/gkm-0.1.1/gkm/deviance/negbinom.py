import numpy as np
from scipy.special import xlogy
from .base import Deviance
from ..helpers import safe_log


class NegativeBinomial(Deviance):
    def __init__(self, r=1):
        self.r = r

    def log_density(self, y, t):
        return y * t + self.r * safe_log(1.0 - np.exp(t))

    def __call__(self, y, t):
        r = self.r
        ell = -self.log_density(y, t)
        ell += xlogy(r, r) - xlogy(y + r, y + r) + xlogy(y, y)
        return ell

    def param2mean(self, t):
        return self.r * (1.0 / (1.0 - np.exp(t)) - 1.0)

    def dparam2mean(self, t):
        et = np.exp(t)
        return self.r * et / (1.0 - et) ** 2

    def mean2param(self, mu):
        return np.log(mu / (self.r + mu))

    def dmean2param(self, mu):
        return 1.0 / mu - 1.0 / (self.r + mu)
