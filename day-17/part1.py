from typing import Mapping, Tuple
import numpy as np
import math

Position = tuple[int, int]
Direction = Position

UP: Direction = (-1, 0)
DOWN: Direction = (1, 0)
LEFT: Direction = (0, -1)
RIGHT: Direction = (0, 1)

directions: Mapping[Direction, int] = {UP: 0, DOWN: 1, LEFT: 2, RIGHT: 3}

arrow_symbols = {UP: "", DOWN: "", LEFT: "", RIGHT: ""}


def add(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return a[0] + b[0], a[1] + b[1]


def sub(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return a[0] - b[0], a[1] - b[1]


def rot_right(direction):
    x, y = direction
    return y, -x


def rot_left(direction):
    x, y = direction
    return -y, x


def read_input(filename):
    with open(filename) as file:
        lines = [list(map(int, line.strip())) for line in file]
    return np.array(lines)


def on_grid(pos, N, M):
    return pos[0] in range(N) and pos[1] in range(M)


def get_neighbors(pos, d, c, N, M):
    neighbors = [(add(pos, new_d), new_d, 1) for new_d in [rot_right(d), rot_left(d)]]
    if c + 1 <= 3:
        neighbors.append((add(pos, d), d, c + 1))
    return [n for n in neighbors if on_grid(n[0], N, M)]


def pop_next(queue, distances):
    min_index = -1
    min_dist = math.inf
    for i, (pos, d, c) in enumerate(queue):
        pos_index = (*pos, directions[d], c)
        if distances[pos_index] < min_dist:
            min_index = i
            min_dist = distances[pos_index]
    return queue.pop(min_index)


def main():
    # grid = read_input("input.txt")
    # grid = read_input("sample.txt")[:6,:12]
    grid = read_input("sample.txt")
    # grid = read_input("sample2.txt")
    distances = np.full((*grid.shape, 4, 4), np.iinfo(np.int32).max)
    visited = np.full((*grid.shape, 4, 4), False)

    distances[0, 0, :, :] = 0

    N, M = grid.shape

    queue: list[tuple[Position, Direction, int]] = [
        ((0, 0), RIGHT, 0),
        ((0, 0), DOWN, 0),
    ]

    while queue:
        # pos, d, c = queue.pop(0)
        pos, d, c = pop_next(queue, distances)

        pos_index = (*pos, directions[d], c)
        if visited[pos_index]:
            continue
        visited[pos_index] = True

        for new_pos, new_d, new_c in get_neighbors(pos, d, c, N, M):
            new_pos_index = (*new_pos, directions[new_d], new_c)
            if not visited[new_pos_index]:
                queue.append((new_pos, new_d, new_c))
            new_dist = distances[pos_index] + grid[new_pos]
            distances[new_pos_index] = min(distances[new_pos_index], new_dist)

    print(distances[-1, -1, :, 1:].min())


if __name__ == "__main__":
    main()
