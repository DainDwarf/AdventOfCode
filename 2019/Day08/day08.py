import pytest


@pytest.mark.parametrize("inp, exp", [
    ("0222112222120000", " X\nX "),
])
def testTwo(inp, exp):
    res = partTwo(inp, width=2, length=2)
    print(f"Test {inp} gives {res}")
    assert res == exp


def partOne(inp, width=25, length=6):
    layer_size = width * length
    layers = [inp[i:i+layer_size] for i in range(0, len(inp), layer_size)]
    min_count_0 = min(l.count('0') for l in layers)
    min0 = [l for l in layers if l.count('0') == min_count_0][0]
    return min0.count('1')*min0.count('2')


def partTwo(inp, width=25, length=6):
    layer_size = width * length
    layers = [inp[i:i+layer_size] for i in range(0, len(inp), layer_size)]
    image = [None]*layer_size
    for l in layers:
        for p in range(layer_size):
            if image[p] is None and l[p] != '2':
                image[p] = ' ' if l[p] == '0' else 'X'
    image_rows = [''.join(image[i:i+width]) for i in range(0, layer_size, width)]
    return '\n'.join(image_rows)


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=partOne(inp)))
    print("Answer for part two is :\n{res}".format(res=partTwo(inp)))
