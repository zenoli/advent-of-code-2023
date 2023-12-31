import numpy as np
from heapq import heappop, heappush
from itertools import product


type Position = tuple[int, int]
type Direction = Position

UP: Direction = (-1, 0)
DOWN: Direction = (1, 0)
LEFT: Direction = (0, -1)
RIGHT: Direction = (0, 1)


def read_input(filename):
    with open(filename) as file:
        lines = [list(line.strip()) for line in file]
    return np.array(lines)


def get_dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


class Part1:
    def __init__(self, input) -> None:
        self.grid = read_input(input)
        self.corner_grid = self.generate_corner_grid(self.grid)
        # np.savetxt("out/corner-grid.txt", self.corner_grid, fmt="%s", delimiter="")

    def on_grid(self, pos) -> bool:
        return (
            all(map(lambda x: x >= 0, pos))
            and pos[0] < self.grid.shape[0]
            and pos[1] < self.grid.shape[1]
        )

    def get_neighbors(self, pos, grid):
        directions = np.array([UP, DOWN, LEFT, RIGHT])
        neighbors = (tuple(n) for n in pos + directions)
        return (n for n in neighbors if self.on_grid(n) and grid[n] != "#")

    def get_start(self):
        return tuple(np.argwhere(self.grid == "S")[0])

    def generate_corner_grid(self, grid):
        corner_grid = np.full(grid.shape, ".")
        corner_grid[1:65, 1:65] = grid[66:-1, 66:-1]
        corner_grid[1:65, 66:-1] = grid[66:-1, 1:65]
        corner_grid[66:-1, 1:65] = grid[1:65, 66:-1]
        corner_grid[66:-1, 66:-1] = grid[1:65, 1:65]
        return corner_grid

    def dijkstra(self, start, grid):
        queue = []

        shortest_paths = np.full(grid.shape, grid.size)
        visited = np.full(grid.shape, False)
        shortest_paths[start] = 0
        heappush(queue, (shortest_paths[start], start))
        while queue:
            _, pos = heappop(queue)
            if visited[pos]:
                continue
            visited[pos] = True

            for neighbor in self.get_neighbors(pos, grid):
                shortest_paths[neighbor] = min(
                    int(shortest_paths[pos] + 1),
                    int(shortest_paths[neighbor]),
                )
                if not visited[neighbor]:
                    heappush(queue, (shortest_paths[neighbor], neighbor))
        return shortest_paths

    def compute_reachable_plots(self, start, steps, even, use_corner_grid=False):
        def checkerboard(even):
            return np.indices(self.grid.shape).sum(axis=0) % 2 == (0 if even else 1)

        shortest_paths = self.dijkstra(
            start, self.grid if not use_corner_grid else self.corner_grid
        )

        reachable = np.count_nonzero((shortest_paths <= steps) & checkerboard(even))
        unreachable = np.count_nonzero(
            (shortest_paths > steps)
            & checkerboard(even)
            & (shortest_paths != self.grid.size)
        )
        return reachable, unreachable

    def solve(self, steps):
        start = self.get_start()
        N, M = self.grid.shape
        shortest_paths = self.dijkstra(start, self.grid)
        max_steps_64 = 0
        for i, j in product(range(N), range(M)):
            if get_dist((i, j), start) <= 65 and shortest_paths[i, j] != self.grid.size:
                max_steps_64 = max(max_steps_64, shortest_paths[i, j])

        return np.count_nonzero((shortest_paths <= steps) * (shortest_paths % 2 == 0))


def main():
    pt1 = Part1("input.txt")
    parity = False
    # arrow_right_corners, unreachable_arrow_right_corners = sum(
    #     pt1.compute_reachable_plots(start, steps, even=parity)
    #     for start, steps in [((0, 130), 64), ((130, 130), 64)]
    # )
    # arrow_right, arrow_right_neg = pt1.compute_reachable_plots((65, 0), 130, even=parity)
    # arrow_left, arrow_left_neg = pt1.compute_reachable_plots((65, 130), 130, even=parity)
    # arrow_up, arrow_up_neg = pt1.compute_reachable_plots((130, 65), 130, even=parity)
    # arrow_down, arrow_down_neg = pt1.compute_reachable_plots((0, 65), 130, even=parity)
    full_block_odd, _ = pt1.compute_reachable_plots((65, 65), 130, even=False)
    _, corners_odd = pt1.compute_reachable_plots(
        (65, 65), 65, even=False, use_corner_grid=False
    )
    full_block_even, _ = pt1.compute_reachable_plots((65, 65), 130, even=True)
    _, corners_even = pt1.compute_reachable_plots(
        (65, 65), 65, even=True, use_corner_grid=False
    )
    n = (26501365 - 65) // 131
    print(
        (n + 1) * (n + 1) * full_block_odd
        - (n + 1) * corners_odd
        + n * n * full_block_even
        + n * corners_even
    )

    # print("Arrows", sum([arrow_right, arrow_left, arrow_up, arrow_down]))
    # print("4 full blocks minus corners", 4 * full_block - 2 * corners)

    # parity = True
    # top_left, arrow_right_neg = pt1.compute_reachable_plots((0, 0), 64, even=parity)
    # top_right, arrow_left_neg = pt1.compute_reachable_plots((0, 130), 64, even=parity)
    # bottom_left, arrow_up_neg = pt1.compute_reachable_plots((130, 0), 64, even=parity)
    # bottom_right, arrow_down_neg = pt1.compute_reachable_plots((130, 130), 64, even=parity)
    # inv_corners, _ = pt1.compute_reachable_plots((65, 65), 65, even=parity, use_corner_grid=True)
    #
    # print("Four corners", sum([top_left, top_right, bottom_left, bottom_right]))
    # print("Inv corners", inv_corners)


if __name__ == "__main__":
    main()
