# -*- coding: utf-8 -*-
"""枚举抖音博主主页的全部作品（图文/视频），落成 sources/douyin_works.json。

为什么不用 douyin-scraper skill：它只吃「单个作品链接」（/note/ /video/ /slides/），
不能列出一个博主的所有作品。这一步必须在浏览器里打开主页，让抖音自己的前端去请求
作品列表接口，我们只在旁边「听」响应——不自己拼 a_bogus 签名，不伪造请求。

用法：
  python tools/douyin_works.py "https://www.douyin.com/user/MS4wLjABAAAA..." 
  python tools/douyin_works.py "<主页链接>" --login    # 首次需要扫码登录，会保存登录态
  python tools/douyin_works.py "<主页链接>" --max 200 --out sources/douyin_works.json

合规：只读公开页面、低频、不批量扩散；图片与文字版权归原作者，入库时保留原作品链接。
"""
import argparse
import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROFILE_DIR = ROOT / "_cache" / "douyin_profile"
STATE_FILE = PROFILE_DIR / "storage.json"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")

POST_API = re.compile(r"/aweme/v1/web/aweme/post/")
SEC_UID = re.compile(r"/user/([A-Za-z0-9_\-]+)")


def _norm_work(it: dict) -> dict:
    """从抖音作品列表接口的原始 item 里，取出我们真正需要的字段。"""
    aweme_id = str(it.get("aweme_id") or "")
    desc = (it.get("desc") or "").strip()
    images = []
    for im in (it.get("images") or []):
        urls = (im.get("url_list") or [])
        # 优先取无 webp 的 jpeg（webp 在部分环境解不开）
        pick = next((u for u in urls if u.endswith(".jpeg") or u.endswith(".jpg")), None)
        pick = pick or (urls[0] if urls else "")
        if pick:
            images.append(pick)
    video = it.get("video") or {}
    cover = ""
    for c in (video.get("cover") or {}).get("url_list") or []:
        cover = c
        break
    create_time = it.get("create_time") or 0
    return {
        "aweme_id": aweme_id,
        "desc": desc[:120],
        "type": "note" if images else ("video" if video else "unknown"),
        "images": images,
        "cover": cover,
        "create_time": create_time,
        "date": time.strftime("%Y-%m-%d", time.localtime(create_time)) if create_time else "",
        "url": f"https://www.douyin.com/note/{aweme_id}" if images
               else f"https://www.douyin.com/video/{aweme_id}",
    }


def collect(profile_url: str, max_items: int, login: bool, headless: bool,
            out: Path, scroll_wait: float) -> int:
    from playwright.sync_api import sync_playwright

    PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    works: dict = {}
    state = {"sec_uid": ""}
    m = SEC_UID.search(profile_url)
    if m:
        state["sec_uid"] = m.group(1)

    with sync_playwright() as pw:
        try:
            browser = pw.chromium.launch(channel="msedge", headless=headless)
        except Exception:
            browser = pw.chromium.launch(headless=headless)
        ctx = browser.new_context(user_agent=UA, viewport={"width": 1440, "height": 900},
                                  storage_state=str(STATE_FILE) if STATE_FILE.exists() else None)
        page = ctx.new_page()

        if login:
            print("→ 打开浏览器，请扫码登录抖音；登录成功后会自动保存登录态。", file=sys.stderr)
            page.goto("https://www.douyin.com/", timeout=60000, wait_until="domcontentloaded")
            page.wait_for_timeout(5000)
            try:
                page.wait_for_function(
                    "() => !!(document.cookie && document.cookie.includes('ttwid'))",
                    timeout=120000)
            except Exception:
                pass
            ctx.storage_state(path=str(STATE_FILE))
            print(f"→ 登录态已保存：{STATE_FILE}", file=sys.stderr)

        def on_response(resp):
            if not POST_API.search(resp.url):
                return
            try:
                data = resp.json()
            except Exception:
                return
            for it in data.get("aweme_list") or []:
                w = _norm_work(it)
                if w["aweme_id"]:
                    works[w["aweme_id"]] = w
            if not state["sec_uid"]:
                mm = re.search(r"sec_user_id=([A-Za-z0-9_\-]+)", resp.url)
                if mm:
                    state["sec_uid"] = mm.group(1)

        page.on("response", on_response)
        page.goto(profile_url, timeout=90000, wait_until="domcontentloaded")
        page.wait_for_timeout(4000)

        last_n, stall = 0, 0
        for i in range(120):
            if len(works) >= max_items:
                break
            page.mouse.wheel(0, 3000)
            page.wait_for_timeout(int(scroll_wait * 1000))
            # 页面自带的「加载更多」按钮兜底
            if len(works) == last_n:
                stall += 1
                try:
                    btn = page.locator("text=加载更多").first
                    if btn.is_visible(timeout=1200):
                        btn.click(timeout=2000)
                        page.wait_for_timeout(2000)
                except Exception:
                    pass
            else:
                stall = 0
            last_n = len(works)
            if stall >= 6:
                break

        # DOM 兜底：有些号只渲染 anchor，不走接口
        try:
            for href in page.eval_on_selector_all(
                    "a[href*='/note/'], a[href*='/video/']",
                    "els => els.map(e => e.getAttribute('href'))"):
                mm = re.search(r"/(note|video)/(\d+)", href or "")
                if not mm:
                    continue
                aid = mm.group(2)
                if aid in works:
                    continue
                works[aid] = {"aweme_id": aid, "desc": "", "type": "note" if mm.group(1) == "note" else "video",
                              "images": [], "cover": "", "create_time": 0, "date": "",
                              "url": f"https://www.douyin.com/{mm.group(1)}/{aid}"}
        except Exception:
            pass

        ctx.storage_state(path=str(STATE_FILE))
        browser.close()

    items = sorted(works.values(), key=lambda x: x.get("create_time") or 0, reverse=True)
    payload = {
        "profile_url": profile_url,
        "sec_user_id": state["sec_uid"],
        "fetched_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "count": len(items),
        "note_count": sum(1 for x in items if x["type"] == "note"),
        "image_total": sum(len(x["images"]) for x in items),
        "works": items,
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    return len(items)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("profile", help="博主主页链接（https://www.douyin.com/user/xxx）")
    ap.add_argument("--max", type=int, default=200, help="最多取多少作品")
    ap.add_argument("--out", default=str(ROOT / "sources" / "douyin_works.json"))
    ap.add_argument("--login", action="store_true", help="先手动扫码登录并保存登录态")
    ap.add_argument("--headless", action="store_true", help="无头模式（已登录时可用）")
    ap.add_argument("--wait", type=float, default=1.2, help="每次滚动后的等待秒数")
    args = ap.parse_args()
    n = collect(args.profile, args.max, args.login, not args.headless,
                Path(args.out), args.wait)
    print(f"抓到 {n} 个作品 → {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
