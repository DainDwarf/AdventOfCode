#!/usr/bin/python3
import re


class Rule:
    def __init__(self, name, children=None, strings=None):
        self.name = name
        self.children = children or []
        self.strings = strings or []

    def __str__(self):
        if self.final:
            if len(self.strings) > 1:
                return f"{self.name}: ({'|'.join(self.strings)})"
            else:
                return f"{self.name}: {self.strings[0]}"
        else:
            return f"{self.name}: {self.children}"

    @classmethod
    def from_desc(cls, desc):
        name, rest = desc.split(': ')
        name = int(name)
        try:
            children = [[int(n) for n in sub.split()] for sub in rest.split(' | ')]
            return cls(name, children=children)
        except ValueError:
            assert rest in ('"a"', '"b"')
            return cls(name, strings=[rest[1]])

    @property
    def final(self):
        return bool(self.strings)

    @property
    def final_string(self):
        if len(self.strings) > 1:
            return f"({'|'.join(self.strings)})"
        else:
            return f"{self.strings[0]}"


class Rulebook:
    def __init__(self):
        self.rules = dict()

    def __str__(self):
        return '\n'.join(str(r) for _, r in sorted(self.rules.items(), key=lambda t:t[0]))

    def add_rule(self, rule):
        self.rules[rule.name] = rule

    @property
    def final(self):
        return all(r.final for r in self.rules.values())

    def simplify(self):
        simple = []
        for r in self.rules.values():
            if r.final:
                continue
            if all(all(self.rules[child].final for child in choice) for choice in r.children):
                simple.append(Rule(r.name, strings=
                    [''.join
                        (
                            ''.join(self.rules[child].final_string)
                        for child in choice)
                    for choice in r.children]
                ))
        for new_r in simple:
            self.rules[new_r.name] = new_r


def part_one(inp):
    rules, tests = inp.split('\n\n')
    book = Rulebook()
    for line in rules.split('\n'):
        book.add_rule(Rule.from_desc(line))
    while not book.final:
        book.simplify()
    print(book.rules[0].final_string)
    rule0 = re.compile(book.rules[0].final_string)
    matches = [line for line in tests.split('\n') if rule0.fullmatch(line) is not None]
    return len(matches)


def part_two(inp):
    pass


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=part_one(inp)))
    print("Answer for part two is : {res}".format(res=part_two(inp)))
