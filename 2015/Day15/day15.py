#!/usr/bin/python3
from __future__ import print_function
import re, itertools

class Ingredient(object):
    def __init__(self, description):
        ingredient_re = r"(\w+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)"
        parse = re.match(ingredient_re, description).groups()
        self.name       =     parse[0]
        self.capacity   = int(parse[1])
        self.durability = int(parse[2])
        self.flavor     = int(parse[3])
        self.texture    = int(parse[4])
        self.calories   = int(parse[5])

def getCalories(ingredients_list):
    return sum(l[0]*l[1].calories for l in ingredients_list)

def getScore(ingredients_list):
    capacity    = max(0, sum(l[0]*l[1].capacity     for l in ingredients_list))
    durability  = max(0, sum(l[0]*l[1].durability   for l in ingredients_list))
    flavor      = max(0, sum(l[0]*l[1].flavor       for l in ingredients_list))
    texture     = max(0, sum(l[0]*l[1].texture      for l in ingredients_list))

    return capacity * durability * flavor * texture

# That's handy, the Advent of Code gives unittests.
def UnitTest():
    ex = """Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3"""

    print("Unit test for Part One.")
    print("Test {inp} gives {res}".format(inp=ex, res=partOne(ex.strip())))

    print("")
    print("Unit test for Part Two.")
    print("Test {inp} gives {res}".format(inp=ex, res=partTwo(ex)))


def partOne(inp):
    ingredients = list(map(Ingredient, inp.split('\n')))
    def _genScores():
        for prod in itertools.product(*([range(100)]*(len(ingredients)-1))):
            if sum(prod) > 100:
                continue
            else:
                last_qty = 100-sum(prod)
                recipe = list(zip(list(prod)+[last_qty], ingredients))
                yield getScore(recipe)
    return max(_genScores())

def partTwo(inp):
    ingredients = list(map(Ingredient, inp.split('\n')))
    def _genScores():
        for prod in itertools.product(*([range(100)]*(len(ingredients)-1))):
            if sum(prod) > 100:
                continue
            else:
                last_qty = 100-sum(prod)
                recipe = list(zip(list(prod)+[last_qty], ingredients))
                if getCalories(recipe) == 500:
                    yield getScore(recipe)
    return max(_genScores())

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
