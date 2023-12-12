def read_input(filename):
    with open(filename) as file:
        lines = [line.rstrip() for line in file]
    return lines


def f(X, c):
    if not c:
        return 0 if "#" in X else 1
    if not X:
        return 0

    res = 0
    if X[0] in "?#" and can_place(X, c[0]):
        res += f(X[c[0] + 1 :], c[1:])

    if X[0] in "?.":
        res += f(X[1:], c)
    return res


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
