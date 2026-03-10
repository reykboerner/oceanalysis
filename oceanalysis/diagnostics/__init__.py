from .projection import reduced_salinity_space

class Compute:
    reduced_salinity_space = staticmethod(reduced_salinity_space)

__all__ = ["Compute"]