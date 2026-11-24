# 조합 레시피 상세 (스킬 간 전달 값)

## A. 에피소드 패키지
입력: 에피소드 줄거리/갈등/반전, 시리즈명(있으면).
1. kr-yt-hook → 코어 한 문장, 훅 유형 1개.
2. kr-yt-title → 후보 5개(공식 2~3개), title_lint 실행. 시리즈면 kr-yt-series-packaging의 제목 템플릿 고정.
3. kr-yt-thumbnail → 문구 2줄(제목과 다른 문장), 구도, 프롬프트, 모바일 검수.
4. 점검: 제목·썸네일·도입부(첫 30초)가 같은 약속인가. 아니면 2~3 재작업.
출력: 코어 문장 / 제목 3안 / 썸네일 안 / 도입부 15초 비트.

## B. 신작 시리즈 기획
1. youtube-growth-playbook → 수요·기회 가설 1개.
2. kr-yt-series-packaging → 시리즈명, 제목·썸네일 템플릿, 몰아보기 시점.
3. kr-yt-script-structure → 1화 비트시트(0~10초 갈등 대사).
4. 레시피 A로 1화 패키지.

## C. 본편 → 쇼츠
1. kr-yt-script-structure의 비트에서 갈등 정점~반전 직전 구간 3~5개 선정.
2. kr-yt-shorts-clip → 클립별 제목(`~한다면?`/`~한 이유` + 시리즈명 화), 첫 프레임.
3. 결말 비공개, 본편 유도.

## D. 채널 진단→실험
1. 플랫폼 growth-playbook 진단 → 병목(노출/클릭/유지/팔로우 전환).
2. 병목→스킬: 클릭=title/thumbnail, 유지=hook/script-structure, 지속 시청=series-packaging, 신규 유입=shorts-clip.
3. 변수 1개만 바꾸는 실험 설계, 지표 명시.

## E. 통합 검수
입력: 제목, 썸네일 문구, 도입부 대사.
출력: 항목별 PASS/약함 + 수정안 1개씩. 판정은 각 스킬 기준을 인용.
