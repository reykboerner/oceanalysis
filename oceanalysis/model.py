from abc import ABC, abstractmethod

from .grid import Grid

class OceanModel(ABC):

        @property
        @abstractmethod
        def grid(self) -> Grid:
            pass
        
        @abstractmethod
        def mask2D(self, region_name=None):
            pass

        @abstractmethod
        def mask3D(self, region_name=None):
            pass