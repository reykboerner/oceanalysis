"""Data handling classes for oceanalysis.

Contains OceanData with subcomponents var and compute.
"""
from __future__ import annotations
from typing import Any
from .var import Var
from ..compute import Compute


class OceanData:
    """Container for data-related utilities."""

    def __init__(self, source: str = "OceanData"):
        self.source = source
        self.var = Var(self)
        self.compute = Compute(self)

    def __repr__(self) -> str:  # pragma: no cover - trivial
        return f"OceanData(source={self.source!r})"
