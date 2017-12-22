#!/usr/bin/python3
from __future__ import print_function

def turnRight(d):
    if d=='up':
        return 'right'
    elif d=='right':
        return 'down'
    elif d=='down':
        return 'left'
    elif d=='left':
        return 'up'

def turnLeft(d):
    if d=='up':
        return 'left'
    elif d=='left':
        return 'down'
    elif d=='down':
        return 'right'
    elif d=='right':
        return 'up'

def reverse(d):
    if d=='up':
        return 'down'
    elif d=='down':
        return 'up'
    elif d=='left':
        return 'right'
    elif d=='right':
        return 'left'

class Carrier(object):
    def __init__(self, start_map):
        self.state = dict()
        self.caused_infections = 0
        for line_num, line in enumerate(start_map.split('\n')):
            for col_num, char in enumerate(line):
                self.state[(line_num, col_num)] = 'I' if char == '#' else 'C'
        self.direction = 'up'
        self.cur_line = (len(start_map.split('\n'))-1) //2
        middle_line = start_map.split('\n')[self.cur_line]
        self.cur_col = (len(middle_line)-1) //2

    def walk(self):
        if self.direction == 'up':
            self.cur_line -= 1
        elif self.direction == 'down':
            self.cur_line += 1
        elif self.direction == 'left':
            self.cur_col -= 1
        elif self.direction == 'right':
            self.cur_col += 1

    def burst(self):
        cur_state = self.state.get((self.cur_line, self.cur_col), 'C')
        if cur_state == 'I':
            self.direction = turnRight(self.direction)
            self.state[self.cur_line, self.cur_col] = 'C'
        elif cur_state == 'C':
            self.direction = turnLeft(self.direction)
            self.state[self.cur_line, self.cur_col] = 'I'
            self.caused_infections += 1
        else:
            raise RuntimeError("Unknown state {s}".format(s=cur_state))
        self.walk()

class Carrier2(Carrier):
   def burst(self):
       cur_state = self.state.get((self.cur_line, self.cur_col), 'C')
       if cur_state == 'C':
           self.state[self.cur_line, self.cur_col] = 'W'
           self.direction = turnLeft(self.direction)
       elif cur_state == 'W':
           self.state[self.cur_line, self.cur_col] = 'I'
           self.caused_infections += 1
           # Does not change direction
       elif cur_state == 'I':
           self.state[self.cur_line, self.cur_col] = 'F'
           self.direction = turnRight(self.direction)
       elif cur_state == 'F':
           self.state[self.cur_line, self.cur_col] = 'C'
           self.direction = reverse(self.direction)
       else:
           raise RuntimeError("Unknown state {s}".format(s=cur_state))
       self.walk()


# That's handy, the Advent of Code gives unittests.
def UnitTest():
    ex = "..#\n#..\n...".strip()

    print("Unit test using map\n{inp}".format(inp=ex))

    print("")
    print("Unit test for Part One.")
    i1 = 7
    i2 = 70
    i3 = 10000
    print("Test for {i} bursts gives {res}".format(i=i1, res=partOne(ex, i1)))
    print("Test for {i} bursts gives {res}".format(i=i2, res=partOne(ex, i2)))
    print("Test for {i} bursts gives {res}".format(i=i3, res=partOne(ex, i3)))

    i4=100
    i5=10000000
    print("")
    print("Unit test for Part Two.")
    print("Test for {i} bursts gives {res}".format(i=i4, res=partTwo(ex, i4)))
    print("Test for {i} bursts gives {res}".format(i=i5, res=partTwo(ex, i5)))


def partOne(inp, bursts=10000):
    car = Carrier(inp)
    for i in range(bursts):
        car.burst()
    return car.caused_infections

def partTwo(inp, bursts=10000000):
    car = Carrier2(inp)
    for i in range(bursts):
        car.burst()
    return car.caused_infections

if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("-t", "--test", help='Unit tests', action='store_true')
    args.add_argument("-i", "--input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    if options.test:
        UnitTest()
    if options.input:
        inp = options.input.read().strip()
        print("Answer for part one is : {res}".format(res=partOne(inp)))
        print("Answer for part two is : {res}".format(res=partTwo(inp)))
