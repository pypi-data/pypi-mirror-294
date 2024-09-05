import numpy as np
from .base import Kernel


class RBF(Kernel):
    def get_bounds(self, bounds):
        return [bounds]

    def _estimate_gamma(self):
        return np.ones(self.dim) * np.log(2.0) / max(self._dsqr.mean(), 1e-10)

    def get_initial(self, gamma0):
        if isinstance(gamma0, (float, int)):
            return np.ones(self.dim) * gamma0
        elif isinstance(gamma0, np.ndarray):
            assert gamma0.shape == (self.dim,)
            return gamma0
        elif isinstance(gamma0, str):
            if gamma0 == 'auto':
                gamma0 = self._estimate_gamma()
            else:
                raise ValueError('unknown string value for gamma0')
        else:
            raise TypeError('gamma0 should by number or "auto"')
        return gamma0

    def prepare(self, X):
        xsqr = (X**2).sum(axis=1)
        self._x = X
        self._xsqr = xsqr
        self._dsqr = np.maximum(xsqr[:, None] + xsqr[None, :] - 2.0 * X.dot(X.T), 0.0)

    def __call__(self, gamma, idx1=slice(None), idx2=slice(None)):
        assert gamma.shape == (1,)
        return np.exp(-gamma[0] * self._dsqr)

    def deriv(self, gamma, k, idx1=slice(None), idx2=slice(None)):
        return (-k[idx1][:, idx2] * self._dsqr[idx1][:, idx2])[None]

    def compute(self, gamma, X):
        xsqr = (X**2).sum(axis=1)
        self._dsqr = xsqr[:, None] + self._xsqr[None, :] - 2.0 * X.dot(self._x.T)
        return np.exp(-gamma[0] * self._dsqr)

    @property
    def dim(self):
        return 1
