#!/usr/bin/python
from __future__ import print_function
from collections import Counter

def isValidOne(passphrase):
    return len(passphrase.strip().split()) == len(set(passphrase.strip().split()))

def isValidTwo(passphrase):
    count_letters = list(map(Counter, passphrase.strip().split()))
    return all(map(lambda i: count_letters.count(i) == 1, count_letters))

# That's handy, the Advent of Code gives unittests.
def UnitTest():
    pass1="aa bb cc dd ee"
    pass2="aa bb cc dd aa"
    pass3="aa bb cc dd aaa"

    print("Unit testing part One.")
    print('Passphrase "{pas}" is valid? {res}'.format(pas=pass1, res=isValidOne(pass1)))
    print('Passphrase "{pas}" is valid? {res}'.format(pas=pass2, res=isValidOne(pass2)))
    print('Passphrase "{pas}" is valid? {res}'.format(pas=pass3, res=isValidOne(pass3)))


    pass4="abde fghij"
    pass5="abcde xyz ecdab"
    pass6="a ab abc abd abf abj"
    pass7="iiii oiii ooii oooi oooo"
    pass8="oiii ioii iioi iiio"

    print("Unit testing part Two.")
    print('Passphrase "{pas}" is valid? {res}'.format(pas=pass4, res=isValidTwo(pass4)))
    print('Passphrase "{pas}" is valid? {res}'.format(pas=pass5, res=isValidTwo(pass5)))
    print('Passphrase "{pas}" is valid? {res}'.format(pas=pass6, res=isValidTwo(pass6)))
    print('Passphrase "{pas}" is valid? {res}'.format(pas=pass7, res=isValidTwo(pass7)))
    print('Passphrase "{pas}" is valid? {res}'.format(pas=pass8, res=isValidTwo(pass8)))


def partOne(inp):
    return len(list(filter(isValidOne, inp.strip().split('\n'))))

def partTwo(inp):
    return len(list(filter(isValidTwo, inp.strip().split('\n'))))
        

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
        print("Answer for part two is : {res}".format(res=partTwo(inp)))
