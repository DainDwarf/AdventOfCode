#!/usr/bin/python3
from __future__ import print_function
from math import ceil
from itertools import combinations

class Item(object):
    def __init__(self, name, cost, damage, armor):
        self.name = name
        self.cost = cost
        self.damage = damage
        self.armor = armor

    def __str__(self):
        return self.name

Weapons = [ Item('Dagger'    ,   8, 4, 0)
          , Item('Shortsword',  10, 5, 0)
          , Item('Warhammer' ,  25, 6, 0)
          , Item('Longsword' ,  40, 7, 0)
          , Item('Greataxe'  ,  74, 8, 0)
]

Armors  = [ Item('Leather'   ,  13, 0, 1)
          , Item('Chainmail' ,  31, 0, 2)
          , Item('Splintmail',  53, 0, 3)
          , Item('Bandedmail',  75, 0, 4)
          , Item('Platemail' , 102, 0, 5)
]

Rings   = [ Item('Damage +1' ,  25, 1, 0)
          , Item('Damage +2' ,  50, 2, 0)
          , Item('Damage +3' , 100, 3, 0)
          , Item('Defense +1',  20, 0, 1)
          , Item('Defense +2',  40, 0, 2)
          , Item('Defense +3',  80, 0, 3)
]

class Character(object):
    def __init__(self, HP, damage, armor):
        self.HP=HP
        self.damage=damage
        self.armor=armor

class Boss(Character):
    def __init__(self, inp):
        desc = dict(l.strip().split(': ') for l in inp.split('\n'))
        super().__init__(int(desc['Hit Points']), int(desc['Damage']), int(desc['Armor']))


class Player(Character):
    def __init__(self, items):
        damage = sum(i.damage for i in items)
        armor  = sum(i.armor for i in items)
        super().__init__(100, damage, armor)

def genItemsPossibilities():
    for w in Weapons:
        for a in Armors + [Item('Naked', 0, 0, 0)]:
            yield [w, a]
            for r in Rings:
                yield [w, a, r]
            for r1, r2 in combinations(Rings, 2):
                yield [w, a, r1, r2]

def wins(attacker, defender):
    att_damage  = max(1, attacker.damage - defender.armor)
    def_damage = max(1, defender.damage - attacker.armor)
    def_HP = defender.HP
    att_HP = attacker.HP
    while True:
        def_HP -= att_damage
        if def_HP <= 0:
            return True
        att_HP -= def_damage
        if att_HP <= 0:
            return False

def genWinningCosts(boss):
    """Generates all costs that win against given boss."""
    for items in genItemsPossibilities():
        if wins(Player(items), boss):
            yield sum(i.cost for i in items)

def genLosingCosts(boss):
    """Generates all costs that win against given boss."""
    for items in genItemsPossibilities():
        if not wins(Player(items), boss):
            yield sum(i.cost for i in items)

def partOne(inp):
    boss = Boss(inp)
    return min(genWinningCosts(boss))

def partTwo(inp):
    boss = Boss(inp)
    return max(genLosingCosts(boss))

if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    # Sadness all around. No unit tests here!
    # args.add_argument("-t", "--test", help='Unit tests', action='store_true')
    args.add_argument("-i", "--input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    # if options.test:
    #     UnitTest()
    if options.input:
        inp = options.input.read().strip()
        print("Answer for part one is : {res}".format(res=partOne(inp)))
        print("Answer for part two is : {res}".format(res=partTwo(inp)))
