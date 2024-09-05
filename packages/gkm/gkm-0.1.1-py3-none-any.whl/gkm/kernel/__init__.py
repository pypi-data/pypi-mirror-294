from .base import Kernel
from .rbf import RBF
from .multi_rbf import MultiRBF
from .multi_rbf_lazy import MultiRBFLazy


def get_kernel(name):
    kernel_cls = {
        'rbf': RBF,
        'multi-rbf': MultiRBF,
        'multi-rbf-lazy': MultiRBFLazy,
    }.get(name, None)
    if kernel_cls is None:
        raise ValueError('unknown kernel')
    return kernel_cls()


__all__ = ['Kernel', 'RBF', 'MultiRBF', 'MultiRBFLazy', 'get_kernel']
