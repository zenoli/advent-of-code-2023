import math
import re
from itertools import cycle


def pick(instruction):
    return 0 if instruction == "L" else 1


def read_input(filename):
    with open(filename) as file:
        lines = [line.rstrip() for line in file]
    return lines


def parse_line(line):
    src, left, right = re.findall(r"\w+", line)
    return src, (left, right)


def get_nodes(suffix, mapping):
    return filter(lambda key: key[2] == suffix, mapping.keys())


def get_mapping(mapping_lines):
    return dict(map(parse_line, mapping_lines))


def move(src, instruction, mapping):
    return mapping[src][pick(instruction)]


def compute_cycle(src, instructions, mapping, dst_nodes):
    for step, instruction in enumerate(cycle(instructions), 1):
        src = move(src, instruction, mapping)
        if src in dst_nodes:
            return step


def solve(lines):
    instructions = lines[0]
    mapping = get_mapping(lines[2:])

    src_nodes = list(get_nodes("A", mapping))
    dst_nodes = set(get_nodes("Z", mapping))

    cycles = (compute_cycle(src, instructions, mapping, dst_nodes) for src in src_nodes)
    return math.lcm(*cycles)


def main():
    # lines = read_input("sample3.txt")
    lines = read_input("input.txt")
    print(solve(lines))


if __name__ == "__main__":
    main()
