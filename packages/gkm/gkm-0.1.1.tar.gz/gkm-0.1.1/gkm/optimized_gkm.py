from typing import Optional
import numpy as np
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted
from sklearn.model_selection import check_cv
from scipy.optimize import minimize, check_grad
from . import deviance
from . import validation
from .gkm import GKM
from .amsgrad import amsgrad
from .kernel import get_kernel
from .loss import Loss
from .helpers import log_tuple_keepnone, safe_exp


class OptimizedGKM(BaseEstimator, RegressorMixin):
    def __init__(
        self,
        lmbda0: float = 1.0,
        gamma0: float | str = 1.0,
        bounds=None,
        loss: Loss = deviance.gaussian,
        loss_val: Optional[Loss] = None,
        regularization=None,
        cv=None,
        sample_objective: float = 1.0,
        verbose=0,
        kernel_type: str = 'rbf',
        minimize_method='L-BFGS-B',
        minimize_options=None,
        callback=None,
    ):
        super().__init__()
        self.lmbda0 = lmbda0
        self.gamma0 = self._gamma0 = gamma0
        self.loss = loss
        self.loss_val = loss_val if loss_val is not None else loss
        self.regularization = regularization
        self.bounds = bounds
        self.verbose = verbose
        self.minimize_method = minimize_method
        self.minimize_options = minimize_options
        self.cv = check_cv(cv)
        self.callback = callback
        if not isinstance(sample_objective, (float, int)):
            raise TypeError('sample_objective should be float')
        if sample_objective <= 0.0:
            raise ValueError('sample_objective should be positive')
        if sample_objective > 1.0:
            raise ValueError('sample_objective should not be greater than one')
        self.sample_objective = sample_objective
        self.kernel_type = kernel_type
        self.kernel = get_kernel(kernel_type)

    def _get_bounds(self):
        if self.bounds is None:
            return None
        lmbda_bounds = log_tuple_keepnone(self.bounds.get('lmbda', (None, None)))
        gamma_bounds = log_tuple_keepnone(self.bounds.get('gamma', (None, None)))
        return [lmbda_bounds] + self.kernel.get_bounds(gamma_bounds)

    def _objective(self, logp, y, groups, idx, regularization):
        y = y[idx]
        if groups is not None:
            groups = groups[idx]
        assert logp.shape == (1 + self.kernel.dim,)
        loglmbda = logp[0]
        lmbda = safe_exp(loglmbda)
        loggamma = logp[1:]
        gamma = safe_exp(loggamma)
        k = self.kernel(gamma, idx, idx)

        val, dval = validation.score(
            GKM(lmbda=lmbda, loss=self.loss),
            gamma,
            k,
            y,
            groups,
            self.cv,
            self.kernel,
            self.loss_val,
            deriv=True,
        )
        avg_err = val
        reg = None
        if regularization is not None:
            reg, dreg = regularization(logp)
            val += reg
            dval += dreg
        if self.verbose >= 1:
            log = dict(
                lmbda=lmbda,
                gamma=gamma,
                val=val,
            )
            if reg is not None:
                log['err'] = avg_err
                log['reg'] = reg
            print(log)
        return val, dval

    def _optimize_parameters(self, y, groups):
        self.gamma0 = self.kernel.get_initial(self.gamma0)
        logp0 = np.log(np.concatenate(([self.lmbda0], self.gamma0)))
        results = dict()
        results['logp0'] = logp0

        def _obj(logp):
            try:
                if self.sample_objective == 1.0:
                    idx = slice(None)
                else:
                    n = y.size
                    idx = np.random.choice(
                        n,
                        round(self.sample_objective * n),
                        replace=False,
                    )
                res = self._objective(
                    logp,
                    y=y,
                    groups=groups,
                    idx=idx,
                    regularization=(
                        None
                        if self.regularization is None
                        else (
                            lambda logp: self.regularization(
                                {
                                    'logp0': logp0,
                                    'logp': logp,
                                }
                            )
                        )
                    ),
                )
                if 'obj0' not in results:
                    results['obj0'], results['dobj0'] = res
                return res
            except FloatingPointError:
                return np.finfo(float).max, np.full_like(logp, np.nan)

        # handle optimization problem
        if self.minimize_method.lower() == 'amsgrad':
            res = amsgrad(
                _obj,
                logp0,
                **(dict() if self.minimize_options is None else self.minimize_options),
            )
        elif self.minimize_method.lower() == 'check_grad':
            print(
                'check_grad:',
                check_grad(
                    lambda x: _obj(x)[0],
                    lambda x: _obj(x)[1],
                    logp0,
                ),
            )
            return
        else:
            if self.sample_objective != 1.0:
                raise ValueError(
                    'minimize method assumes ' 'deterministic objective function'
                )
            res = minimize(
                _obj,
                logp0,
                bounds=self._get_bounds(),
                jac=True,
                method=self.minimize_method,
                options=self.minimize_options,
                callback=self.callback,
            )

        # extract final parameter values
        logp1 = res.x
        results['logp1'] = logp1
        results['obj1'] = res.fun
        results['dobj1'] = res.jac
        p1 = np.exp(logp1)
        lmbda1 = p1[0]
        gamma1 = p1[1:]
        results['param'] = dict(lmbda=lmbda1, gamma=gamma1)
        return results

    @property
    def lmbda(self):
        return self.optimization_results['param']['lmbda']

    @property
    def gamma(self):
        return self.optimization_results['param']['gamma']

    @property
    def value0(self):
        return self.optimization_results['obj0']

    @property
    def value(self):
        return self.optimization_results['obj1']

    def fit(self, X, y, groups=None):
        X, y = check_X_y(X, y)
        # precompute kernel
        self.kernel.prepare(X)
        # optimize
        results = self._optimize_parameters(y, groups)
        self.optimization_results = results
        # perform final fit
        self._model = GKM(lmbda=self.lmbda, loss=self.loss)
        k = self.kernel(self.gamma)
        self._model.fit_with_kernel_matrix(k, y)

    def predict(self, X):
        check_is_fitted(self, ['_model'])
        X = check_array(X)
        # compute kernel
        k = self.kernel.compute(self.gamma, X)
        # predict
        return self._model.predict_with_kernel_matrix(k)
