import numpy as np
from .rbf import RBF


class MultiRBF(RBF):
    def get_bounds(self, bounds):
        return [bounds] * self.dim

    def _estimate_gamma(self):
        return np.log(2.0) / np.maximum(self._dsqr.mean(axis=(1, 2)), 1e-10)

    def prepare(self, X):
        self._x = X
        self._dsqr = np.maximum((X.T[:, :, None] - X.T[:, None, :]) ** 2, 0.0)

    def __call__(self, gamma, idx1=slice(None), idx2=slice(None)):
        assert gamma.shape == (self.dim,)
        return np.exp(
            np.tensordot(
                self._dsqr[:, idx1][:, :, idx2],
                -gamma,
                axes=(0, 0),
            )
        )

    def deriv(self, gamma, k, idx1=slice(None), idx2=slice(None)):
        return -k[idx1][:, idx2] * self._dsqr[:, idx1][:, :, idx2]

    def compute(self, gamma, X):
        dsqr = np.maximum((X.T[:, :, None] - self._x.T[:, None, :]) ** 2, 0.0)
        return np.exp(np.tensordot(dsqr, -gamma, axes=(0, 0)))

    @property
    def dim(self):
        return self._x.shape[1]
