# Seline Analytics — QA 报告

- **成品**: `showcase/seline-analytics/index.html`（8 页 deck，1920×1080 舞台）
- **素材**: `refero-styles/Seline Analytics/`（DESIGN.md / tokens.json / variables.css / theme.css）
- **风格摘要**: Quiet analyst's desk on warm paper
- **生成方式**: 按 skill 15 章 DECK MODE 素材模式（manifest 选型 → DESIGN.md 值层 1:1）
- **签名动作**: The weight-400 headline whisper: Roobert at 52px/400 with tight negative tracking (-0.021em) — authority through restraint, never bumping to 600/700；Exactly one cyan highlight span per headline (#3398e1 text on a #c1e1f7 pill wash) marking the value-prop keyword — the brand's voice marker；The cyan filled pill CTA (#3ba6f1, 9999px radius) as the only chromatic filled element on any screen, used once per viewport maximum；Flat white content cards defined by 1px stone borders, not shadows — the border IS the structure; only the hero dashboard preview earns a deep floating shadow；The hooded line-art mascot sticker with drop-shadow, used once per section as a playful counterweight to the monochrome data UI

## QA 门结果（机器门复验：2026-08-22）

| 门 | 结果 | 证据 |
|---|---|---|
| G1 值层校验 | ✓ | `check-values.py`：deck 用色 ⊆ 素材 palette（含 DESIGN.md 声明例外），零自创 |
| G2 行高 + 安全区 | ✓ | `check-decks.py`：正文行高全部 = 1.5，8 页内容最低点 ≤ y 900 |
| G3 视觉 QA | ✓ | 全量 8 页截图逐页检查通过（2026-08-21 批次，30/30 套全过记录；无重叠/无截断/无颜色违规） |
| G4 结构反趋同 | ✓ | `check-structure.py`：数据 族 / 信号 desk-card, mascot；通用脚手架页 2/5 |

## 备注

- 截图事实源：`showcase/seline-analytics/screenshots/slide-0..7.png`（不入库，shot-all-slides.py 可再生；15.6 视觉 QA 用）。
- 本报告机器门结果来自提交前全量复跑（2026-08-22），行高/安全区为 Playwright 实测值。
