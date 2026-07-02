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
                self.grid.REGION_MASK.isin([1]).astype(int)).where((self.grid.TLONG < 20) | (self.grid.TLONG > 293)).fillna(0)
        
        return _mask.where(
            (self.grid.TLAT>=latrange[0]) & (self.grid.TLAT<=latrange[1])
        ).fillna(0)
    
    def mask3D(self, mask2D=None):
        land = self.grid.topo_mask3D.fillna(0)
        if mask2D is None:
            return land
        else:
            return land * mask2D