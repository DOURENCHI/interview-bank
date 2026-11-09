#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub 操作封装。令牌从系统凭据管理器（GCM）取，不落盘、不写进代码。

为什么要这个：SSH key 只能往「已存在的仓库」推代码，创建仓库必须走 REST API。
有了它就能一条命令建仓库并推送，不用每次手动到网页上点。

用法：
    python tools/gh.py whoami
    python tools/gh.py create interview-bank --desc "..."     # 默认私有
    python tools/gh.py create demo --public
    python tools/gh.py info DOURENCHI/interview-bank
    python tools/gh.py push  [--dir .] [--branch main]

前提：本机 git 的 credential.helper 已登录过 GitHub（GCM），令牌 scope 含 repo。
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

API = "https://api.github.com"


def token() -> str:
    """从 GCM 取 GitHub 令牌。取不到就抛错并提示怎么修。"""
    try:
        r = subprocess.run(
            ["git", "credential", "fill"],
            input="protocol=https\nhost=github.com\n\n",
            capture_output=True, text=True, timeout=30,
            env={**__import__("os").environ,
                 "GIT_TERMINAL_PROMPT": "0", "GCM_INTERACTIVE": "never"},
        )
    except subprocess.TimeoutExpired:
        raise SystemExit("凭据管理器无响应。检查是否弹出了登录窗口。")
    for line in r.stdout.splitlines():
        if line.startswith("password="):
            return line[len("password="):].strip()
    raise SystemExit(
        "取不到 GitHub 令牌。先在终端执行一次：\n"
        "  git ls-remote https://github.com/<你的账号>/<任意仓库>.git\n"
        "按提示在浏览器完成授权，凭据就会存进 GCM。"
    )


def api(method: str, path: str, payload: dict | None = None) -> tuple[int, dict]:
    tok = token()
    body = json.dumps(payload).encode() if payload else None
    req = urllib.request.Request(
        API + path, data=body, method=method,
        headers={
            "Authorization": f"token {tok}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, json.loads(resp.read() or b"{}")
    except urllib.error.HTTPError as e:
        raw = e.read().decode(errors="ignore")
        try:
            return e.code, json.loads(raw)
        except json.JSONDecodeError:
            return e.code, {"message": raw[:300]}


def cmd_whoami(args=None) -> int:
    code, d = api("GET", "/user")
    if code != 200:
        print("失败:", d.get("message"))
        return 1
    print(f"账号   {d.get('login')}")
    print(f"仓库数 {d.get('public_repos', 0)} public / {d.get('total_private_repos', '?')} private")
    print(f"计划   {(d.get('plan') or {}).get('name', '?')}")
    return 0


def cmd_create(args) -> int:
    payload = {
        "name": args.name,
        "description": args.desc or "",
        "private": not args.public,
        "has_issues": True,
        "has_wiki": False,
        "auto_init": False,
    }
    code, d = api("POST", "/user/repos", payload)
    if code == 201:
        print(f"已创建 {d['full_name']}  private={d['private']}")
        print(f"SSH  {d['ssh_url']}")
        return 0
    if code == 422:
        print(f"仓库已存在，直接用：git@github.com:{args.owner or 'DOURENCHI'}/{args.name}.git")
        return 0
    print(f"失败 {code}: {d.get('message')}")
    return 1


def cmd_info(args) -> int:
    code, d = api("GET", f"/repos/{args.repo}")
    if code != 200:
        print(f"失败 {code}: {d.get('message')}")
        return 1
    print(f"{d['full_name']}  private={d['private']}  default={d['default_branch']}")
    print(f"size={d['size']}KB  pushed={d.get('pushed_at','')[:19]}")
    print(f"url={d['html_url']}")
    return 0


def cmd_push(args) -> int:
    d = Path(args.dir).resolve()
    if not (d / ".git").exists():
        print(f"{d} 不是 git 仓库")
        return 1
    r = subprocess.run(["git", "-C", str(d), "push", "-u", "origin", args.branch],
                       capture_output=True, text=True)
    print((r.stdout + r.stderr).strip()[-500:])
    return r.returncode


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("whoami").set_defaults(fn=cmd_whoami)

    c = sub.add_parser("create")
    c.add_argument("name")
    c.add_argument("--desc", default="")
    c.add_argument("--public", action="store_true")
    c.add_argument("--owner", default="")
    c.set_defaults(fn=cmd_create)

    i = sub.add_parser("info")
    i.add_argument("repo")
    i.set_defaults(fn=cmd_info)

    p = sub.add_parser("push")
    p.add_argument("--dir", default=".")
    p.add_argument("--branch", default="main")
    p.set_defaults(fn=cmd_push)

    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
