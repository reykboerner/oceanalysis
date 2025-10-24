class Grid:
    def __init__(self, parent: "OceanModel"):
        self.parent = parent

    def info(self) -> str:
        """Return a short info string about the grid."""
        return f"Grid for model={self.parent!s}"


class Mask:
    def __init__(self, parent: "OceanModel"):
        self.parent = parent

    def plot(self) -> None:
        """Placeholder plotting method."""
        # In a real package this would create a matplotlib plot. Keep simple here.
        print(f"Plotting mask for model={self.parent!s}")
