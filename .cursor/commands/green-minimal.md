# GREEN Minimal — validate_lines

`validate_lines`에 대한 **GREEN 최소 구현**만 수행한다. **현재 실패 중인 테스트**를 통과시키는 `src/validate_lines.py` 변경만 한다. 리팩터·부가 기능·범위 밖 로직은 넣지 않는다.

**슬래시만 실행:** `/green-minimal` — 추가 입력·확인 질문 **금지**. 실패 테스트를 읽고 즉시 최소 구현한다.

---

## Phase 선언 (필수)

응답 **첫 줄**에 반드시 선언:

```
Phase: GREEN
```

이후 `src/` 최소 diff만 허용. 테스트 의미 변경·assert 완화 금지.

---

## 대상·SSOT

| 항목 | 내용 |
|------|------|
| Command | `validate_lines(grid) -> dict` |
| `incomplete` | `0` 존재 → `status=incomplete`, `failed_lines=[]` |
| `pass` | 16칸 완성 + 10선 합 34 |
| `fail` | 16칸 완성 + 합≠34 축 → 해당 R/C/D ID in `failed_lines` |
| R2(중복·범위) | `validate_lines` **밖** — D-003에 넣지 않음 |

참조: `docs/PRD.md` · `Report/03.*` · `.cursorrules`

---

## 자율 실행 절차

1. `pytest tests/test_validate_lines.py -v` 실행 — **실패 목록** 파악.
2. 실패가 없으면: “이미 GREEN” 보고 후 종료 (불필요한 `src/` 수정 금지).
3. 실패 테스트 1건(또는 동일 원인 묶음)에 맞춰 `src/validate_lines.py` **최소** 수정.
4. 해당 테스트 → 전체 파일 순으로 `pytest` 재실행.
5. **전체 PASS**가 목표이나, 이번 사이클은 “방금 RED 1건” 해소만 해도 됨 — 단, 기존 통과 테스트 깨뜨리지 않는다.
6. 보고 형식으로 한국어 출력.

최소 구현 예시 방향 (과도한 추상화 금지):

- 빈칸 검사 → `incomplete` 조기 반환
- 10선 합 계산 → 34 비교 → `failed_lines` 수집
- `failed_lines` 비었으면 `pass`, 아니면 `fail`

---

## pytest

```bash
pytest tests/test_validate_lines.py -v
```

**GREEN 성공 조건**: 대상 실패 테스트 **PASSED**, 기존 테스트 회귀 없음.

---

## 금지 (GREEN)

| 금지 | 이유 |
|------|------|
| `tests/` assert 완화·시나리오 삭제 | 요구사항 변경 |
| R2(중복·1~16 밖) 검사 추가 | FR 범위 밖 |
| Solver·UI·클래스 ECB 일괄 도입 | Non-Goals |
| “행만 34”면 pass 처리 | FR-8 위반 |
| 사용자에게 구현 방식 질문 | 자율 최소 구현 |
| 리팩터(중복 제거·이름 정리) | REFACTOR 단계 |

---

## 보고 형식

```
Phase: GREEN

## 대상 실패
- test_... : (실패 원인 한 줄)

## 변경
- 파일: src/validate_lines.py
- 요약: (추가한 분기·계산 한 줄)

## pytest 결과
- 명령: pytest tests/test_validate_lines.py -v
- 결과: (N passed / 실패 0 또는 남은 실패 목록)

## 다음
- 실패 남음 → /green-minimal 반복
- 전부 PASS → /golden-master
```
