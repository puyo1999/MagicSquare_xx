# REFACTOR Safe — validate_lines

`validate_lines`에 대한 **안전 리팩터**만 수행한다. 동작·공개 계약·테스트 의미는 유지하고 `src/validate_lines.py`만 정리한다. **매 수정 후** `pytest`로 회귀 없음을 확인한다.

**슬래시만 실행:** `/refactor-safe` — 추가 입력·확인 질문 **금지**. (있으면) 직전 `/refactor-smell` 우선 항목부터 즉시 리팩터한다.

---

## Phase 선언 (필수)

응답 **첫 줄**에 반드시 선언:

```
Phase: REFACTOR
```

`tests/` 수정 금지 (필요 시 버그는 GREEN으로 분리). `src/`만 허용.

---

## 대상·SSOT

| 항목 | 내용 |
|------|------|
| Command | `validate_lines(grid) -> dict` — 시그니처·키 불변 |
| 불변 | `incomplete` / `pass` / `fail` 규칙 · 10선 ID · R2 미포함 |
| 회귀 | `pytest tests/test_validate_lines.py -v` **매 단계 PASS** |
| 전제 | 골든 마스터 PASS (`/golden-master` 확정 상태 권장) |

참조: `docs/PRD.md` · `Report/03.*` · `.cursorrules`

---

## 자율 실행 절차

1. `pytest tests/test_validate_lines.py -v` — FAIL이면 REFACTOR **중단**, `/green-minimal` 보고.
2. 리팩터 대상 선택: 직전 smell 보고 #1, 없으면 **중복 합 계산 제거** 또는 **상수·헬퍼 최소 추출** 1건.
3. **작은 diff** 1회 적용 → 즉시 `pytest` 전체 실행.
4. FAIL 시 **즉시 되돌리고** 원인 한 줄 보고 (사용자 질문 없음).
5. PASS 유지 시 다음 smell 1건까지 반복 가능 — 단, 한 응답에서 과도한 대규모 변경 금지.
6. 보고 형식으로 한국어 출력.

안전 리팩터 예:

- `_line_sum(cells) -> int` 등 **private** 헬퍼
- `MAGIC = 34`, `SIZE = 4` 상수
- 10선 `(id, indices)` 루프로 `failed_lines` 수집 통일

---

## pytest (매 단계)

```bash
pytest tests/test_validate_lines.py -v
```

**REFACTOR 성공 조건**: 리팩터 전후 **동일 PASS**, 공개 API·반환 형태 동일.

---

## 금지 (REFACTOR)

| 금지 | 이유 |
|------|------|
| `tests/` assert·시나리오 변경 | 요구 변경 |
| R2·Solver·UI 추가 | 범위 밖 |
| 공개 API 이름·반환 키 변경 | 계약 파괴 |
| pytest FAIL 상태에서 “정리” 계속 | 회귀 |
| 사용자에게 리팩터 범위 질문 | 자율 실행 |
| 행-only pass 등 **동작 변경** | FR-8 |

---

## 보고 형식

```
Phase: REFACTOR

## 리팩터 항목
- 스멜: (이름)
- 변경 요약: (한 줄)

## 변경
- 파일: src/validate_lines.py
- diff 요약: (함수 추출·상수화 등)

## pytest 결과
- 명령: pytest tests/test_validate_lines.py -v
- 결과: X passed (회귀 없음)

## 남은 스멜
- (있으면 목록) → /refactor-smell 재실행 또는 /refactor-safe 반복

## 다음
- 전부 정리됨 → 세션 Export: magic-square-docs 스킬 참고
```
