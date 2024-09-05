import numpy as np
from .multi_rbf import MultiRBF


class MultiRBFLazy(MultiRBF):
    def _estimate_gamma(self):
        return np.log(2.0) / np.maximum(
            [
                ((self._x[:, i][None, :] - self._x[:, i][:, None]) ** 2).mean()
                for i in range(self.dim)
            ],
            1e-10,
        )

    def prepare(self, X):
        self._x = X

    def __call__(self, gamma, idx1=slice(None), idx2=slice(None)):
        assert gamma.shape == (self.dim,)
        xs = self._x * np.sqrt(gamma)[None]
        xssqr = (xs**2).sum(axis=1)
        ndssqr = (
            2.0 * xs[idx1].dot(xs[idx2].T) - xssqr[idx1][:, None] - xssqr[idx2][None, :]
        )
        return np.exp(ndssqr)

    def deriv(self, gamma, k, idx1=slice(None), idx2=slice(None)):
        for i in range(self.dim):
            dsqr = (self._x[idx1, i][:, None] - self._x[idx2, i][None, :]) ** 2
            yield -k[idx1][:, idx2] * dsqr

    def compute(self, gamma, X):
        xs = self._x * np.sqrt(gamma)[None]
        xssqr = (xs**2).sum(axis=1)
        x1s = X * np.sqrt(gamma)[None]
        x1ssqr = (x1s**2).sum(axis=1)
        ndssqr = 2.0 * xs.dot(x1s.T) - xssqr[:, None] - x1ssqr[None, :]
        return np.exp(ndssqr)
