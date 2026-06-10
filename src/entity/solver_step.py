from src.find_blank_coords import find_blank_coords
from src.entity.constants import BLANK_CELL, TARGET_SUM


def solve_step_a(grid: list[list[int]]) -> list[int]:
    solution: list[int] = []
    for row_1, col_1 in find_blank_coords(grid):
        row = grid[row_1 - 1]
        row_sum_filled = sum(cell for cell in row if cell != BLANK_CELL)
        value = TARGET_SUM - row_sum_filled
        solution.extend([row_1, col_1, value])
    return solution


def format_step_a_golden(solution: list[int], *, error_code: str = "") -> str:
    if len(solution) != 6:
        raise ValueError("solution must be int[6]")
    fields = ",".join(str(x) for x in solution)
    lines = [
        "status: success",
        "track: entity",
        "test_id: D-SOL-01",
        f"solution_int6: {fields}",
        f"error_code: {error_code}",
    ]
    return "\n".join(lines) + "\n"
