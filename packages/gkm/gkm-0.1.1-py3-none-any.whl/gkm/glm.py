import numpy as np
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted
from . import deviance
from .loss import compute as Loss


class GLM(BaseEstimator, RegressorMixin):
    def __init__(
        self,
        loss: Loss = deviance.gaussian,
        verbose: int = 0,
        tol: float = 1e-16,
        max_steps: int = 1000,
        add_offset: bool = False,
    ):
        super().__init__()
        self.verbose = verbose
        self.loss = loss
        self.tol = tol
        self.add_offset = add_offset
        self.max_steps = max_steps

    def fit(self, X, y, groups=None):
        X, y = check_X_y(X, y)
        n, nft = X.shape
        assert y.shape == (n,)
        loss = self.loss

        if self.add_offset:
            raise NotImplementedError()

        offset = loss.mean2param(np.mean(y))
        beta = np.linalg.lstsq(X, offset * np.ones(n), rcond=None)[0]
        t = X.dot(beta)

        for step in range(self.max_steps):
            ell = loss(y, t).sum()
            dell = loss.deriv(y, t)
            dell_sqr = dell.dot(dell)
            if self.verbose >= 1:
                print(step + 1, ell, dell_sqr)
            if dell_sqr < self.tol:
                if self.verbose >= 1:
                    print(
                        f'\noptimization terminated after {step}',
                        'steps (violation < tol)',
                    )
                break
            ddell = loss.deriv2(y, t)
            # dbeta = np.linalg.lstsq(ddell[:, None] * X, dell, rcond=None)[0]
            dbeta = np.linalg.solve(X.T.dot(ddell[:, None] * X), X.T.dot(dell))
            # print(dell, ddell)
            print(X.T.dot(ddell[:, None] * X))
            tau = 1.0
            for step_back in range(10):
                betan = beta - tau * dbeta
                tn = X.dot(betan)
                elln = loss(y, tn).sum()
                if self.verbose >= 2:
                    print(' ', step_back, elln - ell)
                if elln < ell:
                    break
                tau *= 0.1
            if ell - elln < self.tol:
                if self.verbose >= 1:
                    print(
                        f'\noptimization terminated after {step+1}',
                        'steps (decrease < tol)',
                    )
                break
            beta = betan
            t = tn

        self._beta = beta

    @property
    def coeffs(self):
        return self._beta

    def predict(self, X):
        check_is_fitted(self, ['_beta'])
        X = check_array(X)
        t = X.dot(self._beta)
        mu = self.loss.param2mean(t)
        return mu

    def sensitivity_prediction(self, mu, x):
        t = x.dot(self._beta)
        dmu = 1.0 / self.loss.dmean2param(mu)
        return dmu * t
