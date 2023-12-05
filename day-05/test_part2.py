from part2 import get_seeds_from_ranges, compute_dst_intervals_from_partitions


def test_get_seeds_from_ranges():
    seeds = list(get_seeds_from_ranges([1, 3, 5, 2]))
    assert seeds == [1, 2, 3, 5, 6]


def test_get_compute_intervals_from_partitions():
    partitions = [15, 20, 30, 40, 45]
    intervals = [10, 20, 30, 40, 50]
    offsets = [0, 2, -5, 22, 13, 0]

    res = compute_dst_intervals_from_partitions(partitions, intervals, offsets)
    assert res == [(17, 15), (15, 52), (52, 53), (53, 58)]
