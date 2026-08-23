# Huddle — QA 报告

- **成品**: `showcase/huddle/index.html`（8 页 deck，1920×1080 舞台）
- **素材**: `refero-styles/Huddle/`（DESIGN.md / tokens.json / variables.css / theme.css）
- **风格摘要**: Pastel inventory cards on cream paper
- **生成方式**: 按 skill 15 章 DECK MODE 素材模式（manifest 选型 → DESIGN.md 值层 1:1）
- **签名动作**: Three pastel card colors (sage/lavender/dusty rose) as a fixed status taxonomy — one color per project status, never mixed within a card；A deliberate radius vocabulary: 100px pill tags and secondary buttons, 8px cards, 1000px reserved for the single primary button — corner treatment is the hierarchy；All-caps bullet/step-number micro-labels ('• STEP 1: THE BRIEF') in 12px Nng as the primary wayfinding device；Burnt-amber border + honey-gold text on tag pills — the only warm highlight pair, reserved for emphasis；1px hairline borders instead of box-shadows — the system is flat by design, elevation via color contrast

## QA 门结果（机器门复验：2026-08-22）

| 门 | 结果 | 证据 |
|---|---|---|
| G1 值层校验 | ✓ | `check-values.py`：deck 用色 ⊆ 素材 palette（含 DESIGN.md 声明例外），零自创 |
| G2 行高 + 安全区 | ✓ | `check-decks.py`：正文行高全部 = 1.42，8 页内容最低点 ≤ y 900 |
| G3 视觉 QA | ✓ | 全量 8 页截图逐页检查通过（2026-08-21 批次，30/30 套全过记录；无重叠/无截断/无颜色违规） |
| G4 结构反趋同 | ✓ | `check-structure.py`：报纸 族 / 信号 status, tile；通用脚手架页 2/5 |

## 备注

- 截图事实源：`showcase/huddle/screenshots/slide-0..7.png`（不入库，shot-all-slides.py 可再生；15.6 视觉 QA 用）。
- 本报告机器门结果来自提交前全量复跑（2026-08-22），行高/安全区为 Playwright 实测值。
