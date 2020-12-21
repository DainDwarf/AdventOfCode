import re
import pytest
from day19 import *



@pytest.mark.parametrize("inp, exp", [
    ("ababbb", True),
    ("bababa", False),
    ("abbbab", True),
    ("aaabbb", False),
    ("aaaabbb", False),
])
def test_rule0(inp, exp):
    book = Rulebook()
    book.add_rule(Rule.from_desc('0: 4 1 5'))
    book.add_rule(Rule.from_desc('1: 2 3 | 3 2'))
    book.add_rule(Rule.from_desc('2: 4 4 | 5 5'))
    book.add_rule(Rule.from_desc('3: 4 5 | 5 4'))
    book.add_rule(Rule.from_desc('4: "a"'))
    book.add_rule(Rule.from_desc('5: "b"'))

    while not book.final:
        book.simplify()

    rule0 = re.compile(book.rules[0].final_string)

    assert bool(rule0.fullmatch(inp)) is exp



inp = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb"""


def test_one():
    res = part_one(inp)
    assert res == 2


@pytest.mark.parametrize("inp, exp", [
])
def test_two(inp, exp):
    res = part_two(inp)
    assert res == exp

