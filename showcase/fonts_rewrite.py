# -*- coding: utf-8 -*-
"""
改写 30 套 deck：Google Fonts 外链 → 本地共享字体库引用
====================================================
把每套 deck 的
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?...">
替换为
  <link rel="stylesheet" href="../fonts/fonts.css">

前提：已运行 fonts_download.py 生成 showcase/fonts/fonts.css 与字体文件。
用法：python showcase/fonts_rewrite.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHOWCASE = ROOT / "showcase"
FONTS_CSS = SHOWCASE / "fonts" / "fonts.css"

LINK_RE = re.compile(
    r'<link\s+rel="stylesheet"\s+href="https://fonts\.googleapis\.com/[^"]*"\s*>'
)

if not FONTS_CSS.exists():
    raise SystemExit("fonts/fonts.css 不存在，请先运行 fonts_download.py")

changed, skipped = [], []
for d in sorted(SHOWCASE.iterdir()):
    if not d.is_dir():
        continue
    idx = d / "index.html"
    if not idx.exists():
        continue
    html = idx.read_text(encoding="utf-8")
    if "fonts.googleapis.com" not in html:
        skipped.append(d.name)
        continue
    new_html, n = LINK_RE.subn(
        '<link rel="stylesheet" href="../fonts/fonts.css">', html
    )
    if n == 0:
        skipped.append(f"{d.name}(未匹配)")
        continue
    idx.write_text(new_html, encoding="utf-8")
    changed.append(f"{d.name}(替换{n}处)")

print(f"已改写 {len(changed)} 套:")
for c in changed:
    print(f"  {c}")
if skipped:
    print(f"跳过 {len(skipped)} 套（无外链或未匹配）:")
    for s in skipped:
        print(f"  {s}")
