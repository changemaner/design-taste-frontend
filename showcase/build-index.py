# -*- coding: utf-8 -*-
"""
build-index.py — 生成选型索引与预览页（P1.3 + P1.4）
====================================================
从 design-manifest.json 程序化生成：
1. selection-index.json  —— 可筛选索引（P1.4）：30 套的选型字段（紧凑，初筛用）
2. gallery/index.html    —— 预览图廊页（P1.3 + P1.5 基础）：每套 1 卡 = 色板 swatch + tagline
                            + 选型标签 + signature moves 摘要；成品截图可回填

用法：
  python showcase/build-index.py            # 生成 selection-index.json + gallery/index.html
  python showcase/build-index.py --check    # 生成 + 校验覆盖率

路径以脚本位置为基准（__file__）。
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "design-manifest.json"
# 展示产物放在 showcase/ 内（8899 服务器 serve 的是 showcase 目录，浏览器可直接打开；
# showcase/ 整体随仓库分发，gallery 与 selection-index 都在这）
SHOWCASE = Path(__file__).resolve().parent
OUT_INDEX = SHOWCASE / "selection-index.json"
GALLERY_DIR = SHOWCASE / "gallery"


def main():
    do_check = "--check" in sys.argv
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    styles = m["styles"]

    # ---- P1.4: selection-index.json（紧凑可筛选）----
    selection = {}
    for slug, e in styles.items():
        sel = e["selection"]
        selection[slug] = {
            "slug": slug,
            "name": e["name"],
            "tagline": e["tagline"],
            "mood": sel["mood"],
            "tone": sel["tone"],
            "formality": sel["formality"],
            "density": sel["density"],
            "scheme": sel["scheme"],
            "best_for": sel["best_for"],
            "avoid_for": sel["avoid_for"],
            "type": e["source"].get("type", "material"),
            "design_md": e["source"].get("path", "").rstrip("/"),
            "preview_available": bool(e["value_layer"].get("palette")),
        }
    OUT_INDEX.write_text(
        json.dumps({"version": "1", "styles": selection}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    print(f"selection-index.json: {len(selection)} 套")

    # ---- P1.3 + P1.5 基础: gallery/index.html（预览图廊）----
    GALLERY_DIR.mkdir(exist_ok=True)
    cards = []
    for slug, e in sorted(styles.items()):
        vl = e["value_layer"]
        palette = vl.get("palette", {})
        # 色板 swatch：取主色 4-6 个
        swatches = "".join(
            f'<span class="sw" style="background:{v}" title="{k}:{v}"></span>'
            for k, v in list(palette.items())[:8])
        signature = e["style_read"]["signature_moves"]
        sig_html = "<br>".join(f"• {s}" for s in signature[:3]) if signature else ""
        # 成品截图回填（存在则用，否则占位）——取自 gallery/<slug>/slide-0.png（P0.3 封面截）
        deck_png = GALLERY_DIR / slug / "slide-0.png"
        img = (f'<img class="shot" src="{slug}/slide-0.png" alt="{e["name"]}">'
               if deck_png.exists() else
               f'<div class="shot placeholder">未生成成品<br>（manifest 合成占位）</div>')
        scheme_badge = {"light": "浅色", "dark": "深色", "mixed": "混合"}.get(e["selection"]["scheme"], e["selection"]["scheme"])
        cards.append(f"""
        <article class="card" data-type="{e['source'].get('type','material')}" data-scheme="{e['selection']['scheme']}" data-density="{e['selection']['density']}">
          <div class="preview">{img}</div>
          <div class="body">
            <h3>{e['name']}</h3>
            <p class="tag">{e['tagline']}</p>
            <div class="swatches">{swatches}</div>
            <div class="tags">
              <span class="chip">{scheme_badge}</span>
              <span class="chip">{e['selection']['density']}</span>
              <span class="chip">{e['selection']['formality']}</span>
            </div>
            <div class="sig">{sig_html}</div>
          </div>
        </article>""")

    html = f"""<!DOCTYPE html>
<html lang="zh"><head><meta charset="utf-8">
<title>设计风格图廊</title>
<style>
  body {{ font-family: system-ui, sans-serif; margin: 0; padding: 32px; background: #f5f5f4; color: #1a1a1a; }}
  h1 {{ font-size: 28px; }} h1 small {{ color: #888; font-weight: normal; }}
  .filters {{ margin: 16px 0 24px; display: flex; gap: 8px; flex-wrap: wrap; }}
  .filters button {{ padding: 6px 12px; border: 1px solid #ccc; background: #fff; border-radius: 20px; cursor: pointer; }}
  .filters button.active {{ background: #1a1a1a; color: #fff; border-color: #1a1a1a; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 20px; }}
  .card {{ background: #fff; border-radius: 12px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,.08); }}
  .preview {{ height: 160px; display: flex; align-items: center; justify-content: center; background: #eee; }}
  .shot {{ width: 100%; height: 100%; object-fit: cover; }}
  .placeholder {{ color: #999; font-size: 13px; text-align: center; }}
  .body {{ padding: 16px; }}
  .body h3 {{ margin: 0 0 6px; font-size: 18px; }}
  .tag {{ margin: 0 0 10px; color: #666; font-size: 13px; }}
  .swatches {{ display: flex; gap: 4px; margin: 0 0 10px; }}
  .sw {{ width: 28px; height: 28px; border-radius: 6px; border: 1px solid rgba(0,0,0,.1); }}
  .tags {{ display: flex; gap: 6px; margin-bottom: 8px; }}
  .chip {{ font-size: 11px; padding: 2px 8px; background: #f0f0ef; border-radius: 10px; }}
  .sig {{ font-size: 12px; color: #555; line-height: 1.6; }}
</style></head><body>
<h1>设计风格图廊 <small>design-taste-frontend · 30 套素材 + 自定义区</small></h1>
<div class="filters">
  <button data-f="all" class="active">全部</button>
  <button data-f="material">品牌素材</button>
  <button data-f="custom">自定义</button>
  <button data-f="light">浅色</button>
  <button data-f="dark">深色</button>
</div>
<div class="grid" id="grid">{''.join(cards)}</div>
<script>
  const btns = document.querySelectorAll('.filters button');
  const cards = document.querySelectorAll('.card');
  btns.forEach(b => b.addEventListener('click', () => {{
    btns.forEach(x => x.classList.remove('active')); b.classList.add('active');
    const f = b.dataset.f;
    cards.forEach(c => {{
      const ok = f === 'all' || c.dataset.type === f || c.dataset.scheme === f;
      c.style.display = ok ? '' : 'none';
    }});
  }}));
</script>
</body></html>"""
    (GALLERY_DIR / "index.html").write_text(html, encoding="utf-8")
    print(f"gallery/index.html: {len(styles)} 张预览卡")

    if do_check:
        complete = sum(1 for e in styles.values() if e["value_layer"].get("palette"))
        print(f"有色板卡: {complete}/{len(styles)}")
        if complete < len(styles):
            sys.exit(1)


if __name__ == "__main__":
    main()
