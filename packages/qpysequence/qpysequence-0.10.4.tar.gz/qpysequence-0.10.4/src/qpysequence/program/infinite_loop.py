"""Iterative Loop module
"""
from .block import Block
from .instructions import Jmp


class InfiniteLoop(Block):
    """Infinite loop class."""

    def __init__(self, name: str):
        super().__init__(name)
        self._generate_builtin_components()

    def _generate_builtin_components(self):
        """Generates the builtin components of the Loop."""
        self.builtin_components.append(Jmp(f"@{self.name}"))

    @property
    def duration(self) -> int:
        """Duration of all the iterations. Since it is an infinite loop, it returns -1.

        Returns:
            int: Duration in nanoseconds of all the iterations.
        """
        return -1
