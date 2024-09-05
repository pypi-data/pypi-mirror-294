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
    nv = 5
    xv, yv = get_data(nv, nft)

    loglmbda = np.log(lmbda)
    k = compute_kernel(x, x)
    clf = gkm.GKM(lmbda=np.exp(loglmbda), loss=loss)
    clf.fit_with_kernel_matrix(k, y)
    s = clf.sensitivity_solution()

    kv = compute_kernel(xv, x)
    fv = clf.predict_with_kernel_matrix(kv).sum()
    dfv = np.ones(nv)

    t = kv.dot(clf._a) / lmbda + clf._b
    dmu = loss.dparam2mean(t)
    dfv *= dmu

    # sensitivity for lmbda
    clf_n = gkm.GKM(lmbda=np.exp(loglmbda + tau), loss=loss)
    clf_n.fit_with_kernel_matrix(k, y)
    kv_n = compute_kernel(xv, x)
    fv_n = clf_n.predict_with_kernel_matrix(kv_n).sum()
    dfv_approx = (fv_n.sum() - fv.sum()) / tau
    da, db = s['loglmbda']
    assert_allclose(
        dfv.dot(kv.dot(da - clf._a) / lmbda + db),
        dfv_approx,
        rtol=1e-4, atol=1e-6,
    )

    # sensitivity for kernel (train)
    clf_n = gkm.GKM(lmbda=np.exp(loglmbda), loss=loss)
    clf_n.fit_with_kernel_matrix(k ** np.exp(tau), y)
    kv_n = compute_kernel(xv, x)
    fv_n = clf_n.predict_with_kernel_matrix(kv_n).sum()
    dfv_approx = (fv_n.sum() - fv.sum()) / tau
    da, db = s['kernel'](k * np.log(k))
    assert_allclose(
        dfv.dot(kv.dot(da) / lmbda + db),
        dfv_approx,
        rtol=1e-4, atol=1e-6,
    )

    # sensitivity for kernel (validate)
    clf_n = gkm.GKM(lmbda=np.exp(loglmbda), loss=loss)
    clf_n.fit_with_kernel_matrix(k, y)
    kv_n = compute_kernel(xv, x) ** np.exp(tau)
    fv_n = clf_n.predict_with_kernel_matrix(kv_n).sum()
    dfv_approx = (fv_n.sum() - fv.sum()) / tau
    da, db = s['kernel'](np.zeros_like(k))
    assert_allclose(
        dfv.dot((kv.dot(da) + (kv * np.log(kv)).dot(clf._a)) / lmbda + db),
        dfv_approx,
        rtol=1e-4, atol=1e-6,
    )

    # sensitivity for kernel (both)
    clf_n = gkm.GKM(lmbda=np.exp(loglmbda), loss=loss)
    clf_n.fit_with_kernel_matrix(k ** np.exp(tau), y)
    kv_n = compute_kernel(xv, x) ** np.exp(tau)
    fv_n = clf_n.predict_with_kernel_matrix(kv_n).sum()
    dfv_approx = (fv_n.sum() - fv.sum()) / tau
    da, db = s['kernel'](k * np.log(k))
    assert_allclose(
        dfv.dot((kv.dot(da) + (kv * np.log(kv)).dot(clf._a)) / lmbda + db),
        dfv_approx,
        rtol=1e-4, atol=1e-6,
    )
