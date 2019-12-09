from intcode.simulator import Simulator


def partOne(code):
    inp = int(input("Ship's air conditioner ID: "))
    simulator = Simulator(code, inp=[inp])
    simulator.run()
    return ",".join(str(i) for i in simulator.output())


def partTwo(code):
    inp = int(input("Ship's thermal radiator ID: "))
    simulator = Simulator(code, inp=[inp])
    simulator.run()
    return ",".join(str(i) for i in simulator.output())


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("code", help='Your code file', type=FileType('r'))
    options = args.parse_args()

    code = options.code.read().strip()
    print("Answer for part one is : {res}".format(res=partOne(code)))
    print("Answer for part two is : {res}".format(res=partTwo(code)))
