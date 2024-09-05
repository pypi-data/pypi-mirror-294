import numpy as np
from numpy.testing import assert_allclose
import gkm


def test_gaussian_deriv():
    tau = 1e-8
    np.random.seed(1)

    n = 1000
    y = np.random.randn(n)

    loss = gkm.deviance.gaussian
    t = loss.mean2param(np.random.randn(n))

    l0 = loss(y, t)
    dl0 = loss.deriv(y, t)
    ddl0 = loss.deriv2(y, t)

    l1 = loss(y, t + tau)
    dl_approx = (l1 - l0) / tau
    assert_allclose(dl0, dl_approx, rtol=1e-5, atol=1e-12)

    dl1 = loss.deriv(y, t + tau)
    ddl_approx = (dl1 - dl0) / tau
    assert_allclose(ddl0, ddl_approx, rtol=1e-5, atol=1e-12)


def test_poisson_deriv():
    tau = 1e-8
    np.random.seed(1)

    n = 1000
    y = np.random.poisson(size=n)

    loss = gkm.deviance.poisson
    t = loss.mean2param(1.0 + np.random.poisson(size=n))

    l0 = loss(y, t)
    dl0 = loss.deriv(y, t)
    ddl = loss.deriv2(y, t)

    l1 = loss(y, t + tau)
    dl_approx = (l1 - l0) / tau
    assert_allclose(dl0, dl_approx, rtol=1e-5, atol=1e-6)

    dl1 = loss.deriv(y, t + tau)
    ddl_approx = (dl1 - dl0) / tau
    assert_allclose(ddl, ddl_approx, rtol=1e-5, atol=1e-6)


def test_binomial_deriv():
    tau = 1e-8
    np.random.seed(1)

    n = 1000
    y = np.random.binomial(5, 0.5, n)
    mu = 1.0 / (1.0 + np.exp(np.random.randn(n)))

    loss = gkm.deviance.Binomial(5)

    l0 = loss(y, mu)
    dl0 = loss.deriv(y, mu)
    ddl = loss.deriv2(y, mu)

    l1 = loss(y, mu + tau)
    dl_approx = (l1 - l0) / tau
    assert_allclose(dl0, dl_approx, rtol=1e-4, atol=1e-12)

    dl1 = loss.deriv(y, mu + tau)
    ddl_approx = (dl1 - dl0) / tau
    assert_allclose(ddl, ddl_approx, rtol=1e-4, atol=1e-12)


def test_geometric_deriv():
    tau = 1e-8
    np.random.seed(1)

    n = 1000
    y = np.random.geometric(0.5, n)

    loss = gkm.deviance.geometric
    t = loss.mean2param(np.random.geometric(0.5, n))

    l0 = loss(y, t)
    dl0 = loss.deriv(y, t)
    ddl = loss.deriv2(y, t)

    l1 = loss(y, t + tau)
    dl_approx = (l1 - l0) / tau
    assert_allclose(dl0, dl_approx, rtol=1e-4, atol=1e-6)

    dl1 = loss.deriv(y, t + tau)
    ddl_approx = (dl1 - dl0) / tau
    assert_allclose(ddl, ddl_approx, rtol=1e-4, atol=1e-6)
