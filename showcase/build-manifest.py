# -*- coding: utf-8 -*-
"""
build-manifest.py — 生成 design-manifest.json（P1.1）
=====================================================
合并两个来源，为每套风格产出一个 manifest 条目：
1. 程序化提取（值层，来自 tokens.json）：
   - palette: color 分组的 hex 色板
   - fonts: font 分组的字体名
   - radii / spacing / surface（若有对应分组）
2. 子代理标注（审美判断，来自 metadata/<slug>.json）：
   - mood / tone / formality / density / scheme / palette_voice /
     typographic_voice / signature_moves / best_for / avoid_for

用法：
  python showcase/build-manifest.py                 # 生成 design-manifest.json
  python showcase/build-manifest.py --check         # 生成 + 校验覆盖率

路径以脚本位置为基准（__file__），克隆后可直接复跑。
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STYLES = ROOT / "refero-styles"
METADATA = ROOT / "metadata"
OUT = ROOT / "design-manifest.json"

# 值层字段：tokens.json 里的分组名 -> manifest 里的键
VALUE_GROUPS = {
    "color": "palette",
    "font": "fonts",
    "radius": "radii",
    "spacing": "spacing",
    "surface": "surfaces",
    "shadow": "shadows",
}


def extract_tokens(tokens_path: Path):
    """从 tokens.json 提取值层（程序化）。返回 dict 或 None（无法解析）。"""
    try:
        data = json.loads(tokens_path.read_text(encoding="utf-8"))
    except Exception:
        return None
    out = {}
    for group, key in VALUE_GROUPS.items():
        g = data.get(group)
        if not isinstance(g, dict):
            continue
        values = {}
        for name, item in g.items():
            if isinstance(item, dict) and "$value" in item:
                v = item["$value"]
                if isinstance(v, str) and (v.startswith("#") or v.startswith("rgb") or v.startswith("hsl")):
                    values[name] = v  # 颜色值
                else:
                    values[name] = v  # 字体名 / 数值
        if values:
            out[key] = values
    return out


def load_annotation(slug: str):
    """读取 metadata/<slug>.json 的审美字段。"""
    p = METADATA / f"{slug}.json"
    if not p.exists():
        return None
    d = json.loads(p.read_text(encoding="utf-8"))
    # 只取审美判断字段（source 保留，值层由 tokens.json 提供）
    return {
        "mood": d.get("mood", []),
        "tone": d.get("tone", []),
        "formality": d.get("formality"),
        "density": d.get("density"),
        "scheme": d.get("scheme"),
        "palette_voice": d.get("palette_voice"),
        "typographic_voice": d.get("typographic_voice"),
        "signature_moves": d.get("signature_moves", []),
        "best_for": d.get("best_for"),
        "avoid_for": d.get("avoid_for"),
        "source": d.get("source"),
        "name": d.get("name"),
        "tagline": d.get("tagline"),
    }


def main():
    do_check = "--check" in sys.argv
    # 读 style-map.json：slug -> 目录名
    sm_path = METADATA / "style-map.json"
    if not sm_path.exists():
        print(f"[!!] 缺 {sm_path}（slug->目录映射）")
        sys.exit(1)
    style_map = json.loads(sm_path.read_text(encoding="utf-8"))

    manifest = {"version": "1", "styles": {}}
    missing_meta = []
    missing_tokens = []
    no_extract = []

    for slug, dirname in sorted(style_map.items()):
        entry = {"slug": slug, "name": dirname, "value_layer": {}, "style_read": {}, "selection": {}, "source": {}}

        # ① 值层：程序化提取
        tokens_path = STYLES / dirname / "tokens.json"
        if not tokens_path.exists():
            missing_tokens.append(slug)
        else:
            vl = extract_tokens(tokens_path)
            if vl is None:
                no_extract.append(slug)
            else:
                entry["value_layer"] = vl

        # ② 审美标注
        ann = load_annotation(slug)
        if ann is None:
            missing_meta.append(slug)
        else:
            entry["name"] = ann.pop("name") or dirname
            entry["tagline"] = ann.pop("tagline")
            entry["style_read"] = {
                "palette_voice": ann.pop("palette_voice"),
                "typographic_voice": ann.pop("typographic_voice"),
                "signature_moves": ann.pop("signature_moves"),
            }
            entry["selection"] = {
                "mood": ann.pop("mood"),
                "tone": ann.pop("tone"),
                "formality": ann.pop("formality"),
                "density": ann.pop("density"),
                "scheme": ann.pop("scheme"),
                "best_for": ann.pop("best_for"),
                "avoid_for": ann.pop("avoid_for"),
            }
            entry["source"] = ann.pop("source", {}) or {}

        manifest["styles"][slug] = entry

    OUT.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    # 覆盖率报告
    total = len(style_map)
    print(f"已生成 {OUT}，{len(manifest['styles'])}/{total} 套条目")
    if missing_meta:
        print(f"[!!] 缺 metadata: {missing_meta}")
    if missing_tokens:
        print(f"[!!] 缺 tokens.json: {missing_tokens}")
    if no_extract:
        print(f"[!!] tokens 无法提取: {no_extract}")

    # 覆盖率统计
    complete = sum(1 for s in manifest["styles"].values()
                   if s["value_layer"] and s["style_read"]["palette_voice"])
    print(f"完整条目（值层+审美都有）: {complete}/{total}")

    if do_check and (missing_meta or missing_tokens or no_extract or complete < total):
        sys.exit(1)


if __name__ == "__main__":
    main()
