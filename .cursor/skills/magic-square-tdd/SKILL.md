---
name: magic-square-tdd
description: >-
  MagicSquare_xx Session 3 validate_lines TDD·ARRR 루프. RED/GREEN/REFACTOR Phase,
  D-001~D-003, 10축 판정, 슬래시 커맨드 연계. validate_lines·pytest·tests/ src/ 작업 시 적용.
---

# MagicSquare TDD · ARRR

Session 3 **Rule · Command · Test Loop** — `validate_lines`만 SSOT. Solver·UI·ECB·R2 본체 구현은 범위 밖.

## ARRR 루프 (슬래시 커맨드)

| 단계 | 커맨드 | Phase | 수정 허용 |
|------|--------|-------|-----------|
| **A**ssess | `/red-test-plan` | RED (Plan) | 없음 (계획만) |
| **R**ED | `/red-skeleton`, `/tdd-red` | RED | `tests/`만 |
| **G**reen | `/green-minimal` | GREEN | `src/` 최소 |
| **G**olden | `/golden-master` | GREEN (Golden) | 없음 (기준선) |
| **R**efactor | `/refactor-smell` → `/refactor-safe` | REFACTOR | `src/`만 (동작 동일) |

**자율 실행:** 모든 커맨드는 슬래시만으로 동작 — 사용자 추가 입력·질문 금지.

## Phase 선언 (필수)

TDD 작업 응답 **첫 줄**:

- `Phase: RED` / `Phase: RED (Plan)`
- `Phase: GREEN` / `Phase: GREEN (Golden Master)`
- `Phase: REFACTOR` / `Phase: REFACTOR (Smell)`

Phase와 실제 수정 파일이 일치해야 함.

## Command 계약

```python
validate_lines(grid) -> dict
# {"status": "pass" | "fail" | "incomplete", "failed_lines": [...]}
```

| status | 조건 |
|--------|------|
| `incomplete` | `0` 빈칸 1개 이상 → `failed_lines=[]`, 10선 보류 |
| `pass` | 16칸 완성 + 10선 합 34 |
| `fail` | 16칸 완성 + 합≠34 축 → ID in `failed_lines` |

10선 ID: **R1~R4**, **C1~C4**, **D1**(주), **D2**(반). 마법상수 **34**.

**R2**(1~16 각 1회, 중복·범위)는 `validate_lines` **밖** — Test **D-003** 별도.

## Test Loop (D-001~D-003)

| ID | 시나리오 | 기대 |
|----|----------|------|
| D-001 | 완전 4×4 마방진 | `pass`, `[]` |
| D-002 | 4행 합 34, 열 또는 대각 ≠34 | `fail`, C* / D1 / D2 |
| D-003 | 중복·1~16 밖 | R2 fail — `validate_lines` 미호출 또는 별도 |

## TDD 금지 (엄격)

- RED: `src/` 수정 · assert 완화 · skip/xfail · D-00x 의미 변경
- GREEN: 테스트 완화 · R2 혼입 · 행-only pass
- REFACTOR: `tests/` 변경 · 동작·API 변경 · pytest FAIL 상태에서 계속

## pytest

```bash
pytest tests/test_validate_lines.py -v
```

## Mom Test 연결 (판정만)

- SC-1: D-002 — “행 34만” 착각 vs 열·대각 깨짐
- SC-2: 시행착오 후 잘못된 16칸 → `fail`
- SC-3: 삽입 후 판정 — 후보 24분 자동화는 Non-Goal

## SSOT 참조

- `.cursorrules`
- `docs/PRD.md`
- `Report/03. MagicSquare_1004 Session 3 워크북.md`
- `.cursor/commands/tdd-red.md` 및 ARRR 커맨드 6종

## 문서·Export

세션 보고·Transcript는 **magic-square-docs** 스킬과 `templates/` 사용.
