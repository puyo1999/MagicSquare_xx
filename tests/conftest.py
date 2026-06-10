import pytest


@pytest.fixture
def grid_g1():
    """G1 — OO 4.1 과제 격자, 빈칸 2개 (1-index: (2,3), (4,4))."""
    return [
        [16, 3, 2, 13],
        [5, 10, 0, 8],
        [9, 6, 7, 12],
        [4, 15, 14, 0],
    ]
