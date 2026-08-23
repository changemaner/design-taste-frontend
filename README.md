# design-taste-frontend

反 AI slop 的前端设计 skill。做两类东西，通用前端设计（landing / portfolio / editorial / redesign / app）和 deck 模式（固定舞台的 HTML 演示文稿），分别对应 SKILL.md 的 Sections 1-14 与 15-16。

AI 生成的页面一眼假，多半败在值层，颜色、字号、间距是模型现编的。这个包的解法很直接，带上 30 套真实品牌的设计系统素材，每套拆成 DESIGN.md / tokens.json / variables.css / theme.css 四个文件，生成时值层 1:1 兑现，再过四道机器 QA 门。像不像，不靠感觉，靠对照。

## 快速开始

纯 skill 目录，克隆进去就能被 Agent 加载，没有构建步骤。推荐装到跨 Agent 的通用目录 `~/.agents/skills/`，这个包不绑定任何一个 Agent；个别 Agent 只认自家 skills 目录（如 `~/.claude/skills/`、`~/.zcode/skills/`），克隆过去即可。

**人手动装**

```bash
git clone --depth 1 https://github.com/changemaner/design-taste-frontend.git ~/.agents/skills/design-taste-frontend
```

**让 AI 装**

现在很多人不手动配 skill 了，直接让 AI 代劳。把下面这段发给你的 Agent，剩下的它来。

```text
帮我把 https://github.com/changemaner/design-taste-frontend 装成 skill。浅克隆（--depth 1）到 ~/.agents/skills/design-taste-frontend（跨 Agent 的通用目录；如果你只从别的 skills 目录加载，就克隆到你认的那个）。装完告诉我装到了哪里。之后的前端设计任务按这个 skill 的 SKILL.md 走。
```


## 怎么用

- **通用前端设计**。按 SKILL.md Sections 1-14 走，读 brief、调三拨盘、落设计系统。
- **deck / 演示文稿**。走 0.E 路由进 Section 15 DECK MODE + 16 STYLE CONTRACT，分两条路。
  - **素材模式（默认）**。拿 brief 匹配素材库，查 `showcase/selection-index.json` 筛选，到 `showcase/gallery/` 看预览，读中选那套的 `DESIGN.md`，然后生成。值层 1:1，四道 QA 门把关（见 SKILL.md 15.6）。
  - **自由发挥模式（回退）**。brief 在素材库之外时，先填 `freeplay-declaration.md` 声明自创风格，按声明生成，QA 门 2/3 照跑。
- **全量截图**。不入库，要时本地重截。`python showcase/shot-all-slides.py [slug 或 deck 目录]` 经 file:// 直读，showcase 套落在 `showcase/<slug>/screenshots/`，包外 deck 落在 deck 旁 `screenshots/`（前置是 playwright + Chrome）。仓库内预览以 gallery 三图为准。
- **图廊**。浏览器打开 `showcase/gallery/index.html`，30 套成品一起挑。图廊只取 `showcase/gallery/<slug>/slide-0/4/7.png` 三张做轻量预览。

## 风格速览（30 套素材 → 30 套成品）

每套配 3 张预览截图（成品 deck 的 slide 0 / 4 / 7）和一段风格介绍，点图跳到该套成品 `showcase/<slug>/index.html`。想按色调、密度、用途筛选，开完整图廊 `showcase/gallery/index.html`。

### 1. Air
纯黑画布上浮着白色幽灵按钮与大号几何无衬线，图像主导，安静得像暗夜里的玻璃雕塑。开发者工具与 AI 产品发布用它正合适，Linear、Vercel 的语感。
<p>
  <a href="showcase/air/index.html"><img src="showcase/gallery/air/slide-0.png" width="32%" alt="Air slide 0"></a>
  <a href="showcase/air/index.html"><img src="showcase/gallery/air/slide-4.png" width="32%" alt="Air slide 4"></a>
  <a href="showcase/air/index.html"><img src="showcase/gallery/air/slide-7.png" width="32%" alt="Air slide 7"></a>
</p>

### 2. Anthropic
象牙纸面配编辑衬线标题，粘土色只在必须行动时出现一次，整页像暖纸上的科学田野日志。AI 研究与深度科技品牌用它，权威而不冰凉。
<p>
  <a href="showcase/anthropic/index.html"><img src="showcase/gallery/anthropic/slide-0.png" width="32%" alt="Anthropic slide 0"></a>
  <a href="showcase/anthropic/index.html"><img src="showcase/gallery/anthropic/slide-4.png" width="32%" alt="Anthropic slide 4"></a>
  <a href="showcase/anthropic/index.html"><img src="showcase/gallery/anthropic/slide-7.png" width="32%" alt="Anthropic slide 7"></a>
</p>

### 3. Caldera
189px 超粗窄版大字配一粒橙色余烬，火山般的紧迫感烧在暖石灰岩底色上。crypto、web3、协议生态适用。
<p>
  <a href="showcase/caldera/index.html"><img src="showcase/gallery/caldera/slide-0.png" width="32%" alt="Caldera slide 0"></a>
  <a href="showcase/caldera/index.html"><img src="showcase/gallery/caldera/slide-4.png" width="32%" alt="Caldera slide 4"></a>
  <a href="showcase/caldera/index.html"><img src="showcase/gallery/caldera/slide-7.png" width="32%" alt="Caldera slide 7"></a>
</p>

### 4. Composer
浅灰画布上，244px 海报级标题撞上几何色块，像混凝土面上一把包豪斯纸屑。金融科技与开发者工具的宣言式营销页，Stripe、Replit 邻域。
<p>
  <a href="showcase/composer/index.html"><img src="showcase/gallery/composer/slide-0.png" width="32%" alt="Composer slide 0"></a>
  <a href="showcase/composer/index.html"><img src="showcase/gallery/composer/slide-4.png" width="32%" alt="Composer slide 4"></a>
  <a href="showcase/composer/index.html"><img src="showcase/gallery/composer/slide-7.png" width="32%" alt="Composer slide 7"></a>
</p>

### 5. Discover
近单色系统只留 1% 珊瑚色做行动色，120px 标志字本身就是英雄图，一座白大理石上的字体博物馆。字体商店与以版式为产品的目录页适用。
<p>
  <a href="showcase/discover/index.html"><img src="showcase/gallery/discover/slide-0.png" width="32%" alt="Discover slide 0"></a>
  <a href="showcase/discover/index.html"><img src="showcase/gallery/discover/slide-4.png" width="32%" alt="Discover slide 4"></a>
  <a href="showcase/discover/index.html"><img src="showcase/gallery/discover/slide-7.png" width="32%" alt="Discover slide 7"></a>
</p>

### 6. Flying Papers
暮紫满版舞台，一屏一幅大字海报，像周六早上的卡通独白，反商业宣言的气质。创意编辑微站与海报式品牌声明适用。
<p>
  <a href="showcase/flying-papers/index.html"><img src="showcase/gallery/flying-papers/slide-0.png" width="32%" alt="Flying Papers slide 0"></a>
  <a href="showcase/flying-papers/index.html"><img src="showcase/gallery/flying-papers/slide-4.png" width="32%" alt="Flying Papers slide 4"></a>
  <a href="showcase/flying-papers/index.html"><img src="showcase/gallery/flying-papers/slide-7.png" width="32%" alt="Flying Papers slide 7"></a>
</p>

### 7. FRANKY'S
奶油底、8-bit 像素字、黑白棋盘格面板，凑成滑板店柜台上那台复古游戏机。街头与滑雪潮牌电商适用，Palace、Polar 邻域。
<p>
  <a href="showcase/frankys/index.html"><img src="showcase/gallery/frankys/slide-0.png" width="32%" alt="FRANKY'S slide 0"></a>
  <a href="showcase/frankys/index.html"><img src="showcase/gallery/frankys/slide-4.png" width="32%" alt="FRANKY'S slide 4"></a>
  <a href="showcase/frankys/index.html"><img src="showcase/gallery/frankys/slide-7.png" width="32%" alt="FRANKY'S slide 7"></a>
</p>

### 8. General Intelligence Company
手绘插画配轻声的衬线显示字，95% 中性暖纸色板，篝火旁翻文学期刊的沉思气。AI 研究、创投、叙事品牌适用。
<p>
  <a href="showcase/general-intelligence-company/index.html"><img src="showcase/gallery/general-intelligence-company/slide-0.png" width="32%" alt="General Intelligence Company slide 0"></a>
  <a href="showcase/general-intelligence-company/index.html"><img src="showcase/gallery/general-intelligence-company/slide-4.png" width="32%" alt="General Intelligence Company slide 4"></a>
  <a href="showcase/general-intelligence-company/index.html"><img src="showcase/gallery/general-intelligence-company/slide-7.png" width="32%" alt="General Intelligence Company slide 7"></a>
</p>

### 9. Good Glyphs
两色系统撑起 288px 大字，类型即建筑，薄荷纸上的一张巨型慈善海报。慈善活动、展览与"版式即产品"的创意站点都用得上。
<p>
  <a href="showcase/good-glyphs/index.html"><img src="showcase/gallery/good-glyphs/slide-0.png" width="32%" alt="Good Glyphs slide 0"></a>
  <a href="showcase/good-glyphs/index.html"><img src="showcase/gallery/good-glyphs/slide-4.png" width="32%" alt="Good Glyphs slide 4"></a>
  <a href="showcase/good-glyphs/index.html"><img src="showcase/gallery/good-glyphs/slide-7.png" width="32%" alt="Good Glyphs slide 7"></a>
</p>

### 10. Henry
100% 单色，无阴影，靠全幅纸墨反转立版面，视觉强度全交给显示大字。暖奶油纸上的哥特宽边海报，作品集与杂志式编辑品牌适用。
<p>
  <a href="showcase/henry/index.html"><img src="showcase/gallery/henry/slide-0.png" width="32%" alt="Henry slide 0"></a>
  <a href="showcase/henry/index.html"><img src="showcase/gallery/henry/slide-4.png" width="32%" alt="Henry slide 4"></a>
  <a href="showcase/henry/index.html"><img src="showcase/gallery/henry/slide-7.png" width="32%" alt="Henry slide 7"></a>
</p>

### 11. Huddle
白纸打底，三种柔和粉彩状态卡把全部结构做完，奶油纸上码得整整齐齐的一叠库存卡。安静的目录式设计工作室、会员与社区启动页适用。
<p>
  <a href="showcase/huddle/index.html"><img src="showcase/gallery/huddle/slide-0.png" width="32%" alt="Huddle slide 0"></a>
  <a href="showcase/huddle/index.html"><img src="showcase/gallery/huddle/slide-4.png" width="32%" alt="Huddle slide 4"></a>
  <a href="showcase/huddle/index.html"><img src="showcase/gallery/huddle/slide-7.png" width="32%" alt="Huddle slide 7"></a>
</p>

### 12. Hyer Aviation
浅天蓝英雄区，187px 机身级标题，每页只放一块粘土色特写卡，座舱暮色下摊开的羊皮纸。奢华航空与高端服务品牌适用。
<p>
  <a href="showcase/hyer-aviation/index.html"><img src="showcase/gallery/hyer-aviation/slide-0.png" width="32%" alt="Hyer Aviation slide 0"></a>
  <a href="showcase/hyer-aviation/index.html"><img src="showcase/gallery/hyer-aviation/slide-4.png" width="32%" alt="Hyer Aviation slide 4"></a>
  <a href="showcase/hyer-aviation/index.html"><img src="showcase/gallery/hyer-aviation/slide-7.png" width="32%" alt="Hyer Aviation slide 7"></a>
</p>

### 13. IKEA
纯白底上，界面工作全部交给唯一一张黄色 CTA 卡面，阳光下的瑞典平板包装展厅。零售、电商与产品叙事的媒体主导首页适用。
<p>
  <a href="showcase/ikea/index.html"><img src="showcase/gallery/ikea/slide-0.png" width="32%" alt="IKEA slide 0"></a>
  <a href="showcase/ikea/index.html"><img src="showcase/gallery/ikea/slide-4.png" width="32%" alt="IKEA slide 4"></a>
  <a href="showcase/ikea/index.html"><img src="showcase/gallery/ikea/slide-7.png" width="32%" alt="IKEA slide 7"></a>
</p>

### 14. Lamanna
橙色满版，星爆徽章，硬切色谱地带，海报能量开到最大，那不勒斯人行道上的霓虹马戏帐篷。食品、烘焙、本地商业适用。
<p>
  <a href="showcase/lamanna/index.html"><img src="showcase/gallery/lamanna/slide-0.png" width="32%" alt="Lamanna slide 0"></a>
  <a href="showcase/lamanna/index.html"><img src="showcase/gallery/lamanna/slide-4.png" width="32%" alt="Lamanna slide 4"></a>
  <a href="showcase/lamanna/index.html"><img src="showcase/gallery/lamanna/slide-7.png" width="32%" alt="Lamanna slide 7"></a>
</p>

### 15. Leandra-isler
滩涂色渐变画布，字号从 14px 一路拉到 173px，没有容器 UI，像压进暖羊皮纸的干花。疗愈、单执业者、画廊式品牌的静谧仪式感适用。
<p>
  <a href="showcase/leandra-isler/index.html"><img src="showcase/gallery/leandra-isler/slide-0.png" width="32%" alt="Leandra-isler slide 0"></a>
  <a href="showcase/leandra-isler/index.html"><img src="showcase/gallery/leandra-isler/slide-4.png" width="32%" alt="Leandra-isler slide 4"></a>
  <a href="showcase/leandra-isler/index.html"><img src="showcase/gallery/leandra-isler/slide-7.png" width="32%" alt="Leandra-isler slide 7"></a>
</p>

### 16. Lpalo
Alfa Slab One 重磅大字在喊，蜡笔涂鸦撒了一地，暖桃纸上的儿童绘本跨页。口吻严肃，表达孩子气，播客与童趣创意社区适用。
<p>
  <a href="showcase/lpalo/index.html"><img src="showcase/gallery/lpalo/slide-0.png" width="32%" alt="Lpalo slide 0"></a>
  <a href="showcase/lpalo/index.html"><img src="showcase/gallery/lpalo/slide-4.png" width="32%" alt="Lpalo slide 4"></a>
  <a href="showcase/lpalo/index.html"><img src="showcase/gallery/lpalo/slide-7.png" width="32%" alt="Lpalo slide 7"></a>
</p>

### 17. Mercury
近黑玛瑙画布，石墨卡，全页只许一枚钴蓝胶囊 CTA，蓝调时刻的高山银行，电影级的克制。金融科技与暗色开发者工具适用。
<p>
  <a href="showcase/mercury/index.html"><img src="showcase/gallery/mercury/slide-0.png" width="32%" alt="Mercury slide 0"></a>
  <a href="showcase/mercury/index.html"><img src="showcase/gallery/mercury/slide-4.png" width="32%" alt="Mercury slide 4"></a>
  <a href="showcase/mercury/index.html"><img src="showcase/gallery/mercury/slide-7.png" width="32%" alt="Mercury slide 7"></a>
</p>

### 18. Monad
编辑衬线标题配等宽正文，数据管线图摆在页面中心，暖羊皮纸上的技术期刊。开发者工具与数据基础设施的文学性表达。
<p>
  <a href="showcase/monad/index.html"><img src="showcase/gallery/monad/slide-0.png" width="32%" alt="Monad slide 0"></a>
  <a href="showcase/monad/index.html"><img src="showcase/gallery/monad/slide-4.png" width="32%" alt="Monad slide 4"></a>
  <a href="showcase/monad/index.html"><img src="showcase/gallery/monad/slide-7.png" width="32%" alt="Monad slide 7"></a>
</p>

### 19. Monopo Saigon
极致黑白单色，225px 无衬线大字，只留一处熔岩虹彩英雄区，虹彩背后是编辑式的沉默。设计工作室与展廊式作品集适用。
<p>
  <a href="showcase/monopo-saigon/index.html"><img src="showcase/gallery/monopo-saigon/slide-0.png" width="32%" alt="Monopo Saigon slide 0"></a>
  <a href="showcase/monopo-saigon/index.html"><img src="showcase/gallery/monopo-saigon/slide-4.png" width="32%" alt="Monopo Saigon slide 4"></a>
  <a href="showcase/monopo-saigon/index.html"><img src="showcase/gallery/monopo-saigon/slide-7.png" width="32%" alt="Monopo Saigon slide 7"></a>
</p>

### 20. MotherDuck
暖奶油画布，等宽字体唱全部角色，按钮带硬偏移阴影，奶油纸上的一台蜡笔终端。"开发者工具拒绝像开发者工具"。
<p>
  <a href="showcase/motherduck/index.html"><img src="showcase/gallery/motherduck/slide-0.png" width="32%" alt="MotherDuck slide 0"></a>
  <a href="showcase/motherduck/index.html"><img src="showcase/gallery/motherduck/slide-4.png" width="32%" alt="MotherDuck slide 4"></a>
  <a href="showcase/motherduck/index.html"><img src="showcase/gallery/motherduck/slide-7.png" width="32%" alt="MotherDuck slide 7"></a>
</p>

### 21. ORYZO AI
暖胡桃黑底配奶油字，绿色切割垫照片做英雄区，排版守博物馆标签的规矩，一本暗房产品编辑志。硬件与单产品品牌的艺术品陈列适用。
<p>
  <a href="showcase/oryzo-ai/index.html"><img src="showcase/gallery/oryzo-ai/slide-0.png" width="32%" alt="ORYZO AI slide 0"></a>
  <a href="showcase/oryzo-ai/index.html"><img src="showcase/gallery/oryzo-ai/slide-4.png" width="32%" alt="ORYZO AI slide 4"></a>
  <a href="showcase/oryzo-ai/index.html"><img src="showcase/gallery/oryzo-ai/slide-7.png" width="32%" alt="ORYZO AI slide 7"></a>
</p>

### 22. Patch
电光靛蓝满版，标题激进压缩，标注全部编号化，制图纸上的一张电光蓝图。工程与机构型 B2B 启动页要下强声明，用它。
<p>
  <a href="showcase/patch/index.html"><img src="showcase/gallery/patch/slide-0.png" width="32%" alt="Patch slide 0"></a>
  <a href="showcase/patch/index.html"><img src="showcase/gallery/patch/slide-4.png" width="32%" alt="Patch slide 4"></a>
  <a href="showcase/patch/index.html"><img src="showcase/gallery/patch/slide-7.png" width="32%" alt="Patch slide 7"></a>
</p>

### 23. Raycast
近黑座舱里排开键帽式内阴影卡，一根珊瑚 accent 亮着，午夜指挥中心的配置。启动器与键盘优先的生产力工具适用。
<p>
  <a href="showcase/raycast/index.html"><img src="showcase/gallery/raycast/slide-0.png" width="32%" alt="Raycast slide 0"></a>
  <a href="showcase/raycast/index.html"><img src="showcase/gallery/raycast/slide-4.png" width="32%" alt="Raycast slide 4"></a>
  <a href="showcase/raycast/index.html"><img src="showcase/gallery/raycast/slide-7.png" width="32%" alt="Raycast slide 7"></a>
</p>

### 24. Seline Analytics
暖石画布，唯一一枚青色 CTA，标题只用 weight-400 细语，暖石桌上安静的统计员。分析与 B2B SaaS 场合，编辑式的自信。
<p>
  <a href="showcase/seline-analytics/index.html"><img src="showcase/gallery/seline-analytics/slide-0.png" width="32%" alt="Seline Analytics slide 0"></a>
  <a href="showcase/seline-analytics/index.html"><img src="showcase/gallery/seline-analytics/slide-4.png" width="32%" alt="Seline Analytics slide 4"></a>
  <a href="showcase/seline-analytics/index.html"><img src="showcase/gallery/seline-analytics/slide-7.png" width="32%" alt="Seline Analytics slide 7"></a>
</p>

### 25. Steep
超大斜体衬线标题，单张桃色引用卡，悬浮的产品卡，暖纸上一篇衬线排的分析文章。AI 与数据分析题材适用，杂志跨页的观感。
<p>
  <a href="showcase/steep/index.html"><img src="showcase/gallery/steep/slide-0.png" width="32%" alt="Steep slide 0"></a>
  <a href="showcase/steep/index.html"><img src="showcase/gallery/steep/slide-4.png" width="32%" alt="Steep slide 4"></a>
  <a href="showcase/steep/index.html"><img src="showcase/gallery/steep/slide-7.png" width="32%" alt="Steep slide 7"></a>
</p>

### 26. SuperHi Plus
双色满版面板左右换边（50/50），全站单字重 400，箭头导航，钴蓝蓝图上洒了 emoji 玻璃珠。学校、社区、产品发布的二元宣言适用。
<p>
  <a href="showcase/superhi-plus/index.html"><img src="showcase/gallery/superhi-plus/slide-0.png" width="32%" alt="SuperHi Plus slide 0"></a>
  <a href="showcase/superhi-plus/index.html"><img src="showcase/gallery/superhi-plus/slide-4.png" width="32%" alt="SuperHi Plus slide 4"></a>
  <a href="showcase/superhi-plus/index.html"><img src="showcase/gallery/superhi-plus/slide-7.png" width="32%" alt="SuperHi Plus slide 7"></a>
</p>

### 27. Superr
奶油纸上有马克笔橙批注、贴纸插图和小写圆软大字，午后暖光照着的一本校园笔记本。文具与趣味 D2C 适用，温暖手作感。
<p>
  <a href="showcase/superr/index.html"><img src="showcase/gallery/superr/slide-0.png" width="32%" alt="Superr slide 0"></a>
  <a href="showcase/superr/index.html"><img src="showcase/gallery/superr/slide-4.png" width="32%" alt="Superr slide 4"></a>
  <a href="showcase/superr/index.html"><img src="showcase/gallery/superr/slide-7.png" width="32%" alt="Superr slide 7"></a>
</p>

### 28. Syllabus
暖瓷白配紫黑墨，CTA 做成黄油色硬阴影贴纸，直角 0px 不让步，奶油纸杂志排进几何无衬线。编辑型科技落地页适用，印刷式的高级感。
<p>
  <a href="showcase/syllabus/index.html"><img src="showcase/gallery/syllabus/slide-0.png" width="32%" alt="Syllabus slide 0"></a>
  <a href="showcase/syllabus/index.html"><img src="showcase/gallery/syllabus/slide-4.png" width="32%" alt="Syllabus slide 4"></a>
  <a href="showcase/syllabus/index.html"><img src="showcase/gallery/syllabus/slide-7.png" width="32%" alt="Syllabus slide 7"></a>
</p>

### 29. Ventriloc
纸白画布，一点橙色余烬高光，非对称切角卡配等宽数据卡，暖纸上的数据天文台。可观测与金融数据平台适用，安静而精确。
<p>
  <a href="showcase/ventriloc/index.html"><img src="showcase/gallery/ventriloc/slide-0.png" width="32%" alt="Ventriloc slide 0"></a>
  <a href="showcase/ventriloc/index.html"><img src="showcase/gallery/ventriloc/slide-4.png" width="32%" alt="Ventriloc slide 4"></a>
  <a href="showcase/ventriloc/index.html"><img src="showcase/gallery/ventriloc/slide-7.png" width="32%" alt="Ventriloc slide 7"></a>
</p>

### 30. Wispr Flow
奶油宽边报与暗天鹅绒厅交替出场，四色页带轮换，厅室圆角开到 40-80px，正文 EB Garamond 400。语音与 AI 生产力工具适用，一册杂志的质感。
<p>
  <a href="showcase/wispr-flow/index.html"><img src="showcase/gallery/wispr-flow/slide-0.png" width="32%" alt="Wispr Flow slide 0"></a>
  <a href="showcase/wispr-flow/index.html"><img src="showcase/gallery/wispr-flow/slide-4.png" width="32%" alt="Wispr Flow slide 4"></a>
  <a href="showcase/wispr-flow/index.html"><img src="showcase/gallery/wispr-flow/slide-7.png" width="32%" alt="Wispr Flow slide 7"></a>
</p>

---
## 结构

```
design-taste-frontend/
├── SKILL.md                      # skill 主体（0.A-0.E + 1-16 章）
├── README.md                     # 本文件
├── manifest-schema.md            # P1.2 design-manifest.json schema
├── annotation-guide.md           # 素材标注词表 / 指引（P0.2）
├── brand-style-reference.md      # 30 套品牌官网风格学习报告（表现手法借鉴规则）
├── deploy-guide.md               # 部署规范（Vercel / 飞书妙搭，AI 代理执行手册）
├── reference/                    # 外置参考（触发式读取：动效骨架 / 设计系统安装命令 / canonical sources / liquid glass / 模式词汇表）
├── freeplay-declaration.md       # 自由发挥模式的自创风格声明模板
├── refero-styles/                # 30 套真实品牌素材（每套 DESIGN.md / tokens.json / variables.css / theme.css）
├── design-manifest.json          # 30 套选型 manifest（值层 + 审美标注，程序化生成可复跑）
├── metadata/                     # style-map.json（slug↔目录映射）+ 30 套标注 json
└── showcase/                     # 效果文件：30 套成品 deck + 图廊 + QA/生成/导出脚本 + 自托管字体
    ├── gallery/                  # 图廊（selection 预览页 + 每套 slide-0/4/7 预览截图）
    ├── fonts/                    # 自托管字体（fonts.css + woff2，不依赖 Google）
    ├── check-decks.py            # 行高 / 安全区自动校验（QA gate 2）
    ├── check-structure.py        # 中段表达族 / 结构趋同检查（QA gate 4）
    ├── check-values.py           # 值层 1:1 校验（QA gate 1）
    ├── build-index.py            # 重建 selection-index.json + gallery/index.html
    ├── build-manifest.py         # 重建 design-manifest.json（程序化提取 + 标注合并）
    ├── shot-all-slides.py / gallery-shots.py / export-pdf.py / export-pptx.py / fonts_*.py
    └── <slug>/                   # 每套成品 deck（index.html + qa.md；全量截图本地可再生、不入库）
```

## 主链路验证（克隆后即可复跑）

```bash
cd design-taste-frontend
python showcase/build-manifest.py --check   # manifest 30/30 完整
python showcase/build-index.py              # 重建 selection-index + 图廊
python showcase/check-decks.py steep        # 行高/安全区/胶囊校验（file:// 直读；需 playwright + Chrome）
python showcase/check-structure.py          # 中段结构反趋同检查（六类表达族，静态分析）
python showcase/shot-all-slides.py steep   # 重截该套全量截图到 showcase/steep/screenshots/（file:// 直读）
python -m http.server 8899                  # gallery-shots 前置（包根启动即可，脚本自动兼容 /showcase/ 前缀）
python showcase/gallery-shots.py steep      # 重截 gallery 预览（slide 0/4/7）
```

结构检查只查 DOM/CSS 里有没有兑现该套风格声明的中段结构信号，替代不了视觉相似度判断。截图仍要按 15.6 的视觉 QA 过目，通用的 `card`、`quote`、`stat` 脚手架不算风格证据。

## 导出 PDF / PPTX

deck 本体是 HTML，两条命令导出，传 slug 或 deck 目录路径都行。showcase 样品按 slug，产物在 `showcase/exports/`；你自己生成的 deck 直接传目录路径（包外任意含 index.html 的目录），产物落在 deck 旁边。

```bash
python showcase/export-pdf.py steep                # 样品 → showcase/exports/steep.pdf
python showcase/export-pptx.py path/to/your-deck   # 你的 deck → your-deck.pptx
```

deck 经 file:// 直读，不用起本地服务；deck 引用的 `../fonts/fonts.css` 按相对路径解析，从 `showcase/fonts/` 拷一份到 deck 同级即可（与部署暂存同结构）。PDF 是 1920×1080 每页一屏，1:1 不缩放；PPTX 逐页截图嵌入 16:9 幻灯片，浏览器里什么样，PPT 里就什么样。前置是 playwright + Chrome，PPTX 另需 `pip install python-pptx`。

导出文件体积大，仓库不带（`.gitignore` 已排除 `showcase/exports/`），需要时本地现导。其余内容全部随仓库分发，克隆即用。

## License

- **代码与文档**（SKILL.md、README、`showcase/` 脚本与生成的 deck HTML 等）：[MIT](LICENSE)。可用、可改、可商用，保留版权声明就行。
- **品牌素材**（`refero-styles/` 30 套设计 token、`brand-style-reference.md` 官网风格报告）：**style reference only — not affiliated**。品牌名、商标与品牌资产归各自所有者，本包不主张任何权利，这部分**不随 MIT 授权分发**，商用如需复刻特定品牌视觉请自行向品牌方确认。详见 `refero-styles/README.md`。
