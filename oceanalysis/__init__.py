from ._proxy import _CallableProxy
from .model import OceanModel as _OceanModelClass
from .data import OceanData as _OceanDataClass
from .diagnostics import Compute

__all__ = ["OceanModel", "OceanData", "compute"]

OceanModel = _CallableProxy(_OceanModelClass)
OceanData = _CallableProxy(_OceanDataClass)
compute: Compute = _CallableProxy(Compute)