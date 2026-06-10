# MagicSquare_1004 — Product Requirements Document (PRD)

| 항목 | 내용 |
|------|------|
| 제품 | MagicSquare_1004 / MagicSquare_xx |
| 버전 | 0.2 (초안) |
| 일자 | 2026-06-10 |
| 상태 | Draft |
| Problem Definition | `Report/01.MagicSquare_ProblemDefinition_Report.md` |
| Session SSOT | `Report/03. MagicSquare_1004 Session 3 워크북.md` |

---

## 1. 개요

### 1.1 배경

OO 과제 **4.1 Magic Square** — 4×4 마방진에서 빈칸 2개를 채워 행·열·대각선 합을 **34**로 맞춘다.

Mom Test (2차)에 따르면 학습자는 **행 합 34만**으로 빈칸 후보를 종이에 적어 좁히는 데 **약 24분**을 쓰고, **열·대각선은 넣어 본 뒤에야** 확인하며, 틀렸을 때 **맞을 때까지 바꿔 넣기**(약 5회)로 **약 25분**을 쓴다. 코드로 다룬 적은 없다.

### 1.2 제품 목표 (Session 3)

> **4×4 부분 마방진을 채운 뒤, “행만 맞으면 된다”고 느끼는 순간과 실제로 열·대각선이 깨지는 순간을 구분할 수 있게, 채워진 격자가 마방진 조건을 만족하는지 판정하는 Rule · Command · Test Loop를 먼저 고정한다.**

### 1.3 비목표 (Non-Goals)

- 마방진 **자동 풀이** (Solver) · 빈칸 **자동 탐색** (MissingFinder)
- **후보군 좁히기** · 종이 계산 자동화 (24분 구간)
- **GUI** / PyQt / 웹 앱
- ECB 전체 · `SquareValidator` **클래스** 일괄 구현
- “검증 앱” UX · 원클릭 체크 · **틀린 이유 설명**

---

## 2. 사용자

### 2.1 Primary Persona

**4×4 부분 마방진 학습자** (Mom Test 2차)

- OO 과제 4.1 — 빈칸 2개, 합 34
- **올해 1월** 동일 유형 **제출 완료**, **약 25분**
- 현재: **손으로만** 풀이; **코드 경험 없음**
- 습관: 후보 **행 합 34 우선** → **넣어 본 뒤** 열·대각; 제출 직전 **대각선부터** 검산

### 2.2 사용자 스토리 (Mom Test 2차 기반)

| ID | As a… | I want… | So that… | Mom Test 근거 |
|----|-------|---------|----------|---------------|
| US-1 | 학습자 | 행만 34인데 **열·대각이 깨진** 격자를 **즉시 실패**로 알 수 | “행 합 34 우선” 후 **넣어본 뒤** 깨지는 갭을 잡는다 | “행 합 34 우선” / “**넣어본 뒤에**” |
| US-2 | 학습자 | **맞을 때까지 바꿔넣기** 끝의 잘못된 격자가 **fail**로 걸리게 | 5번 시행착오 후에도 **검증 루프**로 제출 전 걸러낸다 | “**맞을 때까지**” / “**5번**” |
| US-3 | 학습자 | **10축** 검산 항목이 Rule·Test에 **명시**되어 | 과제 조건·종이 후보 없이 **삽입 후 판정**만으로 재현·설명한다 | “후보군 24분” → Session 3는 **판정** SSOT |

### 2.3 보조 스토리 (Mom Test 1차 — D-002 보강)

| ID | 내용 | 근거 |
|----|------|------|
| US-1b | **행 4개만** 맞아도 완료로 보지 않게 | 1차 “1행→4행→**끝**” |

---

## 3. 도메인 요구사항

### 3.1 Magic Square 규칙

| ID | 규칙 |
|----|------|
| DR-1 | 격자 크기: **4×4** |
| DR-2 | 사용 숫자: **1~16**, 각 1회 (중복·누락 없음) — Rule **R2** |
| DR-3 | 목표 합: **34** |
| DR-4 | 검산 대상: **10축** — 행 R1~R4, 열 C1~C4, 대각 D1(주), D2(반) |
| DR-5 | 과제 입력: **빈칸 2개** — 코드에서는 `0`; 완성 후 검증 |

### 3.2 격자 표현 (Session 3)

| 항목 | 정의 |
|------|------|
| `grid` | `list[list[int]]`, 4×4 |
| 빈칸 | `0` |
| 채워진 칸 | `1~16` |
| `incomplete` | 빈칸이 하나라도 있으면 10축 판정 **보류** |

### 3.3 실패 조건 (Failure Conditions)

| ID | 조건 | Mom Test / Test 연결 |
|----|------|----------------------|
| FC-1 | 16칸 완성, **행 4개 합=34**, **열 하나** ≠34 | US-1 · D-002 |
| FC-2 | 16칸 완성, 행·열=34, **주대각(D1)** ≠34 | 1차 “대각선 빼먹음” · D-002 |
| FC-3 | 16칸 완성, 행·열·D1=34, **반대각(D2)** ≠34 | 10축 완전성 · D-002 |
| FC-4 | **중복** 또는 **1~16 밖** 값 | Rule **R2** · D-003 (`validate_lines` 밖) |

---

## 4. 기능 요구사항 (Session 3)

### 4.1 Command — `validate_lines`

| ID | 요구사항 | 우선순위 |
|----|----------|----------|
| FR-1 | 입력: 4×4 `grid`, 값 `0~16` | P0 |
| FR-2 | **10축** 각각 합 계산 및 34 비교 | P0 |
| FR-3 | 출력: `{ "status", "failed_lines" }` | P0 |
| FR-4 | `status`: `pass` \| `fail` \| `incomplete` | P0 |
| FR-5 | 빈칸(`0`) 존재 시 `incomplete`, `failed_lines=[]` | P0 |
| FR-6 | 16칸 완성 + 10축 모두 34 → `pass` | P0 |
| FR-7 | 16칸 완성인데 합≠34인 축 → `fail` + 해당 줄 ID | P0 |
| FR-8 | **행 4개만** 34여도 `pass` **금지** (열·대각 반드시 검사) | P0 |
| FR-9 | 줄 ID: **R1~R4**, **C1~C4**, **D1**, **D2** | P0 |

**시그니처**

```python
validate_lines(grid) -> dict
# {"status": "pass" | "fail" | "incomplete", "failed_lines": [...]}
```

**범위 밖:** FC-4(중복·범위)는 `validate_lines`가 처리하지 않음 → Rule R2 · D-003.

### 4.2 R-G-I-O

| | |
|---|---|
| **Role** | 1월 과제를 손으로 푼 학습자의 **삽입 후 판정**을 모델링하는 검증 Command |
| **Goal** | 10축 합 34 + `failed_lines`로 “행만 OK” 착각·시행착오 후 잘못된 격자를 구분 |
| **Input** | `grid`: 4×4, `0`=빈칸, `1~16`=채움 |
| **Output** | `status`, `failed_lines[]` (R/C/D ID) |

### 4.3 Rule 문서

| ID | 요구사항 |
|----|----------|
| FR-10 | **R1**: 16칸 완성 시 10축 합 34 (`validate_lines` SSOT) |
| FR-11 | **R2**: 셀 무결성 1~16 각 1회 — `validate_lines` **밖** |
| FR-12 | Rule 항목과 Test **D-001~D-003** 1:1 대응 |

### 4.4 Test Loop

| ID | 요구사항 |
|----|----------|
| FR-13 | `tests/test_validate_lines.py` — TDD Red → Green → Refactor |
| FR-14 | 구현: `src/validate_lines.py` |

**필수 시나리오 (D-001~D-003)**

| Test ID | 시나리오 | 기대 |
|---------|----------|------|
| **D-001** | 표준 완전 4×4 마방진 (`0` 없음) | `status=pass`, `failed_lines=[]` |
| **D-002** | **4행 모두 합 34**, 한 열 또는 대각 ≠34 (1월 “반대로 넣었더니”) | `status=fail`, `failed_lines`에 C* 또는 D1/D2 |
| **D-003** | 숫자 **중복** 또는 **1~16 밖** | Rule R2 **fail** — `validate_lines` 미호출 또는 별도 판정 |

### 4.5 Skill (선택)

| ID | 요구사항 |
|----|----------|
| FR-15 | 체크리스트: “행 34만 보면 안 됨 → **16칸 완성** 후 `validate_lines`로 **10축**” |
| FR-16 | “행만 pass” 테스트·구현 추가 시 리뷰 거부 |

---

## 5. 성공 지표 (Session 3 완료)

| # | 기준 | 검증 방법 |
|---|------|-----------|
| AC-1 | 행=34·열/대각 fail → `status=fail` + `failed_lines` | D-002 |
| AC-2 | 10축 pass 격자 → `status=pass` | D-001 |
| AC-3 | 빈칸 포함 → `status=incomplete` | incomplete 시나리오 |
| AC-4 | R2 위반 → `validate_lines`와 별도 fail | D-003 |
| AC-5 | Solver / UI / 후보 탐색 **미착수** | 코드베이스·Non-Goals |

---

## 6. 8계층 — 세션별 로드맵

| 계층 | Session 3 | 이후 세션 |
|------|-----------|-----------|
| **Rule** | ✅ R1(10축), R2(무결성) | 유지 |
| **Command** | ✅ `validate_lines` | `SquareValidator` 클래스 등 |
| **(Skill)** | ✅ 10축 체크리스트 | — |
| **Test Loop** | ✅ D-001~D-003 | 회귀·Dual-Track 확장 |
| Entity | — | `MagicSquare`, `Cell` |
| Control | — | `MissingFinder`, `Solver` |
| Boundary | — | `GridUI`, `ResultDisplay` |
| Integration | — | ECB 전체 |

---

## 7. 기술 제약

| 항목 | 내용 |
|------|------|
| 언어 | Python |
| 테스트 | pytest (`pyproject.toml`) |
| TDD | RED → tests만 · GREEN → `src/` 최소 구현 |
| 아키텍처 | Session 3는 Command 함수; ECB 클래스는 후속 |
| UI | 범위 외 |

---

## 8. 리스크 및 가정

### 8.1 가정

- Mom Test 2차(올해 1월 1건)가 Session 3 판정 요구의 대표 사례이다.
- 후보 24분 구간은 **이번 릴리스로 해결하지 않는다**.

### 8.2 리스크

| 리스크 | 완화 |
|--------|------|
| 단일 인터뷰 | `Report/02` 질문 10개 · STEP 2 추궁 |
| 1차·2차 습관 차이 | D-002에 행-only·열/대각 fail **둘 다** 포함 |
| 행-only `pass` 재발 | FR-8, FR-16 |
| Solver·후보 자동화 유혹 | Non-Goals 명시 |

---

## 9. 일정 (Session 3)

| 단계 | 산출물 |
|------|--------|
| Rule | R1/R2 문서화 (`docs/rule_magic_square_validation.md` 또는 워크북 SSOT) |
| Red | `tests/test_validate_lines.py` — D-001~D-003 FAIL |
| Green | `src/validate_lines.py` 최소 구현 |
| Refactor | 중복 제거, `failed_lines` 정리 |
| Skill | 10축 체크리스트 초안 |

---

## 10. 참조

| 문서 | 경로 |
|------|------|
| Problem Definition | `Report/01.MagicSquare_ProblemDefinition_Report.md` |
| Mom Test STEP 1 (2차) | `Report/01. MagicSquare_1004 Mom Test STEP1 보고서 (2차).md` |
| Mom Test 질문 10개 | `Report/02. MagicSquare_1004 Mom Test 질문 10개 보고서.md` |
| Session 3 워크북 | `Report/03. MagicSquare_1004 Session 3 워크북.md` |
| Cursor 규칙 | `.cursorrules` |
