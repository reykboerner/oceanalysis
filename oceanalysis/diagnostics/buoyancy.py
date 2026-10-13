import gsw
import xarray as xr
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

    B_T_av = B_T.where(mask).weighted(model.grid.tdA).mean(dim=['i', 'j'])
    B_S_av = B_S.where(mask).weighted(model.grid.tdA).mean(dim=['i', 'j'])

    return xr.Dataset(
        {
            "Bflux_T" : B_T,
            "Bflux_S" : B_S,
            "Bflux_T_av" : B_T_av,
            "Bflux_S_av" : B_S_av,
        }
    )

def buoyancy_frequency(model, data, mask):
    """
    Calculates the Brunt-Väisälä frequency, denoted N^2, decomposed into thermal and
    haline components, for ocean model `data` in the 3D volume specified by `mask`.
    """
    S = data.SALT.where(mask)*1000
    CT = conservative_temperature(data).where(mask)
    p = gsw.conversions.p_from_z(- model.grid.tz, model.grid.tlat)
    alpha = gsw.density.alpha(S, CT, p).isel(k=slice(1,None))
    beta = gsw.density.beta(S, CT, p).isel(k=slice(1,None))

    N_T = - alpha*CT.diff("k")/model.grid.tz.diff("k")
    N_S = beta*S.diff("k")/model.grid.tz.diff("k")

    return xr.Dataset(
        {
            "Nsquared" : model.gravity*(N_T + N_S),
            "Nsquared_T" : model.gravity*N_T,
            "Nsquared_S" : model.gravity*N_S,
        }
    )