"""Golden Master approval — compare actual text to tests/golden/*.approved.txt."""

from __future__ import annotations

import os
from pathlib import Path

_TESTS_DIR = Path(__file__).resolve().parent
_GOLDEN_DIR = _TESTS_DIR / "golden"


def assert_matches_golden(actual: str, relative: str) -> None:
    golden_path = _GOLDEN_DIR / relative
    if os.environ.get("UPDATE_GOLDEN") == "1":
        golden_path.parent.mkdir(parents=True, exist_ok=True)
        golden_path.write_text(actual, encoding="utf-8", newline="\n")
        return

    if not golden_path.is_file():
        raise AssertionError(
            f"golden missing: {golden_path}\n"
            f"Run: UPDATE_GOLDEN=1 python -m pytest ... to create."
        )

    expected = golden_path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(
            f"golden mismatch: {relative}\n"
            f"--- expected ---\n{expected}\n"
            f"--- actual ---\n{actual}"
        )
