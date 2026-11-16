import gsw
import xarray as xr
from .utils import named_dataarray, datadict
from .density import potential_density, conservative_temperature

def surface_buoyancy_flux(model, data, mask, rho0=1027):
    S = data.SALT.isel(k=0).where(mask)*1000
    T = data.TEMP.isel(k=0).where(mask)
    Q_T = data.SHF.where(mask)
    Q_S = data.SFWF.where(mask)

    CT = gsw.conversions.CT_from_pt(S, T)
    p = gsw.conversions.p_from_z(-0.0, 0)
    alpha = gsw.density.alpha(S, CT, p)
    beta = gsw.density.beta(S, CT, p)
    c_p = gsw.cp_t_exact(S, T, p)

    B_T = model.gravity*alpha/(rho0*c_p)*Q_T
    B_S = model.gravity*beta*S/rho0*Q_S

    return datadict((
        (B_T, "Bflux_T", "Surface buoyancy flux (T component)", "W/kg"),
        (B_S, "Bflux_S", "Surface buoyancy flux (S component)", "W/kg"),
    ))

def buoyancy_frequency(model, data, mask):
    """
    Calculates the Brunt-Väisälä frequency, denoted N^2, decomposed into thermal and
    haline components, for ocean model `data` in the 3D volume specified by `mask`.
    """
    S = data.SALT.where(mask)*1000
    CT = conservative_temperature(data).where(mask)
    p = gsw.conversions.p_from_z(-model.grid.tz, model.grid.tlat)
    alpha = gsw.density.alpha(S, CT, p).isel(k=slice(1,None))
    beta = gsw.density.beta(S, CT, p).isel(k=slice(1,None))

    N_T = - alpha*CT.diff("k")/model.grid.tz.diff("k")
    N_S = beta*S.diff("k")/model.grid.tz.diff("k")
    N2 = xr.DataArray(gsw.stability.Nsquared(S, CT, p)[0], dims=["k", "j", "i"],
        coords={"k": model.grid.uz[:-1], "j": model.grid.tlat.j, "i": model.grid.tlon.i})

    return datadict((
        (N2, "Nsquared", "Buoyancy frequency (calculated with gsw)", "rad/s^2"),
        (model.gravity*(N_T), "Nsquared_T", "Buoyancy frequency (T component)", "rad/s^2"),
        (model.gravity*(N_S), "Nsquared_S", "Buoyancy frequency (S component)", "rad/s^2"),
    ))