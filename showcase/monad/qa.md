# Monad — QA 报告

- **成品**: `showcase/monad/index.html`（8 页 deck，1920×1080 舞台）
- **素材**: `refero-styles/Monad/`（DESIGN.md / tokens.json / variables.css / theme.css）
- **风格摘要**: editorial tech journal on warm parchment
- **生成方式**: 按 skill 15 章 DECK MODE 素材模式（manifest 选型 → DESIGN.md 值层 1:1）
- **签名动作**: The serif-mono pairing — Untitled Serif at weight 400 for all headlines, ABC Diatype Mono for every body/nav/button/UI string — the serif announces, the mono instructs；Uppercase + tight-tracking mono labels on nav, buttons, and tags (18px / 14px), making functional text read as data；Lake Blue pill button with a trailing arrow as the single saturated conversion action per screen；The custom data-pipeline diagram — pill-shaped bordered nodes connected by thin curved Ash lines, the page's visual centerpiece；Soft gradient atmospheric washes (Coral → Sky Blue → Mint) with blur(50–75px) as decorative halos behind hero content

## QA 门结果（机器门复验：2026-08-22）

| 门 | 结果 | 证据 |
|---|---|---|
| G1 值层校验 | ✓ | `check-values.py`：deck 用色 ⊆ 素材 palette（含 DESIGN.md 声明例外），零自创 |
| G2 行高 + 安全区 | ✓ | `check-decks.py`：正文行高全部 = 1.35，8 页内容最低点 ≤ y 900 |
| G3 视觉 QA | ✓ | 全量 8 页截图逐页检查通过（2026-08-21 批次，30/30 套全过记录；无重叠/无截断/无颜色违规） |
| G4 结构反趋同 | ✓ | `check-structure.py`：数据 族 / 信号 journal-card, r-note, r-num, read-row；通用脚手架页 2/5 |

## 备注

- 截图事实源：`showcase/monad/screenshots/slide-0..7.png`（不入库，shot-all-slides.py 可再生；15.6 视觉 QA 用）。
- 本报告机器门结果来自提交前全量复跑（2026-08-22），行高/安全区为 Playwright 实测值。
