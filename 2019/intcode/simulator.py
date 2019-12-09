import pytest
from enum import IntEnum, unique

# That's handy, the Advent of Code gives unittests.
@pytest.mark.parametrize("code, exp", [
    ("1,9,10,3,2,3,11,0,99,30,40,50", "3500,9,10,70,2,3,11,0,99,30,40,50"),
    ("1,0,0,0,99", "2,0,0,0,99"),
    ("2,3,0,3,99", "2,3,0,6,99"),
    ("2,4,4,5,99,0", "2,4,4,5,99,9801"),
    ("1,1,1,4,99,5,6,0,99", "30,1,1,4,2,5,6,0,99"),
])
def test_day_02(code, exp):
    simulator = Simulator(code)
    simulator.run()
    res = simulator.state()
    print(f"Test {code} gives {res}")
    assert res == exp

@pytest.mark.parametrize("code, exp", [
    ("1002,4,3,4,33", "1002,4,3,4,99"),
    ("1101,100,-1,4,0", "1101,100,-1,4,99"),
])
def test_day_05(code, exp):
    simulator = Simulator(code)
    simulator.run()
    res = simulator.state()
    print(f"Test {code} gives {res}")
    assert res == exp

@pytest.mark.parametrize("code, inp, exp", [
    ("3,0,4,0,99", [5], [5]),
    # Test equal-to-8 codes
    ("3,9,8,9,10,9,4,9,99,-1,8", [7], [0]),
    ("3,9,8,9,10,9,4,9,99,-1,8", [8], [1]),
    ("3,9,8,9,10,9,4,9,99,-1,8", [9], [0]),
    ("3,3,1108,-1,8,3,4,3,99", [7], [0]),
    ("3,3,1108,-1,8,3,4,3,99", [8], [1]),
    ("3,3,1108,-1,8,3,4,3,99", [9], [0]),
    # Test less-than-8 codes
    ("3,9,7,9,10,9,4,9,99,-1,8", [7], [1]),
    ("3,9,7,9,10,9,4,9,99,-1,8", [8], [0]),
    ("3,9,7,9,10,9,4,9,99,-1,8", [9], [0]),
    ("3,3,1107,-1,8,3,4,3,99", [7], [1]),
    ("3,3,1107,-1,8,3,4,3,99", [8], [0]),
    ("3,3,1107,-1,8,3,4,3,99", [9], [0]),
    # Test jumps
    ("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9", [0], [0]),
    ("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9", [1], [1]),
    ("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9", [2], [1]),
    ("3,3,1105,-1,9,1101,0,0,12,4,12,99,1", [0], [0]),
    ("3,3,1105,-1,9,1101,0,0,12,4,12,99,1", [1], [1]),
    ("3,3,1105,-1,9,1101,0,0,12,4,12,99,1", [2], [1]),
    # Big test
    ("3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99", [7], [999]),
    ("3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99", [8], [1000]),
    ("3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99", [9], [1001]),
])
def test_day_05_input(code, inp, exp):
    simulator = Simulator(code, inp=inp)
    simulator.run()
    res = simulator.output()
    print(f"Test {code} gives {res}")
    assert res == exp


@unique
class ParamMode(IntEnum):
    POSITION = 0,
    IMMEDIATE = 1,


@unique
class Operation(IntEnum):
    ADD = 1,
    MUL = 2,
    INPUT = 3,
    OUTPUT = 4,
    JUMP_TRUE = 5,
    JUMP_FALSE = 6,
    LT = 7,
    EQ = 8,
    FINISH = 99,


class Simulator:
    def __init__(self, code, inp = None):
        self._state = [int(i) for i in code.split(',')]
        self._ip = 0
        self._finished = False
        self._input_values = inp if inp is not None else []
        self._output_values = []

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

    def _add(self,
            lhs_mode: ParamMode = ParamMode.POSITION,
            rhs_mode: ParamMode = ParamMode.POSITION,
            out_mode: ParamMode = ParamMode.POSITION,
    ):
        """Op code 1"""
        lhs = self.param_get(self._ip+1, lhs_mode)
        rhs = self.param_get(self._ip+2, rhs_mode)
        self.param_set(lhs+rhs, self._ip+3, out_mode)
        self._ip += 4

    def _mul(self,
            lhs_mode: ParamMode = ParamMode.POSITION,
            rhs_mode: ParamMode = ParamMode.POSITION,
            out_mode: ParamMode = ParamMode.POSITION,
    ):
        """Op code 2"""
        lhs = self.param_get(self._ip+1, lhs_mode)
        rhs = self.param_get(self._ip+2, rhs_mode)
        self.param_set(lhs*rhs, self._ip+3, out_mode)
        self._ip += 4

    def _input(self, store_mode: ParamMode = ParamMode.POSITION):
        """Op code 3"""
        i = self._input_values.pop(0)
        self.param_set(i, self._ip+1, store_mode)
        self._ip += 2

    def _output(self, get_mode: ParamMode = ParamMode.POSITION):
        """Op code 4"""
        out = self.param_get(self._ip+1, get_mode)
        self._output_values.append(out)
        self._ip += 2

    def _jump_true(self,
                   test_mode: ParamMode = ParamMode.POSITION,
                   jump_mode: ParamMode = ParamMode.POSITION,
    ):
        """Op code 5"""
        test = self.param_get(self._ip+1, test_mode)
        jump = self.param_get(self._ip+2, jump_mode)
        if test != 0:
            self._ip = jump
        else:
            self._ip += 3

    def _jump_false(self,
                   test_mode: ParamMode = ParamMode.POSITION,
                   jump_mode: ParamMode = ParamMode.POSITION,
    ):
        """Op code 6"""
        test = self.param_get(self._ip+1, test_mode)
        jump = self.param_get(self._ip+2, jump_mode)
        if test == 0:
            self._ip = jump
        else:
            self._ip += 3

    def _lt(self,
            lhs_mode: ParamMode = ParamMode.POSITION,
            rhs_mode: ParamMode = ParamMode.POSITION,
            out_mode: ParamMode = ParamMode.POSITION,
    ):
        """Op code 7"""
        lhs = self.param_get(self._ip+1, lhs_mode)
        rhs = self.param_get(self._ip+2, rhs_mode)
        val = 1 if lhs < rhs else 0
        self.param_set(val, self._ip+3, out_mode)
        self._ip += 4


    def _eq(self,
            lhs_mode: ParamMode = ParamMode.POSITION,
            rhs_mode: ParamMode = ParamMode.POSITION,
            out_mode: ParamMode = ParamMode.POSITION,
    ):
        """Op code 8"""
        lhs = self.param_get(self._ip+1, lhs_mode)
        rhs = self.param_get(self._ip+2, rhs_mode)
        val = 1 if lhs == rhs else 0
        self.param_set(val, self._ip+3, out_mode)
        self._ip += 4

    def _decode(self, pos):
        code = self[pos]
        op_code = Operation(code % 100)
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

        op_code, modes = self._decode(self._ip)
        if op_code == Operation.ADD:
            self._add(*modes)
        elif op_code == Operation.MUL:
            self._mul(*modes)
        elif op_code == Operation.INPUT:
            self._input(*modes)
        elif op_code == Operation.OUTPUT:
            self._output(*modes)
        elif op_code == Operation.JUMP_TRUE:
            self._jump_true(*modes)
        elif op_code == Operation.JUMP_FALSE:
            self._jump_false(*modes)
        elif op_code == Operation.LT:
            self._lt(*modes)
        elif op_code == Operation.EQ:
            self._eq(*modes)
        elif op_code == Operation.FINISH:
            self._finished = True
        else:
            raise ValueError(f"Unkown OP code: {op_code}")
        return op_code

    def add_input(self, more_input: [int]):
        self._input_values += more_input

    def run(self, until: Operation = None):
        while not self._finished:
            op_code = self._step()
            if until is not None and op_code is until:
                return

    @property
    def finished(self):
        return self._finished

    def state(self):
        return ",".join(str(i) for i in self._state)

    def output(self):
        return self._output_values
