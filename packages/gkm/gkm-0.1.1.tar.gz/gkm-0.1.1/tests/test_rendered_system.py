import numpy as np
from numpy.testing import assert_allclose
from gkm import rendered


def test_rendered_solve_positive():
    np.random.seed(5)
    n = 10
    for trial in range(10):
        kh = np.random.randn(n, n // 2)
        k = kh.dot(kh.T)
        h = np.random.randn(n) ** 2
        # h = np.concatenate((np.random.randn(n // 2) ** 2, np.zeros(n // 2)))
        lmbda = 1e-3
        rhs_a = np.random.rand(n)
        rhs_b = np.random.rand()
        rhs = rhs_a, rhs_b

        da, db = rendered.solve_positive(k, h, lmbda, rhs)
        rec_a = da + h * k.dot(da) / lmbda + h * db
        rec_b = da.sum()
        assert_allclose(rec_b, rhs_b)
        assert_allclose(rec_a, rhs_a)

        d = np.linalg.solve(np.block([
            [np.eye(n) + h[:, None] * k / lmbda, h[:, None]],
            [np.ones((1, n)), 0.0],
        ]), np.concatenate([rhs_a, [rhs_b]]))
        assert_allclose(np.concatenate((da, [db])), d)

        da, db = rendered.solve_transposed_positive(k, h, lmbda, rhs)
        rec_a = da + k.dot(h * da) / lmbda + db
        rec_b = np.dot(h, da)
        assert_allclose(rec_b, rhs_b)
        assert_allclose(rec_a, rhs_a)

        d = np.linalg.solve(np.block([
            [np.eye(n) + h[:, None] * k / lmbda, h[:, None]],
            [np.ones((1, n)), 0.0],
        ]).T, np.concatenate([rhs_a, [rhs_b]]))
        assert_allclose(np.concatenate((da, [db])), d)


def test_rendered_solve():
    np.random.seed(5)
    n = 10
    for trial in range(10):
        kh = np.random.randn(n, n // 2)
        k = kh.dot(kh.T)
        h = np.concatenate((np.random.randn(n // 2) ** 2, np.zeros(n // 2)))
        lmbda = 1e-3
        rhs_a = np.random.rand(n)
        rhs_b = np.random.rand()

        da, db = rendered.solve(k, h, lmbda, (rhs_a, rhs_b))

        rec_a = da + h * k.dot(da) / lmbda + h * db
        rec_b = da.sum()
        assert_allclose(rec_b, rhs_b)
        assert_allclose(rec_a, rhs_a)

        d = np.linalg.solve(np.block([
            [np.eye(n) + h[:, None] * k / lmbda, h[:, None]],
            [np.ones((1, n)), 0.0],
        ]), np.concatenate([rhs_a, [rhs_b]]))
        assert_allclose(np.concatenate((da, [db])), d)
