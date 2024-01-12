def read_input(filename):
    with open(filename) as file:
        lines = [line.strip() for line in file]

    return list(map(parse, lines))


def parse(line):
    def to_tuple(s):
        return tuple(map(int, s.split(",")))

    return tuple(map(to_tuple, line.split("@")))


def solve(input):
    return read_input(input)


def main():
    res = solve("sample.txt")
    # res = solve("input.txt")
    print(res)


if __name__ == "__main__":
    main()
