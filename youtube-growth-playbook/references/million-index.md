# Million Index: reaction-led YouTube references

## Retrieve candidates

This is the retrieval interface for [market entry](market-entry.md). Start from market signals and actual user-imposed limits, not the channel's preferred genre. If the user leaves the market open, a seed keyword or channel identity is not a prerequisite.

Use Million Index's JSON interface. Prefer an explicitly supplied `MILLION_INDEX_URL` or a user-approved local instance; otherwise use `https://mi.ponslink.com`. POST `/search` as JSON (never send credentials, private Studio data, draft scripts or internal planning into the search: send short public-facing query terms):

```bash
curl --fail-with-body --silent --show-error --max-time 45 \
  -H 'Content-Type: application/json' \
  -d '{"mode":"keyword","platform":"youtube","value":"레트로 미스터리 단편","minViews":100000,"maxSubscribers":1000,"videoFormat":"short","publishedWithinDays":365}' \
  https://mi.ponslink.com/search
```

Recognize `searchContract: "youtube-reference-v1"`, check `filters` echoes the requested conditions, and check HTTP/response errors before interpreting `results`. HTTP 200 without the contract is unsupported, not a valid filter pass. A 403, timeout/network failure, missing deployment or stale contract blocks **Million Index verification**, not all planning. Report the observed failure and use an already-running authorized local Million Index if available. Otherwise follow the [provisional fallback](market-entry.md#when-million-index-is-unavailable). Do not bypass the service restriction or probe private endpoints. No direct YouTube API key required in the skill.

- Each targeted request retrieves up to 50 relevance candidates before filtering; zero matches does not prove no results exist. Use a 365-day starting window when recent evidence is needed. Do not widen an explicit user limit without permission. Do not mix markets or formats to fill a result quota.
- For an intended market, send `regionCode` (e.g. `KR`) and `relevanceLanguage` (e.g. `ko`). Region is a YouTube availability/search setting, not evidence of viewers' locations; language is a relevance preference, not a hard language filter. Confirm actual language and audience context when comparing results. `stages` gives counts for metadata, views, format and final matches; use it to explain sparse returns.
- `videoFormat: short` selects durations up to 180 seconds, `long` above 180, `all` no duration cutoff. `formatBasis: duration_only` never confirms YouTube Shorts classification. Verify format by opening the public video when it changes the decision.
- A returned `subscriberCount` is the rounded current public channel count, not the upload-date count. `unknownSubscriberCount` is the number of otherwise eligible candidate videos excluded for unknown counts. Keep outliers traceable with video ID/URL, channel ID, counts, publication and observation times, duration/proxy and verified format when known. Link using `https://www.youtube.com/watch?v=<id>`.

### No keyword yet

When there is no usable market query, send `value: ""` with `mode: "keyword"` and `platform: "youtube"`; keep requested filters and require `discoveryMode: "random"`. This samples categories and date windows, not YouTube as a whole. Convert promising leads into targeted audience-intent searches; random order is not a quality rank. If empty, resample once with the same filters if budget allows. A different sample is not a controlled filter comparison.

### Separate outlier and demand searches

| Pass | Request | What it can establish |
|---|---|---|
| Outlier discovery | `minViews: 100000`, `maxSubscribers: 1000`; use `10000` if testing that explicit tier or broadening a default cap. Keep tier labels. | Small current audience and unusually large visible reach are leads, not evidence of repeated demand. |
| Demand scan | Targeted query for the same viewer need with `minViews: 0`, first retaining the chosen subscriber cap when diagnosing a sparse outlier search. | Ordinary and weak results exist alongside better ones. It is still a relevance-ranked sample, not a census. |
| Market context if still sparse | Only if needed and allowed, set `maxSubscribers: null` with floor unchanged. Label it mixed-size context; it cannot prove small-channel traction. | Shows what is retrieved when the cap is removed. The API omits subscriber counts when no cap is set; those counts remain unknown. |

When diagnosing a sparse targeted search, hold `value`, country, language, format, and date window fixed. Use `stages` to choose the first change: if few survive `afterViews`, lower the default view floor first; if enough survive `afterFormat` but few match, loosen the default subscriber cap first (or stop if it is a hard user constraint). If both measurements are useful, change one filter per request. Do not change region, language or keywords in the same comparison; a synonym query tests retrieval coverage, not the filter. Log rows scanned → views → format → final, and the unknown-subscriber exclusions. Because successive requests are live, check candidate overlap when observable and attribute count changes cautiously. Never present broader results as passing the original filter.

Default budget: at most six upstream discovery search calls per task (targeted costs one; blank costs two), plus up to two channel baselines. Reserve at least one targeted call after random exploration. If a hard constraint or the budget blocks the next comparison, state what is missing and stop.

### Comparison sample (after outlier discovery)

Call the same `/search` endpoint with `{"mode":"channel-baseline","platform":"youtube","value":"<channelId from discovery>","videoFormat":"all"}` for up to two shortlisted independent channels by default. Require `searchContract: "youtube-channel-baseline-v1"` and the requested `channelId`. These are up to 50 recent public uploads in uploads-list order with **no performance floor**. Do not pass `minViews`, `maxSubscribers`, market options or a date filter. `viewWindow: "lifetime_at_observation"` means current totals, not historical first-week views. Locally select comparable date/format/length/topic rows, excluding the focal video and keeping weak performers. Report unavailable or insufficient cohorts instead of substituting unrelated rows. Comparison calls are separate from the search-call budget.
