# Caldera — QA 报告

- **成品**: `showcase/caldera/index.html`（8 页 deck，1920×1080 舞台）
- **素材**: `refero-styles/Caldera/`（DESIGN.md / tokens.json / variables.css / theme.css）
- **风格摘要**: forge fire on warm limestone. The canvas is raw warm plaster, and every orange element reads as glowing embers pressed into the surface.
- **生成方式**: 按 skill 15 章 DECK MODE 素材模式（manifest 选型 → DESIGN.md 值层 1:1）
- **签名动作**: Triple-radius system — 100px inputs / 40px cards & rectangular buttons / 800px full pills — the consistent roundness that defines every control；189px ultrabold compressed display headline at 0.94 line-height — sign-painted, near-architectural scale as the page signature；Hero halftone dot pattern — orange dots on a violet-to-orange gradient, always at hero scale with 40px radius, the most recognizable motif；Filled Ember (#fc5000) pill CTA with Obsidian text, never rectangular — the sole aggressive chromatic action；Dotted 1.5px Obsidian dividers (not dashed, not solid) as a small consistent signature detail in nav and partner strips

## QA 门结果（机器门复验：2026-08-22）

| 门 | 结果 | 证据 |
|---|---|---|
| G1 值层校验 | ✓ | `check-values.py`：deck 用色 ⊆ 素材 palette（含 DESIGN.md 声明例外），零自创 |
| G2 行高 + 安全区 | ✓ | `check-decks.py`：正文行高全部 = 1.55，8 页内容最低点 ≤ y 900 |
| G3 视觉 QA | ✓ | 全量 8 页截图逐页检查通过（2026-08-21 批次，30/30 套全过记录；无重叠/无截断/无颜色违规） |
| G4 结构反趋同 | ✓ | `check-structure.py`：工业 族 / 信号 card-ember, halftone-*；通用脚手架页 0/5 |

## 备注

- 截图事实源：`showcase/caldera/screenshots/slide-0..7.png`（不入库，shot-all-slides.py 可再生；15.6 视觉 QA 用）。
- 本报告机器门结果来自提交前全量复跑（2026-08-22），行高/安全区为 Playwright 实测值。
