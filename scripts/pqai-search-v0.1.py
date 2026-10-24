#!/usr/bin/env python3
"""PQAI 专利语义查新（https://api.projectpq.ai /search/102）。v0.1

注意：PQAI API 目前只覆盖美国专利（另含部分非专利文献 npl）。
token 需 PQAI+ 订阅；学术/非商业用途可发邮件至 sam@projectpq.ai 申请免费 token。
只发送关键词/技术要点，不要把整份交底书当作 query。
用法：
  export PQAI_TOKEN=xxxx
  python3 scripts/pqai-search-v0.1.py --query "wearable alert band for trauma team leader driven by shock index trend" --n 20 --out outputs/02-prior-art/pqai
输出：<out>.json 与 <out>.md
"""
import argparse, json, os, sys, time, urllib.parse, urllib.request
from pathlib import Path

ENDPOINT = "https://api.projectpq.ai/search/102"


def main():
    ap = argparse.ArgumentParser(description="PQAI 专利语义查新（美国专利）")
    ap.add_argument("--query", required=True)
    ap.add_argument("--n", type=int, default=20)
    ap.add_argument("--type", default="patent", choices=["patent", "npl"])
    ap.add_argument("--after", help="YYYY-MM-DD，可选")
    ap.add_argument("--before", help="YYYY-MM-DD，可选")
    ap.add_argument("--out", default="outputs/02-prior-art/pqai")
    a = ap.parse_args()

    token = os.getenv("PQAI_TOKEN")
    if not token:
        print("PQAI_SKIPPED: 未设置 PQAI_TOKEN。学术用途可邮件 sam@projectpq.ai 申请免费 token；"
              "本步跳过，不影响国知局与 PubMed 查新。")
        return 0

    params = {"q": a.query, "n": a.n, "type": a.type, "snip": 1, "token": token}
    if a.after:
        params["after"] = a.after
    if a.before:
        params["before"] = a.before
    url = ENDPOINT + "?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            data = json.loads(r.read().decode("utf-8"))
    except Exception as e:
        print(f"PQAI_ERROR: {e}", file=sys.stderr)
        return 2

    rows = []
    for d in data.get("results", []):
        pid = d.get("id") or d.get("publication_id") or ""
        rows.append({
            "id": pid,
            "title": d.get("title", ""),
            "date": d.get("publication_date") or d.get("date", ""),
            "score": d.get("score", ""),
            "snippet": (d.get("snippet") or "")[:300],
            "url": d.get("www_link") or (f"https://patents.google.com/patent/{pid}" if pid else ""),
        })
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    meta = {"source": "PQAI /search/102", "query": a.query, "retrieved": len(rows),
            "searched_at": time.strftime("%Y-%m-%d %H:%M %z")}
    out.with_suffix(".json").write_text(json.dumps({"meta": meta, "results": rows}, ensure_ascii=False, indent=2), encoding="utf-8")
    md = [f"# PQAI 查新：{a.query}", "", f"检索时间 {meta['searched_at']}；返回 {len(rows)} 条（美国专利）。", "",
          "| # | 公开号 | 标题 | 日期 | 链接 |", "|---|---|---|---|---|"]
    for i, r in enumerate(rows, 1):
        md.append(f"| {i} | {r['id']} | {r['title'].replace('|', '/')} | {r['date']} | {r['url']} |")
    out.with_suffix(".md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"PQAI_HITS_JSON: {out.with_suffix('.json')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
