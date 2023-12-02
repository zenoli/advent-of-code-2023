from collections.abc import Iterable
from functools import reduce
import math
from typing import Tuple

colors = ["red", "green", "blue"]


def power(max_colors: dict[str, int]) -> int:
    return math.prod(max_colors.values())


def get(key: str, d: dict[str, int]) -> int:
    return d[key] if key in d else 0


def read_input(filename: str) -> Iterable[str]:
    with open(filename) as file:
        return (line.rstrip() for line in file)


def max_reducer(grab1: dict[str, int], grab2: dict[str, int]) -> dict[str, int]:
    return {color: max(get(color, grab1), get(color, grab2)) for color in colors}


def compute_max_colors(grabs: Iterable[dict[str, int]]) -> dict[str, int]:
    return reduce(max_reducer, grabs)


def parse_line(line: str) -> Iterable[dict[str, int]]:
    _, set_string = line.split(": ")
    return map(parse_set_string, set_string.split("; "))


def parse_set_string(set_string: str) -> dict[str, int]:
    entries = set_string.split(", ")
    return dict(map(parse_entry, entries))


def parse_entry(entry: str) -> Tuple[str, int]:
    count, color = entry.split(" ")
    return color, int(count)


def parse_id(id_string: str) -> int:
    return int(id_string.split(" ")[1])


def solve_line(line: str) -> int:
    grabs = parse_line(line)
    return power(compute_max_colors(grabs))


def solve(lines: Iterable[str]) -> int:
    return sum(map(solve_line, lines))


def main():
    lines = read_input("input.txt")
    # lines = read_input("sample-part2.txt")
    print(solve(lines))


if __name__ == "__main__":
    main()
