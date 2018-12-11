#!/usr/bin/python3
from __future__ import print_function


def power(x, y, serial):
    rID = x+10
    pow_lvl = rID*y+serial
    pow_lvl *= rID
    digit = (pow_lvl // 100)%10 -5
    return digit


class FuelCells(object):
    def __init__(self, serial):
        self.serial = serial
        self.preCompute()

    def preCompute(self):
        """Compute an auxillary matrix of sum from 0, 0 to (x, y) for faster computation of squares sums"""
        self.aux = dict()

        # Copy first row
        for x in range(0, 301):
            self.aux[(0, x)] = 0

        # Do row wise sums
        for x in range(1, 301):
            cum_sum=0
            for y in range(0, 301):
                cum_sum+=self[(x, y)]
                self.aux[(x, y)] = cum_sum

        # Do column wise sums
        for x in range(1, 301):
            for y in range(0, 301):
                self.aux[(x, y)] += self.aux[(x-1, y)]

    def __getitem__(self, pos):
        x, y = pos
        if 0 < x < 301 and 0 < y < 301:
            return power(x, y, self.serial)
        else:
            return 0

    def display(self, from_pos, to_pos):
        x1, y1 = from_pos
        x2, y2 = to_pos
        from_x, to_x = min(x1, x2), max(x1, x2)
        from_y, to_y = min(y1, y2), max(y1, y2)
        for y in range(from_y, to_y+1):
            print(" ".join("{:>3}".format(self[(x, y)]) for x in range(from_x, to_x+1)))

    def squarePower(self, from_pos, size=3):
        """Returns the total power of the square "size*size" start from from_pos."""
        from_x, from_y = from_pos
        to_x, to_y = from_x+size-1, from_y+size-1
        return self.aux[(to_x, to_y)] - self.aux[(from_x-1, to_y)] - self.aux[(to_x, from_y-1)] + self.aux[(from_x-1, from_y-1)]

    def HighestSquare(self, size=3):
        """Returns the top-left position of the best square."""
        all_values = dict() #Meh.
        for x in range(1, 301-size):
            for y in range(1, 301-size):
                all_values[(x, y)] = self.squarePower((x, y), size)
        return max(all_values.items(), key =lambda t:t[1])[0]

    def HighestSquareOfThemAll(self):
        best_pos = (0, 0)
        best_size = 0
        best_power = 0
        for size in range(1, 301):
            for x in range(1, 301-size):
                for y in range(1, 301-size):
                    power = self.squarePower((x, y), size)
                    if power > best_power:
                        best_pos = (x, y)
                        best_power = power
                        best_size = size
        return best_pos + (best_size, )



# That's handy, the Advent of Code gives unittests.
def testOne():
    print("Unit test for Part One.")
    print("Fuel cell at {x},{y}, grid serial number {s}: power level {p}".format(
        x=3, y=5, s=8, p=power(3, 5, 8)))
    print("Fuel cell at {x},{y}, grid serial number {s}: power level {p}".format(
        x=122, y=79, s=57, p=power(122, 79, 57)))
    print("Fuel cell at {x},{y}, grid serial number {s}: power level {p}".format(
        x=217, y=196, s=39, p=power(217, 196, 39)))
    print("Fuel cell at {x},{y}, grid serial number {s}: power level {p}".format(
        x=101, y=153, s=71, p=power(101, 153, 71)))
    print()

    s1=18
    cells1 = FuelCells(s1)
    sol1 = cells1.HighestSquare()
    print("For grid serial number {s}, the largest 3x3 square's top-left is "
          "{solution} (with a total power of {pow}); they are in the middle "
          "of this region:"
          .format(s=s1, solution=sol1, pow=cells1.squarePower(sol1)
    ))
    from1=(sol1[0]-1, sol1[1]-1)
    to1=(sol1[0]+3, sol1[1]+3)
    cells1.display(from1, to1)
    print()

    s2=42
    cells2 = FuelCells(s2)
    sol2 = cells2.HighestSquare()
    print("For grid serial number {s}, the largest 3x3 square's top-left is "
          "{solution} (with a total power of {pow}); they are in the middle "
          "of this region:"
          .format(s=s2, solution=sol2, pow=cells2.squarePower(sol2)
    ))
    from2=(sol2[0]-1, sol2[1]-1)
    to2=(sol2[0]+3, sol2[1]+3)
    cells2.display(from2, to2)


def testTwo():
    s1=18
    cells1 = FuelCells(s1)
    sol1 = cells1.HighestSquareOfThemAll()
    pos1 = (sol1[0], sol1[1])
    size1 = sol1[2]
    pow1 = cells1.squarePower(pos1, size1)
    print("For grid serial number {s}, the largest total square (with a total "
          "power of {pow}) is {size}x{size} and has a top-left corner of {pos}, "
          "so its identifier is {id}"
          .format(s=s1, id=",".join(map(str, sol1)), pow=pow1, pos=pos1, size=size1
    ))
    print()

    s2=42
    cells2 = FuelCells(s2)
    sol2 = cells2.HighestSquareOfThemAll()
    pos2 = (sol2[0], sol2[1])
    size2 = sol2[2]
    pow2 = cells2.squarePower(pos2, size2)
    print("For grid serial number {s}, the largest total square (with a total "
          "power of {pow}) is {size}x{size} and has a top-left corner of {pos}, "
          "so its identifier is {id}"
          .format(s=s2, id=",".join(map(str, sol2)), pow=pow2, pos=pos2, size=size2
    ))


def partOne(inp):
    cells = FuelCells(inp)
    return ",".join(map(str, cells.HighestSquare()))


def partTwo(inp):
    cells = FuelCells(inp)
    return ",".join(map(str, cells.HighestSquareOfThemAll()))


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("-t", "--test", help='Unit tests', action='store_true')
    args.add_argument("-i", "--input", help='Your input number', type=int)
    options = args.parse_args()

    if options.test:
        testOne()
        print()
        testTwo()
        print()
    if options.input:
        inp = options.input
        print("Answer for part one is : {res}".format(res=partOne(inp)))
        print("Answer for part two is : {res}".format(res=partTwo(inp)))
