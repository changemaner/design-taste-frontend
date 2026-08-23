# -*- coding: utf-8 -*-
"""
gallery 截图重建（P0.3，字体自托管后重截）
=========================================
每套 deck 截 slide 0/4/7 三张 1920×1080 到 showcase/gallery/<slug>/，
供 gallery/index.html 图廊展示。等待 document.fonts.ready 保证字体加载完成。

用法：python showcase/gallery-shots.py [slug ...]   # 缺省全部
前置：本地 HTTP 服务器（python -m http.server 8899）+ playwright + 系统 Chrome
"""
import asyncio
import sys
from pathlib import Path

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent
SHOWCASE = ROOT / "showcase"
GALLERY = SHOWCASE / "gallery"
BASE_URL = "http://127.0.0.1:8899"
def find_chrome():
    """Chrome 定位：DESIGN_CHROME / CHROME_PATH 环境变量 → 各平台常见安装路径 → None。
    返回 None 时 playwright 回退自带 chromium（需 playwright install chromium）。"""
    import os
    for var in ("DESIGN_CHROME", "CHROME_PATH"):
        p = os.environ.get(var)
        if p and Path(p).exists():
            return p
    for c in (
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        str(Path.home() / "AppData" / "Local" / "Google" / "Chrome" / "Application" / "chrome.exe"),
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/usr/bin/google-chrome",
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
        "/snap/bin/chromium",
    ):
        if Path(c).exists():
            return c
    return None
SHOT_SLIDES = (0, 4, 7)
# 兼容两种 server 启动方式：包根启动（/showcase/<slug>/）或 showcase 目录启动（/<slug>/）
DECK_PATHS = [f"{BASE_URL}/showcase/{{slug}}/index.html", f"{BASE_URL}/{{slug}}/index.html"]


async def goto_deck(page, slug, slide):
    """导航到 deck 页，自动尝试两种 server 根（包根 / showcase 目录）。"""
    for tmpl in DECK_PATHS:
        try:
            await page.goto(tmpl.format(slug=slug) + f"?slide={slide}", wait_until="domcontentloaded", timeout=8000)
            # 判定依据是页面真的渲染出了 deck（有 .slide 元素），
            # 不能只看 title：python http.server 的 404 页标题是 "Error response"，不含 "404"
            has_slide = await page.evaluate("() => !!document.querySelector('.slide')")
            if has_slide:
                return
        except Exception:
            continue
    raise RuntimeError(f"{slug}: 两种 server 根都未加载到 deck 页面")


async def main():
    slugs = sys.argv[1:] or [
        d.name for d in SHOWCASE.iterdir()
        if d.is_dir() and d.name != "gallery" and (d / "index.html").exists()
    ]
    done, fail = [], []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, executable_path=find_chrome())
        for slug in slugs:
            target = GALLERY / slug
            target.mkdir(parents=True, exist_ok=True)
            page = await browser.new_page(viewport={"width": 1920, "height": 1080})
            try:
                for i in SHOT_SLIDES:
                    await goto_deck(page, slug, i)
                    await page.evaluate("document.fonts.ready")
                    await page.wait_for_timeout(1200)  # 等 reveal 动画
                    await page.screenshot(path=str(target / f"slide-{i}.png"))
                done.append(slug)
            except Exception as e:
                fail.append(f"{slug}: {e}")
            await page.close()
        await browser.close()
    print(f"已重截 {len(done)} 套: {', '.join(done)}")
    if fail:
        print(f"失败 {len(fail)} 套:")
        for f in fail:
            print(f"  {f}")


if __name__ == "__main__":
    asyncio.run(main())
