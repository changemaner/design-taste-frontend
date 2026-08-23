# Ventriloc — QA 报告

- **成品**: `showcase/ventriloc/index.html`（8 页 deck，1920×1080 舞台）
- **素材**: `refero-styles/Ventriloc/`（DESIGN.md / tokens.json / variables.css / theme.css）
- **风格摘要**: Editorial data observatory on warm paper — a single orange ember punctuating monochrome precision.
- **生成方式**: 按 skill 15 章 DECK MODE 素材模式（manifest 选型 → DESIGN.md 值层 1:1）
- **签名动作**: The asymmetric border-radius 6px 0px 0px on featured cards — a single cut corner that signals editorial layout instead of a standard card grid, paired with 0px-radius buttons and 200px-radius nav pills (a three-radius system: sharp → asymmetric → fully round)；PolySans at weight 400 with -0.02em tracking for every heading, nav item, and button label — whisper-weight editorial authority that no bold headline could replicate；The 66px display headline at line-height 0.91 with -1.32px tracking — a tight, poster-like typographic statement on white canvas；Dark Graphite-filled sharp-cornered CTA button (0px radius) contrasted against the soft rounded card system；Data dashboard cards (line charts, stat rings, revenue widgets) in Ember Orange and Brass strokes floating on warm-gray surfaces — the charts ARE the imagery, no shadows, alternating white/ash bands instead of dividers

## QA 门结果（机器门复验：2026-08-22）

| 门 | 结果 | 证据 |
|---|---|---|
| G1 值层校验 | ✓ | `check-values.py`：deck 用色 ⊆ 素材 palette（含 DESIGN.md 声明例外），零自创 |
| G2 行高 + 安全区 | ✓ | `check-decks.py`：正文行高全部 = 1.5，8 页内容最低点 ≤ y 900 |
| G3 视觉 QA | ✓ | 全量 8 页截图逐页检查通过（2026-08-21 批次，30/30 套全过记录；无重叠/无截断/无颜色违规） |
| G4 结构反趋同 | ✓ | `check-structure.py`：数据 族 / 信号 card-num, data-card, wm-dot；通用脚手架页 2/5 |

## 备注

- 截图事实源：`showcase/ventriloc/screenshots/slide-0..7.png`（不入库，shot-all-slides.py 可再生；15.6 视觉 QA 用）。
- 本报告机器门结果来自提交前全量复跑（2026-08-22），行高/安全区为 Playwright 实测值。
