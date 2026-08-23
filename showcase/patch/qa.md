# Patch — QA 报告

- **成品**: `showcase/patch/index.html`（8 页 deck，1920×1080 舞台）
- **素材**: `refero-styles/Patch/`（DESIGN.md / tokens.json / variables.css / theme.css）
- **风格摘要**: electric blueprint on drafting paper
- **生成方式**: 按 skill 15 章 DECK MODE 素材模式（manifest 选型 → DESIGN.md 值层 1:1）
- **签名动作**: Full-bleed electric-indigo (#1f00ff) hero and alternating indigo/white section bands — the page is built on the blue/white duopoly；PP Right weight 800 condensed display with sub-1.0 line heights (0.85–0.94), stacking headlines like concrete blocks — never below 21px；The single filled orange (#ff622b) CTA button (5px radius, no shadow) as the only chromatic conversion surface; everything else outlined or text；Two-digit square corner markers (01, 02, 03…) in bordered boxes anchoring every section like a blueprint grid；Hand-drawn black-line sketch illustrations (people, objects) centered inside white 1px-indigo-bordered cards, softening the aggressive type

## QA 门结果（机器门复验：2026-08-22）

| 门 | 结果 | 证据 |
|---|---|---|
| G1 值层校验 | ✓ | `check-values.py`：deck 用色 ⊆ 素材 palette（含 DESIGN.md 声明例外），零自创 |
| G2 行高 + 安全区 | ✓ | `check-decks.py`：正文行高全部 = 1.4，8 页内容最低点 ≤ y 900 |
| G3 视觉 QA | ✓ | 全量 8 页截图逐页检查通过（2026-08-21 批次，30/30 套全过记录；无重叠/无截断/无颜色违规） |
| G4 结构反趋同 | ✓ | `check-structure.py`：工业 族 / 信号 blue-card, blueprint-grid, sketch；通用脚手架页 0/5 |

## 备注

- 截图事实源：`showcase/patch/screenshots/slide-0..7.png`（不入库，shot-all-slides.py 可再生；15.6 视觉 QA 用）。
- 本报告机器门结果来自提交前全量复跑（2026-08-22），行高/安全区为 Playwright 实测值。
