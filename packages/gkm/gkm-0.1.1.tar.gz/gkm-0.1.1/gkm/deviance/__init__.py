from .base import Deviance
from .binom import Binomial
from .negbinom import NegativeBinomial
from .gaussian import Gaussian
from .poisson import Poisson
from .exponential import Exponential


Geometric = NegativeBinomial
gaussian = Gaussian()
poisson = Poisson()
geometric = Geometric()
exponential = Exponential()

Normal = Gaussian
normal = gaussian

__all__ = [
    'Deviance',
    'Binomial',
    'NegativeBinomial',
    'Gaussian',
    'Poisson',
    'Exponential',
    'Geometric',
    'Normal',
]
