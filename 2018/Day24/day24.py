import re
import logging


class Army(object):
    def __init__(self, name):
        self.name = name
        self.groups = dict()

    def addGroup(self, group):
        if self.groups:
            new_num = max(self.groups.keys())+1
            self.groups[new_num] = group
        else:
            self.groups[1] = group

    def summary(self):
        print(self.name + ":")
        for i, group in sorted(self.groups.items()):
            print(f"Group {i} contains {group.units} units")

    def selectTargets(self, ennemies, debug=False):
        ennemies = dict(ennemies.groups.items())
        targets = dict()
        for i, group in sorted(self.groups.items(), key=lambda t:(t[1].power, t[1].init), reverse=True):
            dmg = 0
            power = 0
            init = 0
            selected = None
            for j, ennemy in ennemies.items():
                this_dmg = group.preAttack(ennemy)
                if this_dmg > 0:
                    logging.debug(f"{self.name} group {i} would deal defending group {j} {this_dmg} damage")
                    if this_dmg > dmg or (this_dmg == dmg and ennemy.power > power) or (this_dmg == dmg and ennemy.power == power and ennemy.init > init):
                        selected = j
                        dmg = this_dmg
                        power = ennemy.power
                        init = ennemy.init
            if selected is not None:
                targets[i] = selected
                ennemies.pop(selected)
        return targets

    def boost(self, value):
        for u in self.groups.values():
            u.dmg += value

class Group(object):
    def __init__(self):
        self.units = 0
        self.hp = 0
        self.dmg = 0
        self.type = ""
        self.init = 0
        self.weakness = []
        self.immune = []

    @classmethod
    def fromDescription(cls, desc):
        group_re = re.compile(r"""^(?P<units>\d+)\ units\ 
            each\ with\ (?P<hp>\d+)\ hit\ points\ 
            (?P<effects>\(.*\)\ )?with\ an\ attack\ 
            that\ does\ (?P<dmg>\d+)\ (?P<dmg_type>\w+)\ damage\ 
            at\ initiative\ (?P<init>\d+)$""", re.X)
        match = group_re.match(desc)
        self = cls()
        self.units = int(match.group('units'))
        self.hp = int(match.group('hp'))
        self.dmg = int(match.group('dmg'))
        self.type = match.group('dmg_type')
        self.init = int(match.group('init'))
        effects = match.group('effects') 
        if effects is not None:
            effects = effects.strip(" ()")
            if ';' in effects:
                left, right = effects.split("; ")
                if left.startswith("immune"):
                    self.immune = [s.strip(" ,") for s in left.split()[2:]]
                    self.weakness = [s.strip(" ,") for s in right.split()[2:]]
                else:
                    self.immune = [s.strip(" ,") for s in right.split()[2:]]
                    self.weakness = [s.strip(" ,") for s in left.split()[2:]]
            elif effects.startswith("immune"):
                self.immune = [s.strip(" ,") for s in effects.split()[2:]]
            else:
                self.weakness = [s.strip(" ,") for s in effects.split()[2:]]
        return self

    @property
    def power(self):
        return self.units*self.dmg if self.units > 0 else 0

    def preAttack(self, other):
        if self.units <= 0:
            return 0
        elif other.units <= 0:
            return 0
        elif self.type in other.immune:
            return 0
        elif self.type in other.weakness:
            return self.power*2
        else:
            return self.power
        return ret

    def attack(self, other):
        dmg = self.preAttack(other)
        killed = min(dmg//other.hp, other.units)
        other.units -= killed
        return dmg, killed


def attackPhase(first_army, first_army_targets, second_army, second_army_targets, debug=False):
    all_units = list(first_army.groups.values())+list(second_army.groups.values())
    sum_killed = 0
    for unit in sorted(all_units, key=lambda u:u.init, reverse=True):
        try:
            for i, u in first_army.groups.items():
                if unit is u:
                    j = first_army_targets[i]
                    dmg, killed = first_army.groups[i].attack(second_army.groups[j])
                    sum_killed += killed
                    logging.debug(f"{first_army.name} group {i} attacks defending group {j}, killing {killed} units")
                    if second_army.groups[j].units == 0:
                        second_army.groups.pop(j)
            for i, u in second_army.groups.items():
                if unit is u:
                    j = second_army_targets[i]
                    dmg, killed = second_army.groups[i].attack(first_army.groups[j])
                    sum_killed += killed
                    logging.debug(f"{second_army.name} group {i} attacks defending group {j}, killing {killed} units")
                    if first_army.groups[j].units == 0:
                        first_army.groups.pop(j)
        except KeyError:
            continue #trying to play someone that has no target
    return sum_killed


def battle(first_army, second_army, debug=False):
    while first_army.groups and second_army.groups:
        if debug:
            print()
            first_army.summary()
            second_army.summary()
            print()

        second_targets = second_army.selectTargets(first_army, debug=debug)
        first_targets = first_army.selectTargets(second_army, debug=debug)

        if debug: print()

        killed = attackPhase(first_army, first_targets, second_army, second_targets, debug=debug)
        if killed == 0:
            return


def parseArmies(inp):
    first, second = inp.split("\n\n")
    first_name, first = first.split('\n', 1)
    second_name, second = second.split('\n', 1)
    first_army = Army(first_name.strip(": "))
    for line in first.strip().split('\n'):
        first_army.addGroup(Group.fromDescription(line.strip()))
    second_army = Army(second_name.strip(": "))
    for line in second.strip().split('\n'):
        second_army.addGroup(Group.fromDescription(line.strip()))
    return first_army, second_army

# That's handy, the Advent of Code gives unittests.
def testOne():
    print("Unit test for Part One.")

    inp = """Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4"""
    res = partOne(inp, debug=True)
    print(f"Test example gives {res}")


def testTwo():
    print("Unit test for Part Two.")

    inp = """Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4"""
    res = partTwo(inp)
    print(f"Test example gives {res}")


def partOne(inp, debug=False):
    immune, infection = parseArmies(inp)
    battle(immune, infection, debug=debug)
    if immune.groups:
        return sum(u.units for u in immune.groups.values())
    else:
        return sum(u.units for u in infection.groups.values())


def partTwo(inp):
    for i in range(2000):
        logging.info(f"Checking for boost {i}")
        immune, infection = parseArmies(inp)
        immune.boost(i)
        battle(immune, infection)
        if not infection.groups:
            return sum(u.units for u in immune.groups.values())


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("-t", "--test", help='Unit tests', action='store_true')
    args.add_argument("-i", "--input", help='Your input file', type=FileType('r'))
    args.add_argument("-d", "--debug", help='Add debugging logs', action="store_true")
    options = args.parse_args()

    if options.debug:
        logging.basicConfig(format="%(message)s", level=logging.DEBUG)
    else:
        logging.basicConfig(format="%(message)s", level=logging.INFO)

    if options.test:
        testOne()
        print()
        testTwo()
        print()
    if options.input:
        inp = options.input.read().strip()
        print("Answer for part one is : {res}".format(res=partOne(inp)))
        print("Answer for part two is : {res}".format(res=partTwo(inp)))
