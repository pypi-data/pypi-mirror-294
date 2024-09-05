class Kernel:
    def get_bounds(self, bounds):
        raise NotImplementedError()

    def get_initial(self, gamma0):
        raise NotImplementedError()

    def prepare(self, X):
        raise NotImplementedError()

    def __call__(self, params, idx1=slice(None), idx2=slice(None)):
        raise NotImplementedError()

    def deriv(self, params, k, idx1=slice(None), idx2=slice(None)):
        raise NotImplementedError()

    def compute(self, params, X):
        raise NotImplementedError()

    @property
    def dim(self):
        raise NotImplementedError()
