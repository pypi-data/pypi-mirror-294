import numpy as np
from .base import Link
from ..helpers import safe_exp


class Geometric(Link):
    def _clean(self, x):
        return np.clip(1.0 - 1.0 / x, np.finfo(float).eps, np.inf)

    def __call__(self, mu):
        return np.log(self._clean(1.0 + mu))

    def inverse(self, t):
        return 1.0 / (1.0 - safe_exp(t)) - 1.0
