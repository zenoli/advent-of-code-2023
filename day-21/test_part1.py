from part1 import Part1


def test_get_neighbors():
    pt1 = Part1("day-21/sample.txt")
    assert set(pt1.get_neighbors((0, 0))) == set([(0, 1), (1, 0)])
    assert set(pt1.get_neighbors((3, 1))) == set([(4, 1), (3, 0)])
