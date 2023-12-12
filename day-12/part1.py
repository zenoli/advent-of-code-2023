def read_input(filename):
    with open(filename) as file:
        lines = [line.rstrip() for line in file]
    return lines


def f(X, c):
    if not c:
        return 0 if "#" in X else 1
    if not X:
        return 0

    if X[0] == ".":
        return f(X[1:], c)

    if X[0] == "#":
        if can_place(X, c[0]):
            return f(X[c[0] + 1 :], c[1:])
        else:
            return 0

    return f("#" + X[1:], c) + f("." + X[1:], c)


def can_place(X, group):
    if len(X) < group:
        return False
    if len(X) > group and X[group] == "#":
        return False
    return set(X[:group]) <= {"#", "?"}


def parse_line(line):
    record, groups = line.split()
    groups = list(map(int, groups.split(",")))
    return record, groups


def main():
    # lines = read_input("sample.txt")
    lines = read_input("input.txt")
    result = sum(f(record, group) for record, group in map(parse_line, lines))
    print(result)


if __name__ == "__main__":
    main()
