from os import PathLike
from typing import Union
import numpy as np
import xarray as xr

from .model import OceanModel, Grid


class POP2LR(OceanModel):
    def __init__(self, grid_file: Union[str, PathLike]):
        self._grid_data = xr.load_dataset(grid_file)
        self._grid = Grid.from_gridfile(self._grid_data)

    @classmethod
    def from_file(cls, grid_file: Union[str, PathLike]):
        """Create a POP2LR instance from a grid NetCDF file."""
        return cls(grid_file)

    @property
    def grid(self) -> Grid:
        return self._grid
    
    def mask2D(self, region=None):
        if region is None:
            _mask = self._grid_data.REGION_MASK.isin([1,2,3,6,8,9,10]).astype(int)
        elif region == 'Atlantic':
            _mask = self._grid_data.REGION_MASK.isin([6,8,9]).astype(int)
        elif region == 'AtlanticSouthernOcean':
            _mask = self._grid_data.REGION_MASK.isin([1]).astype(int).where(
                (self._grid.tlon < 20) | (self._grid.tlon > 293)
            ).fillna(0) + self._grid_data.REGION_MASK.isin([6,8,9]).astype(int)
        elif region == 'SouthernOcean':
            _mask = self._grid_data.REGION_MASK.isin([1]).astype(int)
        elif region == 'IndoPacific':
            _mask = self._grid_data.REGION_MASK.isin([2,3]).astype(int)
        elif region == 'Arctic':
            _mask = self._grid_data.REGION_MASK.isin([10]).astype(int)

        return _mask.fillna(0)
    
    def mask3D(self, region=None):
        lsm = self._grid_data.seamask.fillna(0)
        if region is None:
            return lsm
        else:
            return lsm * self.mask2D(region)

    def vector_at_tracer(self, u_variable):
        """
        Linear B-grid interpolation. Averages the four U-grid cells around a T-grid cell.
        Periodic boundary conditions zonally, absorbing boundary condition at northern
        border.
        """
        u = np.pad(u_variable.values, ((0,0), (0,1), (0,0)), constant_values=0.0)
        u_shift = np.roll(u, 1, axis=2)
        u_tracer = (u[:, 1:, :] + u[:, :-1, :] + u_shift[:, 1:, :] + u_shift[:, :-1, :])/4
        return xr.DataArray(u_tracer, dims=["k", "j", "i"])