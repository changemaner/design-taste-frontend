# MotherDuck — QA 报告（重做版）

- **成品**: `showcase/motherduck/index.html`（8 页 deck，1920×1080 舞台）
- **素材**: `refero-styles/MotherDuck/`（DESIGN.md 454 行 + tokens.json 853 行，大素材）
- **生成方式**: 子代理首版（幽灵完成）→ **值层校验失败（深色自创）→ 主模型重做** → 视觉 QA → 修复 → 复验
- **值层核对**: 重做版 22/22 颜色全部在素材色板内（系统外 0）→ `qc: ok`

## 值层违规记录（校验发现）

**首版（子代理）严重偏离素材**：素材是奶油浅色 neo-brutalist（Cream Paper #f4efea 画布 + Charcoal #383838 线色 + Sky Crayon #6fc2ff 主色），子代理却自创深蓝灰底色系（5 个系统外色）做了深色主题——基调错误。
**根因**：子代理未严格执行"值层 1:1 从 tokens.json 取值"；视觉 QA 基准从 HTML 反推（非素材）导致漏检。
**处置**：主模型按素材色板完整重做（奶油画布 + 硬 2px 圆角 + 零模糊硬阴影 + mono-first + 彩虹描边 chip + 手绘鸭子）。

## 重做版视觉 QA（评级 良 → 复验通过）

| 报告问题 | 处理 |
|---|---|
| slide-0 黄色横幅文字截断 | 误判：marquee 滚动横幅的设计效果 |
| slide-6（AI 页）左下内容贴底 | 真实问题：console 底部 ~975 超安全区。修复：顶部间距压缩 + console 精简（删表格行、缩文案）→ console 止于 ~880；右列 3 块改 2 块。像素仲裁确认 y880-1080 仅 chrome 文字 |

## 风格摘要

奶油笔记本 + 终端读数：浅色画布、炭黑线、天蓝唯一 CTA、canary 横幅、彩虹描边 chip、鸭子 logo、硬阴影——neo-brutalist technical-playful。

## 管线经验（重点）

- **值层校验必须独立于视觉 QA**：生成后跑"HTML 颜色 ⊆ tokens.json 色板"脚本（本套 5 个系统外色、IKEA 11 个都是这样抓出来的）；视觉 QA 基准必须从素材 DESIGN.md 提取，不能从 HTML 反推
- 大素材 + 子代理 = 值层自创高风险；重做版由主模型亲手完成
