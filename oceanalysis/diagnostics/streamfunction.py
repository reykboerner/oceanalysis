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
                    v_transp = vel_arr[k, j, i] * 1e-2 * dxu_arr[j, i] * 1e-2 * dz_arr[k]
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
                            mocsig[s, j] -= v_transp * 1e-6
    return mocsig

def moc_streamfunction_sigma(model, data, mask,
    sigmas=np.arange(23, 28.201, 0.1), p_level=0):
    """
    Meridional overturning streamfunction in density coordinates,
    calculated after zonal averaging over the region specified by `mask`.

    The density levels are specified via the `sigmas` kwarg.
    Supports data with or without a time dimension.
    """

    pd = potential_density(data, p_level=p_level)
    vel = data["VVEL"]
    dxu = model.grid.udx
    dz = model.grid.udz

    has_time = "time" in vel.dims
    dxu_arr = dxu.values
    dz_arr = dz.values

    mask_arr = mask.fillna(0).astype(float).values
    jtot = vel.sizes["j"]
    itot = vel.sizes["i"]
    ktot = vel.sizes["k"]

    if has_time:
        ntimes = vel.sizes["time"]
        
        results = []
        for t in range(ntimes):
            pd_slice = pd.isel(time=t).values
            vel_slice = vel.isel(time=t).values
            mocsig = _mocsigma(
                pd_slice, vel_slice, dxu_arr, dz_arr, mask_arr, sigmas, jtot, itot, ktot
            )
            results.append(mocsig)

        stacked = np.stack(results, axis=0)  # Shape: (time, sigma, j)
        j_coords = pd["j"][:-1] if "j" in pd.coords else np.arange(jtot - 1)
        result = xr.DataArray(
            stacked,
            dims=("time", "sigma", "j"),
            coords={
                "time": pd["time"],
                "sigma": np.asarray(sigmas),
                "j": j_coords,
            },
            name="meridional_streamfunction_sigma",
        )
    else:
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

