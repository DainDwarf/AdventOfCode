import pytest
import networkx as nx
from networkx.algorithms.shortest_paths.generic import shortest_path


# That's handy, the Advent of Code gives unittests.
# Careful with the test input, as there wil be no strip() in the code : space has meaning here
@pytest.mark.parametrize("inp, exp", [
    ("""         A           
         A           
  #######.#########  
  #######.........#  
  #######.#######.#  
  #######.#######.#  
  #######.#######.#  
  #####  B    ###.#  
BC...##  C    ###.#  
  ##.##       ###.#  
  ##...DE  F  ###.#  
  #####    G  ###.#  
  #########.#####.#  
DE..#######...###.#  
  #.#########.###.#  
FG..#########.....#  
  ###########.#####  
             Z       
             Z       """, 23),
    ("""                   A               
                   A               
  #################.#############  
  #.#...#...................#.#.#  
  #.#.#.###.###.###.#########.#.#  
  #.#.#.......#...#.....#.#.#...#  
  #.#########.###.#####.#.#.###.#  
  #.............#.#.....#.......#  
  ###.###########.###.#####.#.#.#  
  #.....#        A   C    #.#.#.#  
  #######        S   P    #####.#  
  #.#...#                 #......VT
  #.#.#.#                 #.#####  
  #...#.#               YN....#.#  
  #.###.#                 #####.#  
DI....#.#                 #.....#  
  #####.#                 #.###.#  
ZZ......#               QG....#..AS
  ###.###                 #######  
JO..#.#.#                 #.....#  
  #.#.#.#                 ###.#.#  
  #...#..DI             BU....#..LF
  #####.#                 #.#####  
YN......#               VT..#....QG
  #.###.#                 #.###.#  
  #.#...#                 #.....#  
  ###.###    J L     J    #.#.###  
  #.....#    O F     P    #.#...#  
  #.###.#####.#.#####.#####.###.#  
  #...#.#.#...#.....#.....#.#...#  
  #.#####.###.###.#.#.#########.#  
  #...#.#.....#...#.#.#.#.....#.#  
  #.###.#####.###.###.#.#.#######  
  #.#.........#...#.............#  
  #########.###.###.#############  
           B   J   C               
           U   P   P               """, 58),
])
def test_one(inp, exp):
    res = part_one(inp)
    assert res == exp


@pytest.mark.parametrize("inp, exp", [
])
def test_two(inp, exp):
    res = part_two(inp)
    assert res == exp


def left(pos):
    return (pos[0]-1, pos[1])


def right(pos):
    return (pos[0]+1, pos[1])


def up(pos):
    return (pos[0], pos[1]-1)


def down(pos):
    return (pos[0], pos[1]+1)


def _to_dict(inp):
    """Transforms input into dictionary."""
    parse = dict()
    for y, line in enumerate(inp.split('\n')):
        for x, cell in enumerate(line):
            parse[x, y] = cell
    return parse


def parse_portals(first_pass):
    """Returns a dictionary where empty spaces are not available, and two cell portals are merged into a single cell.

    The two-cell portals will be located at the '.' next to it, becuase we move from one '.' to another on a single step when using portals.
    It makes the later graph construction easier."""
    parse = dict()
    for pos, cell in first_pass.items():
        if not cell.isalpha():
            if cell == '.' and pos not in parse: # avoid overwriting a portal
                parse[pos] = cell
        else:
            neighbors = {neighpos: first_pass.get(neighpos, ' ') for neighpos in [left(pos), right(pos), up(pos), down(pos)]}
            if neighbors[left(pos)] == '.':
                parse[left(pos)] = cell + neighbors[right(pos)]
            elif neighbors[right(pos)] == '.':
                parse[right(pos)] = neighbors[left(pos)] + cell
            elif neighbors[up(pos)] == '.':
                parse[up(pos)] = cell + neighbors[down(pos)]
            elif neighbors[down(pos)] == '.':
                parse[down(pos)] = neighbors[up(pos)] + cell
            # else: don't add to parse portals: This is the other end of the portal word.
    return parse

def _to_graph(inp):
    """Transforms the input into a graph, connecting portals. Also returns start and end positions."""
    first_pass = _to_dict(inp)
    parsed = parse_portals(first_pass)

    # Time to parse it all into a graph!
    G = nx.Graph()
    start = end = None
    for pos, cell in parsed.items():
        if cell == '.':
            for neigh in [left(pos), right(pos), up(pos), down(pos)]:
                if parsed.get(neigh, '#') != '#': # Catches both '.' and portals
                    G.add_edge(pos, neigh)
        elif cell.isalpha(): # portal
            # AA and ZZ are not really portals.
            if cell == 'AA':
                start = pos
            elif cell == 'ZZ':
                end = pos
            else:
                connected = [p for p, c in parsed.items() if c == cell and p != pos]
                if len(connected) < 1:
                    raise RuntimeError(f"({pos}): No sibling for {cell}")
                if len(connected) > 1:
                    raise RuntimeError(f"({pos}): Too many siblings for {cell}: {len(connected)}")
                for connect_pos in connected:
                    G.add_edge(pos, connect_pos)
        # else: it's a wall
    return G, start, end


def part_one(inp):
    G, start, end = _to_graph(inp)
    return len(shortest_path(G, start, end)) - 1


def part_two(inp):
    pass


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read()
    print("Answer for part one is : {res}".format(res=part_one(inp)))
    print("Answer for part two is : {res}".format(res=part_two(inp)))
