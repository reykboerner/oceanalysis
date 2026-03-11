from abc import ABC, abstractmethod
from ..model import OceanModel

from .streamfunction import moc_streamfunction_depth, amoc_strength

class OceanDiagnostics(ABC):

    def __init__(self, model : OceanModel):
        self.model = model
        self.grid = model.grid

    def moc_streamfunction_depth(self, data, mask):
        return moc_streamfunction_depth(self.model, data, mask)

    def amoc_strength(self, data, latitude=26, depth=1000):
        return amoc_strength(self.model, data, latitude, depth)
    