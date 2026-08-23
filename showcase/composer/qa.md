# Composer — QA 报告

- **成品**: `showcase/composer/index.html`（8 页 deck，1920×1080 舞台）
- **素材**: `refero-styles/Composer/`（DESIGN.md / tokens.json / variables.css / theme.css）
- **风格摘要**: Bauhaus confetti on concrete
- **生成方式**: 按 skill 15 章 DECK MODE 素材模式（manifest 选型 → DESIGN.md 值层 1:1）
- **签名动作**: 244px display headline at weight 600, line-height 1.0, positive tracking — transforms headings into posters, paired with a smaller 'headline + dek' subtitle；Confetti color blocks — zero-radius solid rectangles (40-200px) scattered across the gray canvas as geometric information, not decoration；Filled black pill CTA (Obsidian fill, white text, 9999px radius, arrow glyph) — the system's only filled button, never chromatic；Cotton Candy (#ffb4ed) marker-pen highlight on key words in body copy for editorial scannability without changing text color；Sharp-vs-pill geometric tension — 2px icon containers and 6px cards alongside 9999px pill buttons

## QA 门结果（机器门复验：2026-08-22）

| 门 | 结果 | 证据 |
|---|---|---|
| G1 值层校验 | ✓ | `check-values.py`：deck 用色 ⊆ 素材 palette（含 DESIGN.md 声明例外），零自创 |
| G2 行高 + 安全区 | ✓ | `check-decks.py`：正文行高全部 = 1.5，8 页内容最低点 ≤ y 900 |
| G3 视觉 QA | ✓ | 全量 8 页截图逐页检查通过（2026-08-21 批次，30/30 套全过记录；无重叠/无截断/无颜色违规） |
| G4 结构反趋同 | ✓ | `check-structure.py`：报纸 族 / 信号 card, confetti；通用脚手架页 0/5 |

## 备注

- 截图事实源：`showcase/composer/screenshots/slide-0..7.png`（不入库，shot-all-slides.py 可再生；15.6 视觉 QA 用）。
- 本报告机器门结果来自提交前全量复跑（2026-08-22），行高/安全区为 Playwright 实测值。
