import pytest
from enum import IntEnum, unique

# That's handy, the Advent of Code gives unittests.
@pytest.mark.parametrize("inp, exp", [
    ("1,9,10,3,2,3,11,0,99,30,40,50", "3500,9,10,70,2,3,11,0,99,30,40,50"),
    ("1,0,0,0,99", "2,0,0,0,99"),
    ("2,3,0,3,99", "2,3,0,6,99"),
    ("2,4,4,5,99,0", "2,4,4,5,99,9801"),
    ("1,1,1,4,99,5,6,0,99", "30,1,1,4,2,5,6,0,99"),
])
def test_day_02(inp, exp):
    simulator = Simulator(inp)
    simulator.run()
    res = simulator.state()
    print(f"Test {inp} gives {res}")
    assert res == exp

# That's handy, the Advent of Code gives unittests.
@pytest.mark.parametrize("inp, exp", [
    ("1002,4,3,4,33", "1002,4,3,4,99"),
    ("1101,100,-1,4,0", "1101,100,-1,4,99"),
])
def test_day_05(inp, exp):
    simulator = Simulator(inp)
    simulator.run()
    res = simulator.state()
    print(f"Test {inp} gives {res}")
    assert res == exp


@unique
class ParamMode(IntEnum):
    POSITION = 0,
    IMMEDIATE = 1,


class Simulator:
    def __init__(self, inp):
        self._state = [int(i) for i in inp.split(',')]
        self._ip = 0
        self._finished = False

    def __getitem__(self, pos):
        return self._state[pos]

    def __setitem__(self, pos, value):
        self._state[pos] = value

    def param_get(self, pos, mode: ParamMode):
        """Get the value associated with parameter on position ``pos`` on a given mode."""
        if mode is ParamMode.POSITION:
            return self[self[pos]]
        elif mode is ParamMode.IMMEDIATE:
            return self[pos]
        else:
            raise RuntimeError(f"Unknown mode {mode}.")

    def param_set(self, value, pos, mode: ParamMode):
        """Set the value associated with parameter on position ``pos`` on a given mode."""
        if mode is ParamMode.POSITION:
            self[self[pos]] = value
        elif mode is ParamMode.IMMEDIATE:
            raise RuntimeError("Cannot set value on immediate mode.")
        else:
            raise RuntimeError(f"Unknown mode {mode}.")

    def add(self,
            lhs_mode: ParamMode = ParamMode.POSITION,
            rhs_mode: ParamMode = ParamMode.POSITION,
            out_mode: ParamMode = ParamMode.POSITION,
    ):
        """Op code 1"""
        lhs = self.param_get(self._ip+1, lhs_mode)
        rhs = self.param_get(self._ip+2, rhs_mode)
        self.param_set(lhs+rhs, self._ip+3, out_mode)
        self._ip += 4

    def mul(self,
            lhs_mode: ParamMode = ParamMode.POSITION,
            rhs_mode: ParamMode = ParamMode.POSITION,
            out_mode: ParamMode = ParamMode.POSITION,
    ):
        """Op code 2"""
        lhs = self.param_get(self._ip+1, lhs_mode)
        rhs = self.param_get(self._ip+2, rhs_mode)
        self.param_set(lhs*rhs, self._ip+3, out_mode)
        self._ip += 4

    def input(self, store_mode: ParamMode = ParamMode.POSITION):
        """Op code 3"""
        i = int(input("Input instruction: "))
        self.param_set(i, self._ip+1, store_mode)
        self._ip += 2

    def output(self, get_mode: ParamMode = ParamMode.POSITION):
        """Op code 4"""
        print(self.param_get(self._ip+1, get_mode))
        self._ip += 2

    def decode(self, pos):
        code = self[pos]
        op_code = code % 100
        code = code // 100
        modes = []
        while code > 0:
            modes.append(ParamMode(code%10))
            code = code // 10
        return op_code, modes

    def _step(self):
        """Runs a single step."""
        if self._finished:
            return

        op_code, modes = self.decode(self._ip)
        if op_code == 1:
            self.add(*modes)
        elif op_code == 2:
            self.mul(*modes)
        elif op_code == 3:
            self.input(*modes)
        elif op_code == 4:
            self.output(*modes)
        elif op_code == 99:
            self._finished = True
        else:
            raise ValueError(f"Unkown OP code: {op_code}")

    def run(self):
        while not self._finished:
            self._step()

    def state(self):
        return ",".join(str(i) for i in self._state)
