# oceanalysis
Flexible diagnostic calculation from 3D ocean model output

## Concept

This Python package provides a collection of ocean model diagnostics written with respect to an abstract `OceanModel` class.

## Minimal example (POP2 model)
```python
from oceanalysis import POP2LR, OceanDiagnostics

# initialize model from grid file
pop = POP2LR("../models/POP2-LR/POP2_gx1v6_40_grid.nc")
compute = OceanDiagnostics(pop)

# compute AMOC strength
amoc = compute.amoc_strength(data)
```
See also `test/test.py`.

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
- `tdx`, `tdy`, `tdz`: T grid spacing
- `udx`, `udy`, `udz`: U grid spacing
- `tdA(i,j)`, `udA(i,j)`: horizontal grid cell areas
- `seamask(i,j,k)`: 3D land-sea mask (1 - ocean, 0 - land)
