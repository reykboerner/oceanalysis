import xarray as xr
import yaml
from os import path
import numexpr

from .model import OceanModel

class OceanData(xr.Dataset):
    
    __slots__ = ()  # silences the FutureWarning

    def __init__(self, nc_path: str, data_config: str):
        # Load base dataset
        ds = xr.open_dataset(nc_path)

        yaml_path = path.join(path.join(path.dirname(__file__),
            f"../data_config/{data_config}"))
        with open(yaml_path) as f:
            config = yaml.safe_load(f)["data"]
            
        var_map = config["variables"]
        conversions = config.get("unit_conversions", {})

        new_data_vars = {}

        for new_name, old_name in var_map.items():
            if old_name not in ds:
                print(f"⚠️ Variable '{old_name}' not found in dataset; skipping.")
                continue

            da = ds[old_name]

            if new_name in conversions:
                expr = conversions[new_name]
                x = da
                try:
                    da_converted = eval(expr, {"x": x})
                except Exception as e:
                    raise ValueError(f"Error converting '{new_name}': {e}")
            else:
                da_converted = da

            new_data_vars[new_name] = da_converted

        super().__init__(data_vars=new_data_vars, coords=ds.coords, attrs=ds.attrs)
        ds.close()
    
    
    def __repr__(self):
        return f"<OceanData ({list(self.data_vars)})>"