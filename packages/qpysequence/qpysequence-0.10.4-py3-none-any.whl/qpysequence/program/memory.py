"""Memory module."""
from .register import Register


class Memory:
    """Memory class to handle and allocate the registers used by a program.

    Args:
        max_registers (int): Maximum number of registers that can be allocated.
    """

    def __init__(self, max_registers: int):
        self.max_registers = max_registers
        self.registry = [False for _ in range(max_registers)]

    def allocate_register_and_mark_in_use(self, register: Register):
        """Allocates the register with the first available number and marks it in use.

        Args:
            register (Register): Register to allocate.

        Raises:
            MemoryError: Reached allocation limit.
        """
        if not register.allocated:
            try:
                index = self.registry.index(False)
            except ValueError as ex:
                raise MemoryError(
                    f"Memory limit exceeded: the maximum number of registers for this memory instance is {self.max_registers}"
                ) from ex

            register.allocate(index)
            self.mark_in_use(register)

    def mark_in_use(self, register: Register):
        """Mark that the register is in use. This will prevent other registers to be allocated with the same number.

        Args:
            register (Register): Register to mark as in-use.
        """
        if register.allocated and 0 <= register.number < self.max_registers:
            self.registry[register.number] = True

    def mark_out_of_use(self, register: Register):
        """Mark that the register is out of use. This will enable other registers to be allocated with the same number.

        Args:
            register (Register): Register to mark as out-of-use.
        """
        if register.allocated and 0 <= register.number < self.max_registers:
            self.registry[register.number] = False
