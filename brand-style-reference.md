# 官网风格学习报告（Brand Style Reference）

*Style reference only — not affiliated with, endorsed by, or sponsored by any brand named below. 报告基于各品牌公开官网的观察整理，仅供设计学习参考；品牌名与商标归各自所有者，本报告不随仓库 MIT 授权分发。*

> 日期：2026-08-20
> 目的：学习 30 套素材背后的**真实品牌官网**如何表现各自的风格（非照搬，而是学习表现手法），
> 对照已生成 deck 判断是否抓住精髓，沉淀为后续生成 deck 的风格参照资产。
> 数据源：30 套官网首页截图（`qa_shots/brand-sites/<slug>.png`，包外素材不入库，可按 `metadata/brand-urls.json` 自行截图）+ 每套 deck 截图（`showcase/gallery/<slug>/slide-{0,4,7}.png`）+ DESIGN.md。
> 官网链接映射：`metadata/brand-urls.json`（30/30 齐全）。

---

## 风格聚类（30 套 → 7 簇）

| 簇 | 风格类型 | 成员 | 代表官网 |
|---|---|---|---|
| A. 深色高端/极简 | premium, calm, monochrome | mercury / oryzo-ai / air / superhi-plus | mercury.com |
| B. 深色开发工具 | technical, authoritative | raycast | raycast.com |
| C. 编辑/衬线 | editorial, warm, quiet | steep / monad / huddle / syllabus / ventriloc / seline / leandra / wispr / monopo | steep.app |
| D. 工业粗体 | industrial, bold | caldera / henry / good-glyphs / gic / discover / patch / composer / hyer-aviation | caldera.xyz |
| E. 卡通/活力 | playful, chromatic | flying-papers / lamanna / lpalo / superr / frankys | flyingpapers.com |
| F. 北欧极简 | minimal, friendly | ikea / motherduck | ikea.com |

---

## 官网表现规律（按簇）

### A/B. 深色族共同手法
- 深色/低饱和背景 + 高对比文字保证可读性
- 极低元素密度，大量留白，只保留导航 + 核心 CTA
- 单一/少量高亮色作为品牌锚点（mercury 蓝按钮、raycast 珊瑚 logo）
- 超大标题 + 极简正文

### C. 编辑/衬线族共同手法
- 大号衬线/粗无衬线标题建立视觉焦点
- 充足留白、舒展排版
- 极简装饰，产品界面以"轻量悬浮卡片"呈现（steep 的数据卡）
- 纸感/米白背景营造温暖编辑气质（leandra / wispr 的纸感纹理）

### D. 工业/粗体系共同手法
- 超粗无衬线标题 + 单一高饱和品牌色（caldera 橙）
- 大量留白 + 右侧辅助文字对齐（caldera）
- 复古报刊式排版：超粗标题 vs 纤细衬线正文的字体张力（henry / gic）
- 网格/几何元素（patch 工业网格、composer 包豪斯几何）

### E. 卡通/活力族共同手法
- 高饱和亮色 + 手绘/插画元素
- 宽松排版 + 圆润字体
- 真实产品/场景图占比高（烘焙图、绘本图、街机图）
- 标志性图形（superhi 半色调笑脸、wispr 环形装饰文字）

### F. 北欧极简族共同手法
- 真实家居场景大图 + 低饱和自然配色 + 品牌亮黄点缀（ikea）
- 圆润无衬线、层级清晰

---

## deck vs 官网：逐套判定

### 完全贴合（4）
- **raycast**：纯深色+高对比+超大标题，完全符合
- **syllabus** / **seline-analytics** / **wispr-flow**：极简/编辑精髓全抓住

### 大体符合（20）
- mercury / air / steep / monad / huddle / ventriloc / leandra / caldera / ikea / lamanna / lpalo / superr / frankys / flying-papers / good-glyphs / discover / motherduck / composer / hyer-aviation / patch
- 共性偏差：**背景纹理/专属装饰元素缺失**（纸感、半色调、手绘、真实场景图），整体"偏通用好看的极简"

### 有偏差（4，需重点修正）
- **oryzo-ai**：未用官网深橄榄绿背景 + 橙色几何/虚线圆标志 → deck 成了通用极简
- **superhi-plus**：缺半色调印刷风格 + 笑脸品牌元素 → 蓝白对比有但不够品牌化
- **henry**：字体对比不够强（应超粗标题 vs 纤细衬线正文），缺复古报刊装饰（分隔线、侧边小字）
- **general-intelligence-company**：字体过于粗重，缺复古印刷细节，偏现代而非编辑出版

### 装饰过度（2）
- **caldera**：deck 加了点状装饰图形，官网更克制 → 建议移除多余装饰、还原极简留白
- **patch**：网格元素使用过度 → 减少，贴合官网极简工业风

---

## 给 deck 生成的借鉴规则（沉淀进 skill）

1. **官网是风格的"表现标杆"，DESIGN.md 是"事实源"**：生成 deck 时，值层/签名以 DESIGN.md + tokens 为准（1:1），氛围/装饰手法对照官网截图学习（`qa_shots/brand-sites/`，包外不入库；URL 见 `metadata/brand-urls.json`），但**不照搬官网布局**（官网是长页，deck 是 8 页舞台）。
2. **背景纹理是最大缺失项**：编辑族（纸感/米白纹理）、活力族（手绘/半色调）、工业族（网格）的官网都有背景纹理，deck 普遍用纯色——这是"偏通用"的主因。
3. **品牌专属标志元素必须出现**：每个官网都有标志性符号（superhi 笑脸、wispr 环形文字、oryzo 几何圆、raycast 珊瑚 logo），deck 里应至少保留 1 个。
4. **字体对比是编辑族的灵魂**：henry/gic 这类复古编辑风，超粗标题 vs 纤细正文的对比是精髓，字重选择不能温和。
5. **克制优先**：caldera/patch 证明"装饰过多"和"装饰过少"都是偏差——官网的克制程度就是基准。

---

## 附录：验证链路

- 官网截图：30 套（统一为 1280×800 PNG，来源为各品牌官网首屏）
- 截图工具：playwright + 系统 Chrome（headless 1280×800）
- 分析：vision-reader 子代理逐张读图 + 对照 DESIGN.md/tokens
