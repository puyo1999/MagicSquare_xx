# TDD RED — validate_lines

`validate_lines` Command에 대한 **RED 단계만** 수행한다. `tests/`만 수정하고, 실패하는 테스트를 추가한 뒤 `pytest`로 RED를 확인한다.

---

## Phase 선언 (필수)

응답 **첫 줄**에 반드시 선언:

```
Phase: RED
```

이후 모든 작업·보고는 RED 범위(`tests/`만) 안에서만 진행한다.

---

## 대상·SSOT

| 항목 | 내용 |
|------|------|
| Command | `validate_lines(grid) -> dict` |
| 반환 | `{"status": "pass"\|"fail"\|"incomplete", "failed_lines": [...]}` |
| 10선 | R1~R4 · C1~C4 · D1(주) · D2(반), 합 **34** |
| Test Loop | D-001 pass · D-002 행=34·열/대각 fail · (D-003은 R2, `validate_lines` 밖) |

참조: `Report/03.*`, `.cursorrules`

---

## AAA 절차 (테스트 1개당)

1. **Arrange** — 4×4 `grid` 픽스처 준비 (`0`=빈칸, 채움 `1~16`). 시나리오 ID(D-001 등)를 테스트명·docstring에 표기.
2. **Act** — `result = validate_lines(grid)` 호출.
3. **Assert** — `result["status"]`, `result["failed_lines"]`를 워크북 계약대로 검증. RED이므로 **현재 stub 구현 기준 반드시 실패**해야 함.

RED 한 사이클 = **하나의 행위(시나리오) 또는 최소 단위**에 테스트 1개(또는 동일 Arrange의 parametrized 1그룹) 추가 → `pytest` → 실패 확인.

---

## pytest 예시

```python
from src.validate_lines import validate_lines

# D-001 — 표준 4×4 완전 마방진 → pass
def test_d001_complete_magic_square_passes():
    grid = [
        [16,  3,  2, 13],
        [ 5, 10, 11,  8],
        [ 9,  6,  7, 12],
        [ 4, 15, 14,  1],
    ]
    result = validate_lines(grid)
    assert result["status"] == "pass"
    assert result["failed_lines"] == []

# incomplete — 빈칸 1개 이상 → 10선 판정 보류
def test_incomplete_grid_with_blank_returns_incomplete():
    grid = [
        [16,  3,  2, 13],
        [ 5, 10, 11,  8],
        [ 9,  6,  7, 12],
        [ 4, 15,  0,  1],  # 0 = 빈칸
    ]
    result = validate_lines(grid)
    assert result["status"] == "incomplete"
    assert result["failed_lines"] == []

# D-002 — 4행 합 34, 열/대각 깨짐 → fail + failed_lines
def test_d002_all_rows_34_but_column_fails():
    grid = [
        [16,  3,  2, 13],
        [ 5, 10, 11,  8],
        [ 9,  6,  7, 12],
        [ 4, 15, 14,  2],  # C4 등 10선 중 일부 ≠ 34
    ]
    result = validate_lines(grid)
    assert result["status"] == "fail"
    assert "C4" in result["failed_lines"]  # 실제 깨진 줄 ID에 맞게 조정
```

실행:

```bash
pytest tests/test_validate_lines.py -v
```

**RED 성공 조건**: 새 테스트가 **FAILED** (또는 ERROR). 통과하면 테스트가 아직 RED가 아님 — 기대값·시나리오를 재검토 (assert 완화 금지).

---

## 금지 (RED)

| 금지 | 이유 |
|------|------|
| `src/` 수정 (구현·stub·`...` 교체) | GREEN 단계 역할 |
| assert 완화·삭제, `@pytest.mark.skip`, `xfail` | RED 회피 |
| `tests/` 외 파일 수정 (`pyproject.toml`, `.cursorrules` 등) | RED 범위 밖 |
| 테스트 통과 상태에서 RED 종료 | 실패 확인 없음 |
| D-001~D-003 **의미 변경**으로 맞추기 | 시나리오 왜곡 |

---

## 보고 형식

작업 후 아래 순서로 **한국어** 보고:

```
Phase: RED

## 시나리오
- ID: D-00x (또는 incomplete 등)
- 의도: 한 줄 (무엇을 검증하는 RED인지)

## 변경
- 파일: tests/test_validate_lines.py
- 추가: test_... (함수명)

## pytest 결과
- 명령: pytest tests/test_validate_lines.py::test_... -v
- 결과: FAILED — (실패 메시지 한 줄 요약)

## 다음
- GREEN: src/validate_lines.py 최소 구현
```

RED 보고 시 `src/` diff는 **없어야** 한다.
