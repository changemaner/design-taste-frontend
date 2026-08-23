# Flying Papers — QA 报告

- **成品**: `showcase/flying-papers/index.html`（8 页 deck，1920×1080 舞台）
- **素材**: `refero-styles/Flying Papers/`（DESIGN.md + tokens.json + variables.css + theme.css）
- **生成方式**: general-purpose 子代理（43 分钟，自带像素安全区校验）→ 视觉 QA → 仲裁
- **值层核对**: tokens 取自 tokens.json（11 色、6px 卡圆角、100px pill）→ `qc: ok`

## 视觉 QA 结果

评级 **良**。报告 2 个问题，**均为视觉子代理误判，像素仲裁后无真实缺陷**：

| 报告问题 | 仲裁结果 |
|---|---|
| slide-2/slide-6 "3 种卡片配色超限" | DESIGN.md 明确 Matcha 是 "secondary cast of cards"、Pink 用于 pop、Magenta 用于 standout——3 卡 3 色是设计系统意图；"每页 2 accent"是 QA prompt 自设的过严约束，非素材规则 |
| slide-5 "白色 #ffffff 正文文字" | 纯白像素 = 0；实际是骨白 #f9f5f2（系统色）被 doubao 误判为纯白 |

## 管线经验（沉淀）

1. **视觉子代理（doubao）色觉不可靠**：骨白 #f9f5f2 vs 纯白 #ffffff（Δ≈13）会误判；小圆角（8px）会误判为全圆角。**涉及颜色/圆角判定时以 CSS 事实 + 最小像素仲裁为准**
2. **QA prompt 的约束必须来自 DESIGN.md 原文**，不能凭直觉加（"2 accent"就是直觉加的，造成误报循环）
3. **general-purpose 子代理可以完成生成**（Flying Papers 成功），但 4 并发时不稳定（Raycast/MotherDuck 首轮失败）；安全做法是 ≤2 并发
4. 子代理自带像素校验（y≤900 安全区）是加分项，可写进后续生成指令

## 风格摘要

Dusk Violet 紫罗兰纸面 + Archivo 压缩黑体（900）+ 荧光黄/奶油黄双层海报字 + 6px 平涂色卡（magenta/bone/matcha/lilac）+ 100px 奶白胶囊 + JetBrains Mono 收据标签的 riso 印刷感创意工作室演示。
