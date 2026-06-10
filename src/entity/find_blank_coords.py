from src.entity.constants import BLANK_CELL


def find_blank_coords(grid):
    return [
        (r + 1, c + 1)
        for r, row in enumerate(grid)
        for c, cell in enumerate(row)
        if cell == BLANK_CELL
    ]
