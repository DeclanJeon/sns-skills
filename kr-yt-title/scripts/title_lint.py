#!/usr/bin/env python3
"""Usage: title_lint.py "title" ... — rough structural checks for Korean YouTube titles."""
import re, sys
for t in sys.argv[1:]:
    n = len(t); w = []
    if n > 70: w.append("70자 초과: 말줄임 위험")
    elif n < 20: w.append("20자 미만: 갈등/인물 정보 부족 가능")
    head = t[:20]
    if not re.search(r"[가-힣A-Za-z0-9]", head): w.append("앞 20자 정보 없음")
    if len(re.findall(r"[\U0001F300-\U0001FAFF]", t)) > 1: w.append("이모지 2개 이상")
    if len(re.findall(r"[!?]", t)) > 2: w.append("느낌표/물음표 과다")
    if re.search(r"(충격적인|엄청난|대박)", t) and not re.search(r"\d", t): w.append("추상어 위주, 구체 명사/숫자 추가 권장")
    if not re.search(r"(…|\.\.|\?|했더니|알고 보니|최후|그런데|었다|였다|인데|면|았다|찾았다|왔다)", t): w.append("[참고] 반전 공개형/끊김형 중 어느 쪽인지 불분명")
    if not re.search(r"(\d+화|EP|Ep|몰아보기|풀버전|AI)", t): w.append("회차/장르 라벨 없음(시리즈면 추가)")
    print(f"[{n}자] {t}\n   " + ("; ".join(w) if w else "OK"))
