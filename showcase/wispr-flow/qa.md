# Wispr Flow — QA 报告

- **成品**: `showcase/wispr-flow/index.html`（8 页 deck，1920×1080 舞台）
- **素材**: `refero-styles/Wispr Flow/`（DESIGN.md / tokens.json / variables.css / theme.css）
- **风格摘要**: cream broadsheet, dark velvet chambers
- **生成方式**: 按 skill 15 章 DECK MODE 素材模式（manifest 选型 → DESIGN.md 值层 1:1）
- **签名动作**: Cream and dark 'velvet chamber' sections alternating page-wide, each dark chamber bookended by cream, with oversized 40–80px border radii that make sections feel like rounded inset pebbles rather than elevated overlays；EB Garamond weight-400 display serif at 48–120px with 0.85–0.95 line-height — authority through sheer scale and tight leading, never bold; negative tracking (-3.6px at 120px)；The 2px solid Vast Ink border on every interactive element — the thick border is the signature, non-negotiable on the lavender CTA；Lavender Whisper (#f0d7ff) as the sole primary action color, echoed by hand-drawn lavender SVG squiggle underlines beneath 1–2 words in headlines to link emphasis and action；The waveform visualizer pill — cream pill with 2px ink border and 5–7 pulsing vertical bars — doubling as audio indicator and decorative rhythm marker; plus flat phone mockups and curved text arcs as the only graphics

## QA 门结果（机器门复验：2026-08-22）

| 门 | 结果 | 证据 |
|---|---|---|
| G1 值层校验 | ✓ | `check-values.py`：deck 用色 ⊆ 素材 palette（含 DESIGN.md 声明例外），零自创 |
| G2 行高 + 安全区 | ✓ | `check-decks.py`：正文行高全部 = 1.3，8 页内容最低点 ≤ y 900 |
| G3 视觉 QA | ✓ | 全量 8 页截图逐页检查通过（2026-08-21 批次，30/30 套全过记录；无重叠/无截断/无颜色违规） |
| G4 结构反趋同 | ✓ | `check-structure.py`：报纸 族 / 信号 pebble-card, tag-dark；通用脚手架页 1/5 |

## 备注

- 截图事实源：`showcase/wispr-flow/screenshots/slide-0..7.png`（不入库，shot-all-slides.py 可再生；15.6 视觉 QA 用）。
- 本报告机器门结果来自提交前全量复跑（2026-08-22），行高/安全区为 Playwright 实测值。
