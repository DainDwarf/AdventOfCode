from intcode.simulator import Simulator


def partOne(inp):
    simulator = Simulator(inp)
    simulator.run()


def partTwo(inp):
    pass


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read().strip()
    partOne(inp)
    print("Answer for part two is : {res}".format(res=partTwo(inp)))
