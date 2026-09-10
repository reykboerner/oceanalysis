import numpy as np
import xarray as xr

from .utils import *
from .density import *

def moc_streamfunction_depth(model, data, mask):
    """
    Meridional overturning streamfunction in depth coordinates,
    calculated after zonal averaging over the region specified by `mask`.
    """
    v = data.VVEL.where(mask, 0)*100 # TODO: unit conversion
    moc = ((v*model.grid.udx*model.grid.udz).sum("i").cumsum("k")*1e-10)
    return named_dataarray(moc,
        name="meridional_streamfunction_depth",
        long_name="Eulerian meridional overturning streamfunction in depth coordinates",
        units="Sv",
    )

def _mocsigma(pd_arr, vel_arr, dxu_arr, dz_arr,
    mask_arr, sigmas, jtot, itot, ktot):
    """Compute streamfunction for a single time slice."""
    mocsig = np.zeros((len(sigmas), jtot - 1), dtype=np.float64)

    for j in range(jtot - 1):
        for k in range(ktot):
            for i in range(itot):
                if mask_arr[k, j, i] > 0.0:
                    v_transp = vel_arr[k, j, i] * dxu_arr[j, i] * dz_arr[k]
                    if i < itot - 1:
                        sigma = (pd_arr[k, j, i]
                            + pd_arr[k, j + 1, i]
                            + pd_arr[k, j, i + 1]
                            + pd_arr[k, j + 1, i + 1])/4
                    else:
                        sigma = (pd_arr[k, j, i]
                            + pd_arr[k, j + 1, i]
                            + pd_arr[k, j, 0]
                            + pd_arr[k, j + 1, 0])/4
                    for s, sig in enumerate(sigmas):
                        if sigma > sig:
                            mocsig[s, j] -= v_transp
    return mocsig * 1e-6 # in Sv

def moc_streamfunction_sigma(model, data, mask,
    sigmas=np.arange(23, 28.201, 0.1), p_level=0):
    """
    Meridional overturning streamfunction in density coordinates,
    calculated after zonal averaging over the region specified by `mask`.

    The density levels are specified via the `sigmas` kwarg.
    Supports data with or without a time dimension.
    """

    pd = potential_density(data, p_level=p_level)
    vel = data["VVEL"]/100 # TODO: units
    dxu = model.grid.udx
    dz = model.grid.udz

    has_time = "time" in vel.dims
    dxu_arr = dxu.values
    dz_arr = dz.values

    mask_arr = mask.fillna(0).astype(float).values
    jtot = vel.sizes["j"]
    itot = vel.sizes["i"]
    ktot = vel.sizes["k"]

    
    mocsig = _mocsigma(
        pd.values, vel.values, dxu_arr, dz_arr, mask_arr, sigmas, jtot, itot, ktot
    )

    j_coords = pd["j"][:-1] if "j" in pd.coords else np.arange(jtot - 1)
    result = xr.DataArray(
        mocsig,
        dims=("sigma", "j"),
        coords={"sigma": np.asarray(sigmas), "j": j_coords},
        name="meridional_streamfunction_sigma",
    )

    result.attrs["long_name"] = "Eulerian meridional overturning streamfunction in density coordinates"
    result.attrs["units"] = "Sv"
    return result


def amoc_strength(model, data, latitude, depth):
    j = model.grid.uj(latitude)
    v = data.VVEL.where(model.mask3D('Atlantic'), 0).isel(j=j)*100 # TODO: unit conversion
    amoc = ((v*model.grid.udx.isel(j=j)*model.grid.udz).sum("i").cumsum("k")*1e-10
        ).isel(k=model.grid.uk(depth))
    return named_dataarray(amoc,
        name="amoc_strength",
        long_name=f"AMOC at {latitude} degN and {depth} m depth",
        units="Sv",
    )

