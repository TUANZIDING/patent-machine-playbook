#!/usr/bin/env python3
"""PubMed 文献查新（NCBI E-utilities：esearch + esummary）。v0.1

只发送关键词/技术要点，不要把整份交底书当作 query。
用法：
  python3 scripts/pubmed-search-v0.1.py --query "hemorrhagic shock early warning wearable" --retmax 20 --out outputs/02-prior-art/pubmed
可选环境变量：NCBI_API_KEY（提高限速），NCBI_EMAIL
输出：<out>.json 与 <out>.md
"""
import argparse, json, os, sys, time, urllib.parse, urllib.request
from pathlib import Path

BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"


def get(endpoint, params):
    params = dict(params, tool="patent-machine-playbook", retmode="json")
    if os.getenv("NCBI_API_KEY"):
        params["api_key"] = os.environ["NCBI_API_KEY"]
    if os.getenv("NCBI_EMAIL"):
        params["email"] = os.environ["NCBI_EMAIL"]
    url = BASE + endpoint + "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def main():
    ap = argparse.ArgumentParser(description="PubMed 文献查新")
    ap.add_argument("--query", required=True, help="关键词或技术要点（英文效果更好）")
    ap.add_argument("--retmax", type=int, default=20)
    ap.add_argument("--mindate", help="YYYY 或 YYYY/MM/DD，可选")
    ap.add_argument("--out", default="outputs/02-prior-art/pubmed")
    a = ap.parse_args()

    p = {"db": "pubmed", "term": a.query, "retmax": a.retmax, "sort": "relevance"}
    if a.mindate:
        p.update(mindate=a.mindate, maxdate="3000", datetype="pdat")
    try:
        es = get("esearch.fcgi", p)
        ids = es["esearchresult"].get("idlist", [])
        total = es["esearchresult"].get("count", "0")
        rows = []
        if ids:
            time.sleep(0.4)
            sm = get("esummary.fcgi", {"db": "pubmed", "id": ",".join(ids)})["result"]
            for pmid in ids:
                d = sm.get(pmid, {})
                rows.append({
                    "pmid": pmid,
                    "title": d.get("title", ""),
                    "journal": d.get("fulljournalname") or d.get("source", ""),
                    "pubdate": d.get("pubdate", ""),
                    "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                })
    except Exception as e:  # 网络或接口异常
        print(f"PUBMED_ERROR: {e}", file=sys.stderr)
        return 2

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    meta = {"source": "PubMed E-utilities", "query": a.query, "total_hits": total,
            "retrieved": len(rows), "searched_at": time.strftime("%Y-%m-%d %H:%M %z")}
    out.with_suffix(".json").write_text(json.dumps({"meta": meta, "results": rows}, ensure_ascii=False, indent=2), encoding="utf-8")
    md = [f"# PubMed 查新：{a.query}", "",
          f"检索时间 {meta['searched_at']}；命中 {total} 篇，列出前 {len(rows)} 篇。", "",
          "| # | PMID | 标题 | 期刊 | 日期 | 链接 |", "|---|---|---|---|---|---|"]
    for i, r in enumerate(rows, 1):
        t = r["title"].replace("|", "/")
        md.append(f"| {i} | {r['pmid']} | {t} | {r['journal']} | {r['pubdate']} | {r['url']} |")
    out.with_suffix(".md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"PUBMED_HITS_JSON: {out.with_suffix('.json')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
