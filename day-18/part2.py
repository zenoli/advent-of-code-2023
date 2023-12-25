from typing import Mapping
from functools import reduce
from itertools import pairwise, batched
from collections import defaultdict
import numpy as np
import math


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


def closed(r):
    return range(r[0], r[-1] + 2)


def shrink(r):
    return range(r[1], r[-1])


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
        (x, closed(range(min(y1, y2), max(y1, y2))))
        for (x, y1), (_, y2) in pairwise(coords)
        if y1 != y2
    )

    for x, interval in intervals:
        d[x].append(interval)
    return dict(sorted(d.items()))


def get_vertical_intervals(coords):
    return sum(
        max(x1, x2) - min(x1, x2) + 1
        for (x1, _), (x2, _) in pairwise(coords)
        if x1 != x2
    )


def get_intervals(point, intervals):
    return (
        x for x, ranges in intervals.items() if not all(point not in r for r in ranges)
    )


def get_intervals_plus(point, intervals):
    def get_range(point, ranges):
        for r in ranges:
            if point in r:
                return r
        return None

    tmp = [(x, r) for x, ranges in intervals.items() if (r := get_range(point, ranges))]
    return tmp


def calculate_slice(xs):
    return sum(len(range(*b)) + 1 for b in batched(xs, 2))


MAX_INT = 100000000000000000
MIN_INT = -MAX_INT


def calculate_slice_plus(point, intervals):
    slice = 0
    start = None
    direction = None
    opening_interval = None
    closing_interval = (MAX_INT, MIN_INT)
    for x, r in get_intervals_plus(point, intervals):
        r_start, r_end = r[0], r[-1]
        if opening_interval is None:
            opening_interval = (r_start, r_end)
            start = x
            continue

        # Case: <-->
        if opening_interval[0] < point and point < opening_interval[1]:
            closing_interval = (
                min(r_start, closing_interval[0]),
                max(r_end, closing_interval[1]),
            )

            if closing_interval[0] < point and point < closing_interval[1]:
                slice += (x - start) + 1
                opening_interval = None
                closing_interval = (MAX_INT, MIN_INT)
            continue

        if (
            point == opening_interval[0]
            and point == r_end
            or point == opening_interval[1]
            and point == r_start
        ):
            opening_interval = (
                min(r_start, opening_interval[0]),
                max(r_end, opening_interval[1]),
            )
            continue
        # Case: { <--, -->}
        if (
            point == opening_interval[0]
            and point == r_start
            or point == opening_interval[1]
            and point == r_end
            or r_start < point
            and point < r_end
        ):
            slice += (x - start) + 1
            opening_interval = None
            closing_interval = (MAX_INT, MIN_INT)

    return slice


def calculate_block(start, end, intervals):
    start += 1
    xs = get_intervals(start, intervals)
    slice_size = calculate_slice(xs)
    return slice_size * (end - start)


def calculate_pit_size(scan_points, intervals):
    result = sum(
        calculate_block(start, end, intervals) for start, end in pairwise(scan_points)
    )

    return result


def main():
    # instructions = read_input("sample8.txt")
    instructions = read_input("input.txt")

    coords = get_coords(instructions)
    coords = shift_coords(coords)
    grid = draw(coords)
    # print(grid)

    scan_points = get_scan_points(coords)
    intervals = get_horizontal_intervals(coords)
    # print(calculate_slice_plus(4, intervals))
    pit_size = calculate_pit_size(scan_points, intervals)
    N = np.max(np.array(coords), axis=0)[1] + 1
    # print(N)
    for point in scan_points:
        pit_size += calculate_slice_plus(point, intervals)
    # for point in scan_points:
    #     pit_size += calculate_slice_plus(point, intervals)
    # vertical_bars = get_vertical_intervals(coords)

    # col_counts = np.array(
    #     list(map(lambda point: calculate_slice_plus(point, intervals), range(N)))
    # )

    # np.savetxt(
    #     "out/col_counts_incorrect.txt",
    #     col_counts,
    #     fmt="%s",
    #     delimiter=",",
    # )

    # print(col_counts)
    # print(scan_points)
    # print(intervals)
    print(pit_size)


if __name__ == "__main__":
    main()
