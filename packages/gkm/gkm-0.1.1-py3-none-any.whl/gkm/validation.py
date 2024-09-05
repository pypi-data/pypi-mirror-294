from inspect import isgenerator
import numpy as np


def score(clf, gamma, k, y, groups, cv, kernel, loss, deriv=False):
    err = []
    derr = []
    refs = []
    for idx_tr, idx_val in cv.split(k, y, groups):
        kt = k[idx_tr, :][:, idx_tr]
        yt = y[idx_tr]
        clf.fit_with_kernel_matrix(kt, yt)

        kv = k[idx_val, :][:, idx_tr]
        yv = y[idx_val]
        yvp = clf.predict_with_kernel_matrix(kv)
        tvp = loss.mean2param(yvp)
        ttm = loss.mean2param(yt.mean())
        refs.append(loss(yv, ttm * np.ones_like(yvp)).sum())
        err.append(loss(yv, tvp).sum())
        if not deriv:
            continue
        dloss = loss.deriv(yv, tvp) * loss.dmean2param(yvp)
        s = clf.sensitivity(kv, dloss)
        derr_lmbda = s['loglmbda']
        dk_tr = kernel.deriv(gamma, k, idx_tr, idx_tr)
        dk_val = kernel.deriv(gamma, k, idx_val, idx_tr)
        if isgenerator(dk_tr):
            derr_kernel = np.array(
                [
                    s['kernel'](dk_tr_i[None], dk_val_i[None])[0]
                    for dk_tr_i, dk_val_i in zip(dk_tr, dk_val)
                ]
            )
        else:
            derr_kernel = s['kernel'](dk_tr, dk_val)
        derr_kernel *= gamma
        derr.append(np.concatenate(([derr_lmbda], derr_kernel)))
    ref = np.sum(refs)
    avg_err = np.sum(err) / ref
    if not deriv:
        return avg_err
    avg_derr = np.sum(derr, axis=0) / ref
    val = avg_err
    dval = avg_derr
    return val, dval
