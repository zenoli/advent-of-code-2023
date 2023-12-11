from part2 import get_interior_neighbor
import numpy as np


def test_get_interior_neighbor():
    next_pos = get_interior_neighbor(np.array([1, 1]), np.array([2, 1]), 1)
    assert np.array_equal(next_pos, np.array([1, 2]))

    next_pos = get_interior_neighbor(np.array([1, 1]), np.array([1, 0]), 1)
    assert np.array_equal(next_pos, np.array([2, 1]))

    next_pos = get_interior_neighbor(np.array([1, 1]), np.array([1, 2]), -1)
    assert np.array_equal(next_pos, np.array([2, 1]))

    next_pos = get_interior_neighbor(np.array([1, 1]), np.array([2, 1]), -1)
    assert np.array_equal(next_pos, np.array([1, 0]))
