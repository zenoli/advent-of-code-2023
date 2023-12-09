import re
from itertools import pairwise


def parse_numbers(line):
    return list(map(int, re.findall(r"-?\d+", line)))


def read_input(filename):
    with open(filename) as file:
        lines = [line.rstrip() for line in file]
    return lines


def diff(sequence):
    return [y - x for x, y in pairwise(sequence)]


def compute_next(sequence):
    if not any(sequence):
        return 0
    return sequence[-1] + compute_next(diff(sequence))


def compute_prev(sequence):
    if not any(sequence):
        return 0
    return sequence[0] - compute_prev(diff(sequence))


def solve(lines):
    # print(sum(map(compute_next, map(parse_numbers, lines))))
    print(sum(map(compute_prev, map(parse_numbers, lines))))


def main():
    # lines = read_input("sample.txt")
    lines = read_input("input.txt")
    solve(lines)


if __name__ == "__main__":
    main()
