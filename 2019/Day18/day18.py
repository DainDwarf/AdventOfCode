import pytest


# That's handy, the Advent of Code gives unittests.
def test_parse():
    inp = """
#########
#b.A.@.a#
#########"""
    maze = Maze(inp)
    assert maze.player_pos == (5, 1)
    assert maze.keys == {'b': (1, 1), 'a': (7, 1)}


@pytest.mark.parametrize("inp, keys, exp", [
    ("""
#########
#b.A.@.a#
#########""", [], {(7, 1): 2}),
    ("""
#########
#b.A...@#
#########""", ['a'], {(1, 1): 6}),
    ("""
########################
#f.D.E.e.C.@.A...a.B.c.#
######################.#
#d.....................#
########################""", ['a', 'b'], {(21, 1): 10, (1, 3): 34}),
])
def test_path(inp, keys, exp):
    maze = Maze(inp)
    res = maze.keys_paths(maze.player_pos, keys)
    assert res == exp


@pytest.mark.parametrize("inp, exp", [
    ("""
#########
#b.A.@.a#
#########""", 8),
    ("""
########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################""", 86),
    ("""
########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################""", 132),
    ("""
#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################""", 136),
    ("""
########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################""", 81),
])
def test_one(inp, exp):
    res = part_one(inp)
    assert res == exp


@pytest.mark.parametrize("inp, exp", [
])
def test_two(inp, exp):
    res = part_two(inp)
    assert res == exp


class Maze:
    def __init__(self, inp):
        self._maze = dict()
        for y, line in enumerate(inp.strip().split('\n')):
            for x, cell in enumerate(line.strip()):
                self._maze[x, y] = cell

    def __getitem__(self, pos):
        return self._maze[pos]

    def neighbors(self, pos, keys=None):
        if keys is None:
            keys = set()
        x, y = pos

        neigh = []
        for next_pos in [(x-1, y  ),
                         (x+1, y  ),
                         (x  , y+1),
                         (x  , y-1),
        ]:
            next_cell = self[next_pos]
            if next_cell in '.@abcdefghijklmnopqrstuvwxyz':
                neigh.append(next_pos)
            elif next_cell in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' and next_cell.lower() in keys:
                neigh.append(next_pos)
        return neigh

    def keys_paths(self, start_pos, keys):
        """Use BFS/dijkstra to find the shortest path from start_pos to every obtainable keys."""
        explored = set()
        neigh = {start_pos: 0}
        paths = dict()
        while neigh:
            smallest_neigh, distance = min(neigh.items(), key=lambda i: i[1])
            for new_neigh in self.neighbors(smallest_neigh, keys):
                if new_neigh not in explored:
                    neigh[new_neigh] = distance+1
            explored.add(smallest_neigh)
            neigh.pop(smallest_neigh)
            cell = self[smallest_neigh]
            if cell in 'abcdefghijklmnopqrstuvwxyz' and cell not in keys:
                paths[smallest_neigh] = distance
        return paths

    def get_all_keys(self):
        """Use dijkstra to find the shortest path that goes through all keys.

        The nodes are (set(keys_obtained), position)
        The edges are given by calling keys_paths."""

        to_obtain = frozenset(self.keys.keys())
        paths = dict() #node: distance
        neigh = {(frozenset(), self.player_pos): 0}
        while neigh:
            # print(f"Still {len(neigh)} nodes to look at, already explored {len(paths)} nodes.")
            smallest_node, distance = min(neigh.items(), key=lambda i: i[1])
            keys, position = smallest_node
            for new_key_pos, new_distance in self.keys_paths(position, keys).items():
                new_node = (keys.union({self[new_key_pos]}), new_key_pos)
                if new_node not in paths.keys():
                    if new_node in neigh:
                        neigh[new_node] = min(neigh[new_node], distance+new_distance)
                    else:
                        neigh[new_node] = distance+new_distance
            paths[smallest_node] = distance
            neigh.pop(smallest_node)
        # Find the smallest path that goes to a node that has all keys.
        min_path = 99999999
        for node, distance in paths.items():
            if node[0] == to_obtain and distance < min_path:
                min_path = distance
        return min_path

    @property
    def player_pos(self):
        for pos, cell in self._maze.items():
            if cell == '@':
                return pos

    @property
    def keys(self):
        return {cell: pos for pos, cell in self._maze.items()
                if cell in 'abcdefghijklmnopqrstuvwxyz'
        }


def part_one(inp):
    maze = Maze(inp)
    return maze.get_all_keys()


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
