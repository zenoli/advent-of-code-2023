from part2 import calculate_slice, calculate_slice_plus, calculate_block, closed, shrink


def test_calculate_slice():
    assert calculate_slice([2, 4, 10, 12]) == 6
    assert calculate_slice([0, 2, 5, 7]) == 6


def test_calculate_block():
    intervals = {
        0: [range(0, 6)],
        2: [range(0, 2)],
        5: [range(4, 6), range(0, 2)],
        7: [range(4, 6), range(0, 1)],
        9: [range(1, 6)],
    }
    assert calculate_block(0, 1, intervals) == 6
    assert calculate_block(2, 4, intervals) == 20


def test_calculate_slice_plus():
    intervals = {
        0: [closed(range(0, 6))],
        2: [closed(range(0, 2))],
        5: [closed(range(4, 6)), closed(range(0, 2))],
        7: [closed(range(4, 6)), closed(range(0, 1))],
        9: [closed(range(1, 6))],
    }
    assert calculate_slice_plus(0, intervals) == 6
    assert calculate_slice_plus(1, intervals) == 8
    assert calculate_slice_plus(2, intervals) == 10 
    assert calculate_slice_plus(4, intervals) == 10 
    assert calculate_slice_plus(6, intervals) == 9

    intervals = {
        0: [closed(range(2, 6))],
        5: [closed(range(4, 6)), closed(range(0, 2))],
        7: [closed(range(4, 6)), closed(range(0, 1))],
        9: [closed(range(1, 6))],
    }
    assert calculate_slice_plus(0, intervals) == 3
    assert calculate_slice_plus(1, intervals) == 5
    assert calculate_slice_plus(2, intervals) == 10

    intervals = {
        0: [closed(range(2, 4))],
        2: [closed(range(0, 2))],
        4: [closed(range(2, 4))],
        6: [closed(range(0, 2))],
    }
    assert calculate_slice_plus(0, intervals) == 5 
    assert calculate_slice_plus(2, intervals) == 7 


def test_closed_range():
    assert list(closed(range(1, 3))) == [1, 2, 3]
    assert list(closed(range(3))) == [0, 1, 2, 3]


def test_shrinked_range():
    assert list(shrink(closed(range(1, 3)))) == [2]
    assert list(shrink(closed(range(1, 2)))) == []
