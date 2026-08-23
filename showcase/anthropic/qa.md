# Anthropic — QA 报告

- **成品**: `showcase/anthropic/index.html`（8 页 deck，1920×1080 舞台）
- **素材**: `refero-styles/Anthropic/`（DESIGN.md + tokens.json + variables.css + theme.css）
- **值层核对**: tokens.json 与 DESIGN.md Quick Start 完全一致，无冲突 → `qc: ok`
- **视觉 QA**: vision-reader 子代理（doubao-seed-2.0-mini），修复后评级 **良**

## 修复记录（首版 → 定稿）

| # | 问题 | 发现方式 | 修复 |
|---|---|---|---|
| 1 | slide-0 CTA 按钮被正文挤出画布（absolute 定位不受 frame padding 约束） | 坐标检测（clay=0） | 封面改流式 flex column 布局 |
| 2 | slide-3 表格卡底部侵入 chrome 区（y 1062-1078） | 坐标检测 + 视觉确认 | 数据页改两栏（左 stat + 右表格卡），表格行收紧 |
| 3 | slide-5 dark-band 深色带压底（y 560-1040） | 坐标检测 | dark-band 行距/字号收紧，右栏 padding 220→150 |
| 4 | 按钮圆角方向反了（写成上圆角，DESIGN.md 要求底部-only） | 视觉确认 | `border-radius: 0 0 8px 8px`（上角尖、下角圆） |

## 复验

- 视觉子代理：8 页全部通过（无溢出/无字体回退/无颜色违规/无阴影渐变），slide-0、slide-3 修复确认
- 坐标复核：slide-7 按钮四角像素 = 顶部直角 64/64、底部圆角 52/64 → 圆角方向正确（视觉子代理误判为全圆角，8px 圆角太小所致）
- 底部安全区：所有页面内容 ≤ y 920，chrome（fixed 视口层）无冲突

## 管线经验（沉淀给其余 4 套）

1. **值层权威契约生效**：tokens.json 与 DESIGN.md 一致时零摩擦；后续如遇冲突以 tokens.json 为准
2. **绝对定位是溢出主因**：slide 内元素一律用流式布局（frame padding 约束），不用 absolute 堆叠内容
3. **内容高度要预算**：标题 ≤ 96px（×2 舞台），行距/字号按 1080 舞台预算到 y ≤ 900
4. **按钮圆角方向**：按 DESIGN.md 的 signature 写（Anthropic = bottom-only 8px）
5. **视觉子代理对 8px 级细节会误判**：小圆角/小字号差异以坐标复核为准
