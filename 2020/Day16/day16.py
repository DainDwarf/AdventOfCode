#!/usr/bin/python3
import re


class Field:
    def __init__(self, name, ranges):
        self.name = name
        self.ranges = ranges

    @classmethod
    def from_desc(cls, desc):
        m = re.match(r"(.*?): (\d+)-(\d+) or (\d+)-(\d+)", desc)
        name, range1min, range1max, range2min, range2max = m.groups()
        return cls(name, [(int(range1min), int(range1max)), (int(range2min), int(range2max))])

    def is_valid(self, num):
        return any(r[0] <= num <= r[1] for r in self.ranges)


def parse(inp):
    """
    Returns a tuple containing:
        - The list of instanciated Fields
        - The list of numbers for my ticket
        - The list of lists of numbers of all other tickets
    """
    fields, mine, others = inp.split('\n\n')
    fields = [Field.from_desc(line) for line in fields.split('\n')]
    ticket_nums = [list(map(int, line.split(','))) for line in others.split('\n')[1:]]
    my_ticket = [int(num) for num in mine.split('\n')[1].split(',')]
    return fields, my_ticket, ticket_nums


def filter_tickets(tickets, fields):
    """Return only the tickets that are valid for at least a field."""
    valid_tickets = []
    for ticket_nums in tickets:
        if all(any(f.is_valid(num) for f in fields) for num in ticket_nums):
            valid_tickets.append(ticket_nums)
    return valid_tickets


def compute_constraints(tickets, fields):
    """Returns a dictionary of possible index for each field."""
    constraints = {f: [] for f in fields}
    for i in range(len(fields)):
        for f in fields:
            if all(f.is_valid(t[i]) for t in tickets):
                constraints[f].append(i)
    return constraints


def simplify_constraints(constraints):
    """Try to simplify constraints by simply iterating over all constraints and
    removing the trivial case of a constraint that can only go to a single index."""

    simplified = dict()
    for _ in range(len(constraints)):
        fixed_i = fixed_field = None
        for field, indexes in constraints.items():
            if len(indexes) == 1:
                fixed_i = indexes[0]
                fixed_field = field
        if fixed_i is not None:
            constraints.pop(fixed_field)
            for field, indexes in constraints.items():
                try:
                    indexes.remove(fixed_i)
                except ValueError:
                    pass
            simplified[fixed_field.name] = fixed_i
    # Verify that it was enough to solve it all
    assert len(constraints) == 0, "Your set of constraint is not trivialy solvable. Bad luck!"

    return simplified


def part_one(inp):
    fields, mine, others = parse(inp)
    all_count = 0
    for line in others:
        for num in line:
            if not any(f.is_valid(num) for f in fields):
                all_count += num
    return all_count


def part_two(inp):
    fields, mine, others = parse(inp)

    valid_tickets = filter_tickets(others, fields)
    constraints = simplify_constraints(compute_constraints(valid_tickets, fields))

    prod = 1
    for field_name, i in constraints.items():
        if field_name.startswith("departure"):
            prod *= mine[i]

    return prod


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=part_one(inp)))
    print("Answer for part two is : {res}".format(res=part_two(inp)))
