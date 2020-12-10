import pytest
from day10 import *


test1 = "16\n10\n15\n5\n1\n11\n7\n19\n6\n12\n4"
test2 = "28\n33\n18\n42\n31\n14\n46\n20\n48\n47\n24\n23\n49\n45\n19\n38\n39\n11\n1\n32\n25\n35\n8\n17\n7\n9\n4\n2\n34\n10\n3"


@pytest.mark.parametrize("inp, exp", [
    (test1, 35),
    (test2, 220),
])
def test_one(inp, exp):
    res = part_one(inp)
    assert res == exp


@pytest.mark.parametrize("inp, exp", [
    (1, 1),
    (2, 2),
    (3, 4),
    (4, 7),
    (5, 13),
])
def test_tribo(inp, exp):
    res = tribonacci(inp)
    assert res == exp


@pytest.mark.parametrize("inp, exp", [
    (test1, 8),
    (test2, 19208),
])
def test_two(inp, exp):
    res = part_two(inp)
    assert res == exp

