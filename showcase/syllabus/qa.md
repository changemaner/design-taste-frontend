# Syllabus — QA 报告

- **成品**: `showcase/syllabus/index.html`（8 页 deck，1920×1080 舞台）
- **素材**: `refero-styles/Syllabus/`（DESIGN.md / tokens.json / variables.css / theme.css）
- **风格摘要**: cream-paper magazine meets geometric sans-serif. Warm off-white surfaces, near-black violet ink, and one buttery yellow accent that functions as the page's only raised voice — like a sticky note pressed onto fine stationery.
- **生成方式**: 按 skill 15 章 DECK MODE 素材模式（manifest 选型 → DESIGN.md 值层 1:1）
- **签名动作**: The Butter Yellow CTA with a hard-offset black shadow (1px 1px 3px #000000) and 1px Ink Violet border — every action becomes a physical, pressable sticker against the cream；Sharp 0px corners everywhere — buttons, cards, tags, and inputs are all square; the only shadow in the system is the hard yellow-button offset；The strict Roobert 700/400 weight pair at wide size jumps (16→20→24→40→48→56→64px) — hierarchy comes from scale jumps, never interpolated sizes or tracking；1px Ink Violet borders outline cream/white cards and illustration containers like a print frame — the primary structural device；Flat line-art illustrations with selective yellow/teal fills that break past container edges in an 'isometric explosion' pattern — schematic wireframes, never photography

## QA 门结果（机器门复验：2026-08-22）

| 门 | 结果 | 证据 |
|---|---|---|
| G1 值层校验 | ✓ | `check-values.py`：deck 用色 ⊆ 素材 palette（含 DESIGN.md 声明例外），零自创 |
| G2 行高 + 安全区 | ✓ | `check-decks.py`：正文行高全部 = 1.6，8 页内容最低点 ≤ y 900 |
| G3 视觉 QA | ✓ | 全量 8 页截图逐页检查通过（2026-08-21 批次，30/30 套全过记录；无重叠/无截断/无颜色违规） |
| G4 结构反趋同 | ✓ | `check-structure.py`：报纸 族 / 信号 block-*, wm-issue；通用脚手架页 1/5 |

## 备注

- 截图事实源：`showcase/syllabus/screenshots/slide-0..7.png`（不入库，shot-all-slides.py 可再生；15.6 视觉 QA 用）。
- 本报告机器门结果来自提交前全量复跑（2026-08-22），行高/安全区为 Playwright 实测值。
