# design-manifest.json Schema（P1.2 定稿）

> 唯一事实源：`design-manifest.json`（由 `scripts/build-manifest.py` 生成，30 套全量）。
> 本 schema 同时服务"选型（selection）"与"生成前 Style Read（style_read）"，与 skill 15/16 章语言对齐。
>
> 数据来源分工（关键）：
> - `value_layer` = **程序化提取**（build-manifest.py 从 tokens.json 提取，值层契约，生成时 1:1）
> - `style_read` / `selection` = **子代理标注**（metadata/<slug>.json，审美判断）
> - `source` = 溯源 + 值层回退记录（来自 metadata 标注的 source）

---

## 顶层结构

```jsonc
{
  "version": "1",
  "styles": {
    "<slug>": {
      "slug": "motherduck",
      "name": "MotherDuck",
      "tagline": "Crayon-coded terminal on cream paper ...",
      "value_layer": { ... },   // 程序化提取（tokens.json）
      "style_read": { ... },    // 审美标注（palette/typographic voice + signature）
      "selection": { ... },     // 选型字段（mood/tone/formality/density/scheme/best/avoid）
      "source": { ... }         // 溯源 + 值层回退记录
    }
  }
}
```

## 字段明细

### value_layer（程序化，值层契约）

| 键 | 来源 tokens.json 分组 | 说明 |
|---|---|---|
| `palette` | `color` | token名 -> hex 色值 |
| `fonts` | `font` | token名 -> 字体名 |
| `radii` | `radius` | token名 -> 尺寸（如 `sm: 2px`）；**缺省**：Lamanna/Syllabus 无 radius 分组 |
| `spacing` | `spacing` | token名 -> 尺寸 |
| `surfaces` | `surface` | token名 -> 色值 |
| `shadows` | `shadow` | token名 -> 阴影串（如 `rgb(56,56,56) -6px 6px 0px 0px`）；**缺省**：无 shadow 系统的套 |

> 值层 = 素材契约，生成时**必须 1:1**（15.3）。只有 radius/shadows 可缺省（缺省套由 DESIGN.md/variables.css 兜底）。

### style_read（审美标注，喂生成纪律）

| 键 | 说明 |
|---|---|
| `palette_voice` | 一段：底色/结构色/强调色 + 色彩用途规则（谁承担动作、谁只做装饰） |
| `typographic_voice` | 一段：主字体角色 + 字重/字距气质 + 禁用项 |
| `signature_moves` | 2-5 个签名动作（每个一句规格 + 用途） |

### selection（选型字段）

| 键 | 取值 |
|---|---|
| `mood` | 白名单词 2-4 个（technical/editorial/playful/warm/... 见 annotation-guide） |
| `tone` | 白名单词 2-3 个 |
| `formality` | low / medium / high |
| `density` | **素材原词** spacious / comfortable / compact（不映射） |
| `scheme` | light / dark / mixed |
| `best_for` | 一段，具体场景 |
| `avoid_for` | 一段，反面对照 |

### source（溯源 + 回退）

| 键 | 说明 |
|---|---|
| `path` | 素材目录相对路径（`refero-styles/<目录名>/`） |
| `theme` | DESIGN.md 顶部 Theme |
| `leading_body` | 正文行高契约值（来自 variables.css `--leading-body`；无该 token 的套用回退值） |
| `leading_note` | （可选）值层回退/分歧说明 |
| `radius` / `shadow` | DESIGN.md 的圆角/阴影规范（供生成兜底） |

## 已知例外（30 套内）

- **缺 radius 分组**：Lamanna / Syllabus
- **无 `--leading-body` token**：General Intelligence Company / Good Glyphs / Lamanna / Hyer Aviation / Seline Analytics / Ventriloc（回退值 + leading_note 注明，见各套 metadata/source）
- **无 Density 字段**：Your workplace has the answer.（Dala）→ 按布局文字判 spacious
- **Density 字段与布局文字矛盾**：Raycast（顶部 comfortable，Layout 段写 spacious，以顶部字段为准）
