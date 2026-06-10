# Golden Master — validate_lines

`validate_lines` Test Loop의 **골든 마스터(기준선) 고정**을 수행한다. 전체 `pytest`가 **PASS**인 상태를 확인·기록하고, 이후 REFACTOR의 회귀 기준으로 쓸 스냅샷을 남긴다. **구현·테스트 로직 변경은 하지 않는다.**

**슬래시만 실행:** `/golden-master` — 추가 입력·확인 질문 **금지**. 즉시 전체 테스트 실행 후 기준선 보고서를 출력한다.

---

## Phase 선언 (필수)

응답 **첫 줄**에 반드시 선언:

```
Phase: GREEN (Golden Master)
```

코드 diff **없음** (검증·문서화만). 실패 테스트가 있으면 GREEN 미완으로 보고하고 `/green-minimal`을 권장한다.

---

## 대상·SSOT

| 항목 | 내용 |
|------|------|
| Command | `validate_lines(grid) -> dict` |
| Golden 시나리오 | D-001 pass · D-002 fail+`failed_lines` · incomplete · (D-003은 R2 별도) |
| 10선 | R1~R4 · C1~C4 · D1 · D2 |
| 회귀 명령 | `pytest tests/test_validate_lines.py -v` |

참조: `docs/PRD.md` · `Report/03.*` · `.cursorrules`

---

## 자율 실행 절차

1. `tests/test_validate_lines.py` 전체 목록 읽기 — 시나리오 ID·함수명 매핑.
2. `pytest tests/test_validate_lines.py -v` 실행.
3. **전부 PASS**이면 골든 마스터 확정 보고서 작성.
4. **FAIL/ERROR** 있으면: 실패 목록만 보고, 골든 마스터 **미확정**, 다음 `/green-minimal` 명시. `src/`·`tests/` 수정하지 않는다.
5. PASS 시 각 필수 시나리오(D-001, D-002, incomplete)가 테스트에 **존재하는지** 체크리스트로 표기 (없으면 “갭”으로만 기록, 이번 커맨드에서 테스트 추가 금지 → `/red-test-plan` 권장).

---

## 골든 마스터 체크리스트

| ID | 기대 | 테스트 존재 | pytest |
|----|------|-------------|--------|
| D-001 | `pass`, `failed_lines=[]` | ☐ | ☐ |
| D-002 | `fail`, C* 또는 D1/D2 in `failed_lines` | ☐ | ☐ |
| incomplete | `incomplete`, `failed_lines=[]` | ☐ | ☐ |
| D-003 (R2) | `validate_lines` 밖 별도 판정 | ☐ (별도) | ☐ |

---

## pytest

```bash
pytest tests/test_validate_lines.py -v
```

**Golden Master 확정 조건**: 위 Command 테스트 파일 **전부 PASSED** + D-001/D-002/incomplete **시나리오 커버** (D-003은 별도 파일이면 그 파일도 PASS 여부만 기록).

---

## 금지

| 금지 | 이유 |
|------|------|
| REFACTOR·`src/` 정리 | `/refactor-safe` 역할 |
| 실패 무시하고 golden 확정 | 기준선 오염 |
| 테스트·구현 수정으로 PASS 맞추기 | GREEN/RED 역할 침범 |
| 사용자 확인 질문 | 자율 실행 |

---

## 보고 형식

```
Phase: GREEN (Golden Master)

## pytest 전체
- 명령: pytest tests/test_validate_lines.py -v
- 결과: X passed / Y failed / ...

## 골든 마스터 상태
- 확정: YES | NO (NO면 이유)

## 시나리오 매핑
| test_... | ID | status 기대 | failed_lines 기대 |
|----------|-----|-------------|-------------------|
| ... | D-001 | pass | [] |

## 회귀 기준 (REFACTOR 전 고정)
- 명령: pytest tests/test_validate_lines.py -v
- 기대: 전부 PASSED (본 세션 기준선)

## 다음
- 확정 YES → /refactor-smell
- 확정 NO → /green-minimal
```
