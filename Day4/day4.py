#!/usr/bin/python
from __future__ import print_function
from itertools import permutations

def isValid(passphrase):
    return len(passphrase.strip().split()) == len(set(passphrase.strip().split()))

# That's handy, the Advent of Code gives unittests.
def UnitTest():
    pass1="aa bb cc dd ee"
    pass2="aa bb cc dd aa"
    pass3="aa bb cc dd aaa"

    print("Unit testing part One.")
    print('Passphrase "{pas}" is valid? {res}'.format(pas=pass1, res=isValid(pass1)))
    print('Passphrase "{pas}" is valid? {res}'.format(pas=pass2, res=isValid(pass2)))
    print('Passphrase "{pas}" is valid? {res}'.format(pas=pass3, res=isValid(pass3)))


def partOne(inp):
    return len(list(filter(isValid, inp.strip().split('\n'))))
        

if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("-t", "--test", help='Unit tests', action='store_true')
    args.add_argument("-i", "--input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    if options.test:
        UnitTest()
    if options.input:
        inp = options.input.read()
        print("Answer for part one is : {res}".format(res=partOne(inp)))
