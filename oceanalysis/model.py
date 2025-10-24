from yaml import safe_load
from os import path
import xarray as xr

class OceanModel:
    def __init__(self, model_name: str = "POP2-LR"):
        with open(
            path.join(path.dirname(__file__), f"../models/{model_name}.yml"),
            'r') as file:

            _model = safe_load(file)['model']

        self.grid = Grid(_model['grid'], model_name)


class Grid:
    def __init__(self, specs : dict, model_name : str):
        
        self.file_path = path.join(path.dirname(__file__),
            f"../models/{model_name}/{specs["file"]}")
        self.file = xr.load_dataset(self.file_path)

        coords = specs["coords"]

        # grid dimensions
        self.nlon = coords["longitude"]["nlon"]
        self.nlat = coords["latitude"]["nlat"]
        self.nz = coords["depth"]["nz"]

        # grid coordinate indices
        self.ilon = coords["longitude"]["idx"]
        self.ilat = coords["latitude"]["idx"]
        self.iz = coords["depth"]["idx"]

        # scalar points (T-grid)
        self.tlon = self.file[str(coords["longitude"]["name_sca"])]
        self.tlat = self.file[str(coords["latitude"]["name_sca"])]
        
        # vector points (U-grid)
        self.ulon = self.file[str(coords["longitude"]["name_vec"])]
        self.ulat = self.file[str(coords["latitude"]["name_vec"])]

        self.z = coords["depth"]["name"]

        spacing = specs["spacing"]

        self.tdx = spacing["dx"]["sca"]
        self.tdy = spacing["dy"]["sca"]
        self.udx = spacing["dx"]["vec"]
        self.udy = spacing["dy"]["vec"]
        self.tdA = spacing["dA"]["sca"]     # TODO! compute this from dx, dy
        self.udA = spacing["dA"]["vec"]
        
        self.dz = spacing["dz"]