"""Compute subpackage for oceanalysis."""
from .compute import Compute

__all__ = ["Compute"]

class Compute:
    def __init__(self, parent: "object"):
        self.parent = parent

    def run(self, operation: str = "mean") -> Any:
        """Run a simple compute operation (placeholder)."""
        print(f"Running compute operation '{operation}' on data={self.parent}")
        return None
