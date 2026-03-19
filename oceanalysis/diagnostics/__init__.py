from ..model import OceanModel

from .streamfunction import moc_streamfunction_depth, amoc_strength

class OceanDiagnostics:

    def __init__(self, model : OceanModel,
        S0=35.0, T0=0.0):

        self.model = model
        self.grid = model.grid

        # Reference values         
        self.S0 = S0               # Reference salinity (g kg^-1)
        self.T0 = T0               # Reference temperature (deg C)


    def moc_streamfunction_depth(self, data, mask):
        return moc_streamfunction_depth(self.model, data, mask)

    def moc_streamfunction_sigma(self, data, mask, sigmas):
        pass

    def amoc_strength(self, data, latitude=26, depth=1000):
        return amoc_strength(self.model, data, latitude, depth)
    
    def surface_buoyancy_flux(self, data, mask):
        pass

    def freshwater_content(self, data, mask):
        pass

    def heat_content(self, data, mask):
        pass
    