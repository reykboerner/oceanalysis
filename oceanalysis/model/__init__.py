from .model import OceanModel, Grid, Mask, Const

__all__ = ["OceanModel", "Grid", "Mask", "Const"]

from typing import Any
from yaml import safe_load
from os import path

from .grid import Grid, Mask

class Const:
    def __init__(self, parent: "OceanModel"):
        self.parent = parent

    def values(self) -> dict[str, Any]:
        """Return a dictionary of constant values (placeholder)."""
        return {"g": 9.81, "rho0": 1025}


class OceanModel:
    
    def __init__(self, model_name: str = "POP2-LR"):
        with open(
            path.join(path.dirname(__file__), f"../../models/{model_name}.yml"),
            'r') as file:

            _model = safe_load(file)['model']

        self.model = _model

        _grid = _model['grid']
        _coords = _grid['coords']
        self.grid = Grid(self)

        self.nlon = _coords['longitude']['nlon']

        # attach subcomponents
        self.grid = Grid(self)
        self.mask = Mask(self)
        self.const = Const(self)

        import yaml


    def __repr__(self) -> str:  # pragma: no cover - trivial
        return f"OceanModel(name={self.name!r})"
