# Superr — QA 报告

- **成品**: `showcase/superr/index.html`（8 页 deck，1920×1080 舞台）
- **素材**: `refero-styles/Superr/`（DESIGN.md / tokens.json / variables.css / theme.css）
- **风格摘要**: Warm schoolyard notebook in soft afternoon light. A cream page, an orange marker uncapped, and a stack of sticker-laminated name labels waiting to be peeled.
- **生成方式**: 按 skill 15 章 DECK MODE 素材模式（manifest 选型 → DESIGN.md 值层 1:1）
- **签名动作**: The 104px lowercase gelica weight-600 display headline at line-height 1.08 — a tactile object rather than a title, always left-aligned and never center-aligned after the first line；Handwritten Marker Orange captions (gelica 20–24px, weight 400) paired with thin hand-drawn Charcoal SVG arrows pointing at the photographed product object；Photographed leather-bound notebooks as the hero product asset, tilted 5–8° off-axis with a white name-label sticker (Name / Class / Roll no.) on the cover；Flat sticker illustrations (lightning, bear, heart, ghost) with 2px dark outlines placed at random 5–15° rotations — treated as physical peel-and-stick, never grid-aligned；The outlined pill button — cream fill with a 1.5px Charcoal border, no fill state; the identity is the dark border, not the background

## QA 门结果（机器门复验：2026-08-22）

| 门 | 结果 | 证据 |
|---|---|---|
| G1 值层校验 | ✓ | `check-values.py`：deck 用色 ⊆ 素材 palette（含 DESIGN.md 声明例外），零自创 |
| G2 行高 + 安全区 | ✓ | `check-decks.py`：正文行高全部 = 1.5，8 页内容最低点 ≤ y 900 |
| G3 视觉 QA | ✓ | 全量 8 页截图逐页检查通过（2026-08-21 批次，30/30 套全过记录；无重叠/无截断/无颜色违规） |
| G4 结构反趋同 | ✓ | `check-structure.py`：活泼 族 / 信号 note-card, sticker；通用脚手架页 2/5 |

## 备注

- 截图事实源：`showcase/superr/screenshots/slide-0..7.png`（不入库，shot-all-slides.py 可再生；15.6 视觉 QA 用）。
- 本报告机器门结果来自提交前全量复跑（2026-08-22），行高/安全区为 Playwright 实测值。
