from typing import Mapping
from functools import reduce
from itertools import pairwise, batched
from collections import defaultdict
import numpy as np


Position = tuple[int, int]
Direction = Position

UP: Direction = (-1, 0)
DOWN: Direction = (1, 0)
LEFT: Direction = (0, -1)
RIGHT: Direction = (0, 1)

directions: Mapping[str, Direction] = {"U": UP, "D": DOWN, "L": LEFT, "R": RIGHT}


def add(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(map(sum, zip(a, b)))


def mul(a: tuple[int, ...], factor: int) -> tuple[int, ...]:
    return tuple(map(lambda x: x * factor, a))


def sub(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return add(a, mul(b, -1))


def read_input(filename):
    def parse(line):
        dir, steps, color = line.split()
        return directions[dir], int(steps), color[1:-1]

    with open(filename) as file:
        return list(map(parse, file))


def get_coords(instructions):
    def coord_reducer(coords, instruction):
        dir, steps, _ = instruction
        return coords + [add(coords[-1], mul(dir, steps))]

    return reduce(coord_reducer, instructions, [(0, 0)])


def shift_coords(coords):
    res = np.array(coords)
    return res - np.min(res, axis=0)


def draw(coords):
    grid = np.full(np.max(coords, axis=0) + 1, ".")
    for (x1, y1), (x2, y2) in pairwise(coords):
        grid[min(x1, x2) : max(x1, x2) + 1, min(y1, y2) : max(y1, y2) + 1] = "#"
    return grid


def get_scan_points(coords):
    return set(coords[:, 1])


def get_horizontal_intervals(coords):
    d = defaultdict(list)
    intervals = (
        (x, range(min(y1, y2), max(y1, y2)))
        for (x, y1), (_, y2) in pairwise(coords)
        if y1 != y2
    )

    for x, interval in intervals:
        d[x].append(interval)
    return dict(sorted(d.items()))


def get_intervals(point, intervals):
    return (
        x for x, ranges in intervals.items() if not all(point not in r for r in ranges)
    )


def calculate_slice(xs):
    return sum(len(range(*b)) for b in batched(xs, 2))


def calculate_pit_size(scan_points, intervals):
    for start, end in pairwise(scan_points):
        xs = get_intervals(start, intervals)


def main():
    instructions = read_input("sample.txt")
    # instructions = read_input("input.txt")

    coords = get_coords(instructions)
    coords = shift_coords(coords)
    grid = draw(coords)
    print(grid)

    scan_points = get_scan_points(coords)
    intervals = get_horizontal_intervals(coords)
    pit_size = calculate_pit_size(scan_points, intervals)

    print(pit_size)


if __name__ == "__main__":
    main()
