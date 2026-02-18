# oceanalysis
Flexible diagnostic calculation from 3D ocean model output

## Concept

This Python package provides a collection of ocean model diagnostics written in terms of abstract `OceanModel` and `OceanData` objects. That way, they can easily be applied to specific model output by passing the specifications of the given model and its output format.

## Minimal example
```python
from oceanalysis import OceanModel, OceanData, compute

# specify model
model = OceanModel('POP2-LR')

# load model output file
data = OceanData('my_model_output.nc', 'POP2.yml')

# compute Atlantic meridional overturning streamfunction
compute.streamfunction(model, data, mask=model.mask.Atlantic())
```

## Installation
1. Clone this Github repo: `git clone https://github.com/reykboerner/oceanalysis.git`
2. Change to the package folder: `cd oceanalysis`
3. Install via `pip install .` or (in editable/development mode) `pip install -e .`

## Documentation
### Model specification
#### Grid geometry
The grid data for a given model must be stored in a `.nc` file with dimensions `i` (longitude), `j` (latitude) and `k` (depth downwards) containing the following variables:
- `tlat(i,j)` (curvilinear) or `tlat(j)`: tracer grid latitudes
- `tlon(i,j)` (curvilinear) or `tlon(i)`: tracer grid longitudes
- `ulat(i,j)` (curvilinear) or `ulat(j)`: velocity grid latitudes
- `ulon(i,j)` (curvilinear) or `ulon(i)`: velocity grid longitudes
- `tz(k)`: tracer depth (center of layer)
- `uz(k)`: velocity depth (center of layer)
- `tdx`, `tdy`, `tdz`
- `udx`, `udy`, `udz`
- `tdA(i,j)`, `udA(i,j)`
- `seamask(i,j,k)`: 3D land-sea mask (1 - ocean, 0 - land)

## Contributing

### Diagnostics
To contribute a diagnostic function:
1. Write the function using the attributes of the `OceanModel` and `OceanData` classes.
    - `my_function(model : OceanModel, data : OceanData, ...)`
2. Put this function into its own file `my_diagnostic.py` and add this file to the `oceanalysis/diagnostics` folder.
3. In `oceanalysis/diagnostics/base.py`, add the lines
    - at the top: `from .my_diagnostic import *`
    - in the `Compute` class: `my_diagnostic = staticmethod(my_diagnostic)`

This way, the function can be called (and discovered by autocomplete) via `oceanalysis.compute.my_function`.

### Ocean model
To add a new ocean model to the package, create a `my_model.yml` file in the same structure as `model_config/POP2-LR.yml` and place it in the `model_config` folder. Any files that are referred to by this `.yml` file should be placed in a subfolder of `model_config` called `my_model`.