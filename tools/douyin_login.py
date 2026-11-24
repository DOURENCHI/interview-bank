#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""抖音登录（一次性）：弹出浏览器窗口，人工扫码，登录态存 storage_state 供流水线复用。

用法: python douyin_login.py
输出: _cache/douyin_state.json
"""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "_cache" / "douyin_state.json"


def main():
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, channel="msedge")
        ctx = browser.new_context(
            user_agent=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                        "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"),
            viewport={"width": 1380, "height": 860}, locale="zh-CN")
        page = ctx.new_page()
        page.set_default_timeout(60_000)
        page.goto("https://www.douyin.com/login", wait_until="commit", timeout=60_000)
        print("[login] 浏览器已打开登录页。若页面空白请手动点右上角「登录」并扫码……")
        print("[login] 等待登录成功（最多 3 分钟），检测到会话 cookie 后自动保存并关闭。")
        deadline = time.time() + 300
        ok = False
        while time.time() < deadline:
            names = {c["name"] for c in ctx.cookies()}
            if {"sessionid", "sessionid_ss", "sid_guard"} & names:
                ok = True
                break
            time.sleep(3)
        if not ok:
            print("[login] 超时未检测到登录态，未保存任何文件。可重跑再试。")
            browser.close()
            sys.exit(1)
        ctx.storage_state(path=str(STATE))
        print(f"[login] 登录态已保存 -> {STATE}")
        page.wait_for_timeout(1500)
        browser.close()
        print("[login] 完成，浏览器已关闭。")


if __name__ == "__main__":
    main()
