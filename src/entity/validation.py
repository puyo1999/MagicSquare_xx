from src.entity.constants import TARGET_SUM

SIZE = 4


def line_sum(grid, indices):
    return sum(grid[r][c] for r, c in indices)


def all_lines(size=SIZE):
    lines = []
    for i in range(size):
        lines.append((f"R{i + 1}", [(i, j) for j in range(size)]))
    for j in range(size):
        lines.append((f"C{j + 1}", [(i, j) for i in range(size)]))
    lines.append(("D1", [(i, i) for i in range(size)]))
    lines.append(("D2", [(i, size - 1 - i) for i in range(size)]))
    return lines
