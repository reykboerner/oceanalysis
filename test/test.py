import xarray as xr
from oceanalysis import OceanModel, POP2LR, OceanDiagnostics

# instantiate POP model
pop = POP2LR("../models/POP2-LR/POP2_gx1v6_40_grid.nc")

# instantiate diagnostics class
compute = OceanDiagnostics(pop)

# Dummy data
data = xr.load_dataset("~/Documents/work/research/mpop/paper/data/t.edgetrP1_on.tmean.nc")

amoc = compute.amoc_strength(data)
print('AMOC strength: ', amoc.values[0], ' Sv')