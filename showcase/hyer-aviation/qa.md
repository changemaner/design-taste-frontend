# Hyer Aviation — QA 报告

- **成品**: `showcase/hyer-aviation/index.html`（8 页 deck，1920×1080 舞台）
- **素材**: `refero-styles/Hyer Aviation/`（DESIGN.md / tokens.json / variables.css / theme.css）
- **风格摘要**: Cockpit twilight over parchment. A pale dawn-sky meets a slab-serif logo the size of a fuselage, with one warm clay accent breaking the monochrome restraint.
- **生成方式**: 按 skill 15 章 DECK MODE 素材模式（manifest 选型 → DESIGN.md 值层 1:1）
- **签名动作**: 187px weight 700 display headline with -3.74px tracking — type set at near-architectural scale so headlines read as physical objects；Every button and nav item is a full 1000px pill while the featured clay card stays hard-edged 0px — the soft/hard tension defines the system；One Clay Ember (#bc7155) featured card per page — the single warm note in an austere monochrome field, single-use per viewport；Hero headlines end with a period ('Beyond Travel.') — the signature typographic stop；Alternating full-bleed white canvas and #0f0f1c/#151623 midnight bands for vertical oscillation, with 80px section gaps

## QA 门结果（机器门复验：2026-08-22）

| 门 | 结果 | 证据 |
|---|---|---|
| G1 值层校验 | ✓ | `check-values.py`：deck 用色 ⊆ 素材 palette（含 DESIGN.md 声明例外），零自创 |
| G2 行高 + 安全区 | ✓ | `check-decks.py`：正文行高全部 = 1.5，8 页内容最低点 ≤ y 900 |
| G3 视觉 QA | ✓ | 全量 8 页截图逐页检查通过（2026-08-21 批次，30/30 套全过记录；无重叠/无截断/无颜色违规） |
| G4 结构反趋同 | ✓ | `check-structure.py`：工业 族 / 信号 clay-panel, dark-panel, panel-num；通用脚手架页 1/5 |

## 备注

- 截图事实源：`showcase/hyer-aviation/screenshots/slide-0..7.png`（不入库，shot-all-slides.py 可再生；15.6 视觉 QA 用）。
- 本报告机器门结果来自提交前全量复跑（2026-08-22），行高/安全区为 Playwright 实测值。
