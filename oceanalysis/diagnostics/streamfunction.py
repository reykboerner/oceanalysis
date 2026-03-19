import xarray as xr
import numpy as np

from .utils import *

def moc_streamfunction_depth(model, data, mask):
    v = data.VVEL.where(mask, 0)*100 # TODO: unit conversion
    moc = ((v*model.grid.udx*model.grid.udz).sum("i").cumsum("k")*1e-10)
    return named_dataarray(moc,
        name="meridional_streamfunction_depth",
        long_name='Eulerian meridional overturning streamfunction in depth coordinates',
        units='Sv'
    )

def amoc_strength(model, data, latitude, depth):
    j = model.grid.uj(latitude)
    v = data.VVEL.where(model.mask3D('Atlantic'), 0).isel(j=j)*100 # TODO: unit conversion
    amoc = ((v*model.grid.udx.isel(j=j)*model.grid.udz).sum("i").cumsum("k")*1e-10
        ).isel(k=model.grid.uk(depth))
    return named_dataarray(amoc,
        name="amoc_strength",
        long_name=f'AMOC at {latitude} degN and {depth} m depth',
        units='Sv',
    )
