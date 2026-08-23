# -*- coding: utf-8 -*-
"""
中段结构趋同检查（QA gate 4）
==============================

这不是截图相似度检查，而是一个可复跑的结构信号检查：

* 中段默认检查 slide 2-6（0-based；排除 cover / intro / closing）。
* 每套风格在 metadata/structure-contracts.json 中声明自己的中段表达族，
  以及至少两个能证明该表达存在的 DOM/CSS class 信号。
* `card` / `quote` / `stat` / `frame` 等通用脚手架不算风格证据。
  只有真正的数据卡/图表、多栏/编辑结构、插画与旁注、产品/UI artifact、
  贴纸/手写标注、编号/规格/工程标注等差异化信号才算通过。
* 若一套 deck 的中段只剩通用卡片 + 引用 + 统计数字，脚本会报为
  “结构趋同”，而不是因为颜色不同就误判为不同风格。

用法：
  python showcase/check-structure.py              # 检查全部 showcase 套
  python showcase/check-structure.py steep        # 检查指定套
  python showcase/check-structure.py --json       # 输出机器可读结果
  python showcase/check-structure.py path/to/your-deck            # 包外用户 deck
  python showcase/check-structure.py path/to/deck --style steep   # 指定契约基准

包外 deck 的契约基准解析：--style <slug> → deck <head> 的
<meta name="design-source"> 标记（15.3 契约）；都无则报错
（结构契约必须对着素材声明，无自洽降级）。静态分析，无需浏览器。

信号支持：
  - 精确 class / id：`data-card`
  - 前缀通配：`chart-*`
  - HTML 显式标记：`data-structure="data"`（可作为未来新 deck 的稳定逃生舱）
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
SHOWCASE = ROOT / "showcase"
METADATA = ROOT / "metadata"
STYLE_MAP_PATH = METADATA / "style-map.json"
CONTRACT_PATH = METADATA / "structure-contracts.json"


class SlideParser(HTMLParser):
    """只收集每个 `.slide` 及其子树的 class/id/data 属性和文本。"""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.slides: list[dict[str, Any]] = []
        self.current: dict[str, Any] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {key: value or "" for key, value in attrs}
        classes = set(attr_map.get("class", "").split())
        if "slide" in classes:
            self.current = {
                "classes": set(),
                "ids": set(),
                "attributes": [],
                "text": [],
                "explicit_structures": set(),
            }
            self.slides.append(self.current)

        if self.current is None:
            return

        self.current["classes"].update(classes)
        if attr_map.get("id"):
            self.current["ids"].add(attr_map["id"])

        for key, value in attrs:
            if not value:
                continue
            self.current["attributes"].append(f"{key}={value}")
            if key in {"data-structure", "data-layout", "data-middle-expression"}:
                self.current["explicit_structures"].update(value.lower().split())

    def handle_data(self, data: str) -> None:
        if self.current is not None and data.strip():
            self.current["text"].append(" ".join(data.split()))


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"[!!] 缺少 {path}")
        raise SystemExit(1)
    except json.JSONDecodeError as exc:
        print(f"[!!] JSON 无法解析 {path}: {exc}")
        raise SystemExit(1)


def matches(pattern: str, token: str) -> bool:
    if pattern.endswith("*"):
        return token.startswith(pattern[:-1])
    return token == pattern


def collect_tokens(slide: dict[str, Any]) -> set[str]:
    tokens = set(slide["classes"]) | set(slide["ids"])
    for attr in slide["attributes"]:
        key, _, value = attr.partition("=")
        if key.startswith("data-"):
            tokens.update(value.lower().split())
    return {token.lower() for token in tokens if token}


def is_generic(token: str, generic_tokens: set[str]) -> bool:
    if token in generic_tokens:
        return True
    if re.match(r"^(?:card|quote|stat|tag|nav|body|wordmark|wm)-", token):
        return True
    if token in {"button", "button-primary", "button-secondary"}:
        return True
    return False


def parse_deck(path: Path) -> list[dict[str, Any]]:
    parser = SlideParser()
    parser.feed(path.read_text(encoding="utf-8", errors="ignore"))
    return parser.slides


def deck_style_marker(deck: Path):
    """读 deck <head> 的来源标记 <meta name="design-source" content="<slug>">（15.3 契约）。"""
    html = (deck / "index.html").read_text(encoding="utf-8")
    m = re.search(r'<meta\s+name="design-source"\s+content="([^"]+)"', html)
    return m.group(1).strip() if m else None


def evaluate_style(
    label: str,
    html: Path,
    contract: dict[str, Any],
    families: dict[str, Any],
    generic_tokens: set[str],
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "slug": label,
        "family": contract.get("family"),
        "allowed": contract.get("allowed", [contract.get("family")]),
        "signals": [],
        "middle_slides": 0,
        "generic_only_slides": 0,
        "distinctive_tokens": [],
        "role_counts": {},
        "status": "ok",
        "issues": [],
    }

    if not html.exists():
        result["status"] = "skip"
        result["issues"].append("缺 index.html")
        return result

    slides = parse_deck(html)
    start = int(contract.get("middle_from", 2))
    end = int(contract.get("middle_to", 6))
    middle = slides[start : end + 1]
    result["middle_slides"] = len(middle)
    if len(middle) < 3:
        result["status"] = "fail"
        result["issues"].append(f"中段 slide 数量不足：{len(middle)}（至少 3 页）")
        return result

    tokens_by_slide = [collect_tokens(slide) for slide in middle]
    all_tokens = set().union(*tokens_by_slide)
    signal_patterns = contract.get("signals", [])
    hits: set[str] = set()
    hit_slides: dict[str, list[int]] = {}
    generic_only = 0

    for offset, tokens in enumerate(tokens_by_slide, start=start):
        style_hits = {
            pattern
            for pattern in signal_patterns
            if any(matches(pattern.lower(), token) for token in tokens)
        }
        for pattern in style_hits:
            hits.add(pattern)
            hit_slides.setdefault(pattern, []).append(offset)

        distinctive = {token for token in tokens if not is_generic(token, generic_tokens)}
        if not distinctive:
            generic_only += 1

    result["signals"] = [
        {"pattern": pattern, "slides": hit_slides.get(pattern, [])}
        for pattern in sorted(hits)
    ]
    result["distinctive_tokens"] = sorted(
        token for token in all_tokens if not is_generic(token, generic_tokens)
    )
    result["generic_only_slides"] = generic_only

    # 这些角色只用于报告“通用模板形状”，不能单独作为风格证据。
    role_patterns = {
        "stats": re.compile(r"^(?:stat-|d[1-4]$)"),
        "quotes": re.compile(r"^quote-"),
        "cards": re.compile(r"^(?:card|tile|panel)(?:-|$)|(?:-card)$"),
        "nav": re.compile(r"^(?:nav|tag)(?:-|$)"),
    }
    role_counts: Counter[str] = Counter()
    for tokens in tokens_by_slide:
        for role, pattern in role_patterns.items():
            if any(pattern.search(token) for token in tokens):
                role_counts[role] += 1
    result["role_counts"] = dict(role_counts)

    min_signals = int(contract.get("min_distinct_signals", 2))
    if len(hits) < min_signals:
        result["status"] = "fail"
        result["issues"].append(
            f"中段只有 {len(hits)} 个风格信号，至少需要 {min_signals} 个；"
            "通用 card/quote/stat 不计入"
        )

    if generic_only == len(middle):
        result["status"] = "fail"
        result["issues"].append(
            "中段所有页面都只有通用脚手架，疑似结构趋同；"
            "请加入该风格的中段表达（数据/多栏/插画旁注/UI artifact/贴纸/工程标注）"
        )
    elif generic_only >= (len(middle) + 1) // 2:
        result["issues"].append(
            f"中段 {generic_only}/{len(middle)} 页没有可识别的风格结构信号；"
            "单页纯引用/留白页可以是节奏变化，只有中段一半以上退化才提醒"
        )
        # 单页缺少信号是 warning，不让一张纯引言/引用页阻断全套。
        if result["status"] == "ok":
            result["status"] = "warn"

    # 显式 data-structure 标记必须属于该套允许的表达族。
    explicit = set().union(*(slide["explicit_structures"] for slide in middle))
    if explicit:
        unknown = explicit - set(families)
        disallowed = explicit - set(contract.get("allowed", []))
        if unknown:
            result["status"] = "fail"
            result["issues"].append(f"未知 data-structure 标记：{sorted(unknown)}")
        if disallowed:
            result["status"] = "fail"
            result["issues"].append(
                f"显式中段表达 {sorted(disallowed)} 不在允许族 {contract.get('allowed', [])} 内"
            )

    return result


def print_human(results: list[dict[str, Any]], families: dict[str, Any]) -> None:
    print("=== 中段结构趋同检查 ===")
    for result in results:
        family = result.get("family") or "未声明"
        label = families.get(family, {}).get("label", family)
        evidence = ", ".join(item["pattern"] for item in result.get("signals", [])) or "无"
        roles = ", ".join(
            f"{key}:{value}" for key, value in result.get("role_counts", {}).items()
        ) or "无"
        status = {"ok": "ok", "warn": "!!", "fail": "!!", "skip": "skip"}.get(
            result["status"], "!!"
        )
        print(
            f"[{status}] {result['slug']}: {label} / "
            f"中段 {result['middle_slides']} 页 / 信号 {evidence} / 通用角色 {roles}"
        )
        print(
            f"  通用脚手架页: {result['generic_only_slides']}/"
            f"{result['middle_slides']}"
        )
        for issue in result.get("issues", []):
            print(f"  - {issue}")

    failed = [result for result in results if result["status"] == "fail"]
    warned = [result for result in results if result["status"] == "warn"]
    distribution = Counter(result.get("family") for result in results if result["status"] != "skip")
    print("\n表达族分布：" + ", ".join(f"{key}={value}" for key, value in sorted(distribution.items())))
    if len(distribution) <= 1 and results:
        print("[!!] 所有风格都落到同一个中段表达族，库级结构趋同风险高")
    elif len(distribution) >= 3:
        print("[ok] 中段表达至少覆盖 3 个结构族，未收敛到单一模板")
    print(
        f"\n=== 结构检查完成：{len(failed)} 处失败，{len(warned)} 处提醒 ==="
    )


def main() -> None:
    # Keep machine-readable output stable across Windows code pages.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="检查中段结构是否趋同（showcase 套或包外 deck）")
    parser.add_argument("slugs", nargs="*", help="showcase slug 或 deck 目录路径；默认全部 showcase 套")
    parser.add_argument("--style", default=None, help="包外 deck 的契约基准素材 slug")
    parser.add_argument("--json", action="store_true", dest="as_json", help="输出 JSON")
    args = parser.parse_args()

    style_map = load_json(STYLE_MAP_PATH)
    contract_data = load_json(CONTRACT_PATH)
    styles = contract_data.get("styles", {})
    families = contract_data.get("families", {})
    middle = contract_data.get("middle_slides", {})
    generic_tokens = set(contract_data.get("generic_tokens", []))

    # 每个 positional 解析为 (deck 目录, 契约 slug, 显示名)：
    # showcase slug → 自身；包外路径 → --style > meta design-source 标记
    targets: list[tuple[Path, str, str]] = []
    for a in args.slugs or sorted(style_map):
        slug_dir = SHOWCASE / a
        if (slug_dir / "index.html").exists():
            targets.append((slug_dir, a, a))
            continue
        p = Path(a)
        if (p / "index.html").exists():
            deck = p.resolve()
            style = args.style or deck_style_marker(deck)
            if not style:
                raise SystemExit(
                    f"[!!] {deck.name}: 结构契约必须对着素材声明。传 --style <slug>，"
                    f'或 deck <head> 加 <meta name="design-source" content="<slug>">（15.3 契约）')
            targets.append((deck, style, deck.name))
            continue
        raise SystemExit(f"[!!] 未知目标：{a}（既不是 showcase slug，也不是含 index.html 的目录）")

    results: list[dict[str, Any]] = []
    for deck, style, label in targets:
        contract = dict(styles.get(style, {}))
        if not contract:
            results.append(
                {
                    "slug": label,
                    "status": "fail",
                    "issues": [f"metadata/structure-contracts.json 缺少契约 slug：{style}"],
                    "family": None,
                }
            )
            continue
        contract.setdefault("middle_from", middle.get("from", 2))
        contract.setdefault("middle_to", middle.get("to", 6))
        results.append(evaluate_style(label, deck / "index.html", contract, families, generic_tokens))

    if args.as_json:
        print(json.dumps({"version": 1, "results": results}, ensure_ascii=False, indent=2))
    else:
        print_human(results, families)

    failures = sum(result["status"] == "fail" for result in results)
    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    main()
