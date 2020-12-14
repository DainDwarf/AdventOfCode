#!/usr/bin/python3


def part_one(inp):
    timestamp, buses = inp.split('\n')
    timestamp = int(timestamp)
    buses = [int(n) for n in buses.split(',') if n != 'x']
    next_departs = [n-(timestamp % n) for n in buses]
    best_index = next_departs.index(min(next_departs))
    return buses[best_index]*next_departs[best_index]


##### PART TWO, much more difficult! #####
def first_match(num, index, mod):
    """Return the first number ``i*num`` such that ``i*num % mod`` is equal to the index."""
    for i in range(1, mod+1):
        if (num*i)%mod == index%mod:
            return num*i


def recurse_buses_solve(buses):
    """
    It is possible to get a recursive way to handle this:
    Compute the "first match" between the first bus F and each other constraint C.
    This means that for each constraint C at index i, (t+i-first_match(C,i,F)) is divisible by C*F.
    Discarding the first bus F, we can scale to another timestamp T, for example with the lowest(t+i-first_match).
    With M = first_match-i that correspond to that lowest timestamp, the number we search t is such that t = T+M.
    We can generate a new constraint list with 1 less index, such that
    the first bus correspond to that previous highest first match with the new search timestamp.
    If there is only one bus, of course the constraints are resolved at timestamp 0.
    """

    if len(buses) <= 1:
        return 0

    F = buses[0][1]
    matches = [first_match(C, i, F)-i for i, C in buses[1:]]
    M = max(matches)
    # Now, generate the new bus list
    new_buses = []
    for bus, m in zip(buses[1:], matches):
        i, C = bus
        new_buses.append(((M-m)//F, C))
    # Order buses by index
    new_buses = sorted(new_buses, key=lambda t:t[0])
    return M + F*recurse_buses_solve(new_buses)


def part_two(inp):
    buses = [(i, int(n)) for i, n in enumerate(inp.split('\n')[1].split(',')) if n != 'x']
    return recurse_buses_solve(buses)


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=part_one(inp)))
    print("Answer for part two is : {res}".format(res=part_two(inp)))
