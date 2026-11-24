import csv,json,subprocess,re
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
r=list(csv.DictReader(open("youtube_korean_collection_300.csv",encoding="utf-8-sig")))
ai=[x for x in r if x["category"]=="ai_made_drama_film"]
# top AI channels by count/views
cnt=Counter();vs={}
for x in ai:
    cnt[x["channel_handle"]]+=1;vs[x["channel_handle"]]=vs.get(x["channel_handle"],0)+int(x["view_count"])
chs=[h for h,_ in sorted(cnt.items(),key=lambda a:-vs[a[0]]) if h and h.startswith("@")][:25]
def fl(args):
    try:o=subprocess.run(["yt-dlp","--flat-playlist","--dump-json","--no-warnings"]+args,capture_output=True,text=True,timeout=300).stdout
    except Exception:return []
    out=[]
    for l in o.splitlines():
        try:out.append(json.loads(l))
        except:pass
    return out
def chan(h):
    return h,fl(["--playlist-end","80",f"https://www.youtube.com/{h}/videos"])
rows=[]
with ThreadPoolExecutor(5) as ex:
    for h,L in ex.map(chan,chs):
        for i,j in enumerate(L):
            rows.append(dict(channel_handle=h,channel=j.get("channel"),recency_rank=i+1,video_id=j.get("id"),title=j.get("title"),view_count=j.get("view_count"),duration_sec=j.get("duration"),url=j.get("url")))
with open("youtube_ai_channel_videos.csv","w",newline="",encoding="utf-8-sig") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print("channels",len(chs),"videos",len(rows))
# shorts
qs=["AI 드라마 shorts","AI 숏츠 사이다","AI 복수 쇼츠","AI 시어머니 쇼츠","AI 재벌 쇼츠","AI 장군 쇼츠","AI 감동 쇼츠","AI 반전 쇼츠","AI 로맨스 쇼츠","AI 사연 쇼츠","AI 좀비 쇼츠","AI 조선 쇼츠","AI 단편 shorts","AI 갑질 참교육 shorts","AI 며느리 shorts","AI 할머니 shorts"]
def sh(q):return [(q,j) for j in fl([f"https://www.youtube.com/results?search_query={q.replace(' ','+')}&sp=EgIYAQ%253D%253D"])]
seen={}
with ThreadPoolExecutor(5) as ex:
    for L in ex.map(sh,qs):
        for q,j in L:
            v=j.get("view_count") or 0;d=j.get("duration") or 999
            t=(j.get("title") or "")+(j.get("channel") or "")
            if j.get("id") and d<=65 and v>=100000 and re.search(r"[가-힣]",t) and re.search(r"(AI|ai|에이아이)",t+(j.get("description") or "")):
                seen[j["id"]]=dict(video_id=j["id"],url=f"https://www.youtube.com/shorts/{j['id']}",title=j.get("title"),channel=j.get("channel"),view_count=v,duration_sec=d,found_by_query=q)
rows=sorted(seen.values(),key=lambda x:-x["view_count"])
if rows:
    with open("youtube_ai_shorts.csv","w",newline="",encoding="utf-8-sig") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print("shorts",len(rows));[print(x["view_count"],x["title"][:60]) for x in rows[:8]]
