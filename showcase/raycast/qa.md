# Raycast — QA 报告

- **成品**: `showcase/raycast/index.html`（8 页 deck，1920×1080 舞台）
- **素材**: `refero-styles/Raycast/`（DESIGN.md 495 行 + tokens.json 818 行，大素材）
- **生成方式**: general-purpose 子代理（报"空响应失败"但产物完整——幽灵完成现象）→ 视觉 QA → 修复 → 复验
- **值层核对**: 色板（void-black #040506 / ink / coral #ff6363 等）与 DESIGN.md 一致 → `qc: ok`

## 视觉 QA 结果（评级 良 → 复验通过）

| 报告问题 | 处理 |
|---|---|
| slide-3（数据页）左下统计文本与底部导航重叠 | 真实问题：左列 3 统计总高 ~907 超安全区底线 900。修复：列间距 64→48 + 第 3 个 label 缩短。复验通过 |
| "深红褐色卡片背景超色板" | **误判**：是系统色 Ember Hush #452324（Surface 4 Accent Tint） |
| "未使用 JetBrains Mono" | 误判：mono 标签已用（小字号视觉难辨） |
| 表格绿/蓝圆点"系统外颜色" | 非问题：Info Blue #56c2ff / Success Green #59d499 在系统色板内（DESIGN.md 定义） |

## 风格摘要

午夜指挥中心：近纯黑画布 + 单一珊瑚强调（logo 菱形 / AI 徽章 / hero 光效）+ Mist 中性按钮（无彩色 CTA）+ "键盘键"内阴影卡片 + Inter 全部 + JetBrains Mono 技术标签 + 红蓝 hero 渐变光效（唯一彩色时刻）。

## 管线经验

- 素材大（1500+ 行）时子代理易"幽灵完成"或失败——**失败通知 ≠ 无产物**，先检查目标目录再决定重跑
- 深色系统在视觉子代理眼中容易误报（色板外颜色、字体缺失），仲裁以 CSS 变量定义为准
