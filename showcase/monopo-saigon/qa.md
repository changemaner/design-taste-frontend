# Monopo Saigon — QA 报告

- **成品**: `showcase/monopo-saigon/index.html`（8 页 deck，1920×1080 舞台）
- **素材**: `refero-styles/monopo saigon/`（DESIGN.md / tokens.json / variables.css / theme.css）
- **风格摘要**: Liquid iridescence behind editorial silence — a monochrome editorial gallery floating on molten light.
- **生成方式**: 按 skill 15 章 DECK MODE 素材模式（manifest 选型 → DESIGN.md 值层 1:1）
- **签名动作**: Monumental Roobert headlines at 225px weight 400 owning the full viewport — no subheads, no CTAs crowding the hero；The 75px full-pill radius on buttons and tags against 0px corners everywhere else — sharp editorial contrast with no intermediate rounding；Whisper-weight section headlines (78px weight 300) and 94px/0.76 line-height statement blocks — type as art object, lines nearly touching；One iridescent molten-gradient hero backdrop per page — the only chromatic moment, existing only behind text；Patient gliding motion — cubic-bezier(0.19,1,0.22,1) easing with 0.8–1.25s transform durations, plus a rotating circular 'SCROLL DOWN' badge

## QA 门结果（机器门复验：2026-08-22）

| 门 | 结果 | 证据 |
|---|---|---|
| G1 值层校验 | ✓ | `check-values.py`：deck 用色 ⊆ 素材 palette（含 DESIGN.md 声明例外），零自创 |
| G2 行高 + 安全区 | ✓ | `check-decks.py`：正文行高全部 = 1.21，8 页内容最低点 ≤ y 900 |
| G3 视觉 QA | ✓ | 全量 8 页截图逐页检查通过（2026-08-21 批次，30/30 套全过记录；无重叠/无截断/无颜色违规） |
| G4 结构反趋同 | ✓ | `check-structure.py`：插画 族 / 信号 g-note, gallery-row, molten；通用脚手架页 0/5 |

## 备注

- 截图事实源：`showcase/monopo-saigon/screenshots/slide-0..7.png`（不入库，shot-all-slides.py 可再生；15.6 视觉 QA 用）。
- 本报告机器门结果来自提交前全量复跑（2026-08-22），行高/安全区为 Playwright 实测值。
