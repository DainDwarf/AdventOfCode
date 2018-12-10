#!/usr/bin/python3
from __future__ import print_function
import re
import progressbar
from collections import deque


class StupidMarbleGame(object):
    def __init__(self):
        self.circle = deque([0])
        self.current_index = 0

    def playMarble(self, marble):
        if marble % 23 == 0:
            self.circle.rotate(7)
            score = marble + self.circle.popleft()
            return score
        else:
            self.circle.rotate(-2)
            self.circle.appendleft(marble)
            return 0

    def display(self):
        head = self.circle[0]
        zero = self.circle.index(0)
        self.circle.rotate(-zero)
        print(" ".join(str(c) if c != head else f"({c})" for c in self.circle))
        self.circle.rotate(zero)


def getHighScore(players, turns, display=False, progress=False):
    scores = {p:0 for p in range(players)}
    stupid = StupidMarbleGame()
    marbles = range(1, turns+1)
    if progress:
        marbles = progressbar.progressbar(marbles)
    for marble in marbles:
        scores[(marble-1)%players] += stupid.playMarble(marble)
        if display:
            stupid.display()
    return max(scores.values())


# That's handy, the Advent of Code gives unittests.
def testOne():
    ex1 = "9 players; last marble is worth 25 points"

    print("Unit test for Part One.")
    print("{inp}: high score is {res}".format(inp=ex1, res=partOne(ex1, display=True)))

    ex2 = "10 players; last marble is worth 1618 points"
    ex3 = "13 players; last marble is worth 7999 points"
    ex4 = "17 players; last marble is worth 1104 points"
    ex5 = "21 players; last marble is worth 6111 points"
    ex6 = "30 players; last marble is worth 5807 points"

    print("{inp}: high score is {res}".format(inp=ex2, res=partOne(ex2)))
    print("{inp}: high score is {res}".format(inp=ex3, res=partOne(ex3)))
    print("{inp}: high score is {res}".format(inp=ex4, res=partOne(ex4)))
    print("{inp}: high score is {res}".format(inp=ex5, res=partOne(ex5)))
    print("{inp}: high score is {res}".format(inp=ex6, res=partOne(ex6)))


def testTwo():
    print("No unit test for part two!")


def partOne(inp, display=False):
    game_re = re.compile(r"(\d+) players; last marble is worth (\d+) points")
    players, turns = game_re.match(inp).groups()
    players = int(players)
    turns = int(turns)
    return getHighScore(players, turns, display)


def partTwo(inp):
    game_re = re.compile(r"(\d+) players; last marble is worth (\d+) points")
    players, turns = game_re.match(inp).groups()
    players = int(players)
    turns = int(turns)
    return getHighScore(players, turns*100, progress=True)


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
