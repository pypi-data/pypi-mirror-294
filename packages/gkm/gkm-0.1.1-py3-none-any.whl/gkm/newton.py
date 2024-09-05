from typing import Optional
import numpy as np
import numpy.typing as npt
from . import rendered
from .loss import compute as compute_loss, Loss


def solve(
    k: npt.ArrayLike,
    y: npt.ArrayLike,
    loss: Loss,
    lmbda: float,
    z0: Optional[tuple[npt.ArrayLike, float]] = None,
    tol: float = 1e-16,
    max_steps: int = 100,
    max_back_steps: int = 10,
    sigma: float = 0.01,
    eta: float = 0.1,
    verbose: int = 0,
    regularization: float = 1e-10,
):
    # initialize
    k = np.array(k)
    n = k.shape[0]
    if z0 is None:
        a = np.zeros(n)
        b = loss.mean2param(np.mean(y))
        ka = np.zeros(n)
    else:
        a = np.array(z0[0])
        b = z0[1]
        ka = k.dot(a) / lmbda
    t = ka + b

    for step in range(max_steps):
        # compute objective
        reg = 0.5 * ka.dot(a)
        ell, g, h = compute_loss(y, t, loss, derivative=True)
        obj = reg + ell.mean()

        if np.isinf(obj) or np.isnan(obj):
            raise ValueError('objective is inf or nan')
        g /= n
        h /= n

        # compute violation
        rhs_a = a + g
        rhs_b = a.sum()
        rhssqr = (lmbda * rhs_a.dot(rhs_a) + rhs_b**2) / (n + 1)
        # output
        if verbose >= 1:
            print(step + 1, obj, rhssqr, end='')
        # check for termination
        if rhssqr < tol:
            if verbose >= 1:
                print(
                    f'\noptimization terminated after {step}', 'steps (violation < tol)'
                )
            break

        # solve Newton system
        rhs = (rhs_a, rhs_b)
        if h.sum() < regularization:
            h += regularization
        d_a, d_b = rendered.solve(k, h, lmbda, rhs)
        dec = k.dot(rhs_a).dot(d_a) / lmbda + g.sum() * d_b
        if verbose >= 1:
            print('', dec)

        an, bn, kan, tn = a, b, ka, t
        s = 1.0
        for _backstep in range(max_back_steps):
            # update vars
            an = a - s * d_a
            bn = b - s * d_b
            # evaluate
            kan = k.dot(an) / lmbda
            tn = kan + bn
            regn = 0.5 * kan.dot(an)
            elln = compute_loss(y, tn, loss)

            objn = regn + elln.mean()
            # output
            if verbose >= 2:
                print(' > ', _backstep + 1, s, objn - obj)
            # check step
            if objn < obj - sigma * s * dec + tol:
                break
            # decrease step size
            s *= eta

        if (obj - objn) * lmbda < tol:
            if verbose >= 1:
                print(
                    f'\noptimization terminated after {step+1}',
                    'steps (decrease < tol)',
                )
            break

        # update
        a, b, ka, t = an, bn, kan, tn
    else:
        if verbose >= 1:
            print('optimization did not terminate')
    return a, b
