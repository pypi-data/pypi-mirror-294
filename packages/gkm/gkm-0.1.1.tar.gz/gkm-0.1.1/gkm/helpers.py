import numpy as np


def log_keepnone(v):
    if v is None:
        return v
    return np.log(v)


def log_tuple_keepnone(t):
    return tuple(log_keepnone(v) for v in t)


def safe_exp(x):
    return np.exp(np.clip(x, -709.78, 709.78))


def safe_log(x):
    return np.piecewise(
        x,
        [x > np.finfo(float).eps],
        [np.log, lambda x: -np.inf],
    )
