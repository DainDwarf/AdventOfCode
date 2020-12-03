#!/usr/bin/python3


class TreeMap:
    def __init__(self, map_desc):
        self._grid = [l.strip() for l in map_desc.split('\n')]
        self.height = len(self._grid)
        self.length = len(self._grid[0])

    def __getitem__(self, pos):
        return self._grid[pos[0]][pos[1]%self.length]

    def slide(self, from_pos, slide_vector):
        """Count the number of trees you 'collect' starting at ``from_pos`` with a vector of ``slide_vector``.

        WARNING: slide_vector has inverse coordinates from the problem!"""
        count = 0
        current_pos = from_pos
        while current_pos[0] < self.height:
            if self[current_pos] == '#':
                count += 1
            current_pos = (current_pos[0]+slide_vector[0], current_pos[1]+slide_vector[1])
        return count


def part_one(inp):
    tree_map = TreeMap(inp)
    return tree_map.slide((0, 0), (1, 3))


def part_two(inp):
    slopes = [
        (1, 1),
        (1, 3),
        (1, 5),
        (1, 7),
        (2, 1),
    ]
    tree_map = TreeMap(inp)
    prod = 1
    for slope in slopes:
        prod *= tree_map.slide((0, 0), slope)
    return prod


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=part_one(inp)))
    print("Answer for part two is : {res}".format(res=part_two(inp)))
