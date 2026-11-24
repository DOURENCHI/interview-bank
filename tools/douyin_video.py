#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""抖音视频 → 音轨 → Whisper 转写流水线（图文 OCR 流水线的视频版）。

用法:
  python douyin_video.py --works sources/douyin_works_b4.json --out sources/douyin_transcript_b4.jsonl [--limit N] [--ids id1,id2] [--force]

原理:
  1. Playwright 打开视频页，监听 aweme/detail API 拿 aweme_detail JSON（免登录）
  2. 从 video.play_addr / bit_rate[].play_addr / bit_rate[].audio_play_addr 提取直链，
     requests 直连下载（实测直链无需 cookie）
  3. ffmpeg 抽 16k 单声道 wav（下载体是音轨或音视频合成都行，-vn 只留音）
  4. faster-whisper 转写（cuda/float16 → 失败退 cpu/int8），language=zh + vad_filter
  5. 追加写 jsonl: {aweme_id, desc, url, date, duration_s, text, model, device, runtime_s}

已转写的 aweme_id 自动跳过（断点续跑），--force 重跑。模型需已缓存（HF_ENDPOINT 可指向镜像）。
"""
import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TMP = ROOT / "_cache" / "douyin_video"
TMP.mkdir(parents=True, exist_ok=True)
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")


def pick_model():
    from faster_whisper import WhisperModel
    for device, compute in (("cuda", "float16"), ("cpu", "int8")):
        try:
            m = WhisperModel("small", device=device, compute_type=compute)
            print(f"[asr] WhisperModel small on {device}/{compute}")
            return m, device
        except Exception as e:
            print(f"[asr] {device} 不可用: {e}")
    raise RuntimeError("faster-whisper 初始化失败")


def fetch_detail(page, aweme_id):
    """打开视频页，从 detail API 拿 aweme_detail JSON。"""
    box = {}

    def on_resp(r):
        if "/aweme/v1/web/aweme/detail/" in r.url and r.status == 200 and "detail" not in box:
            try:
                d = r.json()
                aw = d.get("aweme_detail") or (d.get("item_list") or [{}])[0]
                if aw:
                    box["detail"] = aw
            except Exception:
                pass

    page.on("response", on_resp)
    try:
        page.goto(f"https://www.douyin.com/video/{aweme_id}",
                  wait_until="domcontentloaded", timeout=45_000)
        page.wait_for_timeout(7000)
    finally:
        page.remove_listener("response", on_resp)
    return box.get("detail")


def candidate_urls(aw):
    """按优先级收集媒体直链：bit_rate 高清视频轨在前，play_addr 兜底。"""
    v = aw.get("video") or {}
    urls = []
    for br in v.get("bit_rate") or []:  # 多码率：HRAPX 主档在前
        gear = br.get("gear_name", "")
        for pa in (br.get("play_addr"), br.get("audio_play_addr")):
            for u in (pa or {}).get("url_list") or []:
                urls.append((gear, u))
    for pa in (v.get("play_addr"), v.get("download_addr")):
        for u in (pa or {}).get("url_list") or []:
            urls.append(("default", u))
    # 去重保序
    seen, out = set(), []
    for gear, u in urls:
        if u not in seen:
            seen.add(u)
            out.append((gear, u))
    return out


def download_media(urls, dest):
    """依次尝试直链，下载首个响应正常的完整媒体体（音轨或音视频均可）。"""
    import requests
    for gear, u in urls:
        try:
            r = requests.get(u, headers={"User-Agent": UA}, timeout=60, stream=True)
            ct = r.headers.get("content-type", "")
            if r.status_code in (200, 206) and ("audio" in ct or "video" in ct or "octet" in ct):
                n = 0
                with dest.open("wb") as f:
                    for chunk in r.iter_content(1 << 18):
                        f.write(chunk)
                        n += len(chunk)
                if n > 300_000:
                    print(f"    [dl] gear={gear} {n/1e6:.1f}MB ct={ct.split(';')[0]}")
                    return True
        except Exception as e:
            print(f"    [dl] 尝试失败: {str(e)[:70]}")
    return False


def transcribe_wav(model, wav_path):
    """wave+numpy 读 wav 喂模型，绕开 PyAV 兼容问题。"""
    import wave
    import numpy as np
    with wave.open(str(wav_path), "rb") as wf:
        sr = wf.getframerate()
        n = wf.getnframes()
        pcm = np.frombuffer(wf.readframes(n), dtype=np.int16)
    audio = pcm.astype(np.float32) / 32768.0
    return model.transcribe(audio, language="zh", vad_filter=True)


def extract_audio(media_path, wav_path):
    if wav_path.exists():
        wav_path.unlink()
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(media_path),
         "-ar", "16000", "-ac", "1", "-vn", str(wav_path)],
        check=True, capture_output=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--works", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--ids", default="")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    works = json.loads(Path(args.works).read_text(encoding="utf-8"))
    works = works if isinstance(works, list) else works.get("works", works)
    videos = [w for w in works if w.get("type") == "video"]
    if args.ids:
        keep = {i.strip() for i in args.ids.split(",")}
        videos = [w for w in videos if w["aweme_id"] in keep]
    out_path = ROOT / args.out
    done = set()
    if out_path.exists() and not args.force:
        for line in out_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                try:
                    done.add(json.loads(line)["aweme_id"])
                except Exception:
                    pass
    todo = [w for w in videos if args.force or w["aweme_id"] not in done]
    if args.limit:
        todo = todo[: args.limit]
    print(f"[plan] 视频 {len(videos)} 条，已转写 {len(done)}，本次 {len(todo)} 条")

    from playwright.sync_api import sync_playwright
    model, device = pick_model()

    ok_n = fail_n = 0
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(user_agent=UA,
                                  viewport={"width": 1380, "height": 860}, locale="zh-CN")
        page = ctx.new_page()
        with out_path.open("a", encoding="utf-8") as fout:
            for i, w in enumerate(todo, 1):
                aid = w["aweme_id"]
                desc = (w.get("desc") or "").replace("\n", " ")
                print(f"\n[{i}/{len(todo)}] {aid} {desc[:40]}")
                mpath = TMP / f"{aid}.bin"
                wpath = TMP / f"{aid}.wav"
                t0 = time.time()
                try:
                    aw = fetch_detail(page, aid)
                    if not aw:
                        raise RuntimeError("detail API 未截获")
                    urls = candidate_urls(aw)
                    if not urls:
                        raise RuntimeError("无候选直链")
                    if not download_media(urls, mpath):
                        raise RuntimeError("全部直链下载失败")
                    extract_audio(mpath, wpath)
                    segs, info = transcribe_wav(model, wpath)
                    text = "".join(s.text for s in segs).strip()
                    rec = {"aweme_id": aid, "desc": w.get("desc", ""),
                           "url": w.get("url", f"https://www.douyin.com/video/{aid}"),
                           "date": w.get("date", ""),
                           "duration_s": round(info.duration, 1),
                           "text": text, "model": "faster-whisper small",
                           "device": device, "runtime_s": round(time.time() - t0, 1)}
                    fout.write(json.dumps(rec, ensure_ascii=False) + "\n")
                    fout.flush()
                    ok_n += 1
                    print(f"    [ok] {info.duration:.0f}s 音频 -> {len(text)} 字，用时 {rec['runtime_s']}s")
                except Exception as e:
                    fail_n += 1
                    print(f"    [FAIL] {e}")
                finally:
                    for f in (mpath, wpath):
                        f.unlink(missing_ok=True)
        browser.close()
    print(f"\n[done] 成功 {ok_n} 失败 {fail_n} -> {out_path}")
    if fail_n:
        sys.exit(2)


if __name__ == "__main__":
    main()
