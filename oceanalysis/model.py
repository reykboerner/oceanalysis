from abc import ABC, abstractmethod

from .grid import Grid

class OceanModel(ABC):

        # Physical model constants
        gravity = 9.81          # Gravitational acceleration (m s^-2)
        
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