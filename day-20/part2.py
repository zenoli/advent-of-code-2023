from itertools import product, chain
from collections import defaultdict
from functools import cache
import math

FF = {
    "hp",
    "gb",
    "qn",
    "vx",
    "gs",
    "tl",
    "bb",
    "gr",
    "vz",
    "jm",
    "dt",
    "lj",
    "mp",
    "db",
    "lq",
    "zb",
    "lb",
    "sz",
    "pm",
    "xv",
    "bh",
    "cd",
    "jk",
    "zq",
    "gf",
    "xh",
    "rt",
    "lg",
    "fm",
    "pb",
    "gz",
    "nk",
    "mb",
    "kj",
    "mv",
}

FF1 = {"gs", "nk", "lq", "zb", "lg", "rt", "vx", "lj", "sz"}
# FF = {"vz", "mv"}


def read_input(filename):
    flipflops = dict()
    conjunctions = dict()

    def parse(line):
        input, outputs = line.split(" -> ")
        outputs = set(outputs.split(", "))
        if input[0] == "%":
            input = input[1:]
            flipflops[input] = False
        elif input[0] == "&":
            input = input[1:]
            conjunctions[input] = dict()
        return product([input], outputs)

    with open(filename) as file:
        lines = [line.rstrip() for line in file]

    input_mapping, output_mapping = defaultdict(set), defaultdict(set)
    for input, output in chain(*map(parse, lines)):
        input_mapping[output].add(input)
        output_mapping[input].add(output)

    return input_mapping, output_mapping, flipflops, conjunctions


def initialize_conjunctions(input_mapping, conjunctions):
    for name, inputs in input_mapping.items():
        if name in conjunctions:
            conjunctions[name] = {input: False for input in inputs}

    return conjunctions


def solve(input):
    dependencies = set()

    def get_dependencies(name):
        for input in input_mapping[name]:
            if input not in dependencies:
                dependencies.add(input)
                get_dependencies(input)

    def push_button(flipflops, conjunctions):
        def process(pulse, src, dst):
            if dst in conjunctions:
                conjunctions[dst][src] = pulse
                out_pulse = not all(conjunctions[dst].values())
                return [(out_pulse, dst, new_dest) for new_dest in output_mapping[dst]]
            if dst in flipflops:
                if not pulse:
                    flipflops[dst] = not flipflops[dst]
                    return [
                        (flipflops[dst], dst, new_dest)
                        for new_dest in output_mapping[dst]
                    ]
                return []
            if dst == "broadcaster":
                return [(pulse, dst, new_dest) for new_dest in output_mapping[dst]]
            return []

        tasks = [(False, "button", "broadcaster")]

        count = 0
        while tasks:
            pulse, src, dst = tasks.pop(0)
            # print(f"{src} -{'high' if pulse else 'low'}-> {dst}")
            count += 1
            if not pulse and dst == "rx":
                return True
            tasks.extend(process(pulse, src, dst))
        return flipflops, conjunctions

    input_mapping, output_mapping, flipflops, conjunctions = read_input(input)

    conjunctions = initialize_conjunctions(input_mapping, conjunctions)
    # for output, inputs in input_mapping.items():
    #     print(f"{output} <-- {inputs}")

    count = 0
    flipped_on = None
    flipped_off = None
    ff_test = "vz"
    ff_on1 = dict()
    ff_off = dict()
    ff_on2 = dict()

    while not all(map(lambda ff: ff in ff_on2, FF)):
        count += 1
        flipflops, conjunctions = push_button(flipflops, conjunctions)

        for ff in FF:
            if ff not in ff_on1 and flipflops[ff] and ff not in ff_on2:
                ff_on1[ff] = count

        for ff in FF:
            if ff in ff_on1 and not flipflops[ff]:
                ff_off[ff] = count

        for ff in FF:
            if ff in ff_on1 and ff in ff_off and flipflops[ff] and ff not in ff_on2:
                ff_on2[ff] = count
                del ff_off[ff]

        if not flipped_on and flipflops[ff_test]:
            flipped_on = count

        if flipped_on and not flipflops[ff_test]:
            flipped_off = count
            print(f"ON: {flipped_on}, duration: {flipped_off - flipped_on}")
            flipped_on = None

    for on1, on2 in zip(ff_on1.items(), ff_on2.items()):
        print(on1, on2)
    # for k, v in ff_on1.items():
    #     print(f"{k}: start: {v[0]}, stepsize: {v[2] - v[0]}, length: {v[1]}")
    print(
        math.lcm(
            *list(map(lambda v: v[1] - v[0], zip(ff_on1.values(), ff_on2.values())))
        )
    )


def main():
    state = {}
    # res = solve("sample2.txt")
    res = solve("input.txt")
    print(res)


if __name__ == "__main__":
    main()
