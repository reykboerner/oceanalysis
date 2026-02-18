from yaml import safe_load
from os import path
import xarray as xr

class OceanModel:
    def __init__(self, model_name: str = "POP2-LR"):
        with open(
            path.join(path.dirname(__file__), f"../model_config/{model_name}.yml"),
            'r') as file:

            _model = safe_load(file)['model']

        self.grid = Grid(_model['grid'], model_name)
        self.mask = Mask(_model['mask'], model_name)

class Grid:
    def __init__(self, specs : dict, model_name : str):
        
        self.file_path = path.join(path.dirname(__file__),
            f"../model_config/{model_name}/{specs["file"]}")
        self.file = xr.load_dataset(self.file_path)

        self.tlat = self.file.tlat
        self.tlon = self.file.tlon
        self.ulat = self.file.ulat
        self.ulon = self.file.ulon
        self.tz = self.file.tz
        self.uz = self.file.uz
        self.tdx = self.file.tdx
        self.tdy = self.file.tdy
        self.tdz = self.file.tdz
        self.udx = self.file.udx
        self.udy = self.file.udy
        self.udz = self.file.udz
        self.tdA = self.file.tdA
        self.udA = self.file.udA

class Mask:
    def __init__(self, specs: dict, model_name : str):

        self.file_path = path.join(path.dirname(__file__),
            f"../model_config/{model_name}/{specs["file"]}")
        self.file = xr.load_dataset(self.file_path)
        
        self.seamask = self.file.seamask


    
    
        