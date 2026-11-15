from .density import insitu_density
from .utils import *

def center_of_mass(model, data, add_ssh=True):
    z = model.grid.tz
    dz = model.grid.tdz
    
    if add_ssh:
        ssh = data.SSH/100
        z = z.broadcast_like(ssh).copy()
        dz = dz.broadcast_like(ssh).copy()
        z[dict(k=0)] -= ssh/2 # z positive downwards
        dz[dict(k=0)] += ssh

    rho = insitu_density(model, data).where(model.mask3D(), 0.0)
    num = (rho*z*dz).sum(dim="k")
    denom = (rho*dz).sum(dim="k")
    return named_dataarray(num/denom,
        name="com",
        long_name=f"Center of mass (add_ssh = {add_ssh})",
        units="m",
    )

def kinetic_energy(model, data):
    u = data.UVEL/100
    v = data.VVEL/100
    V = model.grid.udA*model.grid.udz
    m = V*insitu_density(model, data).where(model.mask3D(), 0.0)
    ekin = (m*(u**2 + v**2))/2
    return named_dataarray(ekin/1e12,
        name="ekin",
        long_name="Kinetic energy (using horizontal velocities)",
        units="TJ"
    )