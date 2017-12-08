#!/usr/bin/python3
from itertools import count, repeat, accumulate, chain, takewhile

#Dealing with infinite lists all along, I should use some haskell instead.

class Vect(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x==other.x and self.y==other.y

    def __add__(self, other):
        return Vect(self.x + other.x, self.y+other.y)

    def __str__(self):
        return '({x}, {y})'.format(x=self.x, y=self.y)

    def __repr__(self):
        return '({x}, {y})'.format(x=self.x, y=self.y)

    def adjacents(self):
        '''Gives all adjacent cells, for part two.'''
        return set((Vect(self.x-1  , self.y-1  )
               , Vect(self.x-1  , self.y    )
               , Vect(self.x-1  , self.y+1  )
               , Vect(self.x    , self.y-1  )
               # , Vect(self.x    , self.y    ) Not including self.
               , Vect(self.x    , self.y+1  )
               , Vect(self.x+1  , self.y-1  )
               , Vect(self.x+1  , self.y    )
               , Vect(self.x+1  , self.y+1  )
        ))

RIGHT   = Vect( 0,  1)
LEFT    = Vect( 0, -1)
UP      = Vect( 1,  0)
DOWN    = Vect(-1,  0)


def genDirections():
    """Gives the vectors to generate the spiral, by giving each direction in correct order.

    To determine when to turn, you can observe that the spiral goes like this:
        1 right, 1 up
        2 left, 2 down
        3 right, 3 up
        4 left, 4 down
        ...
    """

    for i in count(1, 2):
        yield from repeat(RIGHT, i)
        yield from repeat(UP, i)
        yield from repeat(LEFT, i+1)
        yield from repeat(DOWN, i+1)

def genPositions():
    pos = Vect(0, 0)
    for direction in genDirections():
        yield pos
        pos += direction

def getPosition(num):
    '''Returns the position of a given number in the spiral.'''
    if num <= 0:
        raise RuntimeError("Number below 0 are not permitted!")

    for current, pos in enumerate(genPositions(), 1):
        if current == num:
            return pos

def partOne(inp):
    pos = getPosition(inp)
    return abs(pos.x) + abs(pos.y)

def genAdjacentNums():
    previous_nums = {Vect(0, 0): 1}

    for pos in genPositions():
        if pos == Vect(0, 0):
            yield 1
        else:
            this_pos_sum = sum(previous_nums[k] for k in pos.adjacents() if k in previous_nums.keys())
            previous_nums[pos] = this_pos_sum
            yield this_pos_sum


def partTwo(inp):
    nums = genAdjacentNums()
    nums_until_input = list(takewhile(lambda x: x <= inp, nums))
    nums_until_input.append(next(nums))
    return nums_until_input

def visualize(pos_dict):
    """Display as spiral the Vect: num dictionary."""

    start_line = min(map(lambda v:v.x, pos_dict.keys()))
    end_line = max(map(lambda v:v.x, pos_dict.keys()))
    start_column = min(map(lambda v:v.y, pos_dict.keys()))
    end_column = max(map(lambda v:v.y, pos_dict.keys()))

    print("going from {minix}, {miniy} to {maxix}, {maxiy}".format(
        minix=start_column
        , miniy=start_line
        , maxix=end_column
        , maxiy=end_line
    ))

    for x in range(end_line, start_line-1, -1):
        this_line_nums = []
        for y in range(start_column, end_column+1):
            if Vect(x, y) in pos_dict.keys():
                this_line_nums.append(pos_dict[Vect(x, y)])
        print(" ".join(map(lambda n: "{n:>6}".format(n=n), this_line_nums)))

        
        

def visualizePartTwo(inp):
    previous_nums = {Vect(0, 0): 1}

    for pos in genPositions():
        if pos == Vect(0, 0):
            continue
        else:
            this_pos_sum = sum(previous_nums[k] for k in pos.adjacents() if k in previous_nums.keys())
            previous_nums[pos] = this_pos_sum
            if this_pos_sum>=inp:
                break
    visualize(previous_nums)

# That's handy, the Advent of Code gives unittests.
def UnitTest():
    print("Part one unit testing.")
    print("Path from 1 has length {res}".format(res=partOne(1)))
    print("Path from 12 has length {res}".format(res=partOne(12)))
    print("Path from 23 has length {res}".format(res=partOne(23)))
    print("Path from 1024 has length {res}".format(res=partOne(1024)))

    print("")
    print("Part two unit testing.")
    print("Values until 806 and next : {l}".format(l=str(partTwo(806))))

if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("-t", "--test", help='Unit tests', action='store_true')
    args.add_argument("-i", "--input", help='Your input number', type=int)
    options = args.parse_args()

    if options.test:
        UnitTest()
    if options.input:
        print("Path for part one has length {res}".format(res=partOne(options.input)))
        print("Value after {inp} is {res} using values {values}".format(inp=options.input, res=partTwo(options.input)[-1], values=partTwo(options.input)))
        print("")
        visualizePartTwo(options.input)
