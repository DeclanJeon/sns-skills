import csv,json,subprocess,os,re
from concurrent.futures import ThreadPoolExecutor
r=list(csv.DictReader(open("youtube_korean_collection_300.csv",encoding="utf-8-sig")))
ai=[x for x in r if x["category"]=="ai_made_drama_film" and not re.search(r"(트로트|커버|뮤비|MV|Comic Robot|브이로그)",x["title"])]
ds=[x for x in r if x["category"]=="drama_story_1m"]
targets=ai[:70]+ds[:15]
os.makedirs("yt_transcripts",exist_ok=True)
def tr(x):
    out=f"yt_transcripts/{x['video_id']}.md"
    if os.path.exists(out): return x["video_id"],"cached"
    try:
        o=subprocess.run(["flucto","md",x["url"],"--language","ko","--output-dir","/tmp/trt","--json"],capture_output=True,text=True,timeout=240).stdout
        j=json.loads(o)
        if j.get("success") and j.get("markdown") and j.get("wordCount",0)>0:
            open(out,"w").write(j["markdown"]);return x["video_id"],"ok"
        return x["video_id"],"fail:"+str(j.get("error"))[:60]
    except Exception as e: return x["video_id"],"err"
with ThreadPoolExecutor(4) as ex: res=list(ex.map(tr,targets))
from collections import Counter
print(Counter(s.split(":")[0] for _,s in res)); print([s for _,s in res if s.startswith("fail")][:5])
