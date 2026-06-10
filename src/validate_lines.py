from src.entity.constants import BLANK_CELL, TARGET_SUM
from src.entity.validation import all_lines, line_sum


def validate_lines(grid):
    for row in grid:
        for cell in row:
            if cell == BLANK_CELL:
                return {"status": "incomplete", "failed_lines": []}

    failed_lines = [
        line_id
        for line_id, indices in all_lines()
        if line_sum(grid, indices) != TARGET_SUM
    ]

    if failed_lines:
        return {"status": "fail", "failed_lines": failed_lines}

    return {"status": "pass", "failed_lines": []}
