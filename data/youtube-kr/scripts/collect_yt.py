import subprocess, json, re, csv, sys
from concurrent.futures import ThreadPoolExecutor
Q = {
 "ai_drama": ["AI 드라마","AI 단편 드라마","AI 영화 한국","AI 숏드라마","AI로 만든 드라마","AI 웹드라마","AI 시니어 사연 드라마","AI 막장 드라마","AI 복수극","AI 로맨스 드라마","AI 사극 드라마","AI 시간여행 조선","AI 감동 사연 영상","AI 영상 사연 반전","AI 가족 드라마 사연","AI 시어머니 며느리 사연","AI 판타지 웹툰 영상","AI 좀비 영화","AI 공포 영상 한국","AI 단편영화 수상","AI 뮤직비디오 한국","AI 애니메이션 한국 시리즈","AI 로맨스 숏폼","AI 재벌 드라마","AI 이혼 사연 드라마"],
 "drama_story": ["숏드라마","웹드라마 풀버전","사이다 복수 드라마","시어머니 사연 드라마","재벌 로맨스 숏드라마","막장 사연 드라마","감동 실화 사연 영상","노년 사연 드라마 반전","실화 사연 라디오","엄마 감동 사연"],
 "viral_general": ["조회수 천만 한국","한국 유튜브 인기 영상 100만","한국 쇼츠 인기","미스터리 이야기 한국 유튜브","썰 풀이 유튜브 한국","역사 이야기 유튜브 한국","경제 이슈 분석 유튜브","건강 정보 유튜브 시니어","재테크 유튜브 한국","먹방 한국 유튜브","실험 챌린지 한국 유튜브","브이로그 한국 인기","다큐 한국 유튜브 이슈","사건 사고 정리 유튜브","연예 이슈 유튜브 한국","동물 영상 한국 유튜브","커플 몰카 한국","콩트 한국 유튜브","예능 클립 한국","공포 괴담 유튜브 한국","전쟁 군사 유튜브 한국","과학 상식 유튜브 한국","여행 한국 유튜브 인기","자동차 리뷰 유튜브 한국","요리 레시피 유튜브 한국","운동 다이어트 유튜브 한국","심리학 유튜브 한국","북한 이야기 유튜브","부자 스토리 유튜브","국뽕 유튜브 한국"],
}
def run(a):
    cat,q=a
    try:
        o=subprocess.run(["yt-dlp","--flat-playlist","--dump-json",f"ytsearch50:{q}"],capture_output=True,text=True,timeout=180).stdout
    except Exception: return []
    r=[]
    for l in o.splitlines():
        try:j=json.loads(l)
        except: continue
        r.append((cat,q,j))
    return r
jobs=[(c,q) for c,qs in Q.items() for q in qs]
seen={}
with ThreadPoolExecutor(6) as ex:
    for res in ex.map(run,jobs):
        for cat,q,j in res:
            vid=j.get("id"); v=j.get("view_count") or 0
            if not vid or v<1_000_000: continue
            if not re.search(r"[가-힣]",(j.get("title") or "")+(j.get("channel") or "")): continue
            if vid in seen: continue
            seen[vid]=dict(video_id=vid,url=f"https://www.youtube.com/watch?v={vid}",title=j.get("title"),channel=j.get("channel"),channel_handle=j.get("uploader_id"),view_count=v,duration_sec=j.get("duration"),format="shorts" if (j.get("duration") or 999)<=61 else "long",category=cat,found_by_query=q,thumbnail_url=f"https://i.ytimg.com/vi/{vid}/maxresdefault.jpg")
rows=sorted(seen.values(),key=lambda r:-r["view_count"])
with open("youtube_korean_1m_raw.csv","w",newline="",encoding="utf-8-sig") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
from collections import Counter
print(len(rows),Counter(r["category"] for r in rows),Counter(r["format"] for r in rows))
