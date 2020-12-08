#!/usr/bin/python3
import re


class Simulator:

    def __init__(self, code):
        _code_re = re.compile(r"(\w+) ([+-]\d+)")
        self._instructions = []
        self._ip = 0
        self._acc = 0
        for line in code.split('\n'):
            op_code, arg = _code_re.match(line).groups()
            self._instructions.append((op_code, int(arg)))

    def reset(self):
        self._ip = 0
        self._acc = 0

    def step(self):
        op_code, arg = self._instructions[self._ip]
        getattr(self, op_code)(arg)

    def nop(self, arg):
        self._ip += 1

    def acc(self, arg):
        self._acc += arg
        self._ip += 1

    def jmp(self, arg):
        self._ip += arg

    def find_loop(self):
        visited = set()
        while self._ip not in visited:
            visited.add(self._ip)
            self.step()
        return self._acc

    def corrected_code(self):
        for i, code in enumerate(self._instructions):
            op_code, arg = code
            if op_code == "nop":
                self._instructions[i] = ("jmp", arg)
            elif op_code == "jmp":
                self._instructions[i] = ("nop", arg)
            else:
                continue

            try:
                self.find_loop()
            except IndexError:
                if self._ip == len(self._instructions):
                    return self._acc

            self.reset()
            self._instructions[i] = (op_code, arg)



def part_one(inp):
    sim = Simulator(inp)
    return sim.find_loop()


def part_two(inp):
    sim = Simulator(inp)
    return sim.corrected_code()


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=part_one(inp)))
    print("Answer for part two is : {res}".format(res=part_two(inp)))
