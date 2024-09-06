""" WaitTrigger Instruction """

from qpysequence.program.instructions.instruction import Instruction
from qpysequence.program.register import Register
from qpysequence.utils.constants import INST_MAX_WAIT, INST_MIN_WAIT
from qpysequence.utils.enums import InstructionArgument


class WaitTrigger(Instruction):
    """
    Wait for a trigger on the trigger network at the address set using the `address` argument and then wait for
    `wait_time` number of nanoseconds.

    Args:
        address (Register | int): value/register with the trigger network address.
        wait_time (Register | int): value/register with the waiting time in nanoseconds.
    """

    def __init__(self, address: Register | int, wait_time: Register | int):
        args: list[int | str | Register] = [address, wait_time]
        types = [
            [InstructionArgument.IMMEDIATE, InstructionArgument.REGISTER],
            [InstructionArgument.IMMEDIATE, InstructionArgument.REGISTER],
        ]
        bounds: list[tuple[int, int] | None] = [None, (INST_MIN_WAIT, INST_MAX_WAIT)]
        super().__init__(args, types, bounds, wait_time if isinstance(wait_time, int) else None)
        # Add registers to read/write registers sets
        self.add_read_registers({address, wait_time})
