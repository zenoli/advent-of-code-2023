import math
import time
from collections import Counter, defaultdict
from itertools import chain, pairwise
from operator import itemgetter

import numpy as np

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

        n, m = grid.shape
        steps = 3
        while grid[pos] not in [">", "v"] and pos != (n - 2, m - 2):
            pos, direction = compute_next_direction(grid, pos, direction)
            steps += 1

        return compute_next_direction(grid, pos, direction)[0], steps

    paths = []
    for d in (DOWN, RIGHT):
        pos = add(start, d)
        if on_grid(grid, pos) and grid[pos] != "#":
            paths.append(compute_path(grid, pos, d))

    return paths


def compute_in_degrees(graph):
    return Counter(map(itemgetter(0), chain(*graph.values())))


def is_cyclic(graph):
    in_degrees = compute_in_degrees(graph)
    Q = set(v for v in graph if in_degrees[v] == 0)
    while Q:
        v = Q.pop()
        for u, _ in graph[v]:
            in_degrees[u] -= 1
            if in_degrees[u] == 0:
                Q.add(u)
    return set(in_degrees.values()) != {0}


def topological_sort(dag):
    in_degrees = compute_in_degrees(dag)
    Q = set(v for v in dag if in_degrees[v] == 0)
    while Q:
        v = Q.pop()
        yield v
        for u, _ in dag[v]:
            in_degrees[u] -= 1
            if in_degrees[u] == 0:
                Q.add(u)
    return set(in_degrees.values()) != {0}


def get_inverted_edges(graph):
    inverted = defaultdict(list)
    for v, neighbors in graph.items():
        for u, length in neighbors:
            inverted[u].append((v, length))
    return inverted


def to_undirected(graph):
    inverted = get_inverted_edges(graph)
    for v, edges in inverted.items():
        graph[v].extend(edges)
    return graph


def compute_longest_path(graph, node, dst, current_path):
    current_path.add(node)
    if node == dst:
        return 0

    paths = [
        compute_longest_path(graph, neighbor, dst, current_path.copy()) + weight
        for neighbor, weight in graph[node]
        if neighbor not in current_path
    ]
    return max(paths) if paths else -math.inf


def to_graphviz_format(graph):
    def vertex(v):
        return f'"{v}"'

    print("strict digraph {")
    for v, edges in graph.items():
        for u, w in edges:
            print(f"{vertex(v)} -> {vertex(u)} [label={w}]")
            # print(f"{vertex(v)} -> {vertex(u)}")
    print("}")


def solve(input):
    def debug(grid):
        for line in grid:
            print("".join(map(str, line)))

    # np.set_printoptions(linewidth=120)
    grid = read_input(input)
    vertices = find_vertices(grid)
    graph = {vertex: compute_paths(grid, vertex) for vertex in vertices}

    graph = to_undirected(graph)

    for v, edges in graph.items():
        print(f"{v} -> {edges}")

    # to_graphviz_format(graph)

    n, m = grid.shape
    start = time.time()
    longest_path = compute_longest_path(graph, (0, 1), (n - 1, m - 2), set())
    end = time.time()
    print(f"Time elapsed: {end - start}")
    return longest_path


def main():
    # res = solve("sample.txt")
    res = solve("input.txt")
    print(res)


if __name__ == "__main__":
    main()
