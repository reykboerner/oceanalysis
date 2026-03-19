import xarray as xr

def named_dataarray(array, name="", long_name="", units=""):
    array.name = name
    array.attrs('long_name') = long_name
    array.attrs('units') = units
    return array

def named_nparray(array, name="", long_name="", units="", dims=[], coords={}):
    da = xr.DataArray(array, coords=coords, dims=dims)
    return named_dataarray(da, **kwargs)