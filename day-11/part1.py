import numpy as np


def read_input(filename):
    with open(filename) as file:
        lines = [line.rstrip() for line in file]
    return lines


def debug(universe):
    universe_pretty = np.empty_like(universe)
    universe_pretty = np.full(universe.shape, " ")
    universe_pretty[universe] = "#"
    print(universe_pretty)


def expand(universe_raw):
    def empty_rows(universe):
        return [i for i, row in enumerate(universe) if not any(row)]

    def empty_cols(universe):
        return [i for i, row in enumerate(universe.T) if not any(row)]

    universe = np.insert(universe_raw, empty_cols(universe_raw), False, axis=1)
    return np.insert(universe, empty_rows(universe_raw), False, axis=0)


def main():
    lines = read_input("sample.txt")
    # lines = read_input("input.txt")

    universe_raw = np.array(list(map(list, lines))) == "#"
    universe = expand(universe_raw)
    debug(universe_raw)
    debug(universe)


if __name__ == "__main__":
    main()
