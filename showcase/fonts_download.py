# -*- coding: utf-8 -*-
"""
字体自托管：下载 Google Fonts 的 latin 子集 woff2 到本地共享字体库
=================================================================
背景：30 套 deck 全部用 Google Fonts 外链加载字体。发到国内/飞书生态时，
      fonts.googleapis.com / fonts.gstatic.com 可能被墙，导致字体回退系统字体。
      本脚本把每套 deck 用到的字体族按 latin 子集下载到 showcase/fonts/，
      并生成共享 fonts.css，让 deck 改用本地相对路径引用（随 Vercel/妙搭一起托管）。

设计：
  - 字体文件按 <Family>-<Weight>[-<Style>].woff2 命名，放进 showcase/fonts/
  - 只取 latin 子集（deck 内容为英文；省体积、避免 cyrillic/greek 等用不到的子集）
  - 同名同字重字体只下载一次（Inter 被 20+ 套共享）
  - 生成 fonts.css 含所有 @font-face 声明，供 deck 引用

用法：python showcase/fonts_download.py
前置：playwright + 系统 Chrome
"""
import asyncio
import json
import re
import sys
from pathlib import Path

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent
SHOWCASE = ROOT / "showcase"
FONTS_DIR = SHOWCASE / "fonts"
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


def deck_font_urls():
    """扫描每套 deck 的 Google Fonts 外链 URL。"""
    out = {}
    for d in SHOWCASE.iterdir():
        if not d.is_dir():
            continue
        idx = d / "index.html"
        if not idx.exists():
            continue
        m = re.search(r'href="(https://fonts\.googleapis\.com/[^"]+)"', idx.read_text(encoding="utf-8"))
        if m:
            out[d.name] = m.group(1)
    return out


def parse_css_fonts(css: str):
    """从 Google Fonts CSS 提取 @font-face 声明，按 (family, style, weight) 聚合。"""
    faces = []
    # 按块切分 @font-face { ... }
    for block in re.finditer(r"@font-face\s*{([^}]*)}", css):
        body = block.group(1)
        def grab(prop):
            m = re.search(rf"{prop}:\s*([^;]+);", body)
            return m.group(1).strip() if m else None
        src = grab("src")
        if not src:
            continue
        url_m = re.search(r"url\(([^)]+)\)", src)
        family = (grab("font-family") or "").strip("'\"")
        style = grab("font-style") or "normal"
        weight = grab("font-weight") or "400"
        urange = grab("unicode-range") or ""
        faces.append({
            "family": family,
            "style": style,
            "weight": weight,
            "url": url_m.group(1).strip("\"'") if url_m else None,
            "unicode_range": urange,
        })
    return faces


def latin_subset(faces):
    """只保留 latin 子集（unicode-range 含 U+0000-00FF）。"""
    latin = []
    for f in faces:
        ur = f["unicode_range"]
        # latin 子集的 unicode-range 通常是 U+0000-00FF, U+0131, ...
        if ur and ("U+0000-00FF" in ur or ur.startswith("U+0000")):
            latin.append(f)
    return latin


async def main():
    urls = deck_font_urls()
    print(f"扫描到 {len(urls)} 套 deck 有字体外链")
    if not urls:
        sys.exit("未找到任何字体外链")

    FONTS_DIR.mkdir(exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, executable_path=find_chrome())
        page = await browser.new_page()

        # 汇总所有 deck 需要的字体文件
        need = {}  # (family, style, weight) -> url
        all_faces = []  # 全量 @font-face（去重后），生成 fonts.css
        seen_face = set()
        for slug, url in sorted(urls.items()):
            try:
                resp = await page.goto(url, wait_until="load", timeout=30000)
                css = await page.content()
            except Exception as e:
                print(f"[warn] {slug}: 抓 CSS 失败 {e}")
                continue
            faces = parse_css_fonts(css)
            latin = latin_subset(faces)
            if not latin:
                print(f"[warn] {slug}: 无 latin 子集? (faces={len(faces)})")
                latin = faces  # 兜底
            for f in latin:
                if not f["url"]:
                    continue
                key = (f["family"], f["style"], f["weight"])
                need[key] = f["url"]
                if key not in seen_face:
                    seen_face.add(key)
                    all_faces.append(f)
            print(f"[ok] {slug}: {len(latin)} 个 latin 字体面")

        await browser.close()

    print(f"\n合计需要 {len(need)} 个字体文件:")
    for (fam, sty, wt), u in sorted(need.items()):
        print(f"  {fam:22s} {sty:6s} {wt:5s} -> {u.split('/')[-1]}")

    # 下载 woff2
    import urllib.request
    names = {}
    for (fam, sty, wt), url in sorted(need.items()):
        safe = re.sub(r"[^A-Za-z0-9]", "", fam)
        wt_safe = wt.replace(" ", "-")  # 变量字重 "100 900" -> "100-900"，避免文件名空格
        fname = f"{safe}-{wt_safe}{'-italic' if sty == 'italic' else ''}.woff2"
        dest = FONTS_DIR / fname
        names[(fam, sty, wt)] = fname
        if dest.exists() and dest.stat().st_size > 1000:
            print(f"[skip] {fname} 已存在")
            continue
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                data = r.read()
            dest.write_bytes(data)
            print(f"[dl] {fname} {len(data)/1024:.0f}KB")
        except Exception as e:
            print(f"[FAIL] {fname}: {e}")

    # 生成 fonts.css
    css_lines = []
    for f in all_faces:
        key = (f["family"], f["style"], f["weight"])
        fname = names.get(key)
        if not fname:
            continue
        css_lines.append(f"@font-face {{")
        css_lines.append(f"  font-family: '{f['family']}';")
        css_lines.append(f"  font-style: {f['style']};")
        css_lines.append(f"  font-weight: {f['weight']};")
        css_lines.append(f"  font-display: swap;")
        css_lines.append(f"  src: url('{fname}') format('woff2');")
        css_lines.append(f"}}")
    (FONTS_DIR / "fonts.css").write_text("\n".join(css_lines), encoding="utf-8")
    print(f"\n已生成 {FONTS_DIR / 'fonts.css'} ({len(all_faces)} 个 @font-face)")

    # 打印各 deck 需要的文件名映射（供下一步改写引用）
    mapping = {}
    for slug, url in sorted(urls.items()):
        fams = set(re.findall(r"family=([^&:]+)", url))
        mapping[slug] = sorted(fams)
    (FONTS_DIR / "deck-font-map.json").write_text(json.dumps(mapping, indent=2), encoding="utf-8")
    print("已生成 deck-font-map.json")


if __name__ == "__main__":
    asyncio.run(main())
