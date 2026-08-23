# -*- coding: utf-8 -*-
"""
deck 全量校验脚本（防"行高被改回去"复发）
==========================================
对 deck 做三个检查（素材模式）：
1. 正文行高对齐：.body 系类（body/body-muted/body-on-color/...）的 computed
   line-height/font-size 比值必须等于行高基准（±0.02）
2. 安全区：slide 内容（非 chrome）最低 y ≤ 900
3. 导航胶囊可见性与对比度

行高基准解析（素材模式）：
  showcase 套（slug）                 → 素材 variables.css 的 --leading-body（权威）
  包外 deck + --style <slug>          → 同上（严格；--style 仅对包外 deck 生效）
  包外 deck + <meta name="design-source" content="<slug>"> → 同上（严格；15.3 契约要求生成 deck 必带）
  包外 deck 只有 :root --leading-body → 自洽降级（基准=deck 自身声明，输出注明）

用法：
  python showcase/check-decks.py                              # 全部 showcase 套
  python showcase/check-decks.py ikea                         # 指定 showcase 套
  python showcase/check-decks.py path/to/your-deck            # 用户自己的 deck（包外目录）
  python showcase/check-decks.py path/to/your-deck --style steep  # 指定素材基准
  python showcase/check-decks.py --freeplay <slug 或 deck 目录>   # 自由发挥模式（P1.7-B，三查）
     声明文件优先读 deck 旁 freeplay-declaration.md，回退包内模板
     ① 自洽：deck 实际用色/字体 ⊆ 自声明 token 集（声明 ②③）
     ② 边界合规：stage / nav pill / v5 motion / CONFIG 块都在（15.2/15.5/15.8）
     ③ 安全区：内容最低 y ≤ 900（15.4，与素材模式同）

deck 经 file:// 直读，无需起本地 HTTP 服务。前置：playwright + 系统 Chrome。
"""
import asyncio
import json
import re
import sys
from pathlib import Path

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent
SHOWCASE = ROOT / "showcase"
STYLES = ROOT / "refero-styles"
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

# 自由发挥模式的声明文件（0.E：brief 无素材匹配时先填它）
# 随 skill 同包分发：优先用包内 ROOT/freeplay-declaration.md（clone 后路径即用）；
# 回退到用户 skills 目录（兼容旧版安装：.agents / .zcode 两个 home）
import os as _os
_PKG_DECL = ROOT / "freeplay-declaration.md"
_SKILL_HOMES = [
    Path(_os.path.expanduser("~")) / ".agents" / "skills" / "design-taste-frontend",
    Path(_os.path.expanduser("~")) / ".zcode" / "skills" / "design-taste-frontend",
]
FREEPLAY_DECL = _PKG_DECL if _PKG_DECL.exists() else next(
    (h / "freeplay-declaration.md" for h in _SKILL_HOMES if (h / "freeplay-declaration.md").exists()), None)

# 8 种俗色（AI-slop 警示）——反趋同检查用
SLOP_COLORS = {
    "#6366f1", "#7c3aed", "#8b5cf6", "#a855f7", "#ec4899",
    "#8ecae6", "#f4a261", "#e9c46a",
}

# slug -> 素材目录名：直接读 metadata/style-map.json（唯一事实源，勿在此双维护）
STYLE_DIR = json.loads((ROOT / "metadata" / "style-map.json").read_text(encoding="utf-8"))

# 已知的底部装饰元素（设计意图占底部，不算内容溢出）
DECOR_CLASSES = ("hero-art", "glow-", "bar-", "marquee", "sky", "glass", "halftone", "confetti", "checker", "zigzag", "vellum-light", "vellum-dark", "split", "half-", "marble")


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


def deck_own_leading_body(deck: Path):
    """读 deck 自身 :root 的 --leading-body（自洽降级基准；无则 None）。"""
    html = (deck / "index.html").read_text(encoding="utf-8")
    m = re.search(r"--leading-body:\s*([\d.]+)", html)
    return float(m.group(1)) if m else None


async def goto_deck(page, deck: Path, slide):
    """file:// 直读 deck 页；确认真的渲染出了 .slide（防拿普通 HTML 来校验）。"""
    url = (deck / "index.html").as_uri()
    await page.goto(f"{url}?slide={slide}", timeout=8000)
    has_slide = await page.evaluate("() => !!document.querySelector('.slide')")
    if not has_slide:
        raise SystemExit(f"[!!] {deck.name}: 页面无 .slide 元素（不是 deck 骨架？）")


def source_leading_body(slug: str):
    """从素材 variables.css 提取 --leading-body 权威值（值层契约）。

    素材例外：部分套（GIC/Good Glyphs 等）未声明该 token，按契约回退 1.5。
    """
    css_path = STYLES / STYLE_DIR[slug] / "variables.css"
    css = css_path.read_text(encoding="utf-8")
    m = re.search(r"--leading-body:\s*([\d.]+)", css)
    if not m:
        return 1.5
    return float(m.group(1))


async def check_deck(deck: Path, label: str, target: float, target_src: str):
    html = deck / "index.html"
    if not html.exists():
        print(f"[skip] {label}: 无 index.html")
        return 0
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, executable_path=find_chrome())
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})
        await goto_deck(page, deck, 0)
        n_slides = await page.evaluate("document.querySelectorAll('.slide').length")
        issues = 0
        for i in range(n_slides):
            await goto_deck(page, deck, i)
            await page.wait_for_timeout(1200)  # 等 reveal 动画（最长 0.4s+0.35s delay）结束
            res = await page.evaluate(
                """([decor]) => {
                    const out = { lh: [], maxBottom: 0, worst: '' };
                    // 1) 正文行高：所有类名含 body 的元素
                    document.querySelectorAll('.slide.active *').forEach(el => {
                        const cls = el.getAttribute('class') || '';
                        if (!/\\bbody/.test(cls)) return;
                        const cs = getComputedStyle(el);
                        const fs = parseFloat(cs.fontSize);
                        const lh = parseFloat(cs.lineHeight);
                        if (fs > 0) out.lh.push({ text: el.textContent.trim().slice(0, 30),
                                                  cls: cls.slice(0, 30),
                                                  ratio: +(lh / fs).toFixed(3) });
                    });
                    // 2) 安全区：非 chrome / frame / slide / 装饰的内容最低 y
                    //    只统计"视觉可见"元素（有背景色 / 有边框 / 有直接文本），跳过透明容器
                    document.querySelectorAll('.slide.active *').forEach(el => {
                        const cls2 = el.getAttribute('class') || '';
                        if (el.closest('.deck-chrome') || el.classList.contains('frame')
                            || el.classList.contains('slide')) return;
                        const cs = getComputedStyle(el);
                        if (cs.position === 'fixed') return;
                        if (decor.some(d => cls2.includes(d))) return;
                        const hasDirectText = Array.from(el.childNodes).some(n => n.nodeType === 3 && n.textContent.trim());
                        const bg = cs.backgroundColor;
                        const hasBg = bg !== 'rgba(0, 0, 0, 0)' && bg !== 'transparent';
                        const hasBorder = parseFloat(cs.borderTopWidth) > 0;
                        if (!hasDirectText && !hasBg && !hasBorder) return;
                        const r = el.getBoundingClientRect();
                        if (r.height === 0 || r.width === 0) return;
                        if (r.bottom > out.maxBottom) {
                            out.maxBottom = r.bottom;
                            out.worst = el.tagName + '.' + cls2.slice(0, 25);
                        }
                    });
                    // 3) 导航胶囊可见性（2026-08-21）：背景非透明 + 实线描边
                    //    防 color-mix 混合比例写成无单位数字 → 整条声明失效 → 胶囊全透明
                    const alphaOf = (s) => {
                        if (!s) return 0;
                        if (s.startsWith('rgba(')) {         // rgba(0, 0, 0, 0.08)
                            const i = s.lastIndexOf(',');
                            return parseFloat(s.slice(i + 1, -1)) || 0;
                        }
                        const i = s.indexOf(' / ');           // color(srgb r g b / 0.08)
                        if (i >= 0) return parseFloat(s.slice(i + 3, -1)) || 0;
                        if (s === 'transparent' || s.startsWith('rgba(0, 0, 0, 0)')) return 0;
                        return 1;                             // rgb(...) 实色 = 1
                    };
                    const nav = document.querySelector('.deck-chrome .dot-nav') || document.querySelector('.dot-nav');
                    if (nav) {
                        const ncs = getComputedStyle(nav);
                        const lumOf = (s) => {
                            if (!s) return null;
                            let t = null;
                            if (s.startsWith('rgba(') || s.startsWith('rgb(')) {
                                const inner = s.slice(s.indexOf('(') + 1, s.lastIndexOf(')'));
                                const p = inner.split(',');
                                if (p.length >= 3) t = [parseFloat(p[0]), parseFloat(p[1]), parseFloat(p[2])];
                            } else if (s.startsWith('color(srgb')) {
                                const inner = s.slice(s.indexOf('(') + 1, s.lastIndexOf(')'));
                                const q = inner.split(' / ')[0].trim().split(' ');
                                if (q.length >= 4) t = [parseFloat(q[1]), parseFloat(q[2]), parseFloat(q[3])];
                            }
                            if (t === null) return null;
                            return 0.2126 * t[0] + 0.7152 * t[1] + 0.0722 * t[2];
                        };
                        // 胶囊背后的实际底色：elementFromPoint 取胶囊中心正后方元素，向上找非透明背景；
                        // 途中若出现 background-image（照片/渐变层）则无法用 CSS 计算对比度 → 跳过断言（交给像素验证）
                        const r = nav.getBoundingClientRect();
                        const navPE = nav.style.pointerEvents;
                        nav.style.pointerEvents = 'none';
                        let behind = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
                        nav.style.pointerEvents = navPE;
                        let bgLum = null, sawImage = false;
                        while (behind && bgLum === null) {
                            const bc = getComputedStyle(behind);
                            if (bc.backgroundImage && bc.backgroundImage !== 'none') { sawImage = true; break; }
                            if (bc.backgroundColor !== 'transparent' && bc.backgroundColor !== 'rgba(0, 0, 0, 0)') bgLum = lumOf(bc.backgroundColor);
                            behind = behind.parentElement;
                        }
                        const navLum = lumOf(ncs.color);
                        out.pill = { alpha: alphaOf(ncs.backgroundColor),
                                     borderW: parseFloat(ncs.borderTopWidth) || 0,
                                     contrast: (navLum !== null && bgLum !== null && !sawImage)
                                               ? Math.abs(navLum - bgLum) : null,
                                     bg: ncs.backgroundColor, style: ncs.borderTopStyle };
                    } else {
                        out.pill = { alpha: 0, borderW: 0, contrast: null, bg: '', style: 'none' };
                    }
                    return out;
                }""",
                [DECOR_CLASSES],
            )
            for it in res["lh"]:
                if abs(it["ratio"] - target) > 0.02:
                    issues += 1
                    print(f"  !! {label} slide{i} 行高 {it['ratio']} ≠ 基准 {target}（{target_src}）| {it['cls']} | {it['text']}")
            if res["maxBottom"] > 902:  # 2px 容差：行高小数产生的亚像素边界
                issues += 1
                print(f"  !! {label} slide{i} 内容最低 y={round(res['maxBottom'])} > 900 ({res['worst']})")
            pill = res.get("pill", {})
            if pill.get("alpha", 0) <= 0.01 or pill.get("borderW", 0) < 1:
                issues += 1
                print(f"  !! {label} slide{i} 导航胶囊不可见 bg={pill.get('bg')} "
                      f"borderW={pill.get('borderW')} style={pill.get('style')} "
                      f"（color-mix 比例必须是百分比，见 SKILL.md 15.2 CAPSULE RENDERING HARD RULE）")
            ctr = pill.get("contrast")
            if ctr is not None and ctr < 25:
                issues += 1
                print(f"  !! {label} slide{i} 导航胶囊与底色对比度不足 {round(ctr)} < 25 "
                      f"（暗色/饱和 slide 需 data-nav-tone=\"dark\" 亮色胶囊）")
        await browser.close()
        if issues == 0:
            print(f"[ok] {label}: 行高全部 = {target}（基准：{target_src}），{n_slides} 页安全区通过")
        return issues


async def check_freeplay(deck: Path):
    """自由发挥模式三查（P1.7-B）：
    ① 自洽：deck 实际用色/字体 ⊆ 声明 token 集（freeplay-declaration.md ②③）
    ② 边界合规：stage / nav pill / v5 motion / CONFIG 块都在
    ③ 安全区：内容最低 y ≤ 900
    """
    label = deck.name
    html = deck / "index.html"
    if not html.exists():
        print(f"[skip] {label}: 无 index.html")
        return 0

    # 找声明文件：deck 旁 freeplay-declaration.md 优先（包外 deck 自包含），
    # 回退包内模板 / 旧版 skills home
    decl_path = deck / "freeplay-declaration.md"
    if decl_path.exists():
        decl = decl_path.read_text(encoding="utf-8")
        decl_src = str(decl_path)
    elif FREEPLAY_DECL and FREEPLAY_DECL.exists():
        decl = FREEPLAY_DECL.read_text(encoding="utf-8")
        decl_src = str(FREEPLAY_DECL)
    else:
        print(f"[!!] {label}: 找不到 freeplay-declaration.md（deck 旁或包内均可，声明文件是自洽校验锚点）")
        return 1

    # 从声明文件提取自声明 token 集
    declared_colors = set(re.findall(r"#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b", decl))
    declared_fonts = set(re.findall(r"font-family:\s*'([^']+)'", decl)) | \
                     set(re.findall(r"'\s*([^']+)\s*'", decl))
    # 归一化小写，去掉常见非字体命中
    declared_colors = {c.lower() for c in declared_colors}
    declared_fonts = {f.lower() for f in declared_fonts if re.match(r"^[a-z][a-z -]{1,}$", f.lower())}

    # §⑦ 反趋同差异化声明强制：必须已填（占位符 ______ 视为未填 → 重设计）
    diff_placeholder = "**______**" in decl or "______" in decl
    if diff_placeholder:
        print(f"[!!] {label}: 声明 §⑦ 反趋同差异化声明未填（仍是占位符 ______，声明来源 {decl_src}）→ 需写明与库内 30 套的差异点，写不出则重设计")
        return 1

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, executable_path=find_chrome())
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})
        await goto_deck(page, deck, 0)
        n_slides = await page.evaluate("document.querySelectorAll('.slide').length")
        issues = 0
        for i in range(n_slides):
            await goto_deck(page, deck, i)
            await page.wait_for_timeout(1200)
            res = await page.evaluate(
                r"""([decor]) => {
                    const out = { colors: new Set(), fonts: new Set(), maxBottom: 0, worst: '',
                                  hasStage: false, hasPill: false, hasMotion: false, hasConfig: false };
                    const doc = document;
                    out.hasStage = !!doc.querySelector('.slide, #deckStage, [class*="stage"]');
                    out.hasPill = !!doc.querySelector('.nav-dot, #dotNav, [class*="nav"]');
                    out.hasMotion = !!doc.querySelector('.reveal, [class*="visible"]');
                    // CONFIG 块：:root 内 --motion-* 或 --nav-*
                    const rootStyle = doc.querySelector('style') ? doc.querySelector('style').textContent : '';
                    out.hasConfig = /--motion-/.test(rootStyle) || /--nav-/.test(rootStyle);
                    // 收集实际用色/字体
                    const rgbToHex = (s) => {
                        const m = s.match(/rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)/);
                        if (!m) return null;
                        const to2 = (n) => Math.round(Number(n)).toString(16).padStart(2, '0');
                        return '#' + to2(m[1]) + to2(m[2]) + to2(m[3]);
                    };
                    doc.querySelectorAll('.slide.active *').forEach(el => {
                        const cs = getComputedStyle(el);
                        ['color', 'backgroundColor', 'borderTopColor'].forEach(prop => {
                            const v = cs[prop];
                            if (!v) return;
                            let hex = v.match(/#[0-9a-fA-F]{3,6}/);
                            if (hex) out.colors.add(hex[0].length === 4 ? '#' + hex[0].slice(1).split('').map(c => c + c).join('') : hex[0].toLowerCase());
                            else {
                                const h = rgbToHex(v);
                                if (h) out.colors.add(h);
                            }
                        });
                        const ff = cs.fontFamily;
                        if (ff) {
                            ff.split(',').forEach(f => {
                                const t = f.trim().replace(/^['"]|['"]$/g, '').toLowerCase();
                                if (t && !['sans-serif', 'serif', 'monospace', 'cursive', 'fantasy', 'system-ui', 'ui-sans-serif', 'ui-serif', 'ui-monospace', 'ui-rounded', 'arial', 'helvetica', 'helvetica neue', 'times new roman', 'georgia', 'courier new', 'trebuchet ms', 'verdana', 'geneva', 'tahoma', 'lucida grande'].includes(t)) {
                                    out.fonts.add(t);
                                }
                            });
                        }
                    });
                    // 安全区（与 check_deck 同逻辑）
                    doc.querySelectorAll('.slide.active *').forEach(el => {
                        const cls2 = el.getAttribute('class') || '';
                        if (el.closest('.deck-chrome') || el.classList.contains('frame')
                            || el.classList.contains('slide')) return;
                        const cs = getComputedStyle(el);
                        if (cs.position === 'fixed') return;
                        if (decor.some(d => cls2.includes(d))) return;
                        const hasDirectText = Array.from(el.childNodes).some(n => n.nodeType === 3 && n.textContent.trim());
                        const bg = cs.backgroundColor;
                        const hasBg = bg !== 'rgba(0, 0, 0, 0)' && bg !== 'transparent';
                        const hasBorder = parseFloat(cs.borderTopWidth) > 0;
                        if (!hasDirectText && !hasBg && !hasBorder) return;
                        const r = el.getBoundingClientRect();
                        if (r.height === 0 || r.width === 0) return;
                        if (r.bottom > out.maxBottom) {
                            out.maxBottom = r.bottom;
                            out.worst = el.tagName + '.' + cls2.slice(0, 25);
                        }
                    });
                    return {
                        colors: Array.from(out.colors), fonts: Array.from(out.fonts),
                        maxBottom: out.maxBottom, worst: out.worst,
                        hasStage: out.hasStage, hasPill: out.hasPill,
                        hasMotion: out.hasMotion, hasConfig: out.hasConfig
                    };
                }""",
                [DECOR_CLASSES],
            )
            # ① 自洽
            undeclared_colors = [c for c in res["colors"] if c not in declared_colors]
            undeclared_fonts = [f for f in res["fonts"] if f not in declared_fonts]
            if undeclared_colors:
                issues += 1
                print(f"  !! {label} slide{i} 用了未声明的色 {undeclared_colors}（不在声明 ② palette 内）")
            if undeclared_fonts:
                issues += 1
                print(f"  !! {label} slide{i} 用了未声明的字体 {undeclared_fonts}（不在声明 ③ typographic 内）")
            # ② 边界合规
            for name, ok in [("stage 缩放", res["hasStage"]), ("nav pill", res["hasPill"]),
                             ("v5 motion", res["hasMotion"]), ("CONFIG 块", res["hasConfig"])]:
                if not ok:
                    issues += 1
                    print(f"  !! {label} slide{i} 缺 {name}")
            # ③ 安全区
            if res["maxBottom"] > 902:
                issues += 1
                print(f"  !! {label} slide{i} 内容最低 y={round(res['maxBottom'])} > 900 ({res['worst']})")
        await browser.close()
        if issues == 0:
            print(f"[ok] {label} 自由发挥三查通过：自洽 / 边界 / 安全区（声明来源 {decl_src}）")
        return issues


async def check_external(deck: Path, style_flag):
    """包外用户 deck 的素材模式校验：解析行高基准后走 check_deck。"""
    slug = style_flag or deck_style_marker(deck)
    if slug:
        if slug not in STYLE_DIR:
            raise SystemExit(f"[!!] 未知素材 slug：{slug}（--style 或 meta design-source 须为 30 套之一）")
        target, src = source_leading_body(slug), f"素材 variables.css（{slug}）"
    else:
        own = deck_own_leading_body(deck)
        if own is None:
            raise SystemExit(
                f"[!!] {deck.name}: 无法确定行高基准。三条路任选：\n"
                f"    1. 传 --style <slug> 指定素材基准（严格）\n"
                f"    2. deck <head> 加 <meta name=\"design-source\" content=\"<slug>\">（严格，15.3 契约）\n"
                f"    3. deck :root 写 --leading-body（自洽降级）\n"
                f"    自由发挥 deck 则加 --freeplay")
        target, src = own, "deck 自身 :root 声明（自洽降级）"
    return await check_deck(deck, deck.name, target, src)


async def main():
    argv = sys.argv[1:]
    style_flag = None
    if "--style" in argv:
        i = argv.index("--style")
        if i + 1 >= len(argv):
            raise SystemExit("[usage] --style 后面要跟素材 slug")
        style_flag = argv[i + 1]
        if style_flag not in STYLE_DIR:
            raise SystemExit(f"[!!] 未知 --style：{style_flag}（须为 30 套素材 slug 之一）")
        argv = argv[:i] + argv[i + 2:]  # flag 与其值一并剔除，勿当 deck 参数
    freeplay = "--freeplay" in argv
    args = [a for a in argv if not a.startswith("--")]
    if freeplay:
        if not args:
            print("[usage] python showcase/check-decks.py --freeplay <slug 或 deck 目录>")
            sys.exit(2)
        total = 0
        for a in args:
            total += await check_freeplay(resolve_deck(a))
        sys.exit(1 if total else 0)
    if not args:
        # 全部 showcase 套（保持原行为：基准=素材 variables.css）
        total = 0
        for slug in STYLE_DIR:
            total += await check_deck(SHOWCASE / slug, slug, source_leading_body(slug), "素材 variables.css")
    else:
        total = 0
        for a in args:
            deck = resolve_deck(a)
            if deck.parent == SHOWCASE and deck.name in STYLE_DIR:
                total += await check_deck(deck, deck.name, source_leading_body(deck.name), "素材 variables.css")
            else:
                total += await check_external(deck, style_flag)
    print("\n=== 校验完成 ===" if total == 0 else f"\n=== {total} 处违规 ===")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    asyncio.run(main())
