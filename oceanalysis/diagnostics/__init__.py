from ..model import OceanModel

from .streamfunction import amoc_strength, moc_streamfunction_depth, moc_streamfunction_sigma


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

    def surface_buoyancy_flux(self, data, mask):
        pass

    def freshwater_content(self, data, mask):
        pass

    def heat_content(self, data, mask):
        pass
    