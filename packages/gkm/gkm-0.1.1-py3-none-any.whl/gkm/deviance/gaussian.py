from .base import Deviance


class Gaussian(Deviance):
    def __call__(self, y, t):
        return 0.5 * (t - y) ** 2
