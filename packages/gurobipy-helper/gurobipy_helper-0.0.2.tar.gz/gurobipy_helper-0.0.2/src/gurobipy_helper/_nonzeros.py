def _init():
    from math import isclose
    import gurobipy as gp

    def get_nonzero_vars(self: gp.Model):
        return [v for v in self.getVars() if not isclose(v.X, 0.0)]

    gp.Model.getNonzeros = get_nonzero_vars
    gp.Model.getNonzeroVars = get_nonzero_vars


_init()
del _init
