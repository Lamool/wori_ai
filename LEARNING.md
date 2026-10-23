# 학습 노트

## 2026-10-23 · 나만의 스킬 만들기 (explain-back)

**핵심 개념**
- **CLAUDE.md vs 스킬**: 항상 읽는 규칙 vs 필요할 때 읽는 절차
- **description = 트리거**: 호출 전엔 description 만 보고 판단
- **스킬 vs hook**: Claude 가 판단해서 실행 vs 무조건 실행

**퀴즈**
| 문제 | 정답 | 결과 |
|------|------|:----:|
| "항상 `encoding='utf-8'` 쓰기" 규칙은 CLAUDE.md 와 스킬 중 어디에? | CLAUDE.md. 항상 지킬 짧은 규칙이라서 | X |
| 트리거 문장을 description 에서 본문으로 옮기면? | 자연어로 잘 호출되지 않음. 본문은 호출된 뒤에야 읽힘 | X |
| 커밋 전 테스트를 강제하고 실패하면 막으려면? | hook. "반드시·막는다"는 harness 가 실행해야 보장됨 | X |

**복습**
- 셋 중 고르는 기준: 상시 규칙 → CLAUDE.md / 필요할 때 절차 → 스킬 / 무조건 실행 → hook
- description 과 본문이 읽히는 시점의 차이

---

## 2026-10-23 · v01_14_while.py

**핵심 개념**
- **`while True` + `break`**: break 가 유일한 출구
- **`except ValueError`**: 적어 둔 종류의 오류만 잡음
- **타입 힌트**: 메모일 뿐, 실행 중에 검사 안 함

**퀴즈**
| 문제 | 정답 | 결과 |
|------|------|:----:|
| 13번 줄 `break` 를 지우고 5 를 입력하면? | 결과는 출력되지만 같은 질문을 무한 반복 (Ctrl+C 로만 종료) | X |
| 12번 줄의 문제와 `except ValueError` 가 못 잡는 이유는? | `user__meters` 오타 → NameError. except 는 ValueError 만 잡음 | X |
| `meters_to_feet("3")` 을 타입 힌트가 막아 줄까? | 못 막음. 곱셈에서 TypeError (문자열 × float 불가) | X |

**복습**
- except 가 잡는 오류 종류 구분 (ValueError / NameError / TypeError)
- while True 에서 break 의 역할
- 참고: 12번 줄 오타 아직 수정 안 함

---

## 2026-10-23 · v01_1_var_type.py

**핵심 개념**
- **리스트 vs 튜플**: 리스트는 수정 O, 튜플은 수정 X
- **set**: 중복 제거, 순서 없음 (`[0]` 불가)
- **`isinstance()`**: 실행 중에 진짜 타입 검사

**퀴즈**
| 문제 | 정답 | 결과 |
|------|------|:----:|
| `colors[0] = "blue"` 와 `coords[0] = 99` 중 오류 나는 것은? | `coords[0] = 99`. 튜플은 수정 불가 → TypeError | O |
| `nums = {3, 1, 2, 2}` 에서 `print(nums[0])` 이 문제인 이유는? | set 은 순서가 없어서 인덱스로 못 꺼냄 (덤: `len` 은 3) | O |
| `isinstance()` 로 문자열 입력을 막으려면? | `if not isinstance(meters, (int, float)): raise TypeError(...)` | △ |

**복습**
- 여러 타입 허용은 튜플로 묶기: `(int, float)`
- 확인만 하지 말고 `raise` 로 오류를 일으켜야 실제로 막힘

---

## 2026-10-23 · v01_11_def.py

**핵심 개념**
- **`def` vs 호출**: def 는 만들기만, 호출해야 실행
- **`print` vs `return`**: return 이 없으면 None 을 돌려줌
- **타입 힌트와 docstring**: 사용 설명서일 뿐, 막으려면 직접 검사

**퀴즈**
| 문제 | 정답 | 결과 |
|------|------|:----:|
| 14~16번 호출 줄을 모두 지우면 무엇이 출력될까? | 아무것도 출력 안 됨. def 는 정의만 함 | X (힌트) |
| `result = good_sentence("GOOD")` 후 `print(result)` 의 마지막 출력은? | 큰 글씨 GOOD 다음에 None | X (힌트) |
| `good_sentence(123)` 을 막는 코드는? | `if not isinstance(sentence, str): raise TypeError(...)` | X (힌트) |

**복습**
- 함수 정의와 호출의 차이
- return 이 없는 함수는 None 을 돌려줌
- `isinstance` + `raise` 패턴 (두 번째 다시 보기)
- 참고: 현재 Python(anaconda3)에 pyfiglet 미설치

---

## 2026-10-23 · 스킬 플러그인 배포 (explain-back-skill)

**핵심 개념**
- **플러그인 포장 구조**: marketplace.json → plugin.json → SKILL.md
- **로컬 vs GitHub marketplace**: 로컬은 원본 직접, GitHub 는 clone 복사본
- **나라서 되는 것 vs 누구나 되는 것**: 내 PC 성공엔 로그인 정보가 섞임

**퀴즈**
| 문제 | 정답 | 결과 |
|------|------|:----:|
| `explain-back@explain-back-skill` 에서 @ 앞과 뒤는 각각 무엇의 이름? | 앞은 플러그인, 뒤는 marketplace (`플러그인@marketplace`) | X (힌트) |
| 커밋만 하고 push 안 하면 내 PC 새 세션과 친구 PC 에서 보일까? | 내 PC 는 보임 (원본 폴더 직접 읽음), 친구는 안 보임 | △ |
| 내 PC 설치 성공 후 친구에게 공유 전 확인할 것은? | 로그인 없이 받을 수 있는지(public) 확인, 친구에게 실제 설치 부탁 | △ |

**복습**
- 설치 명령 형식: `/plugin install 플러그인@marketplace`
- 로컬 marketplace 는 저장만 해도 반영, 다른 사람은 push + version 올리기 + update
- "업로드했다"와 "누구나 받을 수 있다"는 다름 (public 여부)

---
