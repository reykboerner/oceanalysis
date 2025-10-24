from .model import OceanModel as _OceanModelClass
from .data import OceanData as _OceanDataClass
from .compute import compute as _compute
from .run import run as _run

__all__ = ["OceanModel", "OceanData", "compute", "run"]

class _CallableProxy:
    """A proxy that is callable (to create new instances) and also
    forwards attribute access to a default instance.

    This lets callers both instantiate the class (e.g. OceanModel(name="x"))
    and access a convenient package-level default instance via
    attribute access (e.g. OceanModel.mask.plot()).
    """

    def __init__(self, cls):
        self._cls = cls
        self._default = cls()

    def __call__(self, *args, **kwargs):
        return self._cls(*args, **kwargs)

    def __getattr__(self, name):
        # forward attribute access to the default instance
        return getattr(self._default, name)


# Export proxies named OceanModel and OceanData. They behave like the class
# when called, but also expose attributes from a default instance for
# convenience, allowing: oceanalysis.OceanModel.mask.plot()
OceanModel = _CallableProxy(_OceanModelClass)
OceanData = _CallableProxy(_OceanDataClass)
compute = _CallableProxy(_compute)
run = _CallableProxy(_run)