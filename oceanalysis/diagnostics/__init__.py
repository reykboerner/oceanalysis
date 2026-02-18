from .overturning import streamfunction_z

class Compute:
    streamfunction_z = staticmethod(streamfunction_z)

__all__ = ["Compute"]