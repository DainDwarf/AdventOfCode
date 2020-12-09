#!/usr/bin/python3


def compute_validation_sets(inp, preamble=25):
    valid_sum = [set() for i in range(len(inp))]
    for index, num in enumerate(inp[:-preamble]):
        for forward_index, forward_scan in enumerate(inp[index+1:index+preamble], start=index+1):
            if num != forward_scan:
                for validation_index in range(forward_index+1, index+preamble+1):
                    valid_sum[validation_index].add(num+forward_scan)
    return valid_sum


def part_one(inp, preamble=25):
    inp = list(map(int, inp.split('\n')))
    valid_sum = compute_validation_sets(inp, preamble)
    for x, s in zip(inp[preamble:], valid_sum[preamble:]):
        if x not in s:
            return x


def part_two(inp, preamble=25):
    target = part_one(inp, preamble)
    inp = list(map(int, inp.split('\n')))

    current_sum = 0
    low_index = high_index = 0
    while low_index < len(inp):
        if current_sum == target:
            contiguous_set = inp[low_index:high_index]
            return min(contiguous_set)+max(contiguous_set)
        elif current_sum > target:
            current_sum -= inp[low_index]
            low_index +=1
        elif current_sum < target:
            current_sum += inp[high_index]
            high_index += 1


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=part_one(inp)))
    print("Answer for part two is : {res}".format(res=part_two(inp)))
