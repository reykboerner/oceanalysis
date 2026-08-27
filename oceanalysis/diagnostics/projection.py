from .utils import median_latitude

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

    return upS - upN, upV - dnV, deep