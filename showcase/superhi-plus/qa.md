# SuperHi Plus — QA 报告

- **成品**: `showcase/superhi-plus/index.html`（8 页 deck，1920×1080 舞台）
- **素材**: `refero-styles/SuperHi Plus/`（DESIGN.md / tokens.json / variables.css / theme.css）
- **风格摘要**: Cobalt blueprint scattered with emoji marbles. The page lives half in electric blue, half in ice white, swapping sides as you scroll.
- **生成方式**: 按 skill 15 章 DECK MODE 素材模式（manifest 选型 → DESIGN.md 值层 1:1）
- **签名动作**: The 50/50 split-screen panel: every section is two equal full-bleed panels that swap colors — one Ice White with display type/imagery, one Cobalt Voltage with body — alternating which side is which down the page；Single-weight neo-grotesque type at enormous scale (up to 85px) at weight 400 only — no bold, no light, no italic; size and the blue/white contrast create all hierarchy；The arrow-prefixed (→) text navigation button as the signature affordance for all clickable text, rendered at 42px with no border or fill；Clusters of 3D-rendered emoji-face spheres in cobalt and ice tones filling every empty light panel — the marbles ARE the social proof and personality；1px inset borders (Cobalt Voltage or Ice White) as the universal depth indicator — pill radii (50–72px) sit next to sharp 16px cards, and no drop shadows exist anywhere

## QA 门结果（机器门复验：2026-08-22）

| 门 | 结果 | 证据 |
|---|---|---|
| G1 值层校验 | ✓ | `check-values.py`：deck 用色 ⊆ 素材 palette（含 DESIGN.md 声明例外），零自创 |
| G2 行高 + 安全区 | ✓ | `check-decks.py`：正文行高全部 = 1.33，8 页内容最低点 ≤ y 900 |
| G3 视觉 QA | ✓ | 全量 8 页截图逐页检查通过（2026-08-21 批次，30/30 套全过记录；无重叠/无截断/无颜色违规） |
| G4 结构反趋同 | ✓ | `check-structure.py`：活泼 族 / 信号 half-*, marble, split；通用脚手架页 1/5 |

## 备注

- 截图事实源：`showcase/superhi-plus/screenshots/slide-0..7.png`（不入库，shot-all-slides.py 可再生；15.6 视觉 QA 用）。
- 本报告机器门结果来自提交前全量复跑（2026-08-22），行高/安全区为 Playwright 实测值。
