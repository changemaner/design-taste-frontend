# -*- coding: utf-8 -*-
"""
全页截图（视觉 QA 全量输入）
==============================
每套 deck 截全部 slide 1920×1080：showcase 套落在 showcase/<slug>/screenshots/
（作为每套成品的唯一全量截图目录，gallery 只保留 0/4/7 三张预览）；包外用户
deck 落在 deck 旁 screenshots/。页数按 deck 实际 .slide 数量动态截取。

用法：python showcase/shot-all-slides.py [slug 或 deck 目录 ...]   # 缺省全部 showcase 套
deck 经 file:// 直读，无需起本地 HTTP 服务。前置：playwright + 系统 Chrome
"""
import asyncio
import sys
from pathlib import Path

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent
SHOWCASE = ROOT / "showcase"
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


def resolve_deck(arg: str) -> Path:
    """slug → showcase/<slug>/；否则当作 deck 目录路径（用户自己生成的 HTML）。"""
    slug_dir = SHOWCASE / arg
    if (slug_dir / "index.html").exists():
        return slug_dir
    p = Path(arg)
    if (p / "index.html").exists():
        return p.resolve()
    raise SystemExit(f"[!!] 找不到 deck：{arg}（既不是 showcase/<slug>，也不是含 index.html 的目录）")


async def main():
    args = sys.argv[1:]
    decks = [resolve_deck(a) for a in args] or [
        d for d in SHOWCASE.iterdir()
        if d.is_dir() and d.name != "gallery" and (d / "index.html").exists()
    ]
    done, fail = [], []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, executable_path=find_chrome())
        for deck in decks:
            target = deck / "screenshots"
            target.mkdir(parents=True, exist_ok=True)
            page = await browser.new_page(viewport={"width": 1920, "height": 1080})
            try:
                url = (deck / "index.html").as_uri()
                await page.goto(url, wait_until="domcontentloaded", timeout=8000)
                n = await page.evaluate("document.querySelectorAll('.slide').length")
                if not n:
                    raise RuntimeError("页面无 .slide 元素（不是 deck 骨架？）")
                for i in range(n):
                    await page.goto(f"{url}?slide={i}", wait_until="domcontentloaded", timeout=8000)
                    await page.evaluate("document.fonts.ready")
                    await page.wait_for_timeout(1200)
                    await page.screenshot(path=str(target / f"slide-{i}.png"))
                done.append(deck.name)
                print(f"[ok] {deck.name}: {n} 页")
            except Exception as e:
                fail.append(f"{deck.name}: {e}")
            await page.close()
        await browser.close()
    print(f"完成 {len(done)}/{len(decks)}: {', '.join(done)}")
    if fail:
        print("失败:")
        for f in fail:
            print(f"  {f}")


if __name__ == "__main__":
    asyncio.run(main())
