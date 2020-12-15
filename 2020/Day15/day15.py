#!/usr/bin/python3


def algo1(inp, size):
    nums = list(map(int, inp.split(',')))
    while len(nums) < size:
        try: # Magic formula!
            nums.append(nums[-2::-1].index(nums[-1])+1)
        except ValueError:
            nums.append(0)
    return nums[-1]


def algo2(inp, size):
    # assert no duplicate in input.
    nums = {int(n):i+1 for i, n in enumerate(inp.split(','))}
    new_num = 0
    for i in range(len(nums)+1, size):
        try:
            tmp = nums[new_num]
            nums[new_num] = i
            new_num = i - tmp
        except KeyError:
            nums[new_num] = i
            new_num = 0
    return new_num


def part_one(inp):
    return algo2(inp, 2020)


def part_two(inp):
    return algo2(inp, 30000000)


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=part_one(inp)))
    print("Answer for part two is : {res}".format(res=part_two(inp)))
