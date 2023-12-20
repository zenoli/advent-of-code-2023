from typing import Tuple
import numpy as np
import math

Position = tuple[int, int]
Direction = Position

UP: Direction = (-1, 0)
DOWN: Direction = (1, 0)
LEFT: Direction = (0, -1)
RIGHT: Direction = (0, 1)

directions: list[Direction] = [UP, DOWN, LEFT, RIGHT]

arrow_symbols = {UP: "", DOWN: "", LEFT: "", RIGHT: ""}


def add(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return a[0] + b[0], a[1] + b[1]


def sub(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return a[0] - b[0], a[1] - b[1]


def read_input(filename):
    with open(filename) as file:
        lines = [list(map(int, line.strip())) for line in file]
    return np.array(lines)


def on_grid(pos, N, M):
    return pos[0] in range(N) and pos[1] in range(M)


def main():
    # lines = read_input("input.txt")
    grid = read_input("sample.txt")
    distances = np.full(grid.shape, math.inf)
    visited = np.full(grid.shape, False)

    distances[0, 0] = 0

    N, M = grid.shape
    arrows = np.array([set() for _ in range(N * M)]).reshape(N, M)
    arrows[0, 0].add(UP)

    queue: list[Position] = [(0, 0)]

    while not visited[-1, -1]:
        pos = queue.pop(0)
        if visited[pos]:
            continue
        visited[pos] = True

        for direction in directions:
            neighbor = add(pos, direction)
            if not on_grid(neighbor, N, M):
                continue
            if not visited[neighbor]:
                queue.append(neighbor)
            new_dist = distances[pos] + grid[neighbor]

            distances[neighbor] = min(distances[neighbor], new_dist)

    print(distances)



if __name__ == "__main__":
    main()
