from src.find_blank_coords import find_blank_coords


def test_d_loc_01_find_blank_coords_returns_g1_blanks(grid_g1):
    """D-LOC-01 — G1 격자 빈칸 좌표 (1-index row-major)."""
    result = find_blank_coords(grid_g1)
    assert result == [(2, 3), (4, 4)]
