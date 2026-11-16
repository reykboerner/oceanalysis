import xarray as xr
from .utils import median_latitude, named_dataarray

import numpy as np

def reduced_salinity_space(model, data, S0=35.0):
    lat = median_latitude(model.grid)
    latweights = model.grid.latweights(lat)

    def get_idx(val):
        return int(np.where(lat>val)[0][0])

    zonav = data.SALT.where(model.mask3D('Atlantic')).weighted(model.grid.tdA).mean(dim='i')*1000

    upper = zonav.isel(k=slice(8,21)).weighted(model.grid.tdz.isel(k=slice(8,21))).mean(dim='k')
    lower = zonav.isel(k=slice(21,30)).weighted(model.grid.tdz.isel(k=slice(21,30))).mean(dim='k')

    upN = upper.isel(j=slice(get_idx(40),get_idx(77))).weighted(latweights.isel(j=slice(get_idx(40),get_idx(77)))).mean(dim='j').values
    upS = upper.isel(j=slice(get_idx(0),get_idx(20))).weighted(latweights.isel(j=slice(get_idx(0),get_idx(20)))).mean(dim='j').values

    upV = upper.isel(j=slice(get_idx(46),get_idx(66))).weighted(latweights.isel(j=slice(get_idx(46),get_idx(66)))).mean(dim='j').values
    dnV = lower.isel(j=slice(get_idx(46),get_idx(66))).weighted(latweights.isel(j=slice(get_idx(46),get_idx(66)))).mean(dim='j').values

    deep = zonav.isel(k=slice(21,None)).weighted(model.grid.tdz.isel(k=slice(21,None))).mean(dim='k').isel(
        j=slice(get_idx(50),get_idx(77))).weighted(latweights.isel(
        j=slice(get_idx(50),get_idx(77)))).mean(dim='j').values - S0

    return named_dataarray(np.array([upS - upN, upV - dnV, deep]),
        name="redu", long_name="Reduced salinity space (1: Meridional SG, 2: Vertical SG, 3: deep N. Atl. salinity anomaly)",
        units="g/kg", dims=["redu"], coords={"redu": [1,2,3]})

    # return datadict((
    #     (xr.DataArray(upS - upN), "d1", "Meridional salinity gradient", "g/kg"),
    #     (xr.DataArray(upV - dnV), "d2", "Vertical salinity gradient", "g/kg"),
    #     (xr.DataArray(deep), "d3", "Deep North Atlantic salinity anomaly", "g/kg"),
    # ))