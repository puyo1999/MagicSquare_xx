# RED Skeleton — validate_lines

`validate_lines`에 대한 **RED 스켈레톤**만 수행한다. `tests/test_validate_lines.py`에 **실패하는 테스트 골격**(함수·AAA·assert)을 추가하고 `pytest`로 RED를 확인한다. `src/`는 건드리지 않는다.

**슬래시만 실행:** `/red-skeleton` — 추가 입력·확인 질문 **금지**. SSOT·기존 테스트 갭을 보고 **다음 1사이클** 스켈레톤을 즉시 추가한다.

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
| Test Loop | D-001 · D-002 · incomplete · (D-003은 R2, 별도) |

참조: `Report/03.*` · `.cursorrules` · (있으면) 직전 `/red-test-plan` 출력

---

## 자율 실행 절차

1. `tests/test_validate_lines.py`·`src/validate_lines.py` 읽기.
2. 미커버 시나리오 중 **1건** 선택 (우선: D-001 → D-002 변형 → incomplete). 질문하지 않는다.
3. `test_<id>_<요약>()` 함수 1개 추가 — docstring에 시나리오 ID 표기.
4. Arrange: 4×4 `grid` 리터럴. Act: `validate_lines(grid)`. Assert: 워크북 계약대로 **엄격**히 기술.
5. `pytest tests/test_validate_lines.py::<새함수> -v` 실행 → **FAILED** 확인.
6. 보고 형식(아래)으로 한국어 출력.

스켈레톤 = assert는 완전히 작성하되, **의도적으로 현재 stub과 불일치**하게 RED를 만든다. `pass`·`...`만 있는 빈 테스트로 RED 회피 금지.

---

## pytest 스켈레톤 예시

```python
from src.validate_lines import validate_lines


def test_d002_all_rows_34_but_diagonal_d1_fails():
  """D-002 — 4행 합 34, 주대각(D1) ≠ 34 → fail + failed_lines."""
  grid = [
      [16,  3,  2, 13],
      [ 5, 10, 11,  8],
      [ 9,  6,  7, 12],
      [ 4, 15, 14,  3],  # D1 깨짐 — grid는 실제 합 검증 후 조정
  ]
  result = validate_lines(grid)
  assert result["status"] == "fail"
  assert "D1" in result["failed_lines"]
```

실행:

```bash
pytest tests/test_validate_lines.py::test_d002_all_rows_34_but_diagonal_d1_fails -v
```

**RED 성공 조건**: 새 테스트 **FAILED**. 통과 시 기대값·grid 재검토 (assert 완화 금지).

---

## 금지 (RED Skeleton)

| 금지 | 이유 |
|------|------|
| `src/` 수정 | GREEN 역할 |
| assert 완화·삭제, `@pytest.mark.skip`, `xfail` | RED 회피 |
| `tests/` 외 파일 수정 | RED 범위 밖 |
| 테스트 통과 상태에서 RED 종료 | 실패 미확인 |
| 사용자에게 시나리오 선택 질문 | 자율 실행 |

---

## 보고 형식

```
Phase: RED

## 시나리오
- ID: D-00x (또는 incomplete)
- 의도: 한 줄

## 변경
- 파일: tests/test_validate_lines.py
- 추가: test_... (함수명)

## pytest 결과
- 명령: pytest tests/test_validate_lines.py::test_... -v
- 결과: FAILED — (실패 메시지 한 줄 요약)

## 다음
- GREEN: /green-minimal
```

RED 보고 시 `src/` diff는 **없어야** 한다.
