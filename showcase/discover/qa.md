# Discover — QA 报告

- **成品**: `showcase/discover/index.html`（8 页 deck，1920×1080 舞台）
- **素材**: `refero-styles/Discover/`（DESIGN.md / tokens.json / variables.css / theme.css）
- **风格摘要**: Type museum on white marble — a near-black wordmark, a whisper of coral, and everything else recedes.
- **生成方式**: 按 skill 15 章 DECK MODE 素材模式（manifest 选型 → DESIGN.md 值层 1:1）
- **签名动作**: 120px Aeonik 700 wordmark at -1.32px tracking, near-edge-to-edge on white — the brand name as the hero image；Single 12px Signal Coral notification dot on the wordmark's final letter — one pop of color that says 'new' without a badge；32px border-radius on all cards, buttons, and containers — the large soft radius that defines the modern gallery feel；Oversized 'Aa' type specimens rendered in-card as the product itself, dominating each font preview tile；Ghost text link in Signal Coral with an external-arrow glyph (↗) — the only interactive text color in a monochrome room

## QA 门结果（机器门复验：2026-08-22）

| 门 | 结果 | 证据 |
|---|---|---|
| G1 值层校验 | ✓ | `check-values.py`：deck 用色 ⊆ 素材 palette（含 DESIGN.md 声明例外），零自创 |
| G2 行高 + 安全区 | ✓ | `check-decks.py`：正文行高全部 = 1.5，8 页内容最低点 ≤ y 900 |
| G3 视觉 QA | ✓ | 全量 8 页截图逐页检查通过（2026-08-21 批次，30/30 套全过记录；无重叠/无截断/无颜色违规） |
| G4 结构反趋同 | ✓ | `check-structure.py`：产品 族 / 信号 chip-coral, specimen；通用脚手架页 0/5 |

## 备注

- 截图事实源：`showcase/discover/screenshots/slide-0..7.png`（不入库，shot-all-slides.py 可再生；15.6 视觉 QA 用）。
- 本报告机器门结果来自提交前全量复跑（2026-08-22），行高/安全区为 Playwright 实测值。
