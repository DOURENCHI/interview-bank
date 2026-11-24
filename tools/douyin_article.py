#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""抖音文字笔记（aweme_type=163 article）抓取流水线。

用法:
  枚举主页作品（滚动到底，记录 aweme_type，补齐图文/文字笔记漏抓）:
    python douyin_article.py --enum <主页URL> --works sources/douyin_works_bX.json
  抓正文（对 works 里的每条截 detail API 的 article_info）:
    python douyin_article.py --fetch --works sources/douyin_works_bX.json --out sources/douyin_text_bX.jsonl

输出 jsonl 字段: aweme_id/desc/url/date/aweme_type/text/chars/runtime_s
"""
import argparse
import json
import re
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")


def parse_article(aw):
    """从 aweme_detail 提取文字笔记正文。"""
    art = (aw.get("article_info") or {})
    raw = art.get("article_content") or ""
    if not raw:
        return ""
    try:
        obj = json.loads(raw)
        # 已知键优先：全文 > 摘要
        for k in ("long_article_content", "content", "long_article_abstract"):
            v = obj.get(k)
            if isinstance(v, str) and v.strip():
                return v.strip()
        # 兜底：拼接所有字符串值
        parts = [v for v in obj.values() if isinstance(v, str) and len(v) > 20]
        return "\n".join(parts)
    except Exception:
        return raw


def enum_home(page, home_url, max_n=100):
    """滚动主页收集作品列表（监听 post API），返回 {aweme_id: item}，item 含 aweme_type。"""
    got = {}

    def on_resp(r):
        if re.search(r"/aweme/v1/web/aweme/post/", r.url) and r.status == 200:
            try:
                for it in r.json().get("aweme_list") or []:
                    aid = str(it.get("aweme_id") or "")
                    if not aid:
                        continue
                    imgs = len(it.get("images") or [])
                    got[aid] = {
                        "aweme_id": aid,
                        "desc": it.get("desc", ""),
                        "aweme_type": it.get("aweme_type"),
                        "type": ("article" if it.get("aweme_type") == 163
                                 else "note" if imgs else "video"),
                        "images": imgs,
                        "create_time": it.get("create_time", 0),
                    }
            except Exception:
                pass

    page.on("response", on_resp)
    page.goto(home_url, wait_until="domcontentloaded", timeout=60_000)
    page.wait_for_timeout(5000)
    stale = 0
    for _ in range(60):
        n = len(got)
        page.mouse.wheel(0, 4000)
        page.wait_for_timeout(1500)
        if len(got) == n:
            stale += 1
            if stale >= 8 or n >= max_n:
                break
        else:
            stale = 0
    page.remove_listener("response", on_resp)
    return got


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--enum")
    ap.add_argument("--works")
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--out")
    ap.add_argument("--max", type=int, default=100)
    args = ap.parse_args()

    from playwright.sync_api import sync_playwright

    if args.enum:
        with sync_playwright() as p:
            b = p.chromium.launch(headless=True)
            ctx = b.new_context(user_agent=UA, viewport={"width": 1380, "height": 860},
                                locale="zh-CN")
            pg = ctx.new_page()
            got = enum_home(pg, args.enum, args.max)
            b.close()
        items = sorted(got.values(), key=lambda x: -x["create_time"])
        for it in items:
            it["date"] = (time.strftime("%Y-%m-%d", time.localtime(it["create_time"]))
                          if it["create_time"] else "")
            it["url"] = f"https://www.douyin.com/note/{it['aweme_id']}"
        # 合并旧文件（保留已有 date/images）
        wpath = ROOT / args.works
        old = {}
        if wpath.exists():
            try:
                old_d = json.loads(wpath.read_text(encoding="utf-8"))
                old_list = old_d if isinstance(old_d, list) else old_d.get("works", [])
                old = {w["aweme_id"]: w for w in old_list}
            except Exception:
                pass
        merged = []
        for it in items:
            if it["aweme_id"] in old:
                it = {**old[it["aweme_id"]], **it}
            merged.append(it)
        for aid, w in old.items():
            if aid not in got:
                merged.append(w)
        wpath.write_text(json.dumps(merged, ensure_ascii=False, indent=1), encoding="utf-8")
        from collections import Counter
        print(f"[enum] {len(merged)} 条 -> {wpath}")
        print("  类型分布:", dict(Counter(w["type"] for w in merged)))
        return

    if args.fetch:
        works = json.loads((ROOT / args.works).read_text(encoding="utf-8"))
        works = works if isinstance(works, list) else works.get("works", [])
        out_path = ROOT / args.out
        done = set()
        if out_path.exists():
            for line in out_path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    try:
                        done.add(json.loads(line)["aweme_id"])
                    except Exception:
                        pass
        todo = [w for w in works if w["aweme_id"] not in done]
        print(f"[plan] 共 {len(works)} 条，已抓 {len(done)}，本次 {len(todo)}")
        ok_n = fail_n = 0
        with sync_playwright() as p:
            b = p.chromium.launch(headless=True)
            ctx = b.new_context(user_agent=UA, viewport={"width": 1380, "height": 860},
                                locale="zh-CN")
            pg = ctx.new_page()
            with out_path.open("a", encoding="utf-8") as fout:
                for i, w in enumerate(todo, 1):
                    aid = w["aweme_id"]
                    box = {}
                    handler = _mk_detail_catcher(box)
                    pg.on("response", handler)
                    try:
                        pg.goto(f"https://www.douyin.com/video/{aid}",
                                wait_until="domcontentloaded", timeout=45_000)
                        pg.wait_for_timeout(5000)
                    finally:
                        pg.remove_listener("response", handler)
                    aw = box.get("aw") or {}
                    text = parse_article(aw)
                    rec = {"aweme_id": aid, "desc": w.get("desc", ""), "url": w.get("url", ""),
                           "date": w.get("date", ""), "aweme_type": aw.get("aweme_type"),
                           "text": text, "chars": len(text),
                           "runtime_s": 0}
                    fout.write(json.dumps(rec, ensure_ascii=False) + "\n")
                    fout.flush()
                    if text:
                        ok_n += 1
                        print(f"  [{i}/{len(todo)}] ok {len(text)} 字: {w.get('desc','')[:28]}")
                    else:
                        fail_n += 1
                        print(f"  [{i}/{len(todo)}] FAIL 无正文: {w.get('desc','')[:28]}")
            b.close()
        print(f"[done] 成功 {ok_n} 失败 {fail_n} -> {out_path}")


def _mk_detail_catcher(box):
    def on_resp(r):
        if "/aweme/detail/" in r.url and r.status == 200 and "aw" not in box:
            try:
                box["aw"] = r.json().get("aweme_detail") or {}
            except Exception:
                pass
    return on_resp


if __name__ == "__main__":
    main()
