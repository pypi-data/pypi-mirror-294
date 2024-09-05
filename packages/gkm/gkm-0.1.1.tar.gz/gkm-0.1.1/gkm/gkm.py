import numpy as np
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted
from . import newton
from . import rendered
from . import deviance
from . import validation
from .loss import compute as compute_loss, Loss
from .kernel import get_kernel


class GKM(BaseEstimator, RegressorMixin):
    def __init__(
        self,
        lmbda: float,
        loss: Loss = deviance.gaussian,
        verbose: int = 0,
        tol: float = 1e-16,
        kernel_type: str = 'rbf',
        gamma: float = 1.0,
    ):
        super().__init__()
        self.lmbda = lmbda
        self.verbose = verbose
        self.loss = loss
        self.tol = tol
        self.kernel_type = kernel_type
        self.kernel = get_kernel(kernel_type)
        self.gamma = self.kernel.get_initial(gamma)

    def fit(self, X, y, groups=None):
        X, y = check_X_y(X, y)
        self.kernel.prepare(X)
        k = self.kernel(self.gamma)
        return self.fit_with_kernel_matrix(k, y)

    def fit_with_kernel_matrix(self, k, y):
        # solve training problem using Newton's method
        self._k = k
        self._y = y
        a, b = newton.solve(
            k,
            y,
            self.loss,
            self.lmbda,
            verbose=self.verbose,
            tol=self.tol,
        )
        self._a = a
        self._b = b
        return self

    def predict(self, X):
        check_is_fitted(self, ['_a', '_b'])
        X = check_array(X)
        k = self.kernel.compute(self.gamma, X)
        return self.predict_with_kernel_matrix(k)

    def predict_with_kernel_matrix(self, k):
        check_is_fitted(self, ['_k', '_y', '_a', '_b'])
        ka = k.dot(self._a)
        t = ka / self.lmbda + self._b
        mu = self.loss.param2mean(t)
        return mu

    def sensitivity_solution(self):
        ka = self._k.dot(self._a)
        t = ka / self.lmbda + self._b
        h = compute_loss(self._y, t, self.loss, derivative=True)[2]
        h /= h.size
        return dict(
            loglmbda=rendered.solve(
                self._k,
                h,
                self.lmbda,
                (
                    h * ka / self.lmbda,
                    0.0,
                ),
            ),
            kernel=lambda dk: rendered.solve(
                self._k,
                h,
                self.lmbda,
                (
                    -h * np.tensordot(dk, self._a, axes=(1, 0)) / self.lmbda,
                    0.0,
                ),
            ),
        )

    def sensitivity_prediction(self, mu, dk):
        dmu = 1.0 / self.loss.dmean2param(mu)
        return dmu[:, None] * np.tensordot(dk, self._a, axes=(1, 0))

    def sensitivity(self, kv, de):
        ka = self._k.dot(self._a)
        t = ka / self.lmbda + self._b
        h = compute_loss(self._y, t, self.loss, derivative=True)[2]
        h /= h.size
        if np.isnan(h).any():
            raise FloatingPointError()

        kva = kv.dot(self._a)
        tv = kva / self.lmbda + self._b
        dmuv = self.loss.dparam2mean(tv)
        if np.isnan(dmuv).any():
            raise FloatingPointError()
        gamma = rendered.solve_transposed(
            self._k,
            h,
            self.lmbda,
            (
                (de * dmuv).dot(kv) / self.lmbda,
                (de * dmuv).sum(),
            ),
        )[0]

        def dkernel(dk, dkv):
            return (
                np.tensordot(
                    (
                        np.tensordot(dkv, de * dmuv, axes=(1, 0))
                        - np.tensordot(h[None, None, :] * dk, gamma, axes=(2, 0))
                    ),
                    self._a,
                    axes=(1, 0),
                )
                / self.lmbda
            )

        return dict(
            loglmbda=(gamma.dot(h * ka) - (de * dmuv).dot(kva)) / self.lmbda,
            kernel=dkernel,
        )

    def score(self, x, y):
        y_est = self.predict(x)
        t_est = self.loss.mean2param(y_est)
        t_const = self.loss.mean2param(np.mean(self._y))
        return self.loss(y, t_est).sum() / self.loss(y, t_const * np.ones_like(y)).sum()

    def objective(self, x, y, groups=None, cv=None):
        self.kernel.prepare(x)
        k = self.kernel(self.gamma)
        return validation.score(
            self,
            self.gamma,
            k,
            y,
            groups,
            cv=cv,
            kernel=self.kernel,
            loss=self.loss,
        )
