import gsw_xarray as gsw

def conservative_temperature(data):
    S = data.SALT*1000
    T = data.TEMP
    return gsw.conversions.CT_from_pt(S, T)

def potential_density(data, p_level=0):
    if "PD" in data and p_level == 0:
        return (data["PD"] - 1) * 1000
    elif {"SALT", "TEMP"}.issubset(data.data_vars):
        S = data["SALT"]*1000
        CT = gsw.CT_from_pt(SA=S, pt=data["TEMP"])
        if p_level == 0:
            return gsw.sigma0(S, CT)
        elif p_level == 1:
            return gsw.sigma1(S, CT)
        elif p_level == 2:
            return gsw.sigma2(S, CT)
        else:
            raise ValueError("p_level must be 0, 1 or 2")
    else:
        raise ValueError(
            "Data must contain either a density field 'PD' or the 'SALT'/'TEMP' fields.")