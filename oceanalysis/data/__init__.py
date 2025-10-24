"""Data subpackage for oceanalysis."""
from .data import OceanData
from .var import Var
from ..compute import Compute

__all__ = ["OceanData", "Var", "Compute"]

class OceanData:
    """Container for data-related utilities."""

    def __init__(self, source: str = "OceanData"):
        self.source = source
        self.var = Var(self)
        self.compute = Compute(self)

    def __repr__(self) -> str:  # pragma: no cover - trivial
        return f"OceanData(source={self.source!r})"
