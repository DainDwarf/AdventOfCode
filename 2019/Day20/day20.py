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
             Z       """, 26),
    ("""             Z L X W       C                 
             Z P Q B       K                 
  ###########.#.#.#.#######.###############  
  #...#.......#.#.......#.#.......#.#.#...#  
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  
  #.#...#.#.#...#.#.#...#...#...#.#.......#  
  #.###.#######.###.###.#.###.###.#.#######  
  #...#.......#.#...#...#.............#...#  
  #.#########.#######.#.#######.#######.###  
  #...#.#    F       R I       Z    #.#.#.#  
  #.###.#    D       E C       H    #.#.#.#  
  #.#...#                           #...#.#  
  #.###.#                           #.###.#  
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#  
CJ......#                           #.....#  
  #######                           #######  
  #.#....CK                         #......IC
  #.###.#                           #.###.#  
  #.....#                           #...#.#  
  ###.###                           #.#.#.#  
XF....#.#                         RF..#.#.#  
  #####.#                           #######  
  #......CJ                       NM..#...#  
  ###.#.#                           #.###.#  
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#  
  #.....#        F   Q       P      #.#.#.#  
  ###.###########.###.#######.#########.###  
  #.....#...#.....#.......#...#.....#.#...#  
  #####.#.###.#######.#######.###.###.#.#.#  
  #.......#.......#.#.#.#.#...#...#...#.#.#  
  #####.###.#####.#.#.#.#.###.###.#.###.###  
  #.......#.....#.#...#...............#...#  
  #############.#.#.###.###################  
               A O F   N                     
               A A D   M                     """, 396),
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


class DictMap(dict):
    def __init__(self, inp):
        for y, line in enumerate(inp.split('\n')):
            for x, cell in enumerate(line):
                self[x, y] = cell
        self.minx = 0
        self.miny = 0
        self.maxx = x-1
        self.maxy = y-1


def near_edge(pos, full_map, max_distance=3):
    return (pos[0]-full_map.minx <= max_distance
        or  full_map.maxx-pos[0] <= max_distance
        or  pos[1]-full_map.miny <= max_distance
        or  full_map.maxy-pos[1] <= max_distance
    )


def parse_portals(first_pass):
    """Returns a dictionary of position: tile with only passable tile.

    Regular tiles are '.', while portals are noted as "NAME-inner" and "NAME-outer",
    placed on the adjacent '.' tile on the input map.
    Placing portals on the '.' instead of near it simplifies distance computation.
    Portal are suffixed to simplify the work for part2."""
    parse = dict()
    for pos, cell in first_pass.items():
        if not cell.isalpha():
            if cell == '.' and pos not in parse: # avoid overwriting a portal
                parse[pos] = cell
        else:
            neighbors = {neighpos: first_pass.get(neighpos, ' ') for neighpos in [left(pos), right(pos), up(pos), down(pos)]}
            suffix = "-outer" if near_edge(pos, first_pass) else "-inner"
            if neighbors[left(pos)] == '.':
                parse[left(pos)] = cell + neighbors[right(pos)] + suffix
            elif neighbors[right(pos)] == '.':
                parse[right(pos)] = neighbors[left(pos)] + cell + suffix
            elif neighbors[up(pos)] == '.':
                parse[up(pos)] = cell + neighbors[down(pos)] + suffix
            elif neighbors[down(pos)] == '.':
                parse[down(pos)] = neighbors[up(pos)] + cell + suffix
            # else: don't add to parse portals: This is the other end of the portal word.
    return parse


def _to_donut(parsed):
    """Transforms the parsed input into a graph, connecting portals. Also returns start and end positions."""
    G = nx.Graph()
    start = end = None
    for pos, cell in parsed.items():
        if cell == '.':
            for neigh in [left(pos), right(pos), up(pos), down(pos)]:
                if neigh in parsed:
                    G.add_edge(pos, neigh)
        else: # portal
            # AA and ZZ are not really portals.
            if cell == 'AA-outer':
                start = pos
            elif cell == 'ZZ-outer':
                end = pos
            else:
                connected = [p for p, c in parsed.items() if c[:2] == cell[:2] and p != pos]
                if len(connected) < 1:
                    raise RuntimeError(f"({pos}): No sibling for {cell}")
                if len(connected) > 1:
                    raise RuntimeError(f"({pos}): Too many siblings for {cell}: {len(connected)}")
                for connect_pos in connected:
                    G.add_edge(pos, connect_pos)
    return G, start, end


def _precompute_single_level_paths(parsed):
    """Transform the parsed input into another graph, corresponding to a single recursion level.

    Nodes are the portal (with their inner-outer suffix)
    Edges are weighted by the length of the shortest path + 1 step for going through the portal.
    We keep the +1 on the length, as it simplifies the computation of the whole length of path in part 2.

    Of course, most (and probably all) inputs will generate non-connected graphs."""

    # First, construct the graph of the maze itself.
    Dots = nx.Graph()
    portal_positions = dict()
    for pos, cell in parsed.items():
        if cell == '.':
            for neigh in [left(pos), right(pos), up(pos), down(pos)]:
                if neigh in parsed:
                    Dots.add_edge(pos, neigh)
        else:
            portal_positions[pos] = cell

    # Now, construct the output graph
    Portals = nx.Graph()

    for p1, p1_name in portal_positions.items():
        for p2, p2_name in portal_positions.items():
            if p1 != p2:
                try:
                    path_length = len(shortest_path(Dots, p1, p2))
                    Portals.add_edge(p1_name, p2_name, weight=path_length)
                except nx.NetworkXNoPath:
                    pass
    return Portals


def reverse_portal_name(name):
    if '-outer' in name:
        return name[:2]+'-inner'
    else:
        return name[:2]+'-outer'


def recursive_maze_dijkstra(portals):
    """Take a graph of Node: portals, Edge: shortest_path_length,
    and go from AA-outer on lvl 0 to ZZ-outer on lvl 0.

    We use Dijkstra to find the shortest path: Nodes are (portals, recursion lvl)
    We use the portal name on the "output". i.e., we start at (AA-outer, 0),
    and if we choose to look at portal BC-inner, next node is (BC-outer, 1)."""

    explored = dict() # (portal, lvl): cumulated path length
    neighbors = {('AA-outer', 0): 0} # We start on AA-outer

    while neighbors:
        smallest_node, distance = min(neighbors.items(), key= lambda i:i[1])
        portal, lvl = smallest_node
        if portal == 'AA-inner':  # Actually not possible, discard the node.
            neighbors.pop(smallest_node)
            continue
        if portal == 'ZZ-inner':
            if lvl == -1:
                return distance # Shortest path!
            else: # Actually not possible, discard the node.
                neighbors.pop(smallest_node)
                continue
        if lvl == -1: #Actually not possible either.
            neighbors.pop(smallest_node)
            continue
        for new_portal in portals.neighbors(portal):
            new_lvl = lvl+1 if 'inner' in new_portal else lvl-1
            out_portal = reverse_portal_name(new_portal)
            new_node = (out_portal, new_lvl)
            new_distance = distance + portals.edges[(portal, new_portal)]['weight']
            if new_node not in explored:
                if new_node in neighbors:
                    neighbors[new_node] = min(neighbors[new_node], new_distance)
                else:
                    neighbors[new_node] = new_distance
        explored[smallest_node] = distance
        neighbors.pop(smallest_node)


def part_one(inp):
    first_pass = DictMap(inp)
    parsed = parse_portals(first_pass)
    G, start, end = _to_donut(parsed)
    return len(shortest_path(G, start, end)) - 1


def part_two(inp):
    first_pass = DictMap(inp)
    parsed = parse_portals(first_pass)
    portals = _precompute_single_level_paths(parsed)
    return recursive_maze_dijkstra(portals) - 1


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read()
    print("Answer for part one is : {res}".format(res=part_one(inp)))
    print("Answer for part two is : {res}".format(res=part_two(inp)))
