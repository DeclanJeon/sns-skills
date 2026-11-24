import csv,re,json,subprocess,urllib.request,os
from concurrent.futures import ThreadPoolExecutor
rd=lambda f:list(csv.DictReader(open(f,encoding="utf-8-sig")))
ai=rd("youtube_ai_raw.csv"); gen=rd("youtube_korean_1m_raw.csv")
MADE=re.compile(r"(AI\s?(드라마|단편|영화|숏|웹드라마|시트콤|사극|시리즈|판타지|BL|Drama|Film|Short|Cinema|Fantasy|애니|웹툰|Studio|Comic)|AI\s?(Fantasy\s)?Drama|AI\s?BL|#ai|\[AI|\bAI\]|100% AI|AI드라마|AI 숏폼|에이아이드라마|AI Cinema|AI Studio|AI박스|AI Drama)",re.I)
BAD=re.compile(r"(튜토리얼|tutorial|how to|강연|세바시|뉴스|News|SBS|KBS|MBC|JTBC|뉴스|강의|Lec|Guide|가이드|제작비 100만원|ChatGPT|SNL|개그콘서트|추적60분|따라하|AI 렌즈|AI 안경 출시|효도봇|무기로|AI가 (알려|시키|아무)|무서운 이야기 해달라|Essentials)",re.I)
sel=[]
for r in ai:
    s=r["title"]+" "+r["channel"]
    if (MADE.search(s) or re.search(r"AI",r["channel"])) and not BAD.search(s): sel.append(r)
for r in sel:r["category"]="ai_made_drama_film"
ids={r["video_id"] for r in sel}
MV=re.compile(r"(HYBE|Mnet|MEOMURU|MV\]|M/V|Official MV|ERRDAY|조선힙합|심통봇|국악|스타크래프트|Fantasoner|SORAGAE)",re.I)
g=[r for r in gen if r["video_id"] not in ids and not MV.search(r["title"]+r["channel"])]
# drop AI-topic noise in general
g=[r for r in g if not re.search(r"\bAI\b",r["title"])]
need=300-len(sel)
g=g[:need]
for r in g:r["category"]={"drama_story":"drama_story_1m","viral_general":"general_viral_1m","ai_drama":"drama_story_1m"}[r["category"]]
rows=sel+g
def enr(r):
    try:
        o=subprocess.run(["yt-dlp","--skip-download","--dump-json","--no-warnings",r["url"]],capture_output=True,text=True,timeout=90).stdout
        j=json.loads(o)
        r.update(upload_date=j.get("upload_date"),like_count=j.get("like_count"),comment_count=j.get("comment_count"),tags="|".join((j.get("tags") or [])[:10]),description_head=(j.get("description") or "")[:150].replace("\n"," "),language=j.get("language"),view_count=j.get("view_count") or r["view_count"])
    except Exception: pass
    p=f"yt_thumbs/{r['video_id']}.jpg"
    if not os.path.exists(p):
        for u in (f"https://i.ytimg.com/vi/{r['video_id']}/maxresdefault.jpg",f"https://i.ytimg.com/vi/{r['video_id']}/hqdefault.jpg"):
            try:
                urllib.request.urlretrieve(u,p); break
            except Exception: pass
    r["thumb_file"]=p if os.path.exists(p) else ""
    return r
with ThreadPoolExecutor(8) as ex: rows=list(ex.map(enr,rows))
rows.sort(key=lambda r:(r["category"]!="ai_made_drama_film",-int(r["view_count"])))
fn=["video_id","url","title","channel","channel_handle","category","view_count","like_count","comment_count","upload_date","duration_sec","format","tags","description_head","thumbnail_url","thumb_file","found_by_query"]
with open("youtube_korean_collection_300.csv","w",newline="",encoding="utf-8-sig") as f:
    w=csv.DictWriter(f,fieldnames=fn,extrasaction="ignore");w.writeheader();w.writerows(rows)
from collections import Counter
print(len(rows),Counter(r["category"] for r in rows),sum(1 for r in rows if r["thumb_file"]),sum(1 for r in rows if r.get("upload_date")))
