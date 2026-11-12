# -*- coding: utf-8 -*-
"""UI 冒烟测试 v2：四视图导航 / 首页仪表盘 / chips / 题卡层级 / 快捷键 / 项目连环问 / 分析视图。"""
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
PAGE = (ROOT / "dist" / "bank.html").resolve()

def main() -> int:
    with sync_playwright() as p:
        b = p.chromium.launch(channel="msedge")
        pg = b.new_page(viewport={"width": 1280, "height": 900})
        js_errors = []
        pg.on("pageerror", lambda e: js_errors.append(str(e)))
        pg.goto(PAGE.as_uri())
        pg.wait_for_timeout(300)
        ok = []

        def tab(v):
            pg.click(f'.tab[data-v="{v}"]')
            pg.wait_for_timeout(200)

        # 1. 默认首页：数据卡 4 张 + 快速入口 4 + 今日任务 4 + 岗位进度 8
        n_cards = pg.evaluate("document.querySelectorAll('#scards .scard').length")
        n_quick = pg.evaluate("document.querySelectorAll('#h_quick .qcard').length")
        n_tasks = pg.evaluate("document.querySelectorAll('#h_tasks .titem').length")
        n_profs = pg.evaluate("document.querySelectorAll('#h_profs .prow').length")
        ok.append(("首页默认视图", pg.eval_on_selector("#view-home", "el => el.classList.contains('on')")))
        ok.append(("数据卡/快速入口/任务/岗位进度", n_cards == 4 and n_quick == 5 and n_tasks == 4 and n_profs == 8))

        # 2. 最近记录兜底（无 hist 无 review → 引导文案）
        empty_hist = pg.eval_on_selector("#h_hist", "el => el.innerText.includes('还没有训练记录')")
        ok.append(("最近记录空态引导", empty_hist))

        # 3. 今日任务点击 → 切题库并筛选（今日复习）
        pg.click('#h_tasks .titem[data-a="due"]')
        pg.wait_for_timeout(200)
        ok.append(("任务点击跳筛选", pg.eval_on_selector("#view-bank", "el => el.classList.contains('on')")
                   and pg.eval_on_selector("#rev", "el => el.value") == "due"))

        # 4. 岗位进度点击 → prof 选中并切题库
        tab("home")
        pg.click('#h_profs .prow')  # 第一个岗位模板
        pg.wait_for_timeout(200)
        prof_v = pg.eval_on_selector("#prof", "el => el.value")
        ok.append(("岗位进度点击", pg.eval_on_selector("#view-bank", "el => el.classList.contains('on')") and prof_v != ""))

        # 5. 题库视图：chips / pills / 难度（回归）
        pg.click('#chips .chip[data-c="p0"]'); pg.wait_for_timeout(150)
        ok.append(("P0 chip 联动", pg.eval_on_selector('#chips .chip[data-c="p0"]', "el => el.classList.contains('on')")))
        pg.click("#moref summary"); pg.wait_for_timeout(100)
        pg.select_option("#co", "Momenta"); pg.wait_for_timeout(150)
        ok.append(("公司 pill", "Momenta" in pg.eval_on_selector("#fpills", "el => el.innerText")))
        pg.click("#fpills .fpill i"); pg.wait_for_timeout(150)
        ok.append(("pill × 移除", pg.eval_on_selector("#co", "el => el.value") == ""))
        pg.click('#chips .chip[data-c="all"]'); pg.wait_for_timeout(150)

        # 6. 题卡层级：注入 review → 状态点/难度星/来源底部（回归）
        ids = pg.evaluate("DATA.slice(0, 20).map(q => q.id)")
        now = int(time.time() * 1000)
        review = {qid: {"g": 1 + i % 4, "ts": now - int(i * 2.2 * 864e5)} for i, qid in enumerate(ids)}
        pg.evaluate("rv => localStorage.setItem('ib_review_v1', JSON.stringify(rv))", review)
        pg.reload(); pg.wait_for_timeout(300)
        tab("bank"); pg.wait_for_timeout(100)
        q1 = pg.evaluate("""() => {
          const el = document.querySelector('#list .q');
          return {dot: !!el.querySelector('.qdot'),
                  stars: !!el.querySelector('.qh .tag[title=难度]')};
        }""")
        ok.append(("题卡状态点/难度星", q1["dot"] and q1["stars"]))

        # 7. 快捷键（回归）：/ 聚焦、j、空格、4 自评
        pg.click("body"); pg.keyboard.press("Escape")
        pg.keyboard.press("/")
        ok.append(("/ 聚焦搜索", pg.evaluate("document.activeElement.id") == "q"))
        pg.keyboard.press("Escape")
        pg.keyboard.press("j")
        ok.append(("j 焦点", pg.evaluate("!!document.querySelector('#list .q.foc')")))
        pg.keyboard.press("4"); pg.wait_for_timeout(250)
        hist_n = pg.evaluate("hist.length")
        ok.append(("自评写入训练历史", hist_n >= 1))

        # 8. 训练视图：模拟面试入口 + 项目连环问 6 卡 + 打开连环问
        tab("train")
        n_proj = pg.evaluate("Object.keys(PROJ).length")
        cards = pg.evaluate("document.querySelectorAll('#tr_projects .trcard').length")
        ok.append(("项目连环问卡片", n_proj == 6 and cards == 6))
        pg.click('#tr_projects .trcard')  # 第一个项目（题最多的）
        pg.wait_for_timeout(200)
        running = pg.evaluate("document.getElementById('mockov').style.display === 'block'")
        clock = pg.eval_on_selector("#m_clock", "el => el.textContent")
        src = pg.eval_on_selector("#m_src", "el => el.textContent")
        ok.append(("连环问打开且不限时", running and clock == "不限时" and "项目连环问" in src))
        # 顺序性：第 1 题应是该项目 ID 最小的
        first_ok = pg.evaluate("""() => {
          const sub = MOCK.drill, q = MOCK.list[0];
          const sorted = [...PROJ[sub]].sort((a,b)=>a.id<b.id?-1:1);
          return q.id === sorted[0].id;
        }""")
        ok.append(("连环问顺序抽题", first_ok))
        # 自评两题 → hist 带 m=1
        pg.click("#m_run .gbtn"); pg.wait_for_timeout(100)
        pg.click("#m_next"); pg.wait_for_timeout(100)
        pg.click("#m_run .gbtn"); pg.wait_for_timeout(100)
        m_flag = pg.evaluate("hist.slice(-2).every(h => h.m === 1)")
        ok.append(("连环问训练历史标记", m_flag))
        pg.click("#m_close"); pg.wait_for_timeout(100)
        ok.append(("退出后 live 复位", pg.evaluate("MOCK.live === false")))

        # 9. 首页最近记录现在有 hist
        tab("home")
        ok.append(("最近记录有内容", pg.evaluate("document.querySelectorAll('#h_hist .hitem').length >= 2")))

        # 10. 分析视图（回归）：5 卡 + 8 柱 + 模块行
        tab("rep")
        ok.append(("分析视图渲染", pg.eval_on_selector("#view-rep", "el => el.classList.contains('on')")
                   and pg.evaluate("document.querySelectorAll('#r_cards .rcard').length") == 5
                   and pg.evaluate("document.querySelectorAll('#r_weeks .rbar').length") == 8))
        # 分析里的「今日该复习」卡 → 跳题库
        pg.click('#r_cards .rcard[data-act="due"]'); pg.wait_for_timeout(200)
        ok.append(("分析卡跳题库", pg.eval_on_selector("#view-bank", "el => el.classList.contains('on')")
                   and pg.eval_on_selector("#rev", "el => el.value") == "due"))

        # 11. 岗位视图：8 个种子岗位 + JD 分析 + 训练跳转 + 添加岗位
        tab("jobs")
        n_jobs = pg.evaluate("document.querySelectorAll('#joblist .jcard').length")
        ok.append(("岗位卡片=种子8", n_jobs == 8))
        pg.click('#joblist .jcard .qh')  # 展开第一张（桥介数物 C++ SDK）
        pg.wait_for_timeout(150)
        hit_rows = pg.evaluate("document.querySelectorAll('#joblist .jcard .rtable tbody tr').length")
        ok.append(("JD 技能分析行", hit_rows >= 3))
        grade_badge = pg.evaluate("!!document.querySelector('#joblist .jcard .tstat')")
        ok.append(("缺口判断徽标", grade_badge))
        # V1.6：匹配三维度徽标（覆盖/掌握/资格）+ 技能四态 + 结论行
        badges = pg.evaluate("[...document.querySelector('#joblist .jcard').querySelectorAll('.qh .rscore')].map(x => x.innerText)")
        ok.append(("三维度徽标", any('覆盖' in t for t in badges) and any('掌握' in t for t in badges) and any('届' in t for t in badges)))
        state_col = pg.evaluate("!!document.querySelector('#joblist .jcard .rtable th:nth-child(3)') && document.querySelector('#joblist .jcard .rtable th:nth-child(3)').innerText.includes('证据')")
        ok.append(("技能四态列", state_col))
        concl = pg.evaluate("[...document.querySelectorAll('#joblist .qmeta')].some(x => x.innerText.includes('结论'))")
        ok.append(("结论行", concl))
        # 首页雷达可信行（真实扫描时间）
        tab("home")
        ok.append(("首页雷达可信行", pg.eval_on_selector('#h_radar', "el => el.innerText.includes('岗位雷达') && el.innerText.includes('最近实际扫描')")))
        tab("jobs")   # 回岗位视图，继续「训练该技能」跳转测试
        pg.click('#joblist .jcard .qh'); pg.wait_for_timeout(150)  # 重渲染后重新展开
        # 训练该技能 → 切题库并按模块筛选
        pg.click('#joblist [data-jtrain]'); pg.wait_for_timeout(250)
        ok.append(("技能训练跳题库", pg.eval_on_selector("#view-bank", "el => el.classList.contains('on')")
                   and pg.eval_on_selector("#mod", "el => el.value") != ""))
        # 添加岗位（本地）
        tab("jobs")
        pg.click("#jobform summary"); pg.wait_for_timeout(100)
        pg.fill("#j_co", "宇树科技"); pg.fill("#j_ti", "具身智能软件工程师")
        pg.fill("#j_city", "杭州"); pg.fill("#j_jd", "熟悉 ROS2 与运动学控制，C++ 扎实，了解深度学习部署")
        pg.click("#j_save"); pg.wait_for_timeout(200)
        ok.append(("添加本地岗位", pg.evaluate("document.querySelectorAll('#joblist .jcard').length") == 9))
        ok.append(("本地岗位匹配分析", pg.evaluate("[...document.querySelectorAll('#joblist .jcard')].some(c => c.querySelector('.qh .qt').textContent.includes('具身智能') && c.querySelector('.rscore'))")))
        # 删除本地岗位
        pg.once("dialog", lambda d: d.accept())
        pg.click('#joblist [data-jdel]'); pg.wait_for_timeout(200)
        ok.append(("删除本地岗位", pg.evaluate("document.querySelectorAll('#joblist .jcard').length") == 8))

        # 11.5 岗位雷达：快照注入 + 收藏转正/忽略闭环
        n_radar = pg.evaluate("(RADAR.jobs || []).length")
        ok.append(("雷达快照>50岗", n_radar > 50))
        pg.click("#radarbox summary"); pg.wait_for_timeout(150)
        n_cards = pg.evaluate("document.querySelectorAll('#radarlist .rcard2').length")
        ok.append(("雷达卡渲染(≤40)", 0 < n_cards <= 40))
        pg.click('#radarlist [data-rcollect]'); pg.wait_for_timeout(200)
        ok.append(("收藏转正进正式列表", pg.evaluate(
            "loadJobs().some(j => j.id && j.id.startsWith('radar_'))")))
        pg.click('#radarlist [data-rdismiss]'); pg.wait_for_timeout(200)
        ok.append(("忽略后不重复显示", pg.evaluate(
            "loadDismiss().size >= 1")))

        # 11.8 V1.8：全部公司总览 + 校招/实习分类 + 已收藏/已忽略仍可查
        tab("comp")
        n_all_co = pg.evaluate("allCompanies().length")
        n_all_job = pg.evaluate("(RADAR.jobs || []).length")
        rows_co = pg.evaluate("document.querySelectorAll('#comp_table tbody tr').length")
        rows_job = pg.evaluate("document.querySelectorAll('#comp_jobs tbody tr').length")
        ok.append(("公司总览全量可见", rows_co == n_all_co and rows_co > 100))
        ok.append(("岗位总览含已处理", rows_job == n_all_job and n_all_job > 300))
        heads = pg.eval_on_selector_all('#comp_jobs .rsec', 'els => els.map(e => e.innerText).join(" ")')
        ok.append(("按校招/实习分组", "校招" in heads and "实习" in heads))
        cs = pg.evaluate("RADAR.class_stats || {}")
        pg.click('.chip[data-k="cls"][data-v="实习"]'); pg.wait_for_timeout(200)
        ok.append(("实习筛选数量", pg.evaluate(
            "document.querySelectorAll('#comp_jobs tbody tr').length") == cs.get("实习", 0)))
        pg.click('.chip[data-k="cls"][data-v="校招"]'); pg.wait_for_timeout(200)
        ok.append(("校招筛选数量", pg.evaluate(
            "document.querySelectorAll('#comp_jobs tbody tr').length") == cs.get("校招", 0)))
        ok.append(("公司表不受分类筛选影响", pg.evaluate(
            "document.querySelectorAll('#comp_table tbody tr').length") == n_all_co))
        pg.click('.chip[data-k="cls"][data-v="all"]'); pg.wait_for_timeout(200)
        n_dis = pg.evaluate("[...loadDismiss()].length")
        pg.click('#comp_more summary'); pg.wait_for_timeout(150)   # 展开「更多筛选」
        pg.click('.chip[data-k="st"][data-v="dismissed"]'); pg.wait_for_timeout(200)
        ok.append(("已忽略岗位仍可查", pg.evaluate(
            "document.querySelectorAll('#comp_jobs tbody tr').length") == n_dis and n_dis >= 1))
        pg.click('.chip[data-k="st"][data-v="saved"]'); pg.wait_for_timeout(200)
        ok.append(("已收藏岗位仍可查", pg.evaluate(
            "document.querySelectorAll('#comp_jobs tbody tr').length") >= 1))
        pg.click('.chip[data-k="st"][data-v="all"]'); pg.wait_for_timeout(200)
        pg.fill('#comp_q', "Momenta"); pg.wait_for_timeout(350)
        n_hit = pg.evaluate("document.querySelectorAll('#comp_table tbody tr').length")
        ok.append(("搜索联动公司/岗位", 0 < n_hit < n_all_co and pg.evaluate(
            "document.querySelectorAll('#comp_jobs tbody tr').length") > 0))
        pg.fill('#comp_q', ""); pg.wait_for_timeout(350)
        pg.click('#comp_table tbody tr[data-coname] td:first-child'); pg.wait_for_timeout(350)
        ok.append(("点公司行联动搜索", pg.eval_on_selector('#comp_q', 'el => el.value') != ""
                   and pg.evaluate("document.querySelectorAll('#comp_table tbody tr').length") < n_all_co))
        pg.fill('#comp_q', ""); pg.wait_for_timeout(350)
        city_sum = pg.evaluate("""() => [...document.querySelectorAll(
            '.chip[data-k="city"] b')].reduce((a, b) => a + Number(b.textContent), 0)""")
        expect = pg.evaluate("""() => (RADAR.jobs || []).reduce(
            (a, j) => a + citiesOf(j.city).length, 0)""")
        ok.append(("城市计数覆盖全量", city_sum == expect and expect >= n_all_job > 0))
        pg.click('.chip[data-k="city"][data-v="苏州"]'); pg.wait_for_timeout(250)
        ok.append(("城市筛选联动两表", pg.evaluate(
            "document.querySelectorAll('#comp_table tbody tr').length") <= n_all_co))
        pg.click('.chip[data-k="city"][data-v="all"]'); pg.wait_for_timeout(250)
        ok.append(("牛客面经列展示", pg.eval_on_selector(
            '#comp_table', "el => el.innerText.includes('牛客')")))
        # V1.8.3：重置键 + 面经/真题卷面板
        pg.click('.chip[data-k="cls"][data-v="实习"]'); pg.wait_for_timeout(200)
        ok.append(("重置键显示计数", pg.eval_on_selector(
            '#comp_reset', 'el => el.innerText.includes("重置(")')))
        pg.click('#comp_reset'); pg.wait_for_timeout(250)
        ok.append(("重置键清空筛选", pg.eval_on_selector('#comp_reset', "el => el.innerText.trim()") == '↩ 重置'
                   and pg.evaluate("document.querySelectorAll('#comp_jobs tbody tr').length") == n_all_job
                   and pg.eval_on_selector('#comp_q', 'el => el.value') == ''))
        ok.append(("面经面板默认10篇+更多", pg.evaluate(
            "document.querySelectorAll('#nc_exp .nccard').length") == 10
            and pg.evaluate("!!document.querySelector('[data-ncmore]')")))
        ok.append(("真题卷面板全量", pg.evaluate(
            "document.querySelectorAll('#nc_papers tbody tr').length") == pg.evaluate("(NC.papers||[]).length")))
        pg.fill('#comp_q', '华为'); pg.wait_for_timeout(350)
        ok.append(("面经/套卷随搜索联动", pg.evaluate(
            "document.querySelectorAll('#nc_papers tbody tr').length") < pg.evaluate("(NC.papers||[]).length")
            and pg.eval_on_selector('#nc_exp', 'el => el.innerText.includes("华为")')))
        pg.fill('#comp_q', ''); pg.wait_for_timeout(350)
        # V1.8.4：面经筛选（公司/轮次/只看有题号）+ 原文展开 + 题号跳题库
        n_cards = pg.evaluate("document.querySelectorAll('#nc_exp .nccard').length")
        pg.click('#nc_co_chips .chip[data-nk="co"]:nth-child(2)'); pg.wait_for_timeout(250)
        ok.append(("面经公司筛选", 0 < pg.evaluate(
            "document.querySelectorAll('#nc_exp .nccard').length") <= n_cards))
        pg.click('#nc_co_chips .chip[data-nk="co"][data-v="all"]'); pg.wait_for_timeout(200)
        pg.check('#nc_onlyref'); pg.wait_for_timeout(250)
        n_ref = pg.evaluate("document.querySelectorAll('#nc_exp .nccard').length")
        ok.append(("只看有题号", 0 < n_ref <= n_cards))
        pg.uncheck('#nc_onlyref'); pg.wait_for_timeout(200)
        pg.click('#nc_exp .nccard summary'); pg.wait_for_timeout(250)
        ok.append(("面经展开原文", pg.evaluate(
            "document.querySelectorAll('#nc_exp .nccard[open] .nch').length") >= 1))
        has_ref = pg.evaluate("!!document.querySelector('#nc_exp a.qref[data-q]')")
        if has_ref:
            pg.evaluate("document.querySelector('#nc_exp a.qref[data-q]').click()")
            pg.wait_for_timeout(350)
            ok.append(("题号跳题库", pg.eval_on_selector('#view-bank', "el => el.classList.contains('on')")
                       and pg.eval_on_selector('#q', "el => el.value.indexOf('Q-') === 0")))
            tab("comp")
        else:
            ok.append(("题号跳题库", False))
        tab("home"); pg.click('#h_allco'); pg.wait_for_timeout(200)
        ok.append(("首页入口跳公司总览", pg.eval_on_selector(
            '#view-comp', "el => el.classList.contains('on')")))

        # 12. V1.9.1 宝典考点地图：双教程 / 章计数 / 练这一章题数一致 / 清除 / 首页入口
        tab("rep")
        ok.append(("宝典章节渲染", pg.evaluate(
            "document.querySelectorAll('#tut_body .tch').length") == 8
            and pg.evaluate("(TUT.tutorials||[]).length") == 2))
        n_target = int(pg.evaluate(
            """() => { const b = document.querySelector('#tut_body .tch:nth-child(2) button[data-tids]');
                       return b ? b.innerText.match(/(\\d+)/)[1] : '-1'; }"""))
        pg.click('#tut_body .tch:nth-child(2) button[data-tids]'); pg.wait_for_timeout(400)
        ok.append(("练这一章题数一致", n_target > 0
                   and pg.evaluate("document.querySelectorAll('#list .q').length") == n_target
                   and pg.eval_on_selector('#tutbanner', "el => !el.hidden")))
        pg.click('#tutclear'); pg.wait_for_timeout(300)
        ok.append(("清除章节筛选", pg.evaluate("document.querySelectorAll('#list .q').length")
                   == pg.evaluate("DATA.length")))
        tab("rep")
        pg.click('#tut_tabs .tchip[data-tut="95"]'); pg.wait_for_timeout(300)
        ok.append(("宝典切 tab", pg.eval_on_selector(
            '#tut_meta', "el => el.innerText.includes('机器学习')")))
        ok.append(("宝典缺口提示", pg.eval_on_selector(
            '#tut_lead', "el => el.innerText.includes('缺口')")))
        tab("home"); pg.click('#h_quick .qcard[data-a="tut"]'); pg.wait_for_timeout(300)
        ok.append(("首页进考点地图", pg.eval_on_selector(
            '#view-rep', "el => el.classList.contains('on')")))

        # 13. hash 记忆：刷新后仍在当前 tab
        tab("train")
        pg.reload(); pg.wait_for_timeout(300)
        ok.append(("刷新保持视图", pg.eval_on_selector("#view-train", "el => el.classList.contains('on')")))

        pg.screenshot(path=str(ROOT / "_cache" / "ui2_home.png"))
        b.close()

    ok.append(("无 JS 运行时错误", not js_errors))
    if js_errors:
        print("JS 错误:", js_errors[:3])
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
