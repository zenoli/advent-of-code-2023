import operator
import numpy as np
from numpy.core.multiarray import array


BELOW = np.array([1, 0])
ABOVE = np.array([-1, 0])
LEFT = np.array([0, -1])
RIGHT = np.array([0, 1])


pipes = {
    "L": (ABOVE, RIGHT),
    "7": (LEFT, BELOW),
    "F": (RIGHT, BELOW),
    "J": (ABOVE, LEFT),
    "|": (ABOVE, BELOW),
    "-": (LEFT, RIGHT),
}


def read_input(filename):
    with open(filename) as file:
        lines = [line.rstrip() for line in file]
    return lines


def sub(p1, p2):
    return tuple(x1 - x2 for x1, x2 in zip(p1, p2))


def add(p1, p2):
    return tuple(x1 + x2 for x1, x2 in zip(p1, p2))


def move(current_pos, prev_pos, pipe):
    direction = prev_pos - current_pos
    next_direction = (pipes[pipe][all(pipes[pipe][0] == direction)])
    next_pos = current_pos + next_direction

    return next_pos, next_direction * -1


def solve(lines):
    pass


def main():
    lines = read_input("sample1.txt")
    # lines = read_input("input.txt")
    for line in lines:
        print(line)
    solve(lines)


if __name__ == "__main__":
    print(sub((1, 2), (3, 4)))
    main()
