"""Iterative Loop module
"""

from collections import namedtuple

from .block import Block
from .instructions import Add
from .instructions import Loop as LoopInstr
from .instructions import Move, Nop, Not, Sub
from .register import Register


class IterativeLoop(Block):
    """Loop class, can hold instructions and other blocks and repeat them for a determinate amount of iterations."""

    def __init__(self, name: str, iterations: int, loops: list[tuple[int, int]] | None = None):
        super().__init__(name)
        self._iterations = iterations
        self._loops = loops or []
        self._iteration_register = Register()
        self._loop_registers = [Register() for _ in self._loops]
        self._generate_builtin_components()

    def _generate_builtin_components(self):
        """Generates the builtin components of the Loop."""
        for i, loop in enumerate(self._loops):
            _, step = loop
            if step > 0:
                self.builtin_components.append(Add(self._loop_registers[i], step, self._loop_registers[i]))
            if step < 0:
                self.builtin_components.append(Sub(self._loop_registers[i], -step, self._loop_registers[i]))
        self.builtin_components.append(LoopInstr(self._iteration_register, f"@{self.name}"))

    @property
    def iterations(self) -> int:
        """Iterations of the loop.

        Returns:
            int: Number of iterations.
        """
        return self._iterations

    @property
    def duration_iter(self) -> int:
        """Duration of a single iteration.

        Returns:
            int: Duration in nanoseconds of a single iteration.
        """
        return super().duration

    @property
    def duration(self) -> int:
        """Duration of all the iterations

        Returns:
            int: Duration in nanoseconds of all the iterations.
        """
        return self.duration_iter * self.iterations

    @property
    def loop_registers(self) -> list[Register]:
        """Register used as counter by the loop.

        Returns:
            Register: Register used as counter by the loop.
        """
        return self._loop_registers

    @property
    def iteration_register(self) -> Register:
        """Register used for counting iterations of the loop.

        Returns:
            Register: Register used as counter by the loop.
        """
        return self._iteration_register

    def be_appended(self, destination: Block, bot_position: int = 0):
        """Gets appended to the destination block.

        Args:
            destination (Block): Block to be appended to.
            bot_position (int, optional): Position, counting from the last element, to place the loop.
        """
        destination.components.insert(
            len(destination.components) - bot_position, Move(self._iterations, self._iteration_register)
        )
        for i, loop in enumerate(self._loops):
            start, _ = loop
            destination.components.insert(
                len(destination.components) - bot_position, Move(abs(start), self.loop_registers[i])
            )
            if start < 0:
                destination.components.insert(
                    len(destination.components) - bot_position, Not(self.loop_registers[i], self.loop_registers[i])
                )
                destination.components.insert(len(destination.components) - bot_position, Nop())
                destination.components.insert(
                    len(destination.components) - bot_position, Add(self.loop_registers[i], 1, self.loop_registers[i])
                )
        destination.components.insert(len(destination.components) - bot_position, self)
