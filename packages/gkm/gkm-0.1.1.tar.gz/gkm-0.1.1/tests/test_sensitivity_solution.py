import itertools
import pytest
from numpy.testing import assert_allclose
import numpy as np
import gkm
from common import get_data, compute_kernel, idfn


@pytest.mark.parametrize('lmbda,loss', itertools.product(
    [1.0, 0.1, 1e-3],
    [gkm.deviance.gaussian, gkm.deviance.poisson, gkm.deviance.geometric],
), ids=idfn)
def test_sensitivity(lmbda, loss):
    tau = 1e-6
    np.random.seed(5)
    n, nft = 10, 2
    x, y = get_data(n, nft)

    loglmbda = np.log(lmbda)
    k = compute_kernel(x, x)
    clf = gkm.GKM(lmbda=np.exp(loglmbda), loss=loss)
    clf.fit_with_kernel_matrix(k, y)
    s = clf.sensitivity_solution()

    # sensitivity for lmbda
    clf_n = gkm.GKM(lmbda=np.exp(loglmbda + tau), loss=loss)
    clf_n.fit_with_kernel_matrix(k, y)

    da, db = s['loglmbda']
    da_approx = (clf_n._a - clf._a) / tau
    db_approx = (clf_n._b - clf._b) / tau
    assert_allclose(da, da_approx, rtol=1e-4, atol=1e-8)
    assert_allclose(db, db_approx, rtol=1e-4, atol=1e-8)

    # sensitivity for kernel (train)
    clf_n = gkm.GKM(lmbda=np.exp(loglmbda), loss=loss)
    clf_n.fit_with_kernel_matrix(k ** np.exp(tau), y)

    da, db = s['kernel'](k * np.log(k))
    da_approx = (clf_n._a - clf._a) / tau
    db_approx = (clf_n._b - clf._b) / tau
    assert_allclose(da, da_approx, rtol=1e-4, atol=1e-8)
    assert_allclose(db, db_approx, rtol=1e-4, atol=1e-8)
