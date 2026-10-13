from .utils import named_dataarray
import numpy as np
import gsw

from .density import conservative_temperature

def freshw_content(model, data, mask, return_density_units=False):
    """
    Calculates the freshwater content tendency in the region mask for reference
    salinity 35.
    Returns the freshwater content change in units of Sv.
    """
    S = data.SALT.where(mask)*1000
    S_anom = S - model.S0 # TODO: unit conversion
    dV = (model.grid.tdA*model.grid.tdz).where(mask, 0.0) # TODO: unit conversion
    if return_density_units:
        CT = conservative_temperature(data).where(mask)
        p = gsw.conversions.p_from_z(- model.grid.tz, model.grid.tlat)
        beta = gsw.density.beta(S, CT, p)
        W = - model.gravity*(S_anom*beta*dV).sum(dim=['i', 'j', 'k'])
        units = "kg (density times volume)"
    else:
        W = - (S_anom*dV).sum(dim=['i','j','k'])/model.S0 # in m^3
        units = "m^3"
    return named_dataarray(W,
        name="freshwater_content",
        long_name=f"Freshwater content (ref salinity {model.S0:2.2f} g/kg)",
        units=units,
    )

def ocean_heat_content(model, data, mask, T_ref=0.0, return_density_units=False):
    S = data.SALT.where(mask)*1000 # must be g/kg # TODO: unit conversion
    T = data.TEMP.where(mask) # must be degC # TODO: unit conversion
    CT = gsw.conversions.CT_from_pt(S, T) 
    theta = CT - T_ref
    p = gsw.p_from_z(- model.grid.tz, model.grid.tlat)
    rho = gsw.density.rho(S, CT, p)
    dV = (model.grid.tdA*model.grid.tdz).where(mask, 0.0) # TODO: unit conversion
    if return_density_units:
        alpha = gsw.density.alpha(S, CT, p)
        H = model.gravity*(alpha*theta*dV).sum(dim=['i', 'j', 'k'])
        units = "kg (density times volume)"
    else:
        H = model.c_p*(rho*theta*dV*1e-6).sum(dim=['i', 'j', 'k'])*1e-12
        units = "EJ (10^18 J)"
    return named_dataarray(H,
        name="ocean_heat_content",
        long_name=f"Ocean heat content (ref. temperature {T_ref:2.02f} C)",
        units= units
    )

def freshwater_transport_meridional(model, data, mask, grid_idx):
    v = data.VVEL.where(mask)/100 # TODO: unit conversion
    s = data.SALT.where(mask)*1000 - model.S0 # TODO: unit conversion

    _ov, _az, _bt, _all = tracer_transport_section(model, v, s, grid_idx,
        section_direction="zonal", prefactor=-1e-6/model.S0) # in Sv

    transport_ov = named_dataarray(_ov,
        name="F_ov", long_name="Freshwater transport across S->N section (overturning component)",
        units="Sv", dims=["section"], coords={"section" : [grid_idx]})
    transport_az = named_dataarray(_az,
        name="F_az", long_name="Freshwater transport across S->N section (gyre component)",
        units="Sv", dims=["section"], coords={"section" : [grid_idx]})
    transport_bt = named_dataarray(_bt,
        name="F_bt", long_name="Freshwater transport across S->N section (barotropic component)",
        units="Sv", dims=["section"], coords={"section" : [grid_idx]})
    transport_all = named_dataarray(_all,
        name="F_all", long_name="Freshwater transport across S->N section (total)",
        units="Sv", dims=["section"], coords={"section" : [grid_idx]})
    
    return transport_ov, transport_az, transport_bt, transport_all

def freshwater_transport_zonal(model, data, mask, grid_idx):
    v = data.UVEL.where(mask)/100 # TODO: unit conversion
    s = data.SALT.where(mask)*1000 - model.S0 # TODO: unit conversion

    _ov, _az, _bt, _all = tracer_transport_section(model, v, s, grid_idx,
        section_direction="meridional", prefactor=-1e-6/model.S0) # in Sv

    transport_ov = named_dataarray(_ov,
        name="F_ov", long_name="Freshwater transport across W->E section (overturning component)",
        units="Sv", dims=["section"], coords={"section" : [grid_idx]})
    transport_az = named_dataarray(_az,
        name="F_az", long_name="Freshwater transport across W->E section (gyre component)",
        units="Sv", dims=["section"], coords={"section" : [grid_idx]})
    transport_bt = named_dataarray(_bt,
        name="F_bt", long_name="Freshwater transport across W->E section (barotropic component)",
        units="Sv", dims=["section"], coords={"section" : [grid_idx]})
    transport_all = named_dataarray(_all,
        name="F_all", long_name="Freshwater transport across W->E section (total)",
        units="Sv", dims=["section"], coords={"section" : [grid_idx]})
    
    return transport_ov, transport_az, transport_bt, transport_all

def heat_transport_section(model, data, mask, grid_idx,
    section_direction = "zonal", T_ref = 0.0):
    """Meridional transport decomposition across a zonal section."""

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

    if section_direction == "zonal":
        v = model.vector_at_tracer(vel).isel(j=grid_idx)
        T = data.TEMP.where(mask).isel(j=grid_idx)
        S = data.SALT.where(mask).isel(j=grid_idx)*1000
        theta = gsw.conversions.CT_from_pt(S, T) - T_ref
        p = gsw.p_from_z(- model.grid.tz, model.grid.tlat.isel(j=grid_idx))
        rho = gsw.density.rho(S, theta, p).where(mask.isel(j=grid_idx))

        v_dirav = v.weighted(model.grid.tdx.isel(j=grid_idx)).mean(dim='i')
        theta_dirav = theta.weighted(model.grid.tdx.isel(j=grid_idx)).mean(dim='i')
        
    elif section_direction == "meridional":
        v = model.vector_at_tracer(vel).isel(i=grid_idx)
        T = data.TEMP.where(mask).isel(i=grid_idx)
        S = data.SALT.where(mask).isel(i=grid_idx)*1000
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

    _ov = model.c_p*(
        (rho*v_star*dhor).sum(dim=dim)*theta_dirav*dz).sum(dim='k').data
    _az = model.c_p*(
        (rho*v_prime*theta_prime*dhor).sum(dim=dim)*dz).sum(dim='k').data
    _bt = model.c_p*((rho*v*dhor*dz).sum(dim=['k', dim])*theta_secav).data
    _all = model.c_p*(
        (v*theta*rho*dhor*dz).sum(dim=['k', dim])
    )

    transport_ov = named_dataarray([_ov],
        name="H_ov", long_name="Heat transport across section (overturning component)",
        units="W", dims=["section"], coords={"section" : [grid_idx]})
    transport_az = named_dataarray([_az],
        name="H_az", long_name="Heat transport across section (gyre component)",
        units="W", dims=["section"], coords={"section" : [grid_idx]})
    transport_bt = named_dataarray([_bt],
        name="H_bt", long_name="Heat transport across section (barotropic component)",
        units="W", dims=["section"], coords={"section" : [grid_idx]})
    transport_all = named_dataarray([_all],
        name="H_all", long_name="Heat transport across section (total)",
        units="W", dims=["section"], coords={"section" : [grid_idx]})
    
    return transport_ov, transport_az, transport_bt, transport_all

def tracer_transport_section(model, vel, tracer, grid_idx,
    section_direction = "zonal", prefactor = 1.0):
    """Meridional transport decomposition across a zonal section."""

    dz = model.grid.tdz

    if section_direction == "zonal":
        dhor = model.grid.tdx.isel(j=grid_idx)
        dim = 'i'
    elif section_direction == "meridional":
        dhor = model.grid.tdy.isel(i=grid_idx)
        dim = 'j'
    else:
        raise(ValueError("section_direction must be either zonal or meridional."))

    if section_direction == "zonal":
        v = model.vector_at_tracer(vel).isel(j=grid_idx)
        q = tracer.isel(j=grid_idx)
        v_dirav = v.weighted(model.grid.tdx.isel(j=grid_idx)).mean(dim='i')
        q_dirav = q.weighted(model.grid.tdx.isel(j=grid_idx)).mean(dim='i')
        
    elif section_direction == "meridional":
        v = model.vector_at_tracer(vel).isel(i=grid_idx)
        q = tracer.isel(i=grid_idx)
        v_dirav = v.weighted(model.grid.tdy.isel(i=grid_idx)).mean(dim='j')
        q_dirav = q.weighted(model.grid.tdy.isel(i=grid_idx)).mean(dim='j')

    v_secav = v_dirav.weighted(dz).mean(dim='k')
    q_secav = q_dirav.weighted(dz).mean(dim='k')
    v_star = v - v_secav
    v_prime = v - v_dirav
    q_prime = q - q_dirav

    transport_ov = prefactor*(
        (v_star*dhor).sum(dim=dim)*q_dirav*dz).sum(dim='k').data
    transport_az = prefactor*(
        (v_prime*q_prime*dhor).sum(dim=dim)*dz).sum(dim='k').data
    transport_bt = prefactor*((v*dhor*dz).sum(dim=['k', dim])*q_secav).data
    transport_all = prefactor*((v*q*dhor*dz).sum(dim=['k', dim]))

    return [transport_ov], [transport_az], [transport_bt], [transport_all]
