import sys
from pathlib import Path

_tests_dir = Path(__file__).resolve().parent.parent
if str(_tests_dir) not in sys.path:
    sys.path.insert(0, str(_tests_dir))

from _approval import assert_matches_golden

from src.entity.solver_step import format_step_a_golden, solve_step_a


def test_d_sol_01_step_a_success(grid_g1):
    """D-SOL-01 — G1 step A success, int[6] 1-index golden."""
    solution = solve_step_a(grid_g1)
    actual = format_step_a_golden(solution, error_code="")
    assert_matches_golden(actual, "d_sol_01_g1_step_a.approved.txt")
