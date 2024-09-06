import pytest

from qpysequence.program import Register
from qpysequence.program.instructions import (
    Acquire,
    AcquireTtl,
    AcquireWeighed,
    Add,
    And,
    Asl,
    Asr,
    Jge,
    Jlt,
    Jmp,
    LatchRst,
    Move,
    Not,
    Or,
    Play,
    ResetPh,
    SetAwgGain,
    SetAwgOffs,
    SetCond,
    SetFreq,
    SetLatchEn,
    SetMrk,
    SetPh,
    SetPhDelta,
    Sub,
    UpdParam,
    Wait,
    WaitSync,
    WaitTrigger,
    Xor,
)


@pytest.fixture(name="allocated_register")
def fixture_register() -> Register:
    """Creates an allocated register

    Returns:
        Register: Instance of an allocated register
    """
    r = Register()
    r.allocate(0)
    return r


class TestInstructions:
    """Unitary tests checking the instructions"""

    def test_with_label(self):
        """Test the with_label method."""
        instr = SetFreq(12345678).with_label("label")
        assert repr(instr).startswith("label:")

    def test_with_comment(self):
        """Test the with_label method."""
        instr = SetFreq(12345678).with_comment("comment")
        assert repr(instr).strip().endswith("# comment")

    def test_set_mrk(self):
        """Test the long_wait function."""
        instr = SetMrk(1)
        assert repr(instr).strip() == "set_mrk          1"

    def test_set_freq(self):
        """Test the set_freq function."""
        instr = SetFreq(12345678)
        assert repr(instr).strip() == "set_freq         12345678"

    def test_reset_ph(self):
        """Test the long_wait function."""
        instr = ResetPh()
        assert repr(instr).strip() == "reset_ph"

    def test_set_ph(self):
        """Test the long_wait function."""
        instr = SetPh(123456789)
        assert repr(instr).strip() == "set_ph           123456789"

    def test_set_ph_delta(self):
        """Test the long_wait function."""
        instr = SetPhDelta(123456789)
        assert repr(instr).strip() == "set_ph_delta     123456789"

    def test_set_awg_gain(self):
        """Test the long_wait function."""
        instr = SetAwgGain(100, 200)
        assert repr(instr).strip() == "set_awg_gain     100, 200"

    def test_set_awg_offs(self):
        """Test the long_wait function."""
        instr = SetAwgOffs(100, 200)
        assert repr(instr).strip() == "set_awg_offs     100, 200"

    def test_upd_param(self):
        """Test the long_wait function."""
        instr = UpdParam(4)
        assert repr(instr).strip() == "upd_param        4"

    def test_play(self):
        """Test the long_wait function."""
        instr = Play(0, 1, 4)
        assert repr(instr).strip() == "play             0, 1, 4"

    def test_acquire(self):
        """Test the long_wait function."""
        instr = Acquire(0, 1, 4)
        assert repr(instr).strip() == "acquire          0, 1, 4"

    def test_acquire_weighed(self):
        """Test the long_wait function."""
        instr = AcquireWeighed(0, 1, 2, 3, 4)
        assert repr(instr).strip() == "acquire_weighed  0, 1, 2, 3, 4"

    def test_acquire_ttl(self):
        """Test the acquire_ttl function."""
        instr = AcquireTtl(0, 1, 1, 4)
        assert repr(instr).strip() == "acquire_ttl      0, 1, 1, 4"

    def test_wait(self):
        """Test the long_wait function."""
        instr = Wait(100)
        assert repr(instr).strip() == "wait             100"

    def test_wait_trigger(self):
        """Test the long_wait function."""
        instr = WaitTrigger(5, 100)
        assert repr(instr).strip() == "wait_trigger     5, 100"

    def test_wait_sync(self):
        """Test the long_wait function."""
        instr = WaitSync(4)
        assert repr(instr).strip() == "wait_sync        4"

    def test_move(self, allocated_register: Register):
        """Test the move function."""
        instr = Move(0, allocated_register)
        assert repr(instr).strip() == "move             0, R0"

    def test_not(self, allocated_register: Register):
        """Test the not function."""
        instr = Not(0, allocated_register)
        assert repr(instr).strip() == "not              0, R0"

    def test_add(self, allocated_register: Register):
        """Test the add function."""
        instr = Add(allocated_register, 0, allocated_register)
        assert repr(instr).strip() == "add              R0, 0, R0"

    def test_sub(self, allocated_register: Register):
        """Test the sub function."""
        instr = Sub(allocated_register, 0, allocated_register)
        assert repr(instr).strip() == "sub              R0, 0, R0"

    def test_and(self, allocated_register: Register):
        """Test the and function."""
        instr = And(allocated_register, 0, allocated_register)
        assert repr(instr).strip() == "and              R0, 0, R0"

    def test_or(self, allocated_register: Register):
        """Test the or function."""
        instr = Or(allocated_register, 0, allocated_register)
        assert repr(instr).strip() == "or               R0, 0, R0"

    def test_asl(self, allocated_register: Register):
        """Test the asl function."""
        instr = Asl(allocated_register, 0, allocated_register)
        assert repr(instr).strip() == "asl              R0, 0, R0"

    def test_asr(self, allocated_register: Register):
        """Test the asr function."""
        instr = Asr(allocated_register, 0, allocated_register)
        assert repr(instr).strip() == "asr              R0, 0, R0"

    def test_xor(self, allocated_register: Register):
        """Test the xor function."""
        instr = Xor(allocated_register, 0, allocated_register)
        assert repr(instr).strip() == "xor              R0, 0, R0"

    def test_set_cond(self):
        """Test the set_cond function"""
        instr = SetCond(1, 16383, 2, 4)
        assert repr(instr).strip() == "set_cond         1, 16383, 2, 4"

    def test_set_latch_en(self, allocated_register: Register):
        """Test the set_latch_en function"""
        instr = SetLatchEn(allocated_register, 4)
        assert repr(instr).strip() == "set_latch_en     R0, 4"

    def test_latch_rst(self, allocated_register: Register):
        """Test the latch_rst function"""
        instr = LatchRst(allocated_register)
        assert repr(instr).strip() == "latch_rst        R0"

    def test_jlt(self, allocated_register: Register):
        """Test the jlt function"""
        instr = Jlt(allocated_register, 123, "@label")
        assert repr(instr).strip() == "jlt              R0, 123, @label"

    def test_jge(self, allocated_register: Register):
        """Test the jlt function"""
        instr = Jge(allocated_register, 123, "@label")
        assert repr(instr).strip() == "jge              R0, 123, @label"

    def test_jmp(self, allocated_register: Register):
        """Test the jlt function"""
        instr = Jmp("@label")
        assert repr(instr).strip() == "jmp              @label"
