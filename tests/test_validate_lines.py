from src.validate_lines import validate_lines


def test_d001_complete_magic_square_passes():
    """D-001 — 표준 4×4 완전 마방진 → pass."""
    grid = [
        [16,  3,  2, 13],
        [ 5, 10, 11,  8],
        [ 9,  6,  7, 12],
        [ 4, 15, 14,  1],
    ]
    result = validate_lines(grid)
    assert result["status"] == "pass"
    assert result["failed_lines"] == []
