import xarray as xr
import numpy as np

def moc_streamfunction_depth(model, data, mask):
    v = data.VVEL.where(mask, 0)*100 # TODO: unit conversion
    moc = ((v*model.grid.udx*model.grid.udz).sum("i").cumsum("k")*1e-10)
    moc.name = "meridional_streamfunction_depth"
    moc.attrs['long_name'] = 'Eulerian meridional overturning streamfunction in depth coordinates'
    moc.attrs['units'] = 'Sv'
    return moc

def amoc_strength(model, data, latitude, depth):
    j = model.grid.uj(latitude)
    v = data.VVEL.where(model.mask3D('Atlantic'), 0).isel(j=j)*100 # TODO: unit conversion
    moc = ((v*model.grid.udx.isel(j=j)*model.grid.udz).sum("i").cumsum("k")*1e-10
        ).isel(k=model.grid.uk(depth))
    moc.name = "amoc_strength"
    moc.attrs['long_name'] = f'AMOC at {latitude} degN and {depth} m depth'
    moc.attrs['units'] = 'Sv'
    return moc
    