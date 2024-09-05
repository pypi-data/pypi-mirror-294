import itertools
import pytest
from numpy.testing import assert_allclose
import numpy as np
import gkm
from common import get_data, compute_kernel, idfn


@pytest.mark.parametrize('lmbda,loss', itertools.product(
    [0.1, 1e-3, 1e-5],
    [gkm.deviance.gaussian, gkm.deviance.poisson, gkm.deviance.geometric],
), ids=idfn)
def test_sensitivity(lmbda, loss):
    tau = 1e-8
    np.random.seed(5)
    n, nft = 5, 2
    x, y = get_data(n, nft)
    nv = 10
    xv, yv = get_data(nv, nft)

    def _validation_error(yvp, deriv=False):
        diff = yvp - yv
        val = (diff ** 2).mean()
        if deriv:
            return val, 2.0 * diff / yv.size
        return val

    loglmbda = np.log(lmbda)
    k = compute_kernel(x, x)
    clf = gkm.GKM(lmbda=np.exp(loglmbda), loss=loss)
    clf.fit_with_kernel_matrix(k, y)
    kv = compute_kernel(xv, x)
    fv, dfv = _validation_error(clf.predict_with_kernel_matrix(kv), deriv=True)
    s = clf.sensitivity(kv, dfv)

    # sensitivity for lmbda
    clf_n = gkm.GKM(lmbda=np.exp(loglmbda + tau), loss=loss)
    clf_n.fit_with_kernel_matrix(k, y)
    fv_n = _validation_error(clf_n.predict_with_kernel_matrix(kv))
    dfv_approx = (fv_n - fv) / tau
    assert_allclose(
        s['loglmbda'],
        dfv_approx,
        rtol=1e-5 / lmbda, atol=1e-6,
    )

    # sensitivity for kernel (train)
    clf_n = gkm.GKM(lmbda=np.exp(loglmbda), loss=loss)
    clf_n.fit_with_kernel_matrix(k ** np.exp(tau), y)
    fv_n = _validation_error(clf_n.predict_with_kernel_matrix(kv))
    dfv_approx = (fv_n - fv) / tau
    assert_allclose(
        s['kernel']((k * np.log(k))[None, :, :], np.zeros_like(kv)[None, :, :]),
        dfv_approx,
        rtol=1e-5 / lmbda, atol=1e-6,
    )

    # sensitivity for kernel (validate)
    clf_n = gkm.GKM(lmbda=np.exp(loglmbda), loss=loss)
    clf_n.fit_with_kernel_matrix(k, y)
    fv_n = _validation_error(
        clf_n.predict_with_kernel_matrix(kv ** np.exp(tau))
    )
    dfv_approx = (fv_n - fv) / tau
    assert_allclose(
        s['kernel'](np.zeros_like(k)[None, :, :], (kv * np.log(kv))[None, :, :]),
        dfv_approx,
        rtol=1e-5 / lmbda, atol=1e-6,
    )

    # sensitivity for kernel (both)
    clf_n = gkm.GKM(lmbda=np.exp(loglmbda), loss=loss)
    clf_n.fit_with_kernel_matrix(k ** np.exp(tau), y)
    fv_n = _validation_error(
        clf_n.predict_with_kernel_matrix(kv ** np.exp(tau))
    )
    dfv_approx = (fv_n - fv) / tau
    assert_allclose(
        s['kernel'](
            (k * np.log(k))[None, :, :],
            (kv * np.log(kv))[None, :, :],
        ),
        dfv_approx,
        rtol=1e-5 / lmbda, atol=1e-6,
    )
