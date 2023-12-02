from functools import reduce
import math

colors = ["red", "green", "blue"]


def power(max_colors):
    return math.prod(max_colors.values())


def get(key, d):
    return d[key] if key in d else 0


def read_input(filename):
    with open(filename) as file:
        lines = [line.rstrip() for line in file]
    return lines


def max_reducer(dict1, dict2):
    return {color: max(get(color, dict1), get(color, dict2)) for color in colors}


def compute_max_colors(grabs):
    return reduce(max_reducer, grabs)


def parse_line(line):
    _, set_string = line.split(": ")
    return map(parse_set_string, set_string.split("; "))


def parse_set_string(set_string):
    entries = set_string.split(", ")
    return dict(map(parse_entry, entries))


def parse_entry(entry):
    count, color = entry.split(" ")
    return color, int(count)


def parse_id(id_string):
    return int(id_string.split(" ")[1])


def solve_line(line):
    grabs = parse_line(line)
    return power(compute_max_colors(grabs))


def solve(lines):
    return sum(map(solve_line, lines))


def main():
    lines = read_input("input.txt")
    # lines = read_input("sample-part2.txt")
    print(solve(lines))


if __name__ == "__main__":
    main()
