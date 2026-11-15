import numpy as np
import xarray as xr
import warnings
import glob, os
from joblib import Parallel, delayed

class POP():
    def __init__(self, resolution='gx1v6', gridfile="../../data/pop_grid40.nc"):
        """
        Initialize the POP class.

        Keyword arguments
        -----------------
        - resolution: either 'gx1v6' (default, 1 degree) or 'tx0.1v2' (1/10 degree)
        - gridfile: filepath to the grid geometry file
        """

        grid = xr.load_dataset(gridfile).rename(
            {'nlon': 'i', 'nlat': 'j', 'z_t': 'k'}
        )
        self.grid = grid
        self.res = resolution

        if self.res not in ('gx1v6', 'tx0.1v2'):
            raise ValueError("Resolution must be one of 'gx1v6' or 'tx0.1v2'")

    def mask2D(self, label=None, latrange=(-90,90)):
        if label == 'Atlantic':
            _mask = self.grid.REGION_MASK.isin([6,8,9]).astype(int)
        elif label == 'SouthernOcean':
            _mask = self.grid.REGION_MASK.isin([1]).astype(int)
        elif label == 'IndoPacific':
            _mask = self.grid.REGION_MASK.isin([2,3]).astype(int)
        elif label == 'Arctic':
            _mask = self.grid.REGION_MASK.isin([10]).astype(int)
        elif label == None:
            _mask = self.grid.REGION_MASK.isin([1,2,3,6,8,9,10]).astype(int)
        elif label == 'AtlanticSO':
            _mask = (self.grid.REGION_MASK.isin([6,8,9]).astype(int).fillna(0) + 
                self.grid.REGION_MASK.isin([1]).astype(int)).where(
                (self.grid.TLONG < 20) | (self.grid.TLONG > 293)).fillna(0)
        
        return _mask.where(
            (self.grid.TLAT>=latrange[0]) & (self.grid.TLAT<=latrange[1])
        ).fillna(0)
    
    def mask3D(self, mask2D=None):
        land = self.grid.topo_mask3D.fillna(0)
        if mask2D is None:
            return land
        else:
            return land * mask2D

    def vector_at_tracer(self, u_variable):
        """
        Linear B-grid interpolation. Averages the four U-grid cells around a T-grid cell.
        Periodic boundary conditions zonally, absorbing boundary condition at northern
        border.
        """
        u = np.pad(u_variable.values, ((0,0), (0,1), (0,0)), constant_values=0.0)
        u_shift = np.roll(u, 1, axis=2)
        u_tracer = (u[:, 1:, :] + u[:, :-1, :] + u_shift[:, 1:, :] + u_shift[:, :-1, :])/4
        return xr.DataArray(u_tracer, dims=["k", "j", "i"])

    def postprocess(self, tavg_path, diagnostics, years,
        months=range(1, 13),
        ncores=12,
        pattern="t.*.{yyyymm}.nc"):
        """Means of diagnostics(ds) over `months` for each year; incomplete years are skipped."""
        months = list(months)

        def month(f):
            with xr.open_dataset(f) as ds:
                return unpack_diagnostics(diagnostics(ds)).load()

        annual = []
        with Parallel(n_jobs=ncores) as par:
            for year in years:
                files = [glob.glob(os.path.join(tavg_path,
                    pattern.format(yyyymm=f"{year:04d}{m:02d}"))) for m in months]
                missing = [m for m, f in zip(months, files) if not f]
                if missing:
                    warnings.warn(f"Year {year}: missing months {missing} in {tavg_path}; skipping year.")
                    continue
                mon = par(delayed(month)(f[0]) for f in files)
                annual.append(xr.concat(mon, "month").mean("month",
                    keep_attrs=True).assign_coords(time=year))
        return xr.concat(annual, "time")

def unpack_diagnostics(d):
    """{name: DataArray | dict of DataArrays} -> Dataset ('name_key' for dict entries)."""
    out = {}
    for name, res in d.items():
        if isinstance(res, dict):
            out.update({f"{name}_{k}": v for k, v in res.items()})
        else:
            out[name] = res
    return xr.Dataset(out)