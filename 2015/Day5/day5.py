#!/usr/bin/python3
from __future__ import print_function
import re

def isNice(s):
    """That is the tedious but nonetheless working test."""
    if 'ab' in s:
        return False
    elif 'cd' in s:
        return False
    elif 'pq' in s:
        return False
    elif 'xy' in s:
        return False
    elif s.count('a') + s.count('e') + s.count('i') + s.count('o') + s.count('u') >= 3:
        if 'aa' in s:
            return True
        elif 'bb' in s:
            return True
        elif 'cc' in s:
            return True
        elif 'dd' in s:
            return True
        elif 'ee' in s:
            return True
        elif 'ff' in s:
            return True
        elif 'gg' in s:
            return True
        elif 'hh' in s:
            return True
        elif 'ii' in s:
            return True
        elif 'jj' in s:
            return True
        elif 'kk' in s:
            return True
        elif 'll' in s:
            return True
        elif 'mm' in s:
            return True
        elif 'nn' in s:
            return True
        elif 'oo' in s:
            return True
        elif 'pp' in s:
            return True
        elif 'qq' in s:
            return True
        elif 'rr' in s:
            return True
        elif 'ss' in s:
            return True
        elif 'tt' in s:
            return True
        elif 'uu' in s:
            return True
        elif 'vv' in s:
            return True
        elif 'ww' in s:
            return True
        elif 'xx' in s:
            return True
        elif 'yy' in s:
            return True
        elif 'zz' in s:
            return True
        else:
            return False
    else:
        return False

def isNice2(s):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'

    def cond1(s):
        for l1 in alphabet:
            for l2 in alphabet:
                if re.match('.*'+l1+l2+'.*'+l1+l2, s):
                    return True
        return False


    def cond2(s):
        for l in alphabet:
            if re.match('.*'+l+'.'+l, s):
                return True
        return False

    return cond1(s) and cond2(s)


# That's handy, the Advent of Code gives unittests.
def UnitTest():
    ex1 = "ugknbfddgicrmopn"
    ex2 = "aaa"
    ex3 = "jchzalrnumimnmhp"
    ex4 = "haegwjzuvuyypxyu"
    ex5 = "dvszwmarrgswjxmb"

    print("Unit test for Part One.")
    print("Test {inp} is Nice ? {res}".format(inp=ex1, res=isNice(ex1)))
    print("Test {inp} is Nice ? {res}".format(inp=ex2, res=isNice(ex2)))
    print("Test {inp} is Nice ? {res}".format(inp=ex3, res=isNice(ex3)))
    print("Test {inp} is Nice ? {res}".format(inp=ex4, res=isNice(ex4)))
    print("Test {inp} is Nice ? {res}".format(inp=ex5, res=isNice(ex5)))

    ex6 = "qjhvhtzxzqqjkmpb"
    ex7 = "xxyxx"
    ex8 = "uurcxstgmygtbstg"
    ex9 = "ieodomkazucvgmuy"

    print("")
    print("Unit test for Part Two.")
    print("Test {inp} is Nice ? {res}".format(inp=ex6, res=isNice2(ex6)))
    print("Test {inp} is Nice ? {res}".format(inp=ex7, res=isNice2(ex7)))
    print("Test {inp} is Nice ? {res}".format(inp=ex8, res=isNice2(ex8)))
    print("Test {inp} is Nice ? {res}".format(inp=ex9, res=isNice2(ex9)))


def partOne(inp):
    return len(list(filter(isNice, inp.split('\n'))))

def partTwo(inp):
    return len(list(filter(isNice2, inp.split('\n'))))

if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("-t", "--test", help='Unit tests', action='store_true')
    args.add_argument("-i", "--input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    if options.test:
        UnitTest()
    if options.input:
        inp = options.input.read().strip()
        print("Answer for part one is : {res}".format(res=partOne(inp)))
        print("Answer for part two is : {res}".format(res=partTwo(inp)))
