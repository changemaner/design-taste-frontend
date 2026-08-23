# 标注指引 —— 风格元数据（P0.2）

> 用途：为 refero 素材库每一套风格产出 `metadata/<slug>.json`。
> 这些"审美判断"字段（mood/tone/formality/density/best_for/avoid_for/palette_voice/typographic_voice/signature_moves）
> 无法程序化提取，必须由人/子代理读 DESIGN.md 后标注。色板/字体/radii/spacing 由 build-manifest.py 程序化提取，不在这里标。
>
> 本指引保证多批次标注**词表一致**（反漂移），是全库 30 套标注质量的地基。

---

## 0. 输入与输出

- **输入**：`refero-styles/<风格目录>/DESIGN.md`（唯一事实源，看前 20 行的 style reference 定义 + Do's/Don'ts + Components）
- **输出**：`metadata/<slug>.json`，每套一个文件
- **格式范例**：`metadata/motherduck.json`（已完成，作为校准锚点；新标注必须与其字段结构完全一致）

## 1. 词表白名单（只准用这些词，不许近义替代）

### mood（视觉氛围/气质）— 每套 2-4 个，按第一印象排序

| 词 | 定义 | 示例风格 |
|---|---|---|
| airy | 大留白、轻盈、呼吸感 | 极简 SaaS 落地页 |
| editorial | 杂志式、强文字排版、编辑感 | Steep, Flying Papers |
| playful | 俏皮、童趣、好玩 | MotherDuck |
| technical | 技术感、开发者工具、数据密集 | Raycast, Monad, Composer |
| industrial | 工业/粗粝/工程感 | 航空、硬件品牌 |
| organic | 有机、自然、手绘、不规则 | 手工作坊、插画品牌 |
| retro | 复古、怀旧、时代感 | 老派包装、zine |
| futuristic | 未来感、科幻、科技先锋 | 硬件/AI 先锋品牌 |
| minimal | 极简、克制、少即是多 | IKEA, Superr |
| warm | 温暖、亲切、暖调 | IKEA, Anthropic |
| bold | 大胆、高对比、冲击力 | 宣言式海报 |
| quiet | 安静、低语、内敛 | 高端数据分析 |
| chromatic | 多彩、饱和、鲜艳 | 创意工作室、社区品牌 |
| monochrome | 单色、黑白、严肃 | 咨询、企业 |
| luxurious | 奢华、精致、高级 | 时尚、酒店 |
| brutalist | 粗野主义、neo-brutalist、近直角 | MotherDuck, Monad |

### tone（性格语气/voice）— 每套 2-3 个

| 词 | 定义 |
|---|---|
| playful | 俏皮 |
| confident | 自信、笃定 |
| friendly | 友好、亲切 |
| authoritative | 权威、专家 |
| quirky | 古怪、独特 |
| calm | 平静、沉稳 |
| energetic | 活力、动感 |
| premium | 高级、品质 |
| casual | 随意、轻松 |
| rebellious | 反叛、不羁 |
| approachable | 平易近人 |
| refined | 精炼、考究 |

### formality / density / scheme — 固定三档

- `formality`: `low` / `medium` / `high`
- `density`: **直接抄素材 DESIGN.md 顶部的 Density 标注原词**（`spacious` / `comfortable` / `compact`）——不映射、不转换。素材标什么就是什么（素材已提供的信息优先直接用）。
- `scheme`: `light` / `dark` / `mixed`（直接读 DESIGN.md 顶部 theme 字段；若素材明确写 `mixed`（如 Henry），如实填 `mixed`，不硬归 light/dark）

## 2. 字段填写规范

| 字段 | 怎么填 |
|---|---|
| `tagline` | 直接抄 DESIGN.md 第 2-3 行的 style reference 定义（一句话），不要重写 |
| `mood[]` | 从白名单选 2-4 个，按第一印象排序 |
| `tone[]` | 从白名单选 2-3 个 |
| `formality/density/scheme` | 按第 1 节三档 |
| `palette_voice` | 一句：底色 + 结构色 + 强调色 + 色彩用途规则（谁承担动作、谁只做装饰） |
| `typographic_voice` | 一句：主字体角色（显示/正文/micro）+ 字重/字距气质 + 禁用什么（衬线/斜体…） |
| `signature_moves[]` | 2-5 个：本套签名动作（每套 1 句规格 + 承担什么），直接从 Components/Do's 提炼 |
| `best_for` | 一段：适合什么场景（具体到用途/受众/类型） |
| `avoid_for` | 一段：不适合什么场景（对照 best_for 的反面，具体可验证） |
| `source` | 路径 + DESIGN.md 顶部的 theme + 关键值层（leading_body / radius / shadow） |

> **已知素材例外（标注时注意）**：
> - `General Intelligence Company` / `Good Glyphs` 的 variables.css **没有 `--leading-body`**（只有 caption/subheading/display）。回退规则：用 DESIGN.md 正文规范的行高值（GIC=1.5、Good Glyphs=1.5），并在 source.leading_body 注明"fallback，无 --leading-body"。
> - `Flying Papers` 的 `--leading-body: 1` 是**真实值**（漫画海报超紧凑行高），不是错误，如实填 1.0。
> - `Your workplace has the answer.`（Dala）DESIGN.md 顶部**无 Density 字段**，按布局文字判定：`spacious`（"spacious two-column rhythm… no panels, borders, or cards"）。
> - `Lamanna` 的 variables.css **无 `--leading-body`**，只有 `--leading-body-sm: 1`（body-sm 18px 行高 1.0）。DESIGN.md 文字另有正文 22px/1.67 角色（无 token）。回退规则：source.leading_body 用 **token 真实值 1.0**，并在 leading_note 注明分歧（生成时以 1.0 为契约锚点）。

## 3. 标注流程

1. 读 `DESIGN.md` 开头 3 行 style reference（定义整段声音）+ 底部 Theme 字段
2. 读 Do's/Don'ts（锁定色彩/字体/形状的硬约束）
3. 读 Components（提炼 signature_moves）
4. 填 `palette_voice` / `typographic_voice`（这是生成纪律的 Style Read 来源）
5. 写 `best_for` / `avoid_for`
6. 从白名单选 mood / tone；**选不出就用现有词里最接近的**，不要自造近义词

## 4. 反漂移规则（关键）

- mood/tone **只允许**白名单词；想加新词 → 先提出到本表（记一个待定项），不要就地造词
- 同一风格的情绪判断以 DESIGN.md 定义为准，**不要凭 deck 成品/截图**（成品可能没做全，DESIGN.md 才是事实源）
- `best_for`/`avoid_for` 要具体（"开发者工具/数据基建落地页"），不要空泛（"适合科技公司"）
- 标注完成度：每套字段全填，缺一个都算不完整

---

## 5. 已完成范例（校准锚点）

`metadata/motherduck.json` —— 字段结构、mood/tone 用法、palette/typographic voice 写法，均按本指引。新标注以它为参照。
