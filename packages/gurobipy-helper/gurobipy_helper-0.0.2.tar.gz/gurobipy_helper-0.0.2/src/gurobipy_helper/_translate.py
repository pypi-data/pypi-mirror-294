def _init():
    import gurobipy as gp

    def translate(self: gp.Model, arg):
        m = self
        v = arg
        if isinstance(v, gp.Var):
            return gp.Var(m._cmodel, v._colno)
        if isinstance(v, gp.Constr):
            return gp.Constr(m._cmodel, v._rowno)
        if isinstance(v, gp.tupledict):
            return gp.tupledict({ki: translate(m, vi) for ki, vi in v.items()})
        if isinstance(v, tuple):
            return tuple([translate(m, vi) for vi in v])
        if isinstance(v, list):
            return [translate(m, vi) for vi in v]
        if isinstance(v, set):
            return {translate(m, vi) for vi in v}
        if isinstance(v, dict):
            return {ki: translate(m, vi) for ki, vi in v.items()}
        raise TypeError(f'unknown type: {type(v)}')

    def copy_translate(self: gp.Model, arg):
        mn = self.copy()
        vn = translate(mn, arg)
        return mn, vn

    gp.Model.copyTranslate = copy_translate
    gp.Model.translate = translate


_init()
del _init
