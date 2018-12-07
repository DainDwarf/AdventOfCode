#!/usr/bin/python3
from __future__ import print_function
import re, networkx


def toGraph(inp):
    parse_re = re.compile(r"Step (\w+) must be finished before step (\w+) can begin\.")
    G = networkx.DiGraph()
    for line in inp.split("\n"):
        edge = parse_re.match(line).groups()
        G.add_edge(*edge)
    return G


def timeForTask(c, Atime=61):
    return ord(c)-ord('A')+Atime


# That's handy, the Advent of Code gives unittests.
def testOne():
    ex = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin."""

    print("Unit test for Part One.")
    print("Test for example gives {res}".format(inp=ex, res=partOne(ex)))


def testTwo():
    ex = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin."""

    print("Unit test for Part Two.")
    print("Test for example gives {res}".format(inp=ex, res=partTwo(ex, workers=2, Atime=1, debug=True)))


def partOne(inp):
    G = toGraph(inp)
    ret = []
    while G:
        roots = [n for n, d in G.in_degree if d == 0]
        node = min(roots)
        G.remove_node(node)
        ret.append(node)
    return "".join(ret)


def partTwo(inp, workers=5, Atime=61, debug=False):
    G = toGraph(inp)
    current_time = 0
    current_tasks = dict()  #Node: Absolute time to finish
    while G:
        roots = sorted([n for n, d in G.in_degree if d == 0 and n not in current_tasks])
        available_workers = workers - len(current_tasks)
        for task in roots[:available_workers]:
            current_tasks[task] = current_time + timeForTask(task, Atime)
            if debug:
                print(f"Starting task {task} at time {current_time}")
        # Now, do something!
        finished_task, time = min(current_tasks.items(), key=lambda t:t[1])
        current_time = time
        current_tasks.pop(finished_task)
        G.remove_node(finished_task)
        if debug:
            print(f"Finished task {finished_task} at time {current_time}")
    return max(current_time.values()) if current_tasks else current_time


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("-t", "--test", help='Unit tests', action='store_true')
    args.add_argument("-i", "--input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    if options.test:
        testOne()
        print("")
        testTwo()
    if options.input:
        inp = options.input.read().strip()
        print("Answer for part one is : {res}".format(res=partOne(inp)))
        print("Answer for part two is : {res}".format(res=partTwo(inp)))
