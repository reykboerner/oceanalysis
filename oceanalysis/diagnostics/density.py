import gsw_xarray as gsw

def potential_density(data, p_level=0):
    if "PD" in data and p_level == 0:
        return (data["PD"] - 1) * 1000
    elif {"SALT", "TEMP"}.issubset(data.data_vars):
        conservative_temp = gsw.CT_from_pt(SA=data["SALT"] * 1000, pt=data["TEMP"])
        return gsw.rho(SA=data["SALT"] * 1000, CT=conservative_temp, p=p_level) - 1000
    else:
        raise ValueError(
            "Data must contain either a density field 'PD' or the 'SALT'/'TEMP' fields.")