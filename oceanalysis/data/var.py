"""Variable container for oceanalysis."""
from __future__ import annotations


class Var:
    def __init__(self, parent: "object"):
        self.parent = parent

    def summary(self) -> None:
        """Print a short summary about the variable container."""
        print(f"Variables summary for data={self.parent}")
