#!/usr/bin/python3
import re

import networkx as nx

def parse_to_graph(inp):
    _line_re = re.compile(r"(.*) bags contain (.*)\.")
    _bags_re = re.compile(r"(\d+) (.*) bags?")
    G = nx.DiGraph()

    for line in inp.split('\n'):
        container, content = _line_re.match(line).groups()
        content = content.split(', ')
        for bag in content:
            if match := _bags_re.match(bag):
                num, color = match.groups()
                G.add_edge(container, color, weight=int(num))
    return G


def compute_full_weight(G):
    """
    Compute on each node the full_weight, defined as:
        * 1 if the bag contains nothing (it weights itself)
        * 1+ the sum of the bags it contains : Their full_weight, times how many there are.
    """

    for node in reversed(list(nx.topological_sort(G))):
        G.nodes[node]['full_weight'] = 1 + sum([
            G.nodes[succ]['full_weight']*edge['weight']
            for succ, edge in G[node].items()
        ])


def part_one(inp):
    G = parse_to_graph(inp)
    return len(nx.ancestors(G, 'shiny gold'))


def part_two(inp):
    G = parse_to_graph(inp)
    compute_full_weight(G)
    return G.nodes['shiny gold']['full_weight'] - 1 # Removing the weight of the shiny gold bag itself.


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=part_one(inp)))
    print("Answer for part two is : {res}".format(res=part_two(inp)))
