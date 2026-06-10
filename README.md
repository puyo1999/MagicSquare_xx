# MagicSquare_xx

4×4 부분 마방진(빈칸 2개, 합 34) OO 과제 **4.1 Magic Square** 를 Mom Test → Problem Definition → Session 3 TDD로 진행하는 저장소입니다.

**진짜 문제 (Mom Test 2차 SSOT):** 손으로 풀 때 **행 합 34만**으로 후보를 좁히다 **열·대각선은 넣어 본 뒤에야** 확인하고, **맞을 때까지 바꿔 넣으며** 약 **25분**을 쓴다.

**Session 3 목표:** Solver·UI 이전에 **`validate_lines`** Command와 **10축(행 4·열 4·대각 2) 합=34** 판정을 Rule · Test Loop로 고정한다. 이후 **entity Logic Track**·**boundary UI Track**으로 Dual-Track 확장.

---

## 진행 상태

| 단계 | 상태 | 비고 |
|------|------|------|
| Mom Test STEP 1 (2차) | ✅ | `Report/01.* (2차)` |
| Mom Test 질문 10개 | ✅ | `Report/02.*` |
| Problem Definition | ✅ | `Report/01.MagicSquare_ProblemDefinition_Report.md` |
| Session 3 워크북 | ✅ | `Report/03.*` |
| PRD v0.2 | ✅ | `docs/PRD.md` |
| Command `validate_lines` | 🟡 부분 GREEN | D-001 PASS · D-002 / incomplete / D-003 **미커버** |
| entity Logic Track | 🟡 부분 GREEN | D-LOC-01 · D-SOL-01 PASS (`Report/05.*`) |
| boundary UI Track | 🔴 RED (계획) | **현재 묶음: U-IN-01, U-IN-02** — `tests/boundary/` 미착수 |

```powershell
python -m pytest tests/ -v   # 현재: entity 2 + D-001 (3 passed 기준)
```

---

## Dual-Track 요약

| Track | Layer | 테스트 ID | 파일 패턴 | Then (기대값) | Domain Mock |
|-------|-------|-----------|-----------|---------------|-------------|
| **Logic** | `entity`, `control` | `D-*` | `tests/entity/`, `tests/control/` | 도메인 결과 (`failed_lines`, 좌표 등) | **금지** |
| **Boundary** | `boundary` | `U-*` | `tests/boundary/` | **E001~E007** 코드 | 허용 |

**공통 금지 (RED):** GREEN 전 `src/` 수정 · `skip`/`xfail` · assert 완화 · entity에서 **E001~E005 emit**.

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

### Command Test Loop — 다음 RED 후보 (PRD C2C)

| # | Test ID | Given → Then (요약) |
|---|---------|---------------------|
| 1 | **D-002 / FC-1** | 4행=34, **한 열 ≠34** → `status=fail`, `"C*"` in `failed_lines` |
| 2 | **incomplete** | G1 등 빈칸(`0`) 1개 이상 → `status=incomplete`, `failed_lines=[]` |
| 3 | **D-002 / FC-2** | 행·열=34, **D1 ≠34** → `status=fail`, `"D1"` in `failed_lines` |

---

## RED 계획 — entity Logic Track

`Phase: red | Layer: entity | Track: Logic` · 묶음: **D-LOC-01 (FR-LOC-01)** ~ **D-LOC-03**

**FR-LOC-01 (확정안, PRD 상위: DR-5 · §3.2 · DR-1):** 4×4 `grid`에서 `0`인 칸의 **1-index (row, col)** 를 **row-major** 순으로 반환 (`find_blank_coords`).

| Test ID | Given | Then | Expected RED Failure |
|---------|-------|------|----------------------|
| **D-LOC-01** | `grid_g1` (OO 4.1, 빈칸 (2,3)·(4,4)) | `[(2, 3), (4, 4)]` | ✅ GREEN (`src/find_blank_coords.py`) |
| **D-LOC-02** | `grid_g2` (빈칸 (2,2)·(4,3)) | `[(2, 2), (4, 3)]` | `AssertionError` (G1 하드코딩 방지) |
| **D-LOC-03** | `grid_g3` (빈칸 (1,4)·(3,1), 스캔 순서) | `[(1, 4), (3, 1)]` | `AssertionError` (정렬·역순 오류) |

| 항목 | 내용 |
|------|------|
| 파일 | `tests/entity/test_d_loc_01.py` |
| fixture | `tests/conftest.py` — `grid_g1` · `grid_g2` · `grid_g3` (데이터만) |
| pytest | `python -m pytest tests/entity/test_d_loc_01.py -v` |
| 다음 | `/red-skeleton` (D-LOC-02·03 추가) |

---

## RED 계획 — boundary UI Track (현재 묶음)

`Phase: red | Layer: boundary | Track: UI` · 묶음: **U-IN-01, U-IN-02**

**FR-UI-IN-01 (확정안, PRD 상위: FR-1 · DR-1):** boundary `InputHandler`는 `grid`가 `None`이면 **`E003`**, 4×4가 아니면 **`E001`**을 반환하고 control·entity로 전달하지 않는다.

| Test ID | Given | Then | Expected RED Failure |
|---------|-------|------|----------------------|
| **U-IN-01** | `grid=None` | **`E003`** `INVALID_NULL` | `ModuleNotFoundError` / `ImportError` |
| **U-IN-02** | `grid` = **3×4** (DR-1 위반) | **`E001`** `INVALID_SIZE` | `AssertionError` 또는 `ImportError` |

| 항목 | 내용 |
|------|------|
| 파일 | `tests/boundary/test_u_input_validation.py` |
| 함수명 후보 | `test_u_in_01_grid_none_returns_e003` · `test_u_in_02_grid_wrong_size_returns_e001` |
| pytest | `python -m pytest tests/boundary/test_u_input_validation.py::test_u_in_01_grid_none_returns_e003 -v` |
| 다음 | `/red-skeleton` |

**U-IN-02 Arrange (3×4):**

```python
grid_3x4 = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
```

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

## 프로젝트 구조

```
MagicSquare_xx/
├── README.md
├── .cursorrules
├── pyproject.toml
├── docs/
│   └── PRD.md
├── src/
│   ├── validate_lines.py          # Command — 10축 판정
│   ├── find_blank_coords.py       # entity D-LOC-01
│   └── entity/
│       ├── constants.py
│       ├── solver_step.py         # D-SOL-01
│       └── validation.py          # 10선 line_sum · all_lines
├── tests/
│   ├── conftest.py                # grid_g1 (+ G2/G3 예정)
│   ├── test_validate_lines.py     # D-001
│   ├── entity/
│   │   ├── test_d_loc_01.py       # D-LOC-01
│   │   └── test_d_sol_01.py       # D-SOL-01 + Golden
│   ├── golden/
│   └── boundary/                  # U-IN-01~02 예정
├── Report/
│   ├── 03.* Session 3 워크북
│   └── 05.* entity Logic ARRR 1사이클
├── Prompting/
└── .cursor/commands/              # red-test-plan, tdd-red, green-minimal 등
```

---

## 문서

| 문서 | 설명 |
|------|------|
| [Problem Definition](Report/01.MagicSquare_ProblemDefinition_Report.md) | 페르소나 · 진짜/표면 문제 · 범위 |
| [PRD](docs/PRD.md) | FR/DR · D-001~D-003 · 성공 지표 |
| [Session 3 워크북](Report/03.%20MagicSquare_1004%20Session%203%20%EC%9B%8C%ED%81%AC%EB%B6%81.md) | R-G-I-O · SC-1~3 · Command 계약 |
| [entity ARRR 보고](Report/05.REPORT.md) | D-LOC-01 · D-SOL-01 · REFACTOR |
| [Dual-Track RED Planning](Report/06.%20MagicSquare_1004%20Dual-Track%20RED%20Planning%20%EB%B3%B4%EA%B3%A0%EC%84%9C.md) | D-LOC-02·03 · U-IN-01·02 Plan · README 갱신 |

**Prompting**

| 파일 | 내용 |
|------|------|
| `Prompting/05.Export-Transcript.md` | entity Logic Track ARRR Export |
| `Prompting/06. cursor_magic_square_1004_dual_track_red_planning.md` | Dual-Track RED Planning Export |

---

## TDD (ARRR)

| Phase | 수정 허용 | 슬래시 커맨드 |
|-------|-----------|---------------|
| **RED (Plan)** | 없음 (계획만) | `/red-test-plan` |
| **RED** | `tests/`만 | `/red-skeleton`, `/tdd-red` |
| **GREEN** | `src/` 최소 | `/green-minimal` |
| **Golden** | 없음 (기준선) | `/golden-master` |
| **REFACTOR** | `src/` (동작 동일) | `/refactor-safe` |

```powershell
pytest tests/test_validate_lines.py -v          # Command
pytest tests/entity/ -v                         # Logic entity
pytest tests/boundary/ -v                       # Boundary (예정)
```

---

## 브랜치 (참고)

| 브랜치 | 용도 |
|--------|------|
| `red` | TDD RED · entity/boundary 스켈레톤 |
| `main` | 기본 브랜치 |
| `spec` | 문서·스펙 |
| `staging` | 통합·스테이징 |

---

## 범위 밖 (Non-Goals)

- 빈칸 **후보군** 자동화 (24분 구간) · “검증 앱” UX · 틀린 이유 설명
- GUI / PyQt (boundary는 **headless API** — `InputHandler` 등)
- ECB Integration 전체 · `SquareValidator` **클래스** 일괄 구현

---

## 라이선스 · 기여

OO 과제 / VIBECODING 학습용 프로젝트. 작성자: 김민주.
