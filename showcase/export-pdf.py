# -*- coding: utf-8 -*-
"""
deck 导出 PDF（P2 部署/导出闭环）
================================
每套 deck 打印为 PDF：1920×1080 页面 × N 页（骨架 @media print 每 slide 一页，
这里再注入 @page size 保证 1:1 输出，不缩放不裁切）。

用法：
  python showcase/export-pdf.py <slug>            # showcase 样品 → showcase/exports/<slug>.pdf
  python showcase/export-pdf.py <deck-dir>        # 用户自己的 deck 目录（包外任意含
                                                   # index.html 的目录）→ <deck-dir>/<name>.pdf
  python showcase/export-pdf.py <x> --out dir     # 指定输出目录

deck 经 file:// 直读，无需起本地 HTTP 服务；deck 引用的 ../fonts/fonts.css 等
相对资源按目录结构解析（字体库从 showcase/fonts/ 拷一份到 deck 同级即可，
与部署暂存同结构）。
前置：playwright + Chrome。
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


async def export_pdf(deck: Path, out: Path):
    url = (deck / "index.html").as_uri()
    out.parent.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, executable_path=find_chrome())
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})
        await page.goto(url)
        await page.evaluate("document.fonts.ready")
        # 打印样式脚本级强控：不依赖各 deck 骨架的 @media print（早期 deck 缺该块），
        # 统一 1:1 页面尺寸 + 每 slide 一页 + 隐藏 chrome。
        await page.add_style_tag(content="""
            @page { size: 1920px 1080px; margin: 0; }
            html, body { width: 1920px; height: auto; margin: 0 !important; padding: 0 !important; overflow: visible !important; }
            .deck-viewport { position: static !important; overflow: visible !important; }
            .deck-stage { position: static !important; width: auto !important; height: auto !important; transform: none !important; }
            .slide {
                position: relative !important; display: block !important;
                visibility: visible !important; opacity: 1 !important; pointer-events: auto !important;
                width: 1920px !important; height: 1080px !important;
                break-after: page !important; page-break-after: always !important;
                transform: none !important;
            }
            .slide:last-child { break-after: auto !important; page-break-after: auto !important; }
            .deck-chrome, .speaker-note { display: none !important; }
        """)
        await page.pdf(
            path=str(out),
            print_background=True,
            prefer_css_page_size=True,
        )
        await browser.close()
    try:
        shown = out.relative_to(ROOT)
    except ValueError:
        shown = out.resolve()
    print(f"[ok] {deck.name} -> {shown}")


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    deck = resolve_deck(sys.argv[1])
    if "--out" in sys.argv:
        out_dir = Path(sys.argv[sys.argv.index("--out") + 1])
    elif deck.parent == SHOWCASE:
        out_dir = SHOWCASE / "exports"  # showcase 样品：维持 exports/ 惯例
    else:
        out_dir = deck.parent  # 包外 deck：产物放 deck 旁边
    asyncio.run(export_pdf(deck, out_dir / f"{deck.name}.pdf"))


if __name__ == "__main__":
    main()
