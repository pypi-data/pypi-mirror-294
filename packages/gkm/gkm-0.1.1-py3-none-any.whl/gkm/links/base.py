class Link:
    def __call__(self, mu):
        raise NotImplementedError()

    def deriv(self, mu):
        raise NotImplementedError()

    def deriv2(self, mu):
        raise NotImplementedError()

    def inverse(self, t):
        raise NotImplementedError()

    def inverse_deriv(self, t):
        return 1.0 / self.deriv(self.inverse(t))

    def inverse_deriv2(self, t):
        mu = self.inverse(t)
        return -self.deriv2(mu) / self.deriv(mu) ** 3
