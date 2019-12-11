import pytest
from intcode.simulator import Operation, Simulator


def turn_left(direction):
    if direction == (0, 1):
        return (-1, 0)
    elif direction == (-1, 0):
        return (0, -1)
    elif direction == (0, -1):
        return (1, 0)
    elif direction == (1, 0):
        return (0, 1)
    else:
        raise RuntimeError(f"Unknown direction {direction}")


def turn_right(direction):
    if direction == (0, 1):
        return (1, 0)
    elif direction == (1, 0):
        return (0, -1)
    elif direction == (0, -1):
        return (-1, 0)
    elif direction == (-1, 0):
        return (0, 1)
    else:
        raise RuntimeError(f"Unknown direction {direction}")


def partOne(code):
    robot = Simulator(code)
    position = (0, 0)
    direction = (0, 1) # UP
    panels = dict()
    while not robot.finished:
        robot.add_input([panels.get(position, 0)])
        robot.run(until=Operation.OUTPUT)
        robot.run(until=Operation.OUTPUT)
        color, turn = robot.output()[-2:]
        panels[position] = color
        if turn == 0:
            direction = turn_left(direction)
        elif turn == 1:
            direction = turn_right(direction)
        else:
            raise RuntimeError(f"Unknown turn {turn}")
        position = (position[0]+direction[0], position[1]+direction[1])
    return len(panels)


def partTwo(code):
    robot = Simulator(code)
    position = (0, 0)
    direction = (0, 1) # UP
    panels = {position: 1}
    while not robot.finished:
        robot.add_input([panels.get(position, 0)])
        robot.run(until=Operation.OUTPUT)
        robot.run(until=Operation.OUTPUT)
        color, turn = robot.output()[-2:]
        panels[position] = color
        if turn == 0:
            direction = turn_left(direction)
        elif turn == 1:
            direction = turn_right(direction)
        else:
            raise RuntimeError(f"Unknown turn {turn}")
        position = (position[0]+direction[0], position[1]+direction[1])
    minx = min(p[0] for p in panels.keys())
    maxx = max(p[0] for p in panels.keys())
    miny = min(p[1] for p in panels.keys())
    maxy = max(p[1] for p in panels.keys())
    # Somehow, the letters were upside-down for me. Maybe change the ranges if it does not display nicely.
    for y in range(maxy, miny-1, -1):
        for x in range(minx, maxx+1):
            color = panels.get((x, y), 0)
            if color == 0:
                print(' ', end='')
            else:
                print('X', end='')
        print('\n', end='')



if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=partOne(inp)))
    print()
    partTwo(inp)
