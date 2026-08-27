from ..model import OceanModel

from .streamfunction import amoc_strength, moc_streamfunction_depth, moc_streamfunction_sigma
from .budget import freshw_content, freshwater_transport_meridional, freshwater_transport_zonal, tracer_transport_section, ocean_heat_content, heat_transport_section
from .buoyancy import surface_buoyancy_flux
from .projection import reduced_salinity_space
from .utils import median_latitude

class OceanDiagnostics:

    def __init__(self, model : OceanModel,
        S0=35.0, T0=0.0):

        self.model = model
        self.grid = model.grid

        # Reference values
        self.S0 = S0  # Reference salinity (g kg^-1)
        self.T0 = T0  # Reference temperature (deg C)

    def moc_streamfunction_depth(self, data, mask):
        return moc_streamfunction_depth(self.model, data, mask)

    def moc_streamfunction_sigma(self, data, mask, sigmas, p_level=0):
        return moc_streamfunction_sigma(self.model, data, mask, sigmas=sigmas, p_level=p_level)

    def amoc_strength(self, data, latitude=26, depth=1000):
        return amoc_strength(self.model, data, latitude, depth)

    def surface_buoyancy_flux(self, data, mask, **kw):
        return surface_buoyancy_flux(self.model, data, mask, **kw)

    def freshwater_content(self, data, mask):
        return freshw_content(self.model, data, mask)

    def ocean_heat_content(self, data, mask, T_ref=0.0):
        return ocean_heat_content(self.model, data, mask, T_ref=0.0)

    def freshwater_transport_meridional(self, data, mask, j, **kw):
        return freshwater_transport_meridional(self.model, data, mask, j, **kw)

    def freshwater_transport_zonal(self, data, mask, i, **kw):
        return freshwater_transport_zonal(self.model, data, mask, i, **kw)

    def heat_transport_section(self, data, mask, grid_idx, **kw):
        return heat_transport_section(self.model, data, mask, grid_idx, **kw)

    def tracer_transport_section(self, vel, tracer, grid_idx, **kw):
        return tracer_transport_section(self.model, vel, tracer, grid_idx, **kw)

    def reduced_salinity_space(self, data):
        return reduced_salinity_space(self.model, data)

    ### TEMP

    def surface_heat_flux(self, data, mask):
        _data = data.where(mask)
        swnet = _data.SWNET
        lwnet = _data.LWNET
        latent = _data.LATENT
        sensible = _data.SENSIBLE
        rest = _data.T_STRONG_REST
        total = _data.SHF
        return total, swnet, lwnet, latent, sensible, rest

    def surface_freshwater_flux(self, data, mask):
        """
        Returns net surface freshwater flux in region mask, decomposed into components.
        """
        P = data.PRECIP.where(mask)
        E = data.EVAP.where(mask)
        R = data.RUNOFF.where(mask) # kg/m^2/s
        rest = data.S_WEAK_REST.where(mask)
        total = data.SFWF.where(mask) 
        melt = total - (P + E + R + rest)
        return [total, P, E, R, melt]

    def median_latitude(self):
        return median_latitude(self.model.grid)
    
    