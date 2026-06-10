from src.find_blank_coords import find_blank_coords


def test_d_loc_01_blank_coords_row_major(grid_g1):
    """D-LOC-01 — G1 blank coords row-major (1-index)."""
    # Given: G1 격자 (0이 2개)
    # When: find_blank_coords(grid_g1) 호출
    result = find_blank_coords(grid_g1)
    # Then: [(2,3),(4,4)] 반환 (1-index, row-major)
    assert result == [(2, 3), (4, 4)]
