#!/usr/bin/python3
from __future__ import print_function


class CellularAutomaton(object):
    def __init__(self, rules, state):
        #Only deal with automatons that does not produce spontaneously.
        assert rules["....."] == "."
        self.state = state
        self.rules = rules
        self.first_pos = 0

    @classmethod
    def fromDescription(cls, desc):
        desc = desc.split("\n")
        state = desc[0].split(": ")[1]
        rules = {l.split(" => ")[0].strip(): l.split(" => ")[1].strip() for l in desc[2:]}
        return cls(rules, state)

    def steps(self, n):
        for _ in range(n):
            #Adjust the state to be sure to get all fleeting particules.
            if self.state.startswith('.'):
                self.first_pos += len(self.state.split('#', 1)[0])
            self.first_pos -= 3 #While we add 5 dots, only 3 new pos will remain after the computation phase.
            self.state = "....." + self.state.strip(".") + "....."

            #Compute
            self.state = "".join((self.rules["".join(nb)] for nb in zip(self.state, self.state[1:], self.state[2:], self.state[3:], self.state[4:])))

    def sum(self):
        return sum((i if c == "#" else 0 for i, c in enumerate(self.state, self.first_pos)))

    def fixedPoint(self, n):
        """Compute until you reach a fixed point.

        Because that's the only way part 2 could finish."""
        prev_state = self.state
        prev_pos = self.first_pos
        self.steps(1)
        steps_done = 1
        while prev_state != self.state and steps_done < n:
            prev_state = self.state
            prev_pos = self.first_pos
            self.steps(1)
            steps_done += 1
        #Reached fixed point. Now, compute how far it goes!
        if n > steps_done:
            slide_factor = self.first_pos - prev_pos
            self.first_pos += slide_factor*(n-steps_done)


example_input = """initial state: #..#.#..##......###...###

..... => .
....# => .
...#. => .
...## => #
..#.. => #
..#.# => .
..##. => .
..### => .
.#... => #
.#..# => .
.#.#. => #
.#.## => #
.##.. => #
.##.# => .
.###. => .
.#### => #
#.... => .
#...# => .
#..#. => .
#..## => .
#.#.. => .
#.#.# => #
#.##. => .
#.### => #
##... => .
##..# => .
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #
##### => ."""

# That's handy, the Advent of Code gives unittests.
def testOne():
    ex = example_input
    res = partOne(ex)
    print("Unit test for Part One.")
    print(f"Test on example gives {res}")


def testTwo():
    ex = example_input
    res = partTwo(ex)
    print("No unit test for part 2!")
    print(f"But after fifty billion generations, it gives {res}.")


def partOne(inp):
    automaton = CellularAutomaton.fromDescription(inp)
    automaton.steps(20)
    return automaton.sum()


def partTwo(inp):
    automaton = CellularAutomaton.fromDescription(inp)
    automaton.fixedPoint(50000000000)
    return automaton.sum()


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("-t", "--test", help='Unit tests', action='store_true')
    args.add_argument("-i", "--input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    if options.test:
        testOne()
        print()
        testTwo()
        print()
    if options.input:
        inp = options.input.read().strip()
        print("Answer for part one is : {res}".format(res=partOne(inp)))
        print("Answer for part two is : {res}".format(res=partTwo(inp)))
