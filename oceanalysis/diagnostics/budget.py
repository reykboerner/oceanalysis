from .utils import named_dataarray
import numpy as np
import gsw

def freshw_content(model, data, mask):
    """
    Calculates the freshwater content tendency in the region mask for reference
    salinity 35.
    Returns the freshwater content change in units of Sv.
    """
    S_anom = data.SALT.where(mask)*1000 - model.S0 # TODO: unit conversion
    dV = (model.grid.tdA*model.grid.tdz).where(mask, 0.0) # TODO: unit conversion
    W = - (S_anom*dV).sum(dim=['i','j','k'])/model.S0 # in m^3
    return named_dataarray(W,
        name="freshwater_content",
        long_name=f"Freshwater content (ref salinity {model.S0:2.2f} g/kg)",
        units="m^3",
    )

def ocean_heat_content(model, data, mask, T_ref=0.0):
    S = data.SALT.where(mask)*1000 # must be g/kg # TODO: unit conversion
    T = data.TEMP.where(mask) # must be degC # TODO: unit conversion
    theta = gsw.conversions.CT_from_pt(S, T) - T_ref
    p = gsw.p_from_z(- model.grid.tz, model.grid.tlat)
    rho = gsw.density.rho(S, theta, p)

    dV = (model.grid.tdA*model.grid.tdz).where(mask, 0.0) # TODO: unit conversion
    H = model.c_p*(rho*theta*dV).sum(dim=['i', 'j', 'k'])
    return named_dataarray(H*1e-18,
        name="ocean_heat_content",
        long_name=f"Ocean heat content (ref. temperature {T_ref:2.02f} C)",
        units="EJ (10^18 J)"
    )

def freshwater_transport_meridional(model, data, mask, grid_idx):
    v = data.VVEL.where(mask)/100 # TODO: unit conversion
    s = data.SALT.where(mask)*1000 - model.S0 # TODO: unit conversion

    return tracer_transport_section(model, v, s, grid_idx,
        section_direction="zonal", prefactor=-1e-6/model.S0) # in Sv

def freshwater_transport_zonal(model, data, mask, grid_idx):
    v = data.UVEL.where(mask)/100 # TODO: unit conversion
    s = data.SALT.where(mask)*1000 - model.S0 # TODO: unit conversion

    return tracer_transport_section(model, v, s, grid_idx,
        section_direction="meridional", prefactor=-1e-6/model.S0) # in Sv

def heat_transport_section(model, data, mask, grid_idx,
    section_direction = "zonal", T_ref = 0.0):
    """Meridional transport decomposition across a zonal section."""

    N_time = len(data.time)
    transport_ov = np.zeros(N_time)
    transport_az = np.zeros(N_time)
    transport_bt = np.zeros(N_time)
    transport_all = np.zeros(N_time)
    dz = model.grid.tdz

    if section_direction == "zonal":
        vel = data.VVEL.where(mask)/100
        dhor = model.grid.tdx.isel(j=grid_idx)
        dim = 'i'
    elif section_direction == "meridional":
        vel = data.UVEL.where(mask)/100
        dhor = model.grid.tdy.isel(i=grid_idx)
        dim = 'j'
    else:
        raise(ValueError("section_direction must be either zonal or meridional."))

    for t in range(N_time):
        if section_direction == "zonal":
            v = model.vector_at_tracer(vel.isel(time=t)).isel(j=grid_idx)
            T = data.TEMP.isel(time=t).where(mask).isel(j=grid_idx)
            S = data.SALT.isel(time=t).where(mask).isel(j=grid_idx)*1000
            theta = gsw.conversions.CT_from_pt(S, T) - T_ref
            p = gsw.p_from_z(- model.grid.tz, model.grid.tlat.isel(j=grid_idx))
            rho = gsw.density.rho(S, theta, p).where(mask.isel(j=grid_idx))

            v_dirav = v.weighted(model.grid.tdx.isel(j=grid_idx)).mean(dim='i')
            theta_dirav = theta.weighted(model.grid.tdx.isel(j=grid_idx)).mean(dim='i')
            
        elif section_direction == "meridional":
            v = model.vector_at_tracer(vel.isel(time=t)).isel(i=grid_idx)
            T = data.TEMP.isel(time=t).where(mask).isel(i=grid_idx)
            S = data.SALT.isel(time=t).where(mask).isel(i=grid_idx)*1000
            theta = gsw.conversions.CT_from_pt(S, T) - T_ref
            p = gsw.p_from_z(- model.grid.tz, model.grid.tlat.isel(i=grid_idx))
            rho = gsw.density.rho(S, theta, p).where(mask.isel(i=grid_idx))

            v_dirav = v.weighted(model.grid.tdy.isel(i=grid_idx)).mean(dim='j')
            theta_dirav = theta.weighted(model.grid.tdy.isel(i=grid_idx)).mean(dim='j')

        v_secav = v_dirav.weighted(dz).mean(dim='k')
        theta_secav = theta_dirav.weighted(dz).mean(dim='k')
        v_star = v - v_secav
        v_prime = v - v_dirav
        theta_prime = theta - theta_dirav

        transport_ov[t] = model.c_p*(
            (rho*v_star*dhor).sum(dim=dim)*theta_dirav*dz).sum(dim='k').data
        transport_az[t] = model.c_p*(
            (rho*v_prime*theta_prime*dhor).sum(dim=dim)*dz).sum(dim='k').data
        transport_bt[t] = model.c_p*((rho*v*dhor*dz).sum(dim=['k', dim])*theta_secav).data
        transport_all[t] = model.c_p*(
            (v*theta*rho*dhor*dz).sum(dim=['k', dim])
        )
        
        return transport_ov, transport_az, transport_bt, transport_all

def tracer_transport_section(model, vel, tracer, grid_idx,
    section_direction = "zonal", prefactor = 1.0):
    """Meridional transport decomposition across a zonal section."""

    N_time = len(vel.time)
    transport_ov = np.zeros(N_time)
    transport_az = np.zeros(N_time)
    transport_bt = np.zeros(N_time)
    transport_all = np.zeros(N_time)
    dz = model.grid.tdz

    if section_direction == "zonal":
        dhor = model.grid.tdx.isel(j=grid_idx)
        dim = 'i'
    elif section_direction == "meridional":
        dhor = model.grid.tdy.isel(i=grid_idx)
        dim = 'j'
    else:
        raise(ValueError("section_direction must be either zonal or meridional."))

    for t in range(N_time):
        if section_direction == "zonal":
            v = model.vector_at_tracer(vel.isel(time=t)).isel(j=grid_idx)
            q = tracer.isel(time=t, j=grid_idx)
            v_dirav = v.weighted(model.grid.tdx.isel(j=grid_idx)).mean(dim='i')
            q_dirav = q.weighted(model.grid.tdx.isel(j=grid_idx)).mean(dim='i')
            
        elif section_direction == "meridional":
            v = model.vector_at_tracer(vel.isel(time=t)).isel(i=grid_idx)
            q = tracer.isel(time=t, i=grid_idx)
            v_dirav = v.weighted(model.grid.tdy.isel(i=grid_idx)).mean(dim='j')
            q_dirav = q.weighted(model.grid.tdy.isel(i=grid_idx)).mean(dim='j')

        v_secav = v_dirav.weighted(dz).mean(dim='k')
        q_secav = q_dirav.weighted(dz).mean(dim='k')
        v_star = v - v_secav
        v_prime = v - v_dirav
        q_prime = q - q_dirav

        transport_ov[t] = prefactor*(
            (v_star*dhor).sum(dim=dim)*q_dirav*dz).sum(dim='k').data
        transport_az[t] = prefactor*(
            (v_prime*q_prime*dhor).sum(dim=dim)*dz).sum(dim='k').data
        transport_bt[t] = prefactor*((v*dhor*dz).sum(dim=['k', dim])*q_secav).data
        transport_all[t] = prefactor*(
            (v*q*dhor*dz).sum(dim=['k', dim])
        )
        
        return transport_ov, transport_az, transport_bt, transport_all
