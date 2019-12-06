from intcode.simulator import Simulator


def partOne(inp):
    simulator = Simulator(inp)
    simulator[1] = 12
    simulator[2] = 2
    simulator.run()
    return simulator[0]


def partTwo(inp, target):
    """Let's brute force"""
    for noun in range(100):
        for verb in range(100):
            simulator = Simulator(inp)
            simulator[1] = noun
            simulator[2] = verb
            simulator.run()
            if simulator[0] == target:
                return 100*noun+verb


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("-t", "--target", help='Target number for part 2', type=int)
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=partOne(inp)))
    print("Answer for part two is : {res}".format(res=partTwo(inp, options.target)))
