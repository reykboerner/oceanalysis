import xarray as xr

from .model import OceanModel, Grid

class POP2LR(OceanModel):
    def __init__(self, grid_file : str):
        self.grid_data = xr.load_dataset(grid_file)
        self._grid = Grid.from_gridfile(self.grid_data)
    
    @property
    def grid(self) -> Grid:
        return self._grid
    
    def mask2D(self, region=None):
        if region is None:
            _mask = self.grid_data.REGION_MASK.isin([1,2,3,6,8,9,10]).astype(int)
        elif region == 'Atlantic':
            _mask = self.grid_data.REGION_MASK.isin([6,8,9]).astype(int)
        return _mask.fillna(0)
    
    def mask3D(self, region=None):
        lsm = self.grid_data.seamask.fillna(0)
        if region is None:
            return lsm
        else:
            return lsm * self.mask2D(region)
