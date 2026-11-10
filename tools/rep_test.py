# -*- coding: utf-8 -*-
"""学习报告冒烟测试：注入自评/错题数据 → 打开报告 → 验证各区块渲染。"""
import json
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
PAGE = (ROOT / "dist" / "bank.html").resolve()

def main() -> int:
    with sync_playwright() as p:
        b = p.chromium.launch(channel="msedge")
        pg = b.new_page()
        pg.goto(PAGE.as_uri())
        pg.wait_for_timeout(300)

        # 取前 30 个题 id，注入自评数据：错落的时间与分数
        ids = pg.evaluate("DATA.slice(0, 30).map(q => q.id)")
        review = {}
        import time
        now_ms = int(time.time() * 1000)
        for i, qid in enumerate(ids):
            g = 1 + (i % 4)
            ts = now_ms - i * 3 * 864e5 / 4  # 分布在近几周
            review[qid] = {"g": g, "ts": int(ts)}
        # 保证有确定的到期题：g=4 且 30 天前、g=3 且 10 天前
        review[ids[0]] = {"g": 4, "ts": int(now_ms - 30 * 864e5)}
        review[ids[1]] = {"g": 3, "ts": int(now_ms - 10 * 864e5)}
        n_due_expect = sum(
            1 for v in review.values()
            if v["g"] > 2 and (now_ms - v["ts"]) >= {1: 1, 2: 3, 3: 7, 4: 21}[v["g"]] * 864e5)
        print("预期到期数:", n_due_expect)
        pg.evaluate(
            "([rv, wr]) => { localStorage.setItem('ib_review_v1', JSON.stringify(rv));"
            " localStorage.setItem('ib_wrong_v1', JSON.stringify(wr)); }",
            [review, ids[:5]],
        )
        pg.reload()
        pg.wait_for_timeout(300)

        pg.click('.tab[data-v="rep"]')
        pg.wait_for_timeout(200)
        stat = pg.evaluate("""() => ({
            cards: document.querySelectorAll('#r_cards .rcard').length,
            bars: document.querySelectorAll('#r_weeks .rbar').length,
            modRows: document.querySelectorAll('#r_mods tr[data-mod]').length,
            adv: document.querySelectorAll('#r_adv li').length,
            cardsText: document.getElementById('r_cards').innerText.replace(/\\s+/g, ' '),
            advText: document.getElementById('r_adv').innerText.slice(0, 120),
        })""")
        print("总览卡:", stat["cards"])
        print("周柱:", stat["bars"])
        print("模块行:", stat["modRows"])
        print("建议条数:", stat["adv"])
        print("卡片文本:", stat["cardsText"][:150])
        print("建议文本:", stat["advText"])
        due_n = int(re.search(r"(\d+)\s*今日该复习", stat["cardsText"]).group(1))
        print("今日该复习计数:", due_n, "/ 预期", n_due_expect)
        assert stat["cards"] == 5 and stat["bars"] == 8 and stat["modRows"] > 0
        assert due_n == n_due_expect, "到期计数与预期不一致"

        # 点「今日该复习」卡 → 应跳回列表且 rev=due
        pg.click('#r_cards .rcard[data-act="due"]')
        pg.wait_for_timeout(200)
        rev = pg.eval_on_selector("#rev", "el => el.value")
        onbank = pg.eval_on_selector("#view-bank", "el => el.classList.contains('on')")
        print("点击今日复习卡 → rev =", rev, ", 切到题库视图:", onbank)
        assert rev == "due" and onbank

        # 清理错题本：前5题有 g>=3 的应可清理
        pg.click('.tab[data-v="rep"]')
        pg.wait_for_timeout(200)
        pg.once("dialog", lambda d: d.accept())
        pg.click("#r_clean")
        pg.wait_for_timeout(200)
        left = pg.evaluate("wrong.size")
        print("清理后错题本:", left)
        pg.screenshot(path=str(ROOT / "_cache" / "rep_test.png"), full_page=False)
        b.close()
    print("OK")
    return 0

if __name__ == "__main__":
    sys.exit(main())
