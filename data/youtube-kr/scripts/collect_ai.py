import subprocess, json, re, csv
from concurrent.futures import ThreadPoolExecutor
qs=["AI 드라마","AI 드라마 몰아보기","AI 드라마 풀버전","AI 숏드라마","AI 사극","AI 조선 드라마","AI 복수극","AI 사이다 복수","AI 시니어 드라마","AI 사연 드라마","AI 감동 사연","AI 시어머니","AI 며느리","AI 재벌","AI 회귀","AI 로맨스","AI 판타지 드라마","AI 단편영화","AI 영화 풀버전","AI 시리즈 1화","AI 시리즈 에피소드","AI로 만든 영화","AI 제작 웹드라마","AI 무협","AI 좀비","AI 공포 단편","AI 괴담","AI 막장","AI 불륜 복수","AI 이혼","AI 아버지 감동","AI 엄마 감동","AI 할머니 사연","AI 할아버지 사연","AI 반전 실화","AI 실화 사연 영상","AI 영상툰","AI 애니메이션 시리즈 한국","AI 웹툰 영상","AI 타임슬립","AI 군대 드라마","AI 학교 드라마","AI 학폭 복수","AI 직장 갑질 사이다","AI 재벌 며느리","AI 숏폼 드라마","AI 감성 단편","AI 뮤직비디오","AI 가족 드라마","AI 첫사랑","AI 스릴러","AI 미스터리 드라마","AI 사극 로맨스","AI 장군","AI 전쟁 영화 한국","AI 고구려","AI 임진왜란","AI 외계인 드라마","AI 포스트아포칼립스","AI 능력자","AI 먼치킨","AI 시니어 로맨스","AI 인생 이야기 70대","AI 노년 사연","AI 효도","AI 반전 드라마","Veo3 드라마","Sora 드라마","Kling AI 드라마","Seedance 드라마","나노바나나 드라마","런웨이 AI 단편","AI 생성 영상 드라마 한국","인공지능 드라마 제작","AI 단편 애니","AI 3D 애니 드라마","AI 영화 예고편","AI 공포영화"]
def run(q):
    try:o=subprocess.run(["yt-dlp","--flat-playlist","--dump-json",f"ytsearch50:{q}"],capture_output=True,text=True,timeout=180).stdout
    except Exception:return []
    out=[]
    for l in o.splitlines():
        try:out.append((q,json.loads(l)))
        except:pass
    return out
AI=re.compile(r"(\bAI\b|에이아이|인공지능|veo|sora|kling|seedance|AI드라마)",re.I)
seen={}
with ThreadPoolExecutor(6) as ex:
    for res in ex.map(run,qs):
        for q,j in res:
            vid=j.get("id");v=j.get("view_count") or 0
            t=j.get("title") or "";d=j.get("description") or "";c=j.get("channel") or ""
            if not vid or v<150_000 or vid in seen: continue
            if not re.search(r"[가-힣]",t+c+d): continue
            if not AI.search(t+" "+d+" "+c): continue
            seen[vid]=dict(video_id=vid,url=f"https://www.youtube.com/watch?v={vid}",title=t,channel=c,channel_handle=j.get("uploader_id"),view_count=v,duration_sec=j.get("duration"),format="shorts" if (j.get("duration") or 999)<=61 else "long",category="ai_video",found_by_query=q,thumbnail_url=f"https://i.ytimg.com/vi/{vid}/maxresdefault.jpg")
rows=sorted(seen.values(),key=lambda r:-r["view_count"])
with open("youtube_ai_raw.csv","w",newline="",encoding="utf-8-sig") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print(len(rows),sum(r["view_count"]>=1e6 for r in rows))
for r in rows[:400]:print(r["view_count"],r["channel"][:20],"|",r["title"][:55])
