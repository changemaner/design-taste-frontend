# Lpalo — QA 报告

- **成品**: `showcase/lpalo/index.html`（8 页 deck，1920×1080 舞台）
- **素材**: `refero-styles/Lpalo/`（DESIGN.md / tokens.json / variables.css / theme.css）
- **风格摘要**: A children's storybook spread on warm peach paper — one slab-serif headline shouting through scattered crayon doodles.
- **生成方式**: 按 skill 15 章 DECK MODE 素材模式（manifest 选型 → DESIGN.md 值层 1:1）
- **签名动作**: Chunky single-weight slab-serif headlines (Alfa Slab One, 46–120px) at line-height ≤ 1.20 so type reads as shouting — the brand's heavy lifter；White cards with 2px pure-black borders and 40–47px pill radii — the signature outlined-card language, no shadows；Line-art doodles (headphones, robots, cassettes) scattered at varied rotations around text — asymmetry is part of the storybook feel；Full-bleed flat color bands (60–100px tall) between sections as pure color rhythm；Tilted feature cards (2–4° rotation) with offset behind-layer for a hand-placed scrapbook effect

## QA 门结果（机器门复验：2026-08-22）

| 门 | 结果 | 证据 |
|---|---|---|
| G1 值层校验 | ✓ | `check-values.py`：deck 用色 ⊆ 素材 palette（含 DESIGN.md 声明例外），零自创 |
| G2 行高 + 安全区 | ✓ | `check-decks.py`：正文行高全部 = 1.6，8 页内容最低点 ≤ y 900 |
| G3 视觉 QA | ✓ | 全量 8 页截图逐页检查通过（2026-08-21 批次，30/30 套全过记录；无重叠/无截断/无颜色违规） |
| G4 结构反趋同 | ✓ | `check-structure.py`：活泼 族 / 信号 cc-*, crayon-card, tilt-*；通用脚手架页 2/5 |

## 备注

- 截图事实源：`showcase/lpalo/screenshots/slide-0..7.png`（不入库，shot-all-slides.py 可再生；15.6 视觉 QA 用）。
- 本报告机器门结果来自提交前全量复跑（2026-08-22），行高/安全区为 Playwright 实测值。
