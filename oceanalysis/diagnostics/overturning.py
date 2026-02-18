def streamfunction(model, data, mask=None):
    """
    Computes the Eulerian meridional overturning circulation in the ocean volume
    specified by mask.
    """
    if not mask:
        v = data.vvel
    else:
        v = data.vvel.where(mask, 0)

    print(v.shape)

    print(v.dims)
    print(model.grid.udx.dims)
    moc = (v*model.grid.udx*model.grid.dz).sum(dim=model.grid.ilon).cumsum(dim=model.grid.iz)/1e6
    moc.name = "meridional_streamfunction"
    moc.assign_attrs(
        units="Sv",
        long_name="Eulerian meridional overturning streamfunction"
    )
    return moc