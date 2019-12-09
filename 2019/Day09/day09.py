from intcode.simulator import Simulator


def partOne(code):
    inp = int(input("BOOST test input: "))
    simulator = Simulator(code, inp=[inp])
    simulator.run()
    test_run = simulator.output()
    assert len(test_run) == 1, test_run
    return test_run[0]


def partTwo(inp):
    pass


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=partOne(inp)))
    print("Answer for part two is : {res}".format(res=partTwo(inp)))
