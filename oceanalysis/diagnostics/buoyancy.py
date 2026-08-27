import gsw

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

    return [B_T_av, B_S_av], [B_T, B_S]