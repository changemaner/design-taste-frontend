# FRANKY'S — QA 报告

- **成品**: `showcase/frankys/index.html`（8 页 deck，1920×1080 舞台）
- **素材**: `refero-styles/FRANKY'S/`（DESIGN.md / tokens.json / variables.css / theme.css）
- **风格摘要**: Retro arcade kiosk on a skate-shop counter.
- **生成方式**: 按 skill 15 章 DECK MODE 素材模式（manifest 选型 → DESIGN.md 值层 1:1）
- **签名动作**: Black-and-white checkerboard (#f3e5df / #000000, ~48px tiles) as the hero product panel and brand pattern — never a functional UI surface；6px radius on all CTAs, tags, and toggles with a 1px inset cream highlight (rgb(243,229,223) 0 1px 0 0 inset) for the arcade-button bevel；Marquee sheen gradient band (orange → cream → orange) across the top — the only decorative chromatic surface on the page；Single-arcade-font weight jump (400 body → 700 titles/nav/footer) as the complete hierarchy system；Filled Buy Green Add-To-Cart button (6px radius, white uppercase 700 text) — the only green surface, reserved for purchase only

## QA 门结果（机器门复验：2026-08-22）

| 门 | 结果 | 证据 |
|---|---|---|
| G1 值层校验 | ✓ | `check-values.py`：deck 用色 ⊆ 素材 palette（含 DESIGN.md 声明例外），零自创 |
| G2 行高 + 安全区 | ✓ | `check-decks.py`：正文行高全部 = 1.5，8 页内容最低点 ≤ y 900 |
| G3 视觉 QA | ✓ | 全量 8 页截图逐页检查通过（2026-08-21 批次，30/30 套全过记录；无重叠/无截断/无颜色违规） |
| G4 结构反趋同 | ✓ | `check-structure.py`：活泼 族 / 信号 pixel-card, pixel-table, product-art, product-card；通用脚手架页 1/5 |

## 备注

- 截图事实源：`showcase/frankys/screenshots/slide-0..7.png`（不入库，shot-all-slides.py 可再生；15.6 视觉 QA 用）。
- 本报告机器门结果来自提交前全量复跑（2026-08-22），行高/安全区为 Playwright 实测值。
