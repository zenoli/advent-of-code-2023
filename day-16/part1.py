import numpy as np

Position = tuple[int, int]
Direction = Position

UP: Direction = (-1, 0)
DOWN: Direction = (1, 0)
LEFT: Direction = (0, -1)
RIGHT: Direction = (0, 1)


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def read_input(filename):
    with open(filename) as file:
        lines = [line.rstrip() for line in file]
    return lines


def mirror_slash(x, y):
    return -y, -x


def mirror_backslash(x, y):
    return y, x


def debug(grid, seen):
    def formatter(x):
        if x == UP:
            return ""
        if x == DOWN:
            return ""
        if x == LEFT:
            return ""
        if x == RIGHT:
            return ""
        return " "

    for grid_row, seen_row in zip(grid, seen):
        print(
            " ".join(grid_row)
            + "  "
            + np.array2string(seen_row, formatter={"all": formatter})
        )
    print("=============================================")


def main():
    lines = read_input("sample.txt")
    # lines = read_input("input.txt")
    grid = np.array(list(map(list, lines)))
    seen = np.full(grid.shape, None)

    pos: Position = (0, 0)
    beams: list[tuple[Position, Direction]] = [(pos, RIGHT)]

    seen[pos] = True

    while beams:
        pos, direction = beams.pop()
        if seen[pos] == direction:
            continue

        seen[pos] = direction
        debug(grid, seen)
        next_pos = add(pos, direction)
        if next_pos[0] not in range(len(grid)) or next_pos[1] not in range(
            len(grid[0])
        ):
            continue

        if grid[next_pos] == "|" and direction in {LEFT, RIGHT}:
            beams.append((next_pos, UP))
            beams.append((next_pos, DOWN))
        elif grid[next_pos] == "-" and direction in {UP, DOWN}:
            beams.append((next_pos, LEFT))
            beams.append((next_pos, RIGHT))
        elif grid[next_pos] == "/":
            beams.append((next_pos, mirror_slash(*direction)))
        elif grid[next_pos] == "\\":
            beams.append((next_pos, mirror_backslash(*direction)))
        else:
            beams.append((next_pos, direction))

    print(np.count_nonzero(seen))


if __name__ == "__main__":
    main()
