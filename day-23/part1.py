from heapq import heappop, heappush
import numpy as np


Position = tuple[int, int]
Direction = Position

UP: Direction = (-1, 0)
DOWN: Direction = (1, 0)
LEFT: Direction = (0, -1)
RIGHT: Direction = (0, 1)


def read_input(filename):
    with open(filename) as file:
        lines = [list(line.strip()) for line in file]
    return np.array(lines)


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


def solve(input):
    def debug(grid):
        for line in grid:
            print("".join(map(str, line)))

    grid = read_input(input)

    dijkstra = Dijkstra(grid)
    shortest_paths = dijkstra.solve((0, 1))
    np.set_printoptions(linewidth=120)
    shortest_paths[shortest_paths == shortest_paths.size] = -1
    print(shortest_paths)

    return 0


def main():
    res = solve("sample.txt")
    print(res)


if __name__ == "__main__":
    main()
