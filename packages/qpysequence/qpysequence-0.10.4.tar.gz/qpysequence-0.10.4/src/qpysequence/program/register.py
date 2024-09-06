"""Register module."""
from qpysequence.utils.constants import PROG_REG_PREFIX


class Register:
    """Register class."""

    NOT_ALLOCATED: int = -1

    def __init__(self) -> None:
        self._number: int = Register.NOT_ALLOCATED

    @property
    def number(self) -> int:
        """Returns the number that has been allocated to the register, or -1 if register is not allocated.

        Returns:
            int: The number that has been allocated to the register, or -1 otherwise.
        """
        return self._number

    @property
    def allocated(self) -> bool:
        """Returns true, if the register has been allocated with a number.

        Returns:
            bool: True, if the register has been allocated. False, otherwise.
        """
        return self.number >= 0

    def allocate(self, number: int):
        """Allocate the register to the number.

        Args:
            number (int): The number to allocate the register to.
        """
        self._number = number

    def deallocate(self):
        """Deallocate the register"""
        self._number = Register.NOT_ALLOCATED

    def __repr__(self) -> str:
        """Returns a string representation of the Register.

        Returns:
            str: Q1ASM string representation if allocated, default Python representation otherwise.
        """
        return f"{PROG_REG_PREFIX}{self.number}" if self.allocated else super().__repr__()
