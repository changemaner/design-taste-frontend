# Air — QA 报告

- **成品**: `showcase/air/index.html`（8 页 deck，1920×1080 舞台）
- **素材**: `refero-styles/Air/`（DESIGN.md / tokens.json / variables.css / theme.css）
- **风格摘要**: midnight sky through glass sculpture
- **生成方式**: 按 skill 15 章 DECK MODE 素材模式（manifest 选型 → DESIGN.md 值层 1:1）
- **签名动作**: Ghost buttons — transparent fill + 1px white border + white text, 8px radius — the only nav CTA treatment; no filled colored buttons anywhere；Full-bleed dark photographic sections (clouds, glass sculpture) with centered headline overlays, no container constraint — imagery carries the emotion；Compressed display headline at 259px/900 weight/0.85 leading, uppercase, bleeding to viewport edges, used sparingly for maximum-impact statements；Dual-style headline mixing one cursive italic word (Cursive 56px) against upright Control TNT — typographic tension that carries personality；Flat Haze cards (#f5f5f5, 12px radius, no shadow, no border) sitting as light islands on the dark canvas

## QA 门结果（机器门复验：2026-08-22）

| 门 | 结果 | 证据 |
|---|---|---|
| G1 值层校验 | ✓ | `check-values.py`：deck 用色 ⊆ 素材 palette（含 DESIGN.md 声明例外），零自创 |
| G2 行高 + 安全区 | ✓ | `check-decks.py`：正文行高全部 = 1.5，8 页内容最低点 ≤ y 900 |
| G3 视觉 QA | ✓ | 全量 8 页截图逐页检查通过（2026-08-21 批次，30/30 套全过记录；无重叠/无截断/无颜色违规） |
| G4 结构反趋同 | ✓ | `check-structure.py`：产品 族 / 信号 glass, haze-card；通用脚手架页 0/5 |

## 备注

- 截图事实源：`showcase/air/screenshots/slide-0..7.png`（不入库，shot-all-slides.py 可再生；15.6 视觉 QA 用）。
- 本报告机器门结果来自提交前全量复跑（2026-08-22），行高/安全区为 Playwright 实测值。
