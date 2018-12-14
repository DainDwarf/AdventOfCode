def toDigits(n):
    """Transforms a number into a list of its digits."""
    return list(map(int, str(n)))


class Recipes(object):
    def __init__(self):
        self.rec = [3, 7]
        self.first = 0
        self.second = 1

    def step(self):
        first_n  = self.rec[self.first ]
        second_n = self.rec[self.second]
        self.rec += toDigits(first_n+second_n)
        s = len(self.rec)
        self.first  = (self.first +1+first_n )%s
        self.second = (self.second+1+second_n)%s

    def display(self):
        print("".join("{:^3}".format(
            '('+str(n)+')' if i == self.first else '['+str(n)+']' if i == self.second else n
            )
            for i, n in enumerate(self.rec)
        ))


# That's handy, the Advent of Code gives unittests.
def testOne():
    print("Unit test for Part One.")

    inp = 9
    res = partOne(inp, display=True)
    print(f"After {inp} recipes, the scores of the next ten would be {res}")

    inp = 5
    res = partOne(inp)
    print(f"After {inp} recipes, the scores of the next ten would be {res}")

    inp = 18
    res = partOne(inp)
    print(f"After {inp} recipes, the scores of the next ten would be {res}")

    inp = 2018
    res = partOne(inp)
    print(f"After {inp} recipes, the scores of the next ten would be {res}")


def testTwo():
    print("Unit test for Part Two.")

    inp = "51589"
    res = partTwo(inp)
    print(f"{inp} first appears after {res} recipes.")

    inp = "01245"
    res = partTwo(inp)
    print(f"{inp} first appears after {res} recipes.")

    inp = "92510"
    res = partTwo(inp)
    print(f"{inp} first appears after {res} recipes.")

    inp = "59414"
    res = partTwo(inp)
    print(f"{inp} first appears after {res} recipes.")


def partOne(stopAfter, display=False):
    rec = Recipes()
    limit = stopAfter+10
    while len(rec.rec) < limit:
        if display:
            rec.display()
        rec.step()
    if display:
        rec.display()
    return "".join(map(str, rec.rec[stopAfter:stopAfter+10]))


def partTwo(inp):
    in_l= len(str(inp))
    inp = toDigits(inp)
    rec = Recipes()
    found_index = 0
    while not found_index:     # Hoping it won't be long...
        rec.step()
        if rec.rec[-in_l:] == inp:
            found_index = len(rec.rec)-in_l
        elif rec.rec[-in_l-1:-1] == inp:
            found_index = len(rec.rec)-in_l-1
    return found_index


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
