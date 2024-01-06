from collections import defaultdict
from heapq import heappop, heappush
from itertools import pairwise
import numpy as np
from operator import itemgetter


Position = tuple[int, int]
Direction = Position

UP: Direction = (-1, 0)
DOWN: Direction = (1, 0)
LEFT: Direction = (0, -1)
RIGHT: Direction = (0, 1)


directions = {"^": UP, "v": DOWN, ">": LEFT, "<": RIGHT}


def add(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(map(sum, zip(a, b)))


def rot_right(direction: Direction) -> Direction:
    x, y = direction
    return y, -x


def rot_left(direction: Direction) -> Direction:
    x, y = direction
    return -y, x


def read_input(filename):
    with open(filename) as file:
        lines = [list(line.strip()) for line in file]
    return np.array(lines)


def on_grid(grid, pos) -> bool:
    return (
        all(map(lambda x: x >= 0, pos))
        and pos[0] < grid.shape[0]
        and pos[1] < grid.shape[1]
    )


class Dijkstra:
    def __init__(self, grid) -> None:
        self.grid = grid

    def on_grid(self, pos) -> bool:
        return (
            all(map(lambda x: x >= 0, pos))
            and pos[0] < self.grid.shape[0]
            and pos[1] < self.grid.shape[1]
        )

    def get_neighbors(self, pos):
        directions = np.array([UP, DOWN, LEFT, RIGHT])
        neighbors = (tuple(n) for n in pos + directions)
        return (n for n in neighbors if self.on_grid(n) and self.grid[n] != "#")

    def solve(self, start):
        queue = []

        shortest_paths = np.full(self.grid.shape, self.grid.size)
        visited = np.full(self.grid.shape, False)
        shortest_paths[start] = 0
        heappush(queue, (shortest_paths[start], start))
        while queue:
            _, pos = heappop(queue)
            if visited[pos]:
                continue
            visited[pos] = True

            for neighbor in self.get_neighbors(pos):
                shortest_paths[neighbor] = min(
                    int(shortest_paths[pos] + 1),
                    int(shortest_paths[neighbor]),
                )
                if not visited[neighbor]:
                    heappush(queue, (shortest_paths[neighbor], neighbor))
        return shortest_paths


def find_vertices(grid):
    left_arrow_indices = zip(*np.where(grid == ">"))
    down_arrow_indices = zip(*np.where(grid == "v"))

    n, m = grid.shape

    set1 = set(
        (x1, y1 + 1)
        for (x1, y1), (x2, y2) in pairwise(
            sorted(left_arrow_indices, key=itemgetter(0))
        )
        if (x1 == x2 and abs(y2 - y1) == 2)
    )
    set2 = set(
        (x1 + 1, y1)
        for (x1, y1), (x2, y2) in pairwise(
            sorted(down_arrow_indices, key=itemgetter(1))
        )
        if (y1 == y2 and abs(x2 - x1) == 2)
    )

    return set1.union(set2).union({(0, 1), (n - 1, m - 2)})


def compute_paths(grid, start):
    paths = []
    for d in (DOWN, RIGHT):
        pos = add(start, d)
        if on_grid(grid, pos) and grid[pos] != "#":
            paths.append(compute_path(grid, pos, d))

    return paths


def compute_path(grid, start, direction):
    def compute_next_direction(
        grid, curr_pos: Position, curr_dir: Direction
    ) -> tuple[Position, Direction]:  # type: ignore
        for next_dir in (curr_dir, rot_left(curr_dir), rot_right(curr_dir)):
            next_pos = add(curr_pos, next_dir)
            if on_grid(grid, next_pos) and grid[next_pos] != "#":
                return next_pos, next_dir  # type: ignore
        return curr_dir, curr_pos

    pos, direction = compute_next_direction(grid, start, direction)

    steps = 3
    while grid[pos] not in [">", "v"]:
        pos, direction = compute_next_direction(grid, pos, direction)
        steps += 1

    return compute_next_direction(grid, pos, direction)[0], steps


def solve(input):
    def debug(grid):
        for line in grid:
            print("".join(map(str, line)))

    grid = read_input(input)
    grid[-2, -2] = "v"

    # dijkstra = Dijkstra(grid)
    # shortest_paths = dijkstra.solve((0, 1))
    np.set_printoptions(linewidth=120)
    # shortest_paths[shortest_paths == shortest_paths.size] = -1
    # print(shortest_paths)
    # debug(grid)
    vertices = find_vertices(grid)
    graph = {vertex: compute_paths(grid, vertex) for vertex in vertices}

    for k, v in graph.items():
        print(k, v)

    return 0


def main():
    res = solve("sample.txt")
    print(res)


if __name__ == "__main__":
    main()
