#!/usr/bin/python3
from __future__ import print_function
from functools import reduce
import re


def toPass(n):
    tmp = n
    ret = ""
    while tmp > 0:
        ret = chr(tmp%27 + ord('a')-1) + ret
        tmp = tmp // 27
    return ret


def toNum(s):
    return reduce(lambda prev, n: 27*prev+(n-ord('a')+1), map(ord, s), 0)


def valid(s):
    if 'i' in s or 'o' in s or 'l' in s:
        return False

    if 'abc' in s or 'bcd' in s or 'cde' in s or 'def' in s or 'efg' in s or 'fgh' in s or 'pqr' in s or 'qrs' in s or 'rst' in s or 'stu' in s or 'tuv' in s or 'uvw' in s or 'vwx' in s or 'wxy' in s or 'xyz' in s:
        if re.match(r".*(aa|bb|cc|dd|ee|ff|gg|hh|jj|kk|mm|nn|pp|qq|rr|ss|tt|uu|vv|ww|xx|yy|zz).*(aa|bb|cc|dd|ee|ff|gg|hh|jj|kk|mm|nn|pp|qq|rr|ss|tt|uu|vv|ww|xx|yy|zz).*", s):
            return True

    return False

class PasswordGenerator(object):
    def __init__(self, pas):
        self.__cur = toNum(pas) +1

    def __next__(self):
        #Start with nothing fancy, just iterate all passwords.
        while not valid(toPass(self.__cur)):
            self.__cur += 1
        ret = toPass(self.__cur)
        self.__cur += 1
        return ret

# That's handy, the Advent of Code gives unittests.
def UnitTest():
    ex1 = "hijklmmn" # Bad
    ex2 = "abbceffg" # Bad
    ex3 = "abbcegjk" # Bad
    ex4 = "abcdefgh" # Bad
    ex5 = "abcdffaa" # Good
    ex6 = "ghijklmn" # Bad
    ex7 = "ghjaabcc" # Good

    print("Unit test for Part One.")
    print("Is password {inp} valid ? {v}".format(inp=ex1, v=valid(ex1)))
    print("Is password {inp} valid ? {v}".format(inp=ex2, v=valid(ex2)))
    print("Is password {inp} valid ? {v}".format(inp=ex3, v=valid(ex3)))
    print("Is password {inp} valid ? {v}".format(inp=ex4, v=valid(ex4)))
    print("Is password {inp} valid ? {v}".format(inp=ex5, v=valid(ex5)))
    print("Is password {inp} valid ? {v}".format(inp=ex6, v=valid(ex6)))
    # Not doing this one, it asks for some optimisation for 'i'.
    # print("Is password {inp} valid ? {v}".format(inp=ex7, v=valid(ex7)))

    print("Password after {inp} is {res}".format(inp=ex4, res=partOne(ex4)))
    print("Password after {inp} is {res}".format(inp=ex6, res=partOne(ex6)))

    print("")
    print("Unit test for Part Two.")


def partOne(inp):
    gen = PasswordGenerator(inp)
    return next(gen)

def partTwo(inp):
    gen = PasswordGenerator(inp)
    next(gen)
    return next(gen)

if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("-t", "--test", help='Unit tests', action='store_true')
    args.add_argument("-i", "--input", help='Your input', type=str)
    options = args.parse_args()

    if options.test:
        UnitTest()
    if options.input:
        inp = options.input.strip()
        print("Answer for part one is : {res}".format(res=partOne(inp)))
        print("Answer for part two is : {res}".format(res=partTwo(inp)))
