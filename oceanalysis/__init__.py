from .model import OceanModel as _OceanModelClass
from .diagnostics import Compute

class _CallableProxy:
    """Forwards attribute lookups and calls to the target class."""

    def __init__(self, target_cls):
        self._target_cls = target_cls

    def __getattr__(self, name):
        # Forward attributes to the class
        return getattr(self._target_cls, name)

    def __call__(self, *args, **kwargs):
        # Allow calling the proxy directly if desired
        return self._target_cls(*args, **kwargs)

__all__ = ["OceanModel", "compute"]

OceanModel = _CallableProxy(_OceanModelClass)
compute: Compute = _CallableProxy(Compute)