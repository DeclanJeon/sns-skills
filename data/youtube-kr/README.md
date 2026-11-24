# youtube-kr 수집 데이터

한국 YouTube 영상 수집본. `kr-yt-*` 스킬의 근거 데이터. 정본은 이 폴더(원본 작업 폴더 `~/Documents/SNS/`는 작업용 사본).

- `youtube_korean_collection_300.csv`: 300개(AI 드라마 119 / 드라마·사연 42 / 일반 139), 썸네일 파일 `thumb_file` 컬럼
- `youtube_ai_channel_videos.csv`: AI 드라마 채널 25개의 영상 961개
- `youtube_ai_shorts.csv`: AI 채널 쇼츠 241개 (드라마 무관 채널 `@jjflight`, `@bomulsum_g` 포함)
- `youtube_ai_raw.csv`, `youtube_korean_1m_raw.csv`: 중간 수집 원본
- `yt_transcripts/<video_id>.md`: 자동 자막 77개 (고유명사 오류 있음)
- `yt_thumbs/<video_id>.jpg`: 썸네일 300개
- `scripts/`: 수집 스크립트 (yt-dlp, flucto 사용). 스크립트 내부 경로는 작업 폴더 기준이라 재실행 시 cwd를 이 폴더로 맞출 것.

한계: 유지율·CTR 없음, 조회수는 수집 시점 누적값, 자막은 자동 생성.
