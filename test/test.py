import xarray as xr
import matplotlib.pyplot as plt
import numpy as np

from oceanalysis import POP2LR, OceanDiagnostics

# instantiate POP model
pop = POP2LR.from_file("../models/POP2-LR/POP2_gx1v6_40_grid.nc")

# instantiate diagnostics class
diag = OceanDiagnostics(pop)

# Dummy data
data = xr.load_dataset("~/Documents/work/research/mpop/paper/data/t.edgetrP1_on.tmean.nc")

amoc = diag.amoc_strength(data)
print('AMOC strength: ', amoc.values[0], ' Sv')

sfc = diag.moc_streamfunction_depth(data, pop.mask3D('Atlantic'))
plt.contourf(sfc.isel(time=0))
plt.show()

sfc_sig = diag.moc_streamfunction_sigma(data, pop.mask3D('Atlantic'), np.arange(23, 28.201, 0.1))
print(sfc_sig)
plt.contourf(sfc_sig.isel(time=0))
plt.show()