from part2 import get_seeds_from_ranges


def test_get_seeds_from_ranges():
    seeds = list(get_seeds_from_ranges([1, 3, 5, 2]))
    assert seeds == [1, 2, 3, 5, 6]
