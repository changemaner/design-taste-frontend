# General Intelligence Company — QA 报告

- **成品**: `showcase/general-intelligence-company/index.html`（8 页 deck，1920×1080 舞台）
- **素材**: `refero-styles/General Intelligence Company/`（DESIGN.md / tokens.json / variables.css / theme.css）
- **风格摘要**: Literary journal beside a bonfire
- **生成方式**: 按 skill 15 章 DECK MODE 素材模式（manifest 选型 → DESIGN.md 值层 1:1）
- **签名动作**: Frosted navigation pill — floating top-center, rgba white + backdrop-blur(9-20px), 50px pill radius, 1px twilight border — lets the illustrated hero show through；Full-bleed hand-painted atmospheric illustrations (moonlit skylines, wildflower meadows) as the emotional work, with UI living on clean white between scenes；Border-only CTA in Signal Blue (#41a1cf) at 8px radius — no fill, no shadow, the chromatic border is the button's entire identity；Green-tinted 1px Mist (#dee2de) hairline borders on cards — the signature edge treatment that harmonizes with the illustrations；Cerulean (#0081c0) saturated card surface as a lone punctuation moment of color intensity

## QA 门结果（机器门复验：2026-08-22）

| 门 | 结果 | 证据 |
|---|---|---|
| G1 值层校验 | ✓ | `check-values.py`：deck 用色 ⊆ 素材 palette（含 DESIGN.md 声明例外），零自创 |
| G2 行高 + 安全区 | ✓ | `check-decks.py`：正文行高全部 = 1.5，8 页内容最低点 ≤ y 900 |
| G3 视觉 QA | ✓ | 全量 8 页截图逐页检查通过（2026-08-21 批次，30/30 套全过记录；无重叠/无截断/无颜色违规） |
| G4 结构反趋同 | ✓ | `check-structure.py`：插画 族 / 信号 cerulean-card, paper-card, read-note, read-row；通用脚手架页 1/5 |

## 备注

- 截图事实源：`showcase/general-intelligence-company/screenshots/slide-0..7.png`（不入库，shot-all-slides.py 可再生；15.6 视觉 QA 用）。
- 本报告机器门结果来自提交前全量复跑（2026-08-22），行高/安全区为 Playwright 实测值。
