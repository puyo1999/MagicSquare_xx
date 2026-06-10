# REFACTOR Smell — validate_lines

`validate_lines` 구현의 **코드 스멜 분석**만 수행한다. `src/`·`tests/` **파일을 수정하지 않고**, 골든 마스터(PASS) 전제 하에 리팩터 후보와 위험도를 보고한다.

**슬래시만 실행:** `/refactor-smell` — 추가 입력·확인 질문 **금지**. `src/validate_lines.py`를 읽고 즉시 스멜 보고서를 출력한다.

---

## Phase 선언 (필수)

응답 **첫 줄**에 반드시 선언:

```
Phase: REFACTOR (Smell)
```

분석만 — **diff 없음**.

---

## 대상·SSOT

| 항목 | 내용 |
|------|------|
| 파일 | `src/validate_lines.py` |
| 계약 | `validate_lines` 반환·10선·`incomplete` 규칙 불변 |
| 전제 | `pytest tests/test_validate_lines.py -v` **전부 PASS** (아니면 스멜 분석 전 `/golden-master` 또는 `/green-minimal` 권장만 하고 종료) |
| 범위 밖 | R2 검사 도입 · Solver · 클래스 추출(과도) |

참조: `docs/PRD.md` · `.cursorrules`

---

## 자율 실행 절차

1. `pytest tests/test_validate_lines.py -v` 1회 — FAIL이면 스멜 분석 **보류**, 실패 요약 후 `/green-minimal` 안내.
2. `src/validate_lines.py` 전체 읽기.
3. 아래 스멜 체크리스트로 **관찰만** 기록 (심각도: High / Med / Low).
4. 각 스멜에 **안전한 리팩터 방향** 1줄 (구현 코드 작성 없음).
5. `/refactor-safe`에서 다룰 **우선 1~2건** 추천.

---

## 스멜 체크리스트 (Session 3 맥락)

| 스멜 | 징후 | Session 3 주의 |
|------|------|----------------|
| 중복 합 계산 | 행/열/대각 loop 복붙 | 추출 시 10선 ID 매핑 유지 |
| 매직 넘버 | `34`, `4` 반복 | 상수화는 허용, 과도한 설정 객체 금지 |
| 긴 함수 | 한 함수에 incomplete+10선+반환 | 단계 함수 분리만 |
| 불명확 ID | R/C/D 문자열 하드코딩 산재 | 튜플/루프로 통일 가능 |
| 범위 침범 | R2·중복 검사 혼입 | **리팩터로도 추가 금지** |
| 행-only pass | 열/대각 생략 분기 | **버그** — 스멜이 아니라 즉시 GREEN 버그로 보고 |
| dead code | stub `...` 잔존 | 제거 후보 |

---

## 금지

| 금지 | 이유 |
|------|------|
| `src/`·`tests/` 수정 | `/refactor-safe` 역할 |
| 동작 변경 제안 (FR-8 위반) | 계약 파괴 |
| 사용자에게 “리팩터할까요?” 질문 | 자율 보고 |

---

## 보고 형식

```
Phase: REFACTOR (Smell)

## 전제
- pytest: (passed / failed — failed면 분석 보류)

## 스멜 목록
| # | 스멜 | 위치(함수/줄) | 심각도 | 안전한 방향 |
|---|------|---------------|--------|-------------|
| 1 | ... | ... | Med | ... |

## 리팩터 비대상
- (의도적 최소 구현·Non-Goals 등)

## 다음
- /refactor-safe — 우선: (#1, #2)
```
