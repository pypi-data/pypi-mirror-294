import numpy as np
import scipy.linalg as sla


def solve_positive(k, h, lmbda, rhs):
    rhs_a, rhs_b = rhs
    mat = k / lmbda
    mat.flat[:: mat.shape[0] + 1] += 1.0 / h
    try:
        decomp = sla.cho_factor(mat)
        p = sla.cho_solve(decomp, rhs_a / h)
        q = sla.cho_solve(decomp, np.ones_like(rhs_a))
    except np.linalg.LinAlgError:
        p = sla.solve(mat, rhs_a / h)
        q = sla.solve(mat, np.ones_like(rhs_a))

    d_b = (p.sum() - rhs_b) / q.sum()
    d_a = p - d_b * q
    return d_a, d_b


def solve(k, h, lmbda, rhs, tol=1e-12):
    rhs_a, rhs_b = rhs
    idx_0 = h <= tol
    idx_1 = ~idx_0
    rhs_0, rhs_1 = rhs_a[idx_0], rhs_a[idx_1]
    h_1 = h[idx_1]
    rhs_rem_a = rhs_1 - h_1 * k[idx_1][:, idx_0].dot(rhs_0) / lmbda
    rhs_rem_b = rhs_b - rhs_0.sum()
    rhs_rem = rhs_rem_a, rhs_rem_b
    k_1 = k[idx_1][:, idx_1]
    d_rem_a, d_rem_b = solve_positive(k_1, h_1, lmbda, rhs_rem)
    d_a = np.zeros_like(h)
    d_a[idx_1] = d_rem_a
    d_a[idx_0] = rhs_0
    d_b = d_rem_b
    return d_a, d_b


def solve_transposed_positive(k, h, lmbda, rhs):
    rhs_a, rhs_b = rhs
    mat = k / lmbda
    mat.flat[:: mat.shape[0] + 1] += 1.0 / h
    try:
        decomp = sla.cho_factor(mat)
        p = sla.cho_solve(decomp, rhs_a)
        q = sla.cho_solve(decomp, np.ones_like(rhs_a))
    except np.linalg.LinAlgError:
        p = sla.solve(mat, rhs_a)
        q = sla.solve(mat, np.ones_like(rhs_a))

    d_b = (p.sum() - rhs_b) / q.sum()
    d_a = (p - d_b * q) / h
    return d_a, d_b


def solve_transposed(k, h, lmbda, rhs, tol=1e-12):
    rhs_a, rhs_b = rhs
    idx_0 = h <= tol
    idx_1 = ~idx_0
    rhs_0, rhs_1 = rhs_a[idx_0], rhs_a[idx_1]
    rhs_rem = (rhs_1, rhs_b)
    h_1 = h[idx_1]
    k_1 = k[idx_1][:, idx_1]
    d_rem_a, d_rem_b = solve_transposed_positive(k_1, h_1, lmbda, rhs_rem)
    d_a = np.zeros_like(h)
    d_a[idx_1] = d_rem_a
    d_a[idx_0] = rhs_0 - k[idx_0][:, idx_1].dot(h_1 * d_rem_a) - d_rem_b
    d_b = d_rem_b
    return d_a, d_b
