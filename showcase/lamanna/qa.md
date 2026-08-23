# Lamanna — QA 报告

- **成品**: `showcase/lamanna/index.html`（8 页 deck，1920×1080 舞台）
- **素材**: `refero-styles/Lamanna/`（DESIGN.md / tokens.json / variables.css / theme.css）
- **风格摘要**: Neon circus tent on a Naples sidewalk
- **生成方式**: 按 skill 15 章 DECK MODE 素材模式（manifest 选型 → DESIGN.md 值层 1:1）
- **签名动作**: Full-bleed color bands with hard chromatic transitions (orange → blush → yellow) as section dividers — no max-width container, no card padding, every element touches the viewport edge；Right Grotesk Spatial display at line-height 0.89 so headlines stack into dense solid slabs rather than airy type；3D drop-shadow headlines — a solid #ff4100 offset on #ffc700 text, no blur, built-in dimensional depth；Sun-yellow starburst product badges instead of rectangular cards — no shadows, just geometric sun shapes；Zigzag SVGs, pointing hands, and royal-blue outlined links as decorative punctuation; 0px radius everywhere

## QA 门结果（机器门复验：2026-08-22）

| 门 | 结果 | 证据 |
|---|---|---|
| G1 值层校验 | ✓ | `check-values.py`：deck 用色 ⊆ 素材 palette（含 DESIGN.md 声明例外），零自创 |
| G2 行高 + 安全区 | ✓ | `check-decks.py`：正文行高全部 = 1.5，8 页内容最低点 ≤ y 900 |
| G3 视觉 QA | ✓ | 全量 8 页截图逐页检查通过（2026-08-21 批次，30/30 套全过记录；无重叠/无截断/无颜色违规） |
| G4 结构反趋同 | ✓ | `check-structure.py`：活泼 族 / 信号 band-*, zigzag-*；通用脚手架页 1/5 |

## 备注

- 截图事实源：`showcase/lamanna/screenshots/slide-0..7.png`（不入库，shot-all-slides.py 可再生；15.6 视觉 QA 用）。
- 本报告机器门结果来自提交前全量复跑（2026-08-22），行高/安全区为 Playwright 实测值。
