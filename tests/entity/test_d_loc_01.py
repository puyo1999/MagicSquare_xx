import pytest

from src.find_blank_coords import find_blank_coords


def test_d_loc_01_blank_coords_row_major(grid_g1):
    """D-LOC-01 — G1 blank coords row-major (1-index)."""
    # Given: G1 격자 (0이 2개)
    # When: find_blank_coords(grid_g1) 호출
    find_blank_coords(grid_g1)
    # Then: [(2,2),(3,3)] 반환 (1-index, row-major)
    pytest.fail("RED: D-LOC-01 — 구현 없음, 의도적 실패")
