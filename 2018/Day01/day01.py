#!//usr/local/bin/python3

import itertools

def testOne():
    inp1 = "+1, -2, +3, +1"
    inp2 = "+1, +1, +1"
    inp3 = "+1, +1, -2"
    inp4 = "-1, -2, -3"

    print("Unit test for Part One.")
    testFormat = "Sum for {inp} is {res}."
    print(testFormat.format(inp=inp1, res=partOne(inp1.split(", "))))
    print(testFormat.format(inp=inp2, res=partOne(inp2.split(", "))))
    print(testFormat.format(inp=inp3, res=partOne(inp3.split(", "))))
    print(testFormat.format(inp=inp4, res=partOne(inp4.split(", "))))

def testTwo():
    inp1 = "+1, -2, +3, +1"
    inp2 = "+1, -1"
    inp3 = "+3, +3, +4, -2, -4"
    inp4 = "-6, +3, +8, +5, -6"
    inp5 = "+7, +7, -2, -7, -4"

    print("Unit test for Part Two.")
    testFormat = "First double frequency for {inp} is {res}."
    print(testFormat.format(inp=inp1, res=partTwo(inp1.split(", "))))
    print(testFormat.format(inp=inp2, res=partTwo(inp2.split(", "))))
    print(testFormat.format(inp=inp3, res=partTwo(inp3.split(", "))))
    print(testFormat.format(inp=inp4, res=partTwo(inp4.split(", "))))
    print(testFormat.format(inp=inp5, res=partTwo(inp5.split(", "))))

def partOne(inp):
    return sum(int(s) for s in inp)

def partTwo(inp):
    knownFrequency = {0}
    freq = 0
    for num in itertools.cycle(inp):
        freq += int(num)
        if freq in knownFrequency:
            return freq
        else:
            knownFrequency.add(freq)

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
    if options.input:
        inp = options.input.read().strip().split("\n")
        print("Answer for part one is : {res}".format(res=partOne(inp)))
        print("Answer for part two is : {res}".format(res=partTwo(inp)))
