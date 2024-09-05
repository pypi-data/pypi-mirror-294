from .base import Deviance
from ..helpers import safe_log


class Exponential(Deviance):
    def log_density(self, y, t):
        return y * t + safe_log(-t)

    def __call__(self, y, t):
        return -self.log_density(y, t) - 1 - safe_log(y)

    def param2mean(self, t):
        return -1.0 / t

    def dparam2mean(self, t):
        return 1.0 / t**2

    def mean2param(self, mu):
        return -1.0 / mu

    def dmean2param(self, mu):
        return 1.0 / mu**2
