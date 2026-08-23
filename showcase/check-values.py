# -*- coding: utf-8 -*-
"""
值层校验（gate1）— deck 用色 ⊆ 素材 palette
==========================================
静态扫描 deck HTML 的全部 hex 颜色，与素材 palette（design-manifest.json 的
value_layer，源自 tokens.json）对比。无需浏览器。

素材声明的例外（DESIGN.md 明确允许，非 palette token）：
  - good-glyphs: #ffffff — "white-on-black glyph artwork inside the dark
    showcase band" 是素材唯一的对比 moment（tokens 只有 mint/ink/carbon）。

用法：
  python showcase/check-values.py                              # 全部 showcase 套
  python showcase/check-values.py ikea                         # 指定 showcase 套
  python showcase/check-values.py path/to/your-deck            # 包外用户 deck
  python showcase/check-values.py path/to/your-deck --style steep  # 指定素材基准

包外 deck 的素材基准解析：--style <slug> → deck <head> 的
<meta name="design-source" content="<slug>"> 标记（15.3 契约）。两者都无则报错：
值层校验必须对着素材 palette，没有自洽降级（自洽检查在自由发挥模式的
check-decks.py --freeplay 里）。
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHOWCASE = ROOT / "showcase"

manifest = json.loads((ROOT / "design-manifest.json").read_text(encoding="utf-8"))["styles"]

# 素材 DESIGN.md 声明的 palette 外颜色（附声明出处）
DECLARED_EXCEPTIONS = {
    "good-glyphs": {"#ffffff"},  # DESIGN.md: white-on-black showcase band
}


def resolve_deck(arg: str) -> Path:
    """slug → showcase/<slug>/；否则当作 deck 目录路径（用户自己生成的 HTML）。"""
    slug_dir = SHOWCASE / arg
    if (slug_dir / "index.html").exists():
        return slug_dir
    p = Path(arg)
    if (p / "index.html").exists():
        return p.resolve()
    raise SystemExit(f"[!!] 找不到 deck：{arg}（既不是 showcase/<slug>，也不是含 index.html 的目录）")


def deck_style_marker(deck: Path):
    """读 deck <head> 的来源标记 <meta name="design-source" content="<slug>">（15.3 契约）。"""
    html = (deck / "index.html").read_text(encoding="utf-8")
    m = re.search(r'<meta\s+name="design-source"\s+content="([^"]+)"', html)
    return m.group(1).strip() if m else None


def outside_colors(html_path: Path, slug: str):
    """返回越界色列表（空列表 = 通过）。"""
    html = html_path.read_text(encoding="utf-8")
    palette = set(v.lower() for v in manifest[slug]["value_layer"]["palette"].values())
    allowed = palette | DECLARED_EXCEPTIONS.get(slug, set())
    hexes = {h.lower() for h in re.findall(r"#(?:[0-9a-fA-F]{6})\b", html)}
    return sorted(hexes - allowed)


def main():
    argv = sys.argv[1:]
    style_flag = None
    if "--style" in argv:
        i = argv.index("--style")
        if i + 1 >= len(argv):
            raise SystemExit("[usage] --style 后面要跟素材 slug")
        style_flag = argv[i + 1]
        if style_flag not in manifest:
            raise SystemExit(f"[!!] 未知 --style：{style_flag}（须为 30 套素材 slug 之一）")
        argv = argv[:i] + argv[i + 2:]  # flag 与其值一并剔除，勿当 deck 参数

    issues = []
    if not argv:
        # 全部 showcase 套（保持原行为）
        for slug in manifest:
            outside = outside_colors(SHOWCASE / slug / "index.html", slug)
            if outside:
                issues.append((slug, outside))
        if issues:
            for slug, colors in issues:
                print(f"[!!] {slug}: 用色越界 {colors}")
            raise SystemExit(f"gate1 失败：{len(issues)} 套越界")
        print(f"[ok] gate1：{len(manifest)}/{len(manifest)} 套 deck 用色 ⊆ 素材 palette（含声明例外）")
        return

    for a in argv:
        deck = resolve_deck(a)
        if deck.parent == SHOWCASE and deck.name in manifest:
            slug = deck.name  # showcase 套：基准 = 自身 slug
        else:
            slug = style_flag or deck_style_marker(deck)
            if not slug:
                raise SystemExit(
                    f"[!!] {deck.name}: 值层校验必须对着素材 palette。传 --style <slug>，"
                    f'或 deck <head> 加 <meta name="design-source" content="<slug>">（15.3 契约）')
            if slug not in manifest:
                raise SystemExit(f"[!!] 未知素材 slug：{slug}（须为 30 套之一）")
        outside = outside_colors(deck / "index.html", slug)
        if outside:
            issues.append((deck.name, outside))

    if issues:
        for label, colors in issues:
            print(f"[!!] {label}: 用色越界 {colors}")
        raise SystemExit(f"gate1 失败：{len(issues)} 个 deck 越界")
    print(f"[ok] gate1：{len(argv)} 个 deck 用色 ⊆ 素材 palette（含声明例外）")


if __name__ == "__main__":
    main()
