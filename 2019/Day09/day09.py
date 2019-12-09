from intcode.simulator import Simulator


def partOne(code):
    simulator = Simulator(code, inp=[1])
    simulator.run()
    test_run = simulator.output()
    assert len(test_run) == 1, test_run
    return test_run[0]


def partTwo(code):
    simulator = Simulator(code, inp=[2])
    simulator.run()
    real_run = simulator.output()
    assert len(real_run) == 1, real_run
    return real_run[0]


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    code = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=partOne(code)))
    print("Answer for part two is : {res}".format(res=partTwo(code)))
