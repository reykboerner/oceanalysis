from dataclasses import dataclass, fields
import xarray as xr
import numpy as np

@dataclass
class Grid:
    tlat: xr.DataArray
    tlon: xr.DataArray
    ulat: xr.DataArray
    ulon: xr.DataArray
    tz: xr.DataArray
    uz: xr.DataArray
    tdx: xr.DataArray
    tdy: xr.DataArray
    tdz: xr.DataArray
    udx: xr.DataArray
    udy: xr.DataArray
    udz: xr.DataArray
    tdA: xr.DataArray
    udA: xr.DataArray

    @classmethod
    def from_gridfile(cls, ds: xr.Dataset):
        kwargs = {}
        for f in fields(cls):
            name = f.name
            if name in ds:
                kwargs[name] = ds[name]
            else:
                raise ValueError(f"Grid nc file missing required variable '{name}'")
        return cls(**kwargs)

    def tj(self, latitude):
        """Return the j index of a curvilinear T grid centered around a given latitude."""
        j = np.abs(self.tlat - latitude).mean(dim='i').argmin()
        return j.item()
    
    def uj(self, latitude):
        """Return the j index of a curvilinear U grid centered around a given latitude."""
        j = np.abs(self.ulat - latitude).mean(dim='i').argmin()
        return j.item()
    
    def uk(self, depth):
        return np.abs(self.uz - depth).argmin().item()

    def tlat_1d(self, mask=None):
        if not mask:
            return self.tlat.mean(dim='i')
        else:
            return self.tlat.where(mask).mean(dim='i')
    
    def ulat_1d(self, mask=None):
        if not mask:
            return self.ulat.mean(dim='i')
        else:
            return self.ulat.where(mask).mean(dim='i')