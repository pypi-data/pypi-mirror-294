import numpy as np
from ..loss import Loss


class Deviance(Loss):
    def deriv(self, y, t):
        return self.param2mean(t) - y

    def deriv2(self, y, t):
        return self.dparam2mean(t)

    def density(self, y, t):
        return np.exp(self.log_density(y, t))
