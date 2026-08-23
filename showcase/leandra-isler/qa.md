# Leandra-isler — QA 报告

- **成品**: `showcase/leandra-isler/index.html`（8 页 deck，1920×1080 舞台）
- **素材**: `refero-styles/Leandra-isler/`（DESIGN.md / tokens.json / variables.css / theme.css）
- **风格摘要**: dried botanicals pressed into warm vellum — calm, tactile, editorial, almost reverent.
- **生成方式**: 按 skill 15 章 DECK MODE 素材模式（manifest 选型 → DESIGN.md 值层 1:1）
- **签名动作**: Extreme display scaling — one typeface stretched from 14px captions to 158–173px weight-500 hero headlines; scale itself is the hierarchy；Underlined text links only — 1px underline offset 2–4px below the baseline, never a filled button, never a pill chip；Edge-to-edge vellum canvas with no max-width container; sections separated by 80–120px of space and occasional 1px hairlines, never cards or panels；A single botanical photograph bleeding past the viewport edges — the 'specimen pressed on paper' metaphor；Warm vertical vellum gradient wash on the hero only — the one place light and shadow exist in the system

## QA 门结果（机器门复验：2026-08-22）

| 门 | 结果 | 证据 |
|---|---|---|
| G1 值层校验 | ✓ | `check-values.py`：deck 用色 ⊆ 素材 palette（含 DESIGN.md 声明例外），零自创 |
| G2 行高 + 安全区 | ✓ | `check-decks.py`：正文行高全部 = 1.5，8 页内容最低点 ≤ y 900 |
| G3 视觉 QA | ✓ | 全量 8 页截图逐页检查通过（2026-08-21 批次，30/30 套全过记录；无重叠/无截断/无颜色违规） |
| G4 结构反趋同 | ✓ | `check-structure.py`：插画 族 / 信号 botanical, press-card, proc-*；通用脚手架页 0/5 |

## 备注

- 截图事实源：`showcase/leandra-isler/screenshots/slide-0..7.png`（不入库，shot-all-slides.py 可再生；15.6 视觉 QA 用）。
- 本报告机器门结果来自提交前全量复跑（2026-08-22），行高/安全区为 Playwright 实测值。
