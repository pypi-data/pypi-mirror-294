import numpy as np
from scipy.optimize import OptimizeResult


def amsgrad(
    f,
    x0,
    n_iter: int = 100,
    alpha: float = 0.001,
    beta_grad: float = 0.9,
    beta_gradsqr: float = 0.99,
    beta_fun: float = 0.9,
    epsilon: float = 1e-12,
    verbose: int = 0,
    callback=None,
):
    x = np.array(x0)
    n = x0.shape
    avg_grad = np.zeros(n)
    avg_gradsqr = np.zeros(n)
    avg_gradsqr_max = np.zeros(n)
    avg_fun = None

    for t in range(1, n_iter + 1):
        fun, grad = f(x)
        if avg_fun is None:
            avg_fun = fun
        else:
            avg_fun = beta_fun * avg_fun + (1.0 - beta_fun) * fun
        avg_gradsqr = beta_gradsqr * avg_gradsqr + (1.0 - beta_gradsqr) * grad**2
        if verbose > 0:
            print(t, avg_fun, avg_gradsqr.mean())
        if callback is not None:
            try:
                callback(
                    OptimizeResult(
                        x=x,
                        success=True,
                        fun=avg_fun,
                        jac=avg_grad,
                        nit=t,
                    )
                )
            except StopIteration:
                break
        avg_grad = beta_grad**t * avg_grad + (1.0 - beta_grad**t) * grad
        avg_gradsqr_max = np.maximum(avg_gradsqr_max, avg_gradsqr)
        x -= alpha * avg_grad / (np.sqrt(avg_gradsqr_max) + epsilon)
    return OptimizeResult(
        x=x,
        success=True,
        fun=avg_fun,
        jac=avg_grad,
        nit=t,
    )
