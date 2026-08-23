# Good Glyphs — QA 报告

- **成品**: `showcase/good-glyphs/index.html`（8 页 deck，1920×1080 舞台）
- **素材**: `refero-styles/Good Glyphs/`（DESIGN.md / tokens.json / variables.css / theme.css）
- **风格摘要**: oversized charity poster on mint paper — type so large it behaves as architecture, not text.
- **生成方式**: 按 skill 15 章 DECK MODE 素材模式（manifest 选型 → DESIGN.md 值层 1:1）
- **签名动作**: 288px / weight 300 / line-height 0.80 / -0.03em tracking display headline — the brand name rendered as a locked wall of ink, size IS the identity；Full-bleed mint-to-black band alternation producing poster-strip rhythm rather than card-based hierarchy；Fully pill-shaped 140px controls for every interactive element — no squared or rounded-rect variants, hover inverts fill (mint→black, black→mint)；Black showcase band spanning viewport width with 288px dingbat glyphs in Pledge Mint — the product proven at use size, the only color-on-black moment；1px solid black borders + 14px soft card radius — components feel stamped rather than designed

## QA 门结果（机器门复验：2026-08-22）

| 门 | 结果 | 证据 |
|---|---|---|
| G1 值层校验 | ✓ | `check-values.py`：deck 用色 ⊆ 素材 palette（含 DESIGN.md 声明例外），零自创 |
| G2 行高 + 安全区 | ✓ | `check-decks.py`：正文行高全部 = 1.5，8 页内容最低点 ≤ y 900 |
| G3 视觉 QA | ✓ | 全量 8 页截图逐页检查通过（2026-08-21 批次，30/30 套全过记录；无重叠/无截断/无颜色违规） |
| G4 结构反趋同 | ✓ | `check-structure.py`：报纸 族 / 信号 glyph, poster-card；通用脚手架页 1/5 |

## 备注

- 截图事实源：`showcase/good-glyphs/screenshots/slide-0..7.png`（不入库，shot-all-slides.py 可再生；15.6 视觉 QA 用）。
- 本报告机器门结果来自提交前全量复跑（2026-08-22），行高/安全区为 Playwright 实测值。
