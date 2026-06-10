# MagicSquare_xx

4×4 부분 마방진(빈칸 2개, 합 34) OO 과제 **4.1 Magic Square** 를 Mom Test → Problem Definition → Session 3 TDD로 진행하는 저장소입니다.

**진짜 문제 (Mom Test 2차 SSOT):** 손으로 풀 때 **행 합 34만**으로 후보를 좁히다 **열·대각선은 넣어 본 뒤에야** 확인하고, **맞을 때까지 바꿔 넣으며** 약 **25분**을 쓴다.

**Session 3 목표:** Solver·UI 이전에 **`validate_lines`** Command와 **10축(행 4·열 4·대각 2) 합=34** 판정을 Rule · Test Loop로 고정한다.

---

## 진행 상태

| 단계 | 상태 | 비고 |
|------|------|------|
| Mom Test STEP 1 (2차) | ✅ | `Report/01.* (2차)` |
| Mom Test 질문 10개 | ✅ | `Report/02.*` |
| Problem Definition | ✅ | `Report/01.MagicSquare_ProblemDefinition_Report.md` |
| Session 3 워크북 | ✅ | `Report/03.*` |
| PRD v0.2 | ✅ | `docs/PRD.md` |
| TDD (`validate_lines`) | 🔴 RED | `src/` 스텁 · `tests/` 스켈레톤 |

---

## 빠른 시작

```powershell
cd MagicSquare_xx
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install pytest
pytest tests/ -v
```

---

## Command API (Session 3)

```python
from src.validate_lines import validate_lines

result = validate_lines(grid)  # 4×4, 0=빈칸, 1~16=채움
# {"status": "pass" | "fail" | "incomplete", "failed_lines": ["R1", "C2", "D1", ...]}
```

| `status` | 의미 |
|----------|------|
| `incomplete` | 빈칸(`0`) 존재 — 10축 판정 보류 |
| `pass` | 16칸 완성 + 10축 모두 합 34 |
| `fail` | 16칸 완성인데 일부 축 합 ≠ 34 |

10축 ID: 행 **R1~R4**, 열 **C1~C4**, 대각 **D1**(주), **D2**(반).  
셀 무결성(중복·범위)은 Rule **R2** · Test **D-003** (`validate_lines` 밖).

---

## 프로젝트 구조

```
MagicSquare_xx/
├── README.md
├── .cursorrules              # Session 3 · TDD · validate_lines SSOT
├── pyproject.toml
├── docs/
│   └── PRD.md                # 제품 요구사항 v0.2
├── src/
│   └── validate_lines.py     # Command (GREEN 대상)
├── tests/
│   └── test_validate_lines.py
├── Report/
│   ├── 01. MagicSquare_1004 Mom Test STEP1 보고서 (2차).md
│   ├── 01.MagicSquare_ProblemDefinition_Report.md
│   ├── 02. MagicSquare_1004 Mom Test 질문 10개 보고서.md
│   └── 03. MagicSquare_1004 Session 3 워크북.md
├── Prompting/                # Cursor Transcript Export
└── .cursor/commands/         # tdd-red 등
```

---

## 문서

| 문서 | 설명 |
|------|------|
| [Problem Definition](Report/01.MagicSquare_ProblemDefinition_Report.md) | 페르소나 · 진짜/표면 문제 · 범위 |
| [PRD](docs/PRD.md) | FR/DR · D-001~D-003 · 성공 지표 |
| [Mom Test STEP1 (2차)](Report/01.%20MagicSquare_1004%20Mom%20Test%20STEP1%20%EB%B3%B4%EA%B3%A0%EC%84%9C%20(2%EC%B0%A8).md) | 인터뷰 증거 · Q&A |
| [Mom Test 질문 10개](Report/02.%20MagicSquare_1004%20Mom%20Test%20%EC%A7%88%EB%AC%B8%2010%EA%B0%9C%20%EB%B3%B4%EA%B3%A0%EC%84%9C.md) | Mom Test 준수/위반 질문 세트 |
| [Session 3 워크북](Report/03.%20MagicSquare_1004%20Session%203%20%EC%9B%8C%ED%81%AC%EB%B6%81.md) | R-G-I-O · SC-1~3 · Command 계약 |

**Prompting (Transcript)**

| 파일 | 내용 |
|------|------|
| `Prompting/01.*_step1_2nd.md` | Mom Test 2차 인터뷰 |
| `Prompting/02.*_questions_10.md` | 질문 10개 세션 |
| `Prompting/03.*_session3_workbook.md` | Session 3 워크북 |

---

## TDD (Session 3)

| Phase | 수정 허용 | 목표 |
|-------|-----------|------|
| **RED** | `tests/`만 | D-001~D-003 **FAIL** |
| **GREEN** | `src/` 최소 구현 | pytest **PASS** |
| **REFACTOR** | 정리 (동작 유지) | 회귀 없음 |

```powershell
pytest tests/test_validate_lines.py -v
```

Cursor 슬래시 커맨드: `.cursor/commands/tdd-red.md`

---

## 브랜치 (참고)

| 브랜치 | 용도 |
|--------|------|
| `spec` | 문서·스펙·Session 3 설계 |
| `main` | 기본 브랜치 |
| `staging` | 통합·스테이징 |

---

## 범위 밖 (Non-Goals)

- Solver · MissingFinder · 빈칸 후보 자동화 (24분 구간)
- GUI · ECB Boundary 전체 · `SquareValidator` 클래스
- “검증 앱” UX · 틀린 이유 설명

---

## 라이선스 · 기여

OO 과제 / VIBECODING 학습용 프로젝트. 작성자: 김민주.
