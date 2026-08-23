# Henry — QA 报告

- **成品**: `showcase/henry/index.html`（8 页 deck，1920×1080 舞台）
- **素材**: `refero-styles/Henry/`（DESIGN.md / tokens.json / variables.css / theme.css）
- **风格摘要**: Gothic broadside poster on warm cream paper. One hundred percent monochrome, no chromatic accent, all visual intensity carried by display type and full-bleed paper-to-ink inversions.
- **生成方式**: 按 skill 15 章 DECK MODE 素材模式（manifest 选型 → DESIGN.md 值层 1:1）
- **签名动作**: Full-bleed Paper/Ink section inversion — cream type on Ink bands and ink type on Paper, flipped like a broadsheet, never gradient-blended；Manuka section mastheads at 226-371px, weight 400, line-height 0.75, uppercase, edge-to-edge — condensed type as the entire section identity；Louize Display headline at 116-132px with an intersecting half-size italic phrase set inside the same baseline (e.g. 'of the' at 35px within 132px type)；Square-cornered monochrome halftone plate as a typographic counterweight to the display headline — no radius, no caption, no color；Brand ticker strip — repeated Louize Display wordmarks on a dark Ink band with 'COMING SOON' ghost tags (12px radius, 1px outline)

## QA 门结果（机器门复验：2026-08-22）

| 门 | 结果 | 证据 |
|---|---|---|
| G1 值层校验 | ✓ | `check-values.py`：deck 用色 ⊆ 素材 palette（含 DESIGN.md 声明例外），零自创 |
| G2 行高 + 安全区 | ✓ | `check-decks.py`：正文行高全部 = 1.5，8 页内容最低点 ≤ y 900 |
| G3 视觉 QA | ✓ | 全量 8 页截图逐页检查通过（2026-08-21 批次，30/30 套全过记录；无重叠/无截断/无颜色违规） |
| G4 结构反趋同 | ✓ | `check-structure.py`：报纸 族 / 信号 h-display, ink-card, paper-card；通用脚手架页 2/5 |

## 备注

- 截图事实源：`showcase/henry/screenshots/slide-0..7.png`（不入库，shot-all-slides.py 可再生；15.6 视觉 QA 用）。
- 本报告机器门结果来自提交前全量复跑（2026-08-22），行高/安全区为 Playwright 实测值。
