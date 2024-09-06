""" SetAwgOffs Instruction """

from qpysequence.program.instructions.instruction import Instruction
from qpysequence.program.register import Register
from qpysequence.utils.constants import AWG_MAX_OFFSET, AWG_MIN_OFFSET
from qpysequence.utils.enums import InstructionArgument


class SetAwgOffs(Instruction):
    """
    Set AWG gain path 0 using `gain_0` and path 1 using `gain_1`. Both offset values are divided in 2**sample path width
    steps. The parameters are cached and only updated when the `upd_param`, `play`, `acquire` or `acquire_weighted`
    instructions are executed. The arguments are either all set through immediates or registers.

    Args:
        gain_0 (Register | int): value/register with the gain for path 0.
        gain_1 (Register | int): value/register with the gain for path 1.
    """

    def __init__(self, offset_0: Register | int, offset_1: Register | int):
        args: list[int | str | Register] = [offset_0, offset_1]
        types = [
            [InstructionArgument.IMMEDIATE, InstructionArgument.REGISTER],
            [InstructionArgument.IMMEDIATE, InstructionArgument.REGISTER],
        ]
        bounds: list[tuple[int, int] | None] = [(AWG_MIN_OFFSET, AWG_MAX_OFFSET)]
        super().__init__(args, types, bounds)
        # Add registers to read/write registers sets
        self.add_read_registers({offset_0, offset_1})
