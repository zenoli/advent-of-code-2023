from functools import reduce

constraints = {"red": 12, "green": 13, "blue": 14}


def get(key, d):
    return d[key] if key in d else 0


def validate(max_colors):
    return all(
        get(color, constraints) >= get(color, max_colors)
        for color in constraints.keys()
    )


def read_input(filename):
    with open(filename) as file:
        lines = [line.rstrip() for line in file]
    return lines


def max_reducer(dict1, dict2):
    return {
        color: max(get(color, dict1), get(color, dict2)) for color in constraints.keys()
    }


def parse_line(line):
    id_string, set_string = line.split(": ")
    id = parse_id(id_string)
    set_strings = set_string.split("; ")
    max_colors = reduce(max_reducer, map(parse_set_string, set_strings))
    return id, validate(max_colors)


def parse_set_string(set_string):
    entries = set_string.split(", ")
    return dict(map(parse_entry, entries))


def parse_entry(entry):
    count, color = entry.split(" ")
    return color, int(count)


def parse_id(id_string):
    return int(id_string.split(" ")[1])


def solve(lines):
    pass


def main():
    lines = read_input("input.txt")
    # lines = read_input("sample-part1.txt")
    print(
        sum(map(lambda x: x[0], list(filter(lambda x: x[1], map(parse_line, lines)))))
    )


if __name__ == "__main__":
    main()
