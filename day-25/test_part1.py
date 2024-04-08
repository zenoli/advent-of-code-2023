from part1 import Karger, debug


def test_edge_contraction():
    input = {
        1: [2, 3],
        2: [3, 4, 4],
        3: [4]
    }  # fmt: off
    karger = Karger(input)
    karger.contract((1, 2))

    debug(karger.adj)
    assert karger.adj == [
        [0, 2, 0, 0],
        [2, 0, 3, 0],
        [0, 3, 0, 0],
        [0, 0, 0, 0]
    ]  # fmt: off

    assert karger.N == 3
    assert karger.edge_counts == [2, 5, 3, 0]
    assert karger.vertex_merge_counts == [1, 2, 1, 0]
