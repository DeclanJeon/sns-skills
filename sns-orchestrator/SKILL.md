---
name: sns-orchestrator
description: Use when an SNS or YouTube request needs one or more skills from the SNS skill library routed or combined - channel growth planning, Korean AI drama/story video packaging (title, thumbnail, hook, script, series, shorts), or SNS comments/replies - and it is unclear which skill applies (SNS 스킬 연결, 조합, 어떤 스킬 써야 해, 유튜브 영상 패키지 만들어줘, SNS 운영 전체).
---

# SNS 오케스트레이터

SNS 스킬 라이브러리의 **라우터이자 조합기**다. 직접 콘텐츠 규칙을 갖지 않고, 요청을 분류해 아래 스킬을 순서대로 읽고 적용한다. 규칙은 각 스킬이 정본이며 여기에 복제하지 않는다.

라이브러리 루트: `/home/declan/Documents/Projects/Products/04_Skills/Skills-and-Automation/SNS/`
(스킬은 `<루트>/<이름>/SKILL.md`. Pi에 이미 등록된 스킬은 이름으로 로드, 아니면 이 경로를 `read`.)

데이터 정본: `<루트>/data/youtube-kr/` (README.md 참조). `kr-yt-*`의 근거 CSV·자막·썸네일이 여기 있다.

## 1. 라우팅 표

| 요청 신호 | 사용 스킬 |
|---|---|
| 플랫폼 팔로워 성장·정체 진단 | `youtube-growth-playbook` / `instagram-growth-playbook` / `threads-growth-playbook` / `tiktok-growth-playbook` / `x-growth-playbook` |
| 유튜브 수요조사, 다음 영상 선정 | `youtube-growth-playbook` |
| AI 드라마·사연 영상 제목 | `kr-yt-title` |
| 썸네일 기획·문구·프롬프트 | `kr-yt-thumbnail` |
| 클릭/도입부/클리프행어 | `kr-yt-hook` |
| 에피소드 대본·비트시트 | `kr-yt-script-structure` |
| 시리즈명·회차·몰아보기·재생목록 | `kr-yt-series-packaging` |
| 쇼츠·클립 변환 | `kr-yt-shorts-clip` |
| X/Threads 댓글·답글 | `sns-comment-writing` |
| 릴스·인스타·스레드·틱톡 캡션/제목/자막 문안 | `persona-social-writing`(문안 정본) + 해당 플랫폼 growth-playbook(전략). 전용 `kr-yt-*` 같은 데이터 기반 규칙은 없음을 밝힌다 |
| 이미 완성된 영상의 다채널 업로드·홍보 | 별도 `sns-launch-orchestrator` (이 스킬이 대체하지 않음) |
| 한서윤 캐릭터 계정 | `han-seoyun-*`, `persona-social-writing` (해당 전용 스킬 우선) |

한 요청이 여러 신호를 가지면 아래 조합 레시피를 쓴다. 해당 없으면 가장 가까운 단일 스킬 + 한 줄로 이유를 말한다. 라이브러리에 없는 영역(예: 릴스 캡션)은 없다고 말하고 임의 규칙을 만들지 않는다.

## 1.5 시작 전 입력 확인

레시피 A·C·E는 **줄거리/갈등/반전 한 줄**이 없으면 시작할 수 없다. 없으면 이것만 한 번 묻는다("누가 무엇을 당하고 무엇이 뒤집히나요?"). 시리즈명·플랫폼은 추정 가능하면 묻지 않고 가정을 밝힌다.
요청이 모호하면(예: "SNS 운영 도와줘") 플랫폼 하나와 목표(성장/제작/업로드)만 묻고 라우팅한다.

## 2. 조합 레시피

자세한 입출력 전달은 `references/recipes.md`.

- **A. 에피소드 패키지** ("이 영상 제목·썸네일 만들어줘"): `kr-yt-hook`(코어 한 문장) → `kr-yt-title` → `kr-yt-thumbnail` → 정합성 점검.
- **B. 신작 시리즈 기획**: `youtube-growth-playbook`(수요) → `kr-yt-series-packaging` → `kr-yt-script-structure`(1화) → 레시피 A.
- **C. 본편 → 쇼츠 확장**: `kr-yt-script-structure`(정점 장면 선택) → `kr-yt-shorts-clip` → `kr-yt-title`(쇼츠 제목 규칙은 shorts-clip 우선).
- **D. 채널 진단→실험**: 플랫폼 growth-playbook → 약한 지점에 맞는 `kr-yt-*` 1~2개 → 실험 1개.
- **E. 통합 검수**: 초안 제목+썸네일 문구+도입부를 받아 hook 정합성 3점 → title 점검(`kr-yt-title/scripts/title_lint.py`) → thumbnail 모바일 검수 순.

## 3. 실행 규칙

1. 요청을 분류하고 **사용할 스킬과 순서를 한 줄로 먼저 알린다**(예: "hook → title → thumbnail").
2. 각 스킬의 SKILL.md를 실제로 읽은 뒤 적용한다. 기억으로 대체하지 않는다.
3. 충돌 시 우선순위: 전용(캐릭터·플랫폼) 스킬 > 장르 스킬(`kr-yt-*`) > growth-playbook 일반론. 제목·썸네일 문구는 같은 문장 반복 금지(역할 분리).
4. 단계 사이에 **코어 훅 한 문장**을 공통 기준으로 넘긴다. 단계 결과가 이 문장과 어긋나면 되돌린다.
5. 범위 밖 요청(롱폼 일반 장르, 썸네일 이미지 실제 생성 등): 라이브러리에 없음을 먼저 말하고 가장 가까운 스킬(growth-playbook, `higgsfield-youtube-thumbnail` 등 별도 스킬)을 **제안**만 한다. `kr-yt-*` 규칙을 다른 장르로 확장해 적용하지 않는다.
6. `kr-yt-*`는 한국 AI 드라마·사연 장르 전용이다. 다른 장르(먹방, 경제 등)에는 growth-playbook만 쓰고 한계를 알린다.
7. 데이터 근거와 한계(상관관계, 유지율 없음)를 각 스킬이 명시한 대로 최종 답에 유지한다.
8. 게시·계정 변경·유료 생성은 하지 않는다. 필요하면 해당 전용 스킬/사용자 승인으로 넘긴다.

## 4. 최종 출력

사용한 스킬 순서 / 산출물(스킬별 섹션) / 코어 훅과의 정합성 확인 / 미해결·검증 필요 항목.

## 5. 라이브러리 유지

새 스킬을 SNS 폴더에 추가하면 이 파일의 라우팅 표와 `references/recipes.md`에 한 줄을 추가한다. 정본은 이 폴더이며 `~/.agents/skills/`의 `sns-orchestrator`와 `kr-yt-*` 6개는 모두 이 폴더를 가리키는 심볼릭 링크다. 수정은 이 폴더에서만 한다.
