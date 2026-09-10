import numpy as np
import xarray as xr

def named_dataarray(array, name="", long_name="", units="", dims=[], coords={}):
    if type(array) in [np.ndarray, list]:
        da = xr.DataArray(array, coords=coords, dims=dims)
    else:
        print(type(array))
        da = array
    da.name = name
    da.attrs['long_name'] = long_name
    da.attrs['units'] = units
    return da


def median_latitude(grid):
    return xr.DataArray(
        np.array([grid.tlat[i,:].median() for i in range(len(grid.tlat.j))]),
        dims=["j"]
    )