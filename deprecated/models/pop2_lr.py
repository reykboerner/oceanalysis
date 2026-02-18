from ..model import OceanModel, Mask

class POP2LR(OceanModel):
    def __init__(self): 
        super().__init__()
        self.mask = OceanModel.mask