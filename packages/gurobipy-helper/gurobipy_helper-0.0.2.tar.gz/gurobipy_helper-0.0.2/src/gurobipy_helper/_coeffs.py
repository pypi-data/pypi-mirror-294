def _init():
    import gurobipy as gp

    def get_coeffs(self: gp.Model, arg: gp.Var):
        lin = self.getRow(arg)
        return {lin.getVar(i): lin.getCoeff(i) for i in range(lin.size())}

    gp.Model.getCoeffs = get_coeffs


_init()
del _init
