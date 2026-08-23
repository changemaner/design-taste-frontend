# ORYZO AI — QA 报告

- **成品**: `showcase/oryzo-ai/index.html`（8 页 deck，1920×1080 舞台）
- **素材**: `refero-styles/ORYZO AI/`（DESIGN.md / tokens.json / variables.css / theme.css）
- **风格摘要**: Darkroom product editorial. A lone object floating in warm darkness, cream typography the only decoration.
- **生成方式**: 按 skill 15 章 DECK MODE 素材模式（manifest 选型 → DESIGN.md 值层 1:1）
- **签名动作**: Green cutting-mat photographic hero (top-down cork coaster on #445231 with white grid, pencils, craft knife, paperclip) — the brand's in-context moment; sections below switch to warm-dark void mode；Uppercase weight 500 for labels, nav, and display with the sole exception of 29px/400 Literata serif body — the serif mixed-case shift is the signal that you are reading description, not label；Museum-label typography at line-height 0.9 on 41–51px display sizes — uppercase letterforms overlap their bounds and stack as sculptural solid form；The DESIGNED BY LUSION attribution card (semi-transparent dark panel, dashed divider, italic serif tagline) and the vertical 'ORYZO 1-MODEL' edge label — physical-product artifacts translated to UI；Brand Gold (#ffbf02) ORYZO mark on the video thumbnail card and the circular 'SCROLL TO CONTINUE' text badge；1px dashed hairline dividers in Cork Border as the only structural breaks — always carrying meaning, never decoration

## QA 门结果（机器门复验：2026-08-22）

| 门 | 结果 | 证据 |
|---|---|---|
| G1 值层校验 | ✓ | `check-values.py`：deck 用色 ⊆ 素材 palette（含 DESIGN.md 声明例外），零自创 |
| G2 行高 + 安全区 | ✓ | `check-decks.py`：正文行高全部 = 1.26，8 页内容最低点 ≤ y 900 |
| G3 视觉 QA | ✓ | 全量 8 页截图逐页检查通过（2026-08-21 批次，30/30 套全过记录；无重叠/无截断/无颜色违规） |
| G4 结构反趋同 | ✓ | `check-structure.py`：产品 族 / 信号 obj-body, obj-num, obj-panel；通用脚手架页 0/5 |

## 备注

- 截图事实源：`showcase/oryzo-ai/screenshots/slide-0..7.png`（不入库，shot-all-slides.py 可再生；15.6 视觉 QA 用）。
- 本报告机器门结果来自提交前全量复跑（2026-08-22），行高/安全区为 Playwright 实测值。
