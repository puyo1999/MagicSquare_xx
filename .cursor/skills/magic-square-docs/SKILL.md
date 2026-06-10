---
name: magic-square-docs
description: >-
  MagicSquare_xx Session 보고서·Prompting Transcript Export·10축 체크리스트 작성.
  Report/·Prompting/ 저장, export-session 형식, Mom Test·워크북 SSOT 정렬 시 적용.
---

# MagicSquare Docs · Export

Session 3 산출물을 **Report/**(보고) · **Prompting/**(Transcript)에 맞춰 저장한다. 코드 구현·pytest·git commit은 사용자가 명시할 때만.

## 저장 규칙

| 종류 | 경로 | 파일명 패턴 |
|------|------|-------------|
| 보고서 | `Report/` | `NN. MagicSquare_1004 <제목>.md` |
| Transcript | `Prompting/` | `NN. cursor_magic_square_1004_<slug>.md` |
| 체크리스트 | `Report/` 또는 `docs/` | 워크북·Skill 부록 |

번호 `NN`은 세션·단계 SSOT에 맞춤 (예: Session 3 → `03`).

## Export 절차 (export-session SSOT)

사용자가 세션 Export를 요청하거나 REFACTOR 완료 후 문서화할 때:

1. **대화 요약** — User 요청·Cursor 조치·pytest 결과·Phase 이력을 시간순으로 정리.
2. **보고서** — `templates/report-session-template.md` 채워 `Report/`에 저장.
3. **Transcript** — `templates/transcript-export-template.md` 채워 `Prompting/`에 저장.
4. **체크리스트** — 필요 시 `templates/checklist-10axis-template.md`를 Report 부록 또는 `docs/`에 저장.
5. 저장 경로를 응답에 **전체 경로**로 명시.

Transcript 첫머리 형식 (고정):

```markdown
# <제목>
_Exported on <YYYY-MM-DD> from Cursor_
```

## SSOT 정렬

문서 본문은 다음과 **모순 없이** 맞춘다:

- `docs/PRD.md` — FR/DR · D-001~D-003
- `Report/03. MagicSquare_1004 Session 3 워크북.md` — R-G-I-O · SC-1~3 · Command 계약
- `.cursorrules` — Phase · 파일 역할

**Non-Goals 반복 금지 과다** — 표면 문제 표는 워크북 §4 수준으로 유지.

## 10축 Skill 체크리스트 (FR-15)

학습자 행동 규칙 (자동화 아님):

1. 행 합 34만으로 완료 판단하지 않는다.
2. **16칸 완성** 확인 후 `validate_lines` 호출.
3. `failed_lines`에 **R1~R4 · C1~C4 · D1 · D2** 중 무엇이 깨졌는지 본다.
4. 빈칸(`0`)이 있으면 `incomplete` — 10축 판정 보류.
5. 중복·범위는 **R2 / D-003** — `validate_lines`만으로 판단하지 않는다.

템플릿: `templates/checklist-10axis-template.md`

## 템플릿 위치

| 파일 | 용도 |
|------|------|
| `templates/report-session-template.md` | Report 보고서 골격 |
| `templates/transcript-export-template.md` | Prompting Export 골격 |
| `templates/checklist-10axis-template.md` | 10축 검증 체크리스트 |

## 기존 Export 참고

- `Prompting/01. cursor_magic_square_1004_mom_test_step1_2nd.md`
- `Prompting/03. cursor_magic_square_1004_session3_workbook.md`

## 금지

- SSOT 없이 Command 계약·status 의미 변경
- Solver·UI·ECB를 Session 3 완료 산출로 기술
- 사용자 확인 없이 git commit/push (명시 요청 시만)
