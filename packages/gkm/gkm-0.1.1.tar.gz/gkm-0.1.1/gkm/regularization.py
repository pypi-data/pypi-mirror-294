import numpy as np


def penalize_gamma(factor):
    def _regularization(data):
        gamma = np.exp(data['logp'][1:])
        gamma0 = np.exp(data['logp0'][1:])
        dim = gamma.size
        reg = gamma / gamma0
        dreg = np.concatenate(([0.0], reg / dim))
        return factor * reg.mean(), factor * dreg

    return _regularization
