import numpy as np
import gkm


def get_data(n, nft):
    # random features
    x = np.random.rand(n, nft)
    # deterministic target
    y = 10.0 * np.prod(np.sin(2.0 * np.pi * x), axis=1) ** 2
    y = np.floor(y)
    # scale features
    xsqr = (x ** 2).sum(axis=1)
    dsqr = xsqr[:, None] + xsqr[None, :] - 2.0 * x.dot(x.T)
    mscale = np.mean(dsqr)
    x /= np.sqrt(mscale) / 2
    return x, y


def compute_kernel(x0, x1=None):
    if x1 is None:
        x1 = x0
    x0sqr = (x0 ** 2).sum(axis=1)
    x1sqr = (x1 ** 2).sum(axis=1)
    return np.exp(2.0 * x0.dot(x1.T) - x0sqr[:, None] - x1sqr[None, :])


def idfn(val):
    if isinstance(val, gkm.Loss):
        return type(val).__name__
