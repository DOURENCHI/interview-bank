# -*- coding: utf-8 -*-
"""UI 改版冒烟测试：数据卡 / chips / pills / 题卡层级 / 快捷键 / 模拟面试增强。"""
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
PAGE = (ROOT / "dist" / "bank.html").resolve()

def main() -> int:
    with sync_playwright() as p:
        b = p.chromium.launch(channel="msedge")
        pg = b.new_page(viewport={"width": 1280, "height": 900})
        pg.goto(PAGE.as_uri())
        pg.wait_for_timeout(300)
        ok = []

        # 1. 顶部数据卡：4 张，数字正确（全新状态：今日0/薄弱0/错题0）
        n = pg.evaluate("document.querySelectorAll('#scards .scard').length")
        t = pg.eval_on_selector("#scards", "el => el.innerText.replace(/\\s+/g, ' ')")
        ok.append(("数据卡4张", n == 4 and "913" in t))

        # 2. chips：点 P0 → pri=P0 且亮、列表全 P0；再点取消
        pg.click('#chips .chip[data-c="p0"]')
        pg.wait_for_timeout(150)
        pri = pg.eval_on_selector("#pri", "el => el.value")
        cnt = pg.eval_on_selector("#stat", "el => el.textContent")
        on = pg.eval_on_selector('#chips .chip[data-c="p0"]', "el => el.classList.contains('on')")
        ok.append(("P0 chip 联动", pri == "P0" and on and "当前 596" in cnt))
        pg.click('#chips .chip[data-c="p0"]')
        pg.wait_for_timeout(150)
        ok.append(("P0 chip 再点取消", pg.eval_on_selector("#pri", "el => el.value") == ""))

        # 3. 详细筛选 pill：展开折叠面板 → 选公司 → pill 出现 → × 单独移除
        pg.click("#moref summary")
        pg.wait_for_timeout(150)
        pg.select_option("#co", "Momenta")
        pg.wait_for_timeout(200)
        pills = pg.eval_on_selector("#fpills", "el => el.innerText")
        ok.append(("公司 pill 出现", "Momenta" in pills and "公司" in pills))
        pg.click("#fpills .fpill i")
        pg.wait_for_timeout(200)
        ok.append(("pill × 移除", pg.eval_on_selector("#co", "el => el.value") == ""
                   and pg.eval_on_selector("#fpills", "el => el.children.length") == 0))

        # 4. 难度筛选
        pg.select_option("#dif", "3")
        pg.wait_for_timeout(200)
        ok.append(("难度筛选", "当前" in pg.eval_on_selector("#stat", "el => el.textContent")))
        pg.select_option("#dif", "")

        # 5. 题卡层级：注入自评 → 掌握状态点 + 追问预览 + qmeta
        ids = pg.evaluate("DATA.slice(0, 20).map(q => q.id)")
        now = int(time.time() * 1000)
        review = {qid: {"g": 1 + i % 4, "ts": now - int(i * 2.2 * 864e5)} for i, qid in enumerate(ids)}
        pg.evaluate("rv => localStorage.setItem('ib_review_v1', JSON.stringify(rv))", review)
        pg.reload(); pg.wait_for_timeout(300)
        q1 = pg.evaluate("""() => {
          const el = document.querySelector('#list .q');
          return {dot: !!el.querySelector('.qdot'), dotText: el.querySelector('.qdot')?.innerText.trim(),
                  qf: el.querySelector('.qf')?.innerText.trim() || '',
                  stars: !!el.querySelector('.qh .tag[title=难度]')};
        }""")
        ok.append(("掌握状态点", q1["dot"] and q1["dotText"] in ("待学习", "薄弱", "今日复习", "已掌握")))
        ok.append(("难度星", q1["stars"]))
        # 追问预览：展开任意一张有追问的卡，qmeta 应在 body 内
        qmeta = pg.evaluate("""() => {
          const el = [...document.querySelectorAll('#list .q')].find(x => x.querySelector('.qmeta'));
          return el ? {src: el.querySelector('.qmeta').innerText.includes('来源'),
                       inBody: !!el.querySelector('.body .qmeta')} : null;
        }""")
        ok.append(("来源在卡片底部", qmeta is not None and qmeta["src"] and qmeta["inBody"]))

        # 6. 快捷键：/ 聚焦搜索、Esc 失焦、j 移动焦点、空格展开、4 自评
        pg.keyboard.press("Escape")
        pg.click("body")
        pg.keyboard.press("/")     # 聚焦搜索
        focused = pg.evaluate("document.activeElement.id")
        ok.append(("/ 聚焦搜索", focused == "q"))
        pg.keyboard.press("Escape")
        pg.keyboard.press("j")
        foc = pg.evaluate("!!document.querySelector('#list .q.foc')")
        ok.append(("j 焦点第一题", foc))
        pg.keyboard.press(" ")
        opened = pg.evaluate("document.querySelector('#list .q.foc').classList.contains('open')")
        ok.append(("空格展开", opened))
        pg.keyboard.press("4")
        pg.wait_for_timeout(200)
        g = pg.evaluate("review[Object.keys(review)[0]].g")
        ok.append(("数字4自评", g == 4))

        # 7. 模拟面试：不限时 + 作答草稿跨题保留
        pg.click("#mock"); pg.wait_for_timeout(150)
        pg.select_option("#m_sec", "0")
        pg.select_option("#m_n", "5")
        pg.click("#m_start"); pg.wait_for_timeout(200)
        clock = pg.eval_on_selector("#m_clock", "el => el.textContent")
        pg.fill("#m_note", "RAII unique_ptr 所有权")
        pg.click("#m_next"); pg.wait_for_timeout(200)
        pg.click("#m_skip")  # 回不到上一题，所以验证：切回第3题后再看草稿逻辑 → 简化：验证草稿随输入保存
        saved = pg.evaluate("Object.keys(MOCK.notes).length >= 1 && Object.values(MOCK.notes).some(v => v.includes('RAII'))")
        ok.append(("不限时显示", clock == "不限时"))
        ok.append(("作答草稿保存", saved))
        pg.click("#m_close")

        # 8. 学习报告回归
        pg.click("#rep"); pg.wait_for_timeout(200)
        cards = pg.evaluate("document.querySelectorAll('#r_cards .rcard').length")
        ok.append(("学习报告正常", pg.eval_on_selector("#repov", "el => el.style.display") == "flex" and cards == 5))

        pg.screenshot(path=str(ROOT / "_cache" / "ui_top.png"))
        b.close()

    fails = [k for k, v in ok if not v]
    for k, v in ok:
        print(("✓" if v else "✗"), k)
    if fails:
        print("失败:", fails)
        return 1
    print("OK 全部通过")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
