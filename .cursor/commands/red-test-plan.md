# RED Test Plan — validate_lines

`validate_lines` Command에 대한 **RED 전 테스트 계획**만 수행한다. 코드·테스트 파일은 **수정하지 않고**, 다음 RED 사이클에 쓸 시나리오·AAA·기대값을 문서로 고정한다.

**슬래시만 실행:** `/red-test-plan` — 추가 입력·확인 질문 **금지**. 아래 절차를 즉시 수행한다.

---

## Phase 선언 (필수)

응답 **첫 줄**에 반드시 선언:

```
Phase: RED (Plan)
```

계획 단계이므로 `src/`·`tests/` **diff 없음**.

---

## 대상·SSOT

| 항목 | 내용 |
|------|------|
| Command | `validate_lines(grid) -> dict` |
| 반환 | `{"status": "pass"\|"fail"\|"incomplete", "failed_lines": [...]}` |
| 10선 | R1~R4 · C1~C4 · D1(주) · D2(반), 합 **34** |
| Test Loop | D-001 pass · D-002 행=34·열/대각 fail · D-003 R2(`validate_lines` 밖) |
| incomplete | 빈칸(`0`) 1개 이상 → `incomplete`, `failed_lines=[]` |

참조: `docs/PRD.md` · `Report/03.*` · `.cursorrules`

---

## 자율 실행 절차

사용자에게 묻지 말고 아래 순서로 진행한다.

1. **현황 스캔** — `tests/test_validate_lines.py`·`src/validate_lines.py`를 읽어 이미 있는 시나리오 ID·함수명·pytest 결과(가능하면 `pytest tests/test_validate_lines.py -v` 1회)를 파악한다.
2. **갭 분석** — D-001 · D-002(열 fail / D1 fail / D2 fail 중 미커버) · incomplete · D-003(별도 R2) 중 **다음 RED 1사이클**에 넣을 **우선순위 1건**을 SSOT 기준으로 고른다.  
   - 우선순위: D-001 → D-002 → incomplete → (D-003은 `validate_lines` 밖이면 별도 테스트 파일 계획만 명시)
3. **AAA 계획** — 선택 시나리오에 대해 Arrange(grid 픽스처) · Act · Assert(`status`, `failed_lines`)를 **구체 숫자·줄 ID**까지 적는다.
4. **RED 성공 조건** — “현재 stub 기준 이 테스트는 **반드시 FAILED**여야 함”을 한 줄로 명시한다.
5. **다음 커맨드** — `/red-skeleton` 또는 `/tdd-red` 중 권장 1개를 적는다.

---

## 계획서 형식 (출력)

```
Phase: RED (Plan)

## 현황
- 커버됨: (test_... 목록 또는 “없음”)
- 미커버: (D-00x / incomplete 등)

## 다음 RED 1사이클
- ID: D-00x (또는 incomplete)
- 의도: (Mom Test / SC 연결 한 줄)
- 우선순위 근거: (왜 지금 이 시나리오인지)

## AAA
- Arrange: 4×4 grid (리터럴 또는 “표준 마방진 변형” 설명)
- Act: validate_lines(grid)
- Assert: status=..., failed_lines=[...]

## 픽스처 메모
- 깨질 축: (예: C4, D2)
- 행 합 34 유지 여부: (D-002면 예)

## RED 성공 조건
- pytest 시 FAILED — (예상 실패 메시지 요약)

## 금지 확인
- src/ 수정 계획 없음 · assert 완화 없음 · D-00x 의미 변경 없음

## 다음
- /red-skeleton 또는 /tdd-red
```

---

## 금지 (Plan)

| 금지 | 이유 |
|------|------|
| `src/`·`tests/` 파일 수정 | 실행은 `/red-skeleton`·`/tdd-red` |
| 사용자에게 “어떤 시나리오?” 질문 | SSOT·갭 분석으로 자율 선택 |
| D-001~D-003 **의미 변경** | 시나리오 왜곡 |
| Solver·UI·R2를 `validate_lines`에 넣는 계획 | Session 3 범위 밖 |

---

## Mom Test 연결 (참고)

| 시나리오 | Mom Test |
|----------|----------|
| D-002 | “행 합 34 우선” 후 “넣어본 뒤” 열·대각 깨짐 (SC-1) |
| incomplete | 풀이 중 빈칸 — 10축 판정 보류 |
| D-001 | 16칸 완성·10축 pass (AC-2) |
