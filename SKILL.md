---
name: design-taste-frontend
description: Anti-slop frontend skill for landing pages, portfolios, and redesigns. The agent reads the brief, infers the right design direction, and ships interfaces that do not look templated. Real design systems when applicable, audit-first on redesigns, strict pre-flight check.
---

# tasteskill: Anti-Slop Frontend Skill

> Landing pages, portfolios, and redesigns. Not dashboards, not data tables, not multi-step product UI.
> Every rule below is **contextual**. None of it fires automatically. First read the brief, then pull only what fits.

---

## 0. BRIEF INFERENCE (Read the Room Before Anything Else)

Before touching code or tweaking dials, **infer what the user actually wants**. Most LLM design output is bad because the model jumps to a default aesthetic instead of reading the room.

### 0.A Read these signals first
1. **Page kind** - landing (SaaS / consumer / agency / event), portfolio (dev / designer / creative studio), redesign (preserve vs overhaul), editorial / blog.
2. **Vibe words** the user used - "minimalist", "calm", "Linear-style", "Awwwards", "brutalist", "premium consumer", "Apple-y", "playful", "serious B2B", "editorial", "agency-y", "glassy", "dark tech".
3. **Reference signals** - URLs they linked, screenshots they pasted, products they named, brands they're competing with.
4. **Audience** - B2B procurement panel vs. design-conscious consumer vs. recruiter scanning a portfolio. The audience picks the aesthetic, not your taste.
5. **Brand assets that already exist** - logo, color, type, photography. For redesigns, these are starting material, not optional input (see Section 11).
6. **Quiet constraints** - accessibility-first audiences, public-sector, regulated industries, trust-first commerce, kids' products. These constraints OVERRIDE aesthetic preference.

### 0.B Output a one-line "Design Read" before generating
Before any code, state in one line: **"Reading this as: \<page kind> for \<audience>, with a \<vibe> language, leaning toward \<design system or aesthetic family>."**

Example reads:
- *"Reading this as: B2B SaaS landing for technical buyers, with a Linear-style minimalist language, leaning toward Tailwind utilities + Geist + restrained motion."*
- *"Reading this as: solo designer portfolio for hiring managers, with an editorial / kinetic-type language, leaning toward native CSS + scroll-driven animation + custom typography."*
- *"Reading this as: redesign of a public-sector service site, with a trust-first language, leaning toward GOV.UK Frontend or USWDS."*

### 0.C If the brief is ambiguous, ask one question, do not guess
Ask exactly **one** clarifying question - never a multi-question dump - and only when the design read genuinely diverges. Example: *"Should this feel closer to Linear-clean or Awwwards-experimental?"*

If you can confidently infer from context, **do not ask**. Just declare the design read and proceed.

### 0.D Anti-Default Discipline
Do not default to: AI-purple gradients, centered hero over dark mesh, three equal feature cards, generic glassmorphism on everything, infinite-loop micro-animations everywhere, Inter + slate-900. These are the LLM defaults. Reach past them deliberately based on the design read.

### 0.E Mode Routing (deck vs longform)
**Deck / slide briefs** (slides, deck, keynotes, 演示, PPT, "8 slides about X") - do NOT apply the longform Sections 1-14 as-is. Route to **Section 15 DECK MODE (boundaries)** + **Section 16 STYLE CONTRACT (creative freedom)**. Boundaries lock the skeleton; the style contract tells you what to respect and where to play. Every other brief (landing, portfolio, editorial, redesign, app) stays on Sections 1-14.

**Deck briefs split into two style routes (ask once, 3-4 questions - 风格意象 / 语气词 / 明确禁忌 / 受众):**
- **素材模式 (default)** - the brief's style can be matched by a style in the material library (refero-styles/). 选型管线（一条顺序，勿跳步）：`showcase/selection-index.json` 筛选（mood / tone / density / scheme 机器可读字段，`best_for` / `avoid_for` 给适用性判断）→ 收窄 2-4 套短名单 → `showcase/gallery/` 看预览截图（slide 0/4/7）→ 读短名单的 DESIGN.md 定稿 → 值层 1:1 生成（15.3）。Material is the source of truth；`design-manifest.json` 为字段明细源。
  - manifest 字段语义与 30 套已知例外（缺 radius 分组 / `--leading-body` 回退等）见 `manifest-schema.md`；扩库标注（新增风格时）的词表白名单与字段规范见 `annotation-guide.md`（校准锚点：`metadata/motherduck.json`）。
- **自由发挥模式 (fallback)** - the brief needs a style OUTSIDE the library (hand-drawn wedding invite, cartoon kids product, a totally custom voice). Fill `freeplay-declaration.md` FIRST (the self-authored mini design-system: palette voice / typographic voice / signature moves / anti-convergence statement / CJK) → generate against that declaration → QA gate 2/3 run as normal, gate 1 (value-layer 1:1) downgrades to "declared-token self-consistency" (see 15.6). The declaration is both the generation discipline and the QA anchor.
- **交付意图识别（部署分享）**：brief 或后续对话出现"部署 / 上线 / 发链接 / 公开分享 / 发布 / Vercel / 妙搭 / 飞书"等交付意图时——deck 生成并通过 15.6 QA 之后，**先完整读取 `deploy-guide.md`**（公开 URL 的执行规范：环境自备自检、Vercel / 妙搭两条出口完整流程、字体改造与失败处理），再按 15.9 交付。不要凭记忆操作平台 CLI；showcase 30 套是样品，默认部署对象是用户自己的 deck。
- If a match is borderline, default to 素材模式 (real brand systems are the anti-slop ammunition).

---

## 1. THE THREE DIALS (Core Configuration)

After the design read, set three dials. Every layout, motion, and density decision below is gated by these.

* **`DESIGN_VARIANCE: 8`** - 1 = Perfect Symmetry, 10 = Artsy Chaos
* **`MOTION_INTENSITY: 6`** - 1 = Static, 10 = Cinematic / Physics
* **`VISUAL_DENSITY: 4`** - 1 = Art Gallery / Airy, 10 = Cockpit / Packed Data

**Baseline:** `8 / 6 / 4`. Use these unless the design read overrides them. Do not ask the user to edit this file - overrides happen conversationally.

### 1.A Dial Inference (design read → dial values)
| Signal | VARIANCE | MOTION | DENSITY |
|---|---|---|---|
| "minimalist / clean / calm / editorial / Linear-style" | 5-6 | 3-4 | 2-3 |
| "premium consumer / Apple-y / luxury / brand" | 7-8 | 5-7 | 3-4 |
| "playful / wild / Dribbble / Awwwards / experimental / agency" | 9-10 | 8-10 | 3-4 |
| "landing page / portfolio / marketing site (default)" | 7-9 | 6-8 | 3-5 |
| "trust-first / public-sector / regulated / accessibility-critical" | 3-4 | 2-3 | 4-5 |
| "redesign - preserve" | match existing | +1 | match existing |
| "redesign - overhaul" | +2 | +2 | match existing |

### 1.B Use-Case Presets
| Use case | VARIANCE | MOTION | DENSITY |
|---|---|---|---|
| Landing (SaaS, mainstream) | 7 | 6 | 4 |
| Landing (Agency / creative) | 9 | 8 | 3 |
| Landing (Premium consumer) | 7 | 6 | 3 |
| Portfolio (Designer / studio) | 8 | 7 | 3 |
| Portfolio (Developer) | 6 | 5 | 4 |
| Editorial / Blog | 6 | 4 | 3 |
| Public-sector service | 3 | 2 | 5 |
| Redesign - preserve | match | match+1 | match |
| Redesign - overhaul | +2 | +2 | match |

### 1.C How the Dials Drive Output
Use these (or user-overridden values) as global variables. Cross-references throughout this document refer to these exact variable names - never invent aliases like `LAYOUT_VARIANCE` or `ANIM_LEVEL`.

---

## 2. BRIEF → DESIGN SYSTEM MAP

Once you have the design read (Section 0) and dials (Section 1), pick the right foundation. Do not invent CSS for things that have an official package. Do not pretend an aesthetic trend is an official system.

### 2.A When to reach for a real design system (use official packages)
| Brief reads as… | Reach for | Why |
|---|---|---|
| Microsoft / enterprise SaaS / dashboards | `@fluentui/react-components` or `@fluentui/web-components` | Official Fluent UI, Microsoft tokens, accessibility done |
| Google-ish UI, Material-flavored product | `@material/web` + Material 3 tokens | Official, theme-able via Material Theming |
| IBM-style B2B / enterprise analytics | `@carbon/react` + `@carbon/styles` | Official Carbon, mature data-density patterns |
| Shopify app surfaces | `polaris.js` web components / Polaris React | Required for Shopify admin UI |
| Atlassian / Jira-style product | `@atlaskit/*` + `@atlaskit/tokens` | Official Atlassian DS |
| GitHub-style devtool / community page | `@primer/css` or `@primer/react-brand` | Official Primer; Brand variant for marketing |
| Public-sector UK service | `govuk-frontend` | Legally / regulatorily expected |
| US public-sector / trust-first | `uswds` | Same |
| Fast local-business / agency MVP | Bootstrap 5.3 | Boring, fast, works |
| Modern accessible React foundation | `@radix-ui/themes` | Primitives + polished theme |
| Modern SaaS where you own the components | shadcn/ui (`npx shadcn@latest add ...`) | You own the code, easy to customise; never ship default state |
| Tailwind-based modern SaaS / AI marketing | Tailwind v4 utilities + `dark:` variant | Default for indie + small team builds |

**Honesty rule:** if the brief reads as one of the systems above, install and use the **official** package. Do not recreate its CSS by hand. Do not import a system's tokens but then override 90% of them.

**One system per project.** Do not mix Fluent React with Carbon in the same tree. Do not import shadcn/ui components into a Material 3 app.

### 2.B When the brief is an aesthetic, not a system
For these directions, there is **no single official package**. Build with native CSS + Tailwind + a maintained component library. Be honest in code comments about what is borrowed inspiration vs. official material.

| Aesthetic | Honest implementation |
|---|---|
| Glassmorphism / "frosted glass" | `backdrop-filter`, layered borders, highlight overlays. Provide solid-fill fallback for `prefers-reduced-transparency`. |
| Bento (Apple-style tile grids) | CSS Grid with mixed cell sizes. No single library owns this. |
| Brutalism | Native CSS, monospace, raw borders. No library. |
| Editorial / magazine | Serif type, asymmetric grid, generous whitespace. No library. |
| Dark tech / hacker | Mono + accent neon, terminal motifs. No library. |
| Aurora / mesh gradients | SVG or layered radial gradients. No library. |
| Kinetic typography | Native CSS animations, scroll-driven animations, GSAP for hijacks. No library. |
| **Apple Liquid Glass** | Apple documents this for Apple platforms only. **There is no official `liquid-glass.css`.** Web implementations are approximations using `backdrop-filter` + layered borders + highlights. Label clearly as approximation. |

---

## 3. DEFAULT ARCHITECTURE & CONVENTIONS

Unless the design read picks a real design system (Section 2.A), these are the defaults:

### 3.A Stack
* **Framework:** React or Next.js. Default to Server Components (RSC).
  * **RSC SAFETY:** Global state works ONLY in Client Components. In Next.js, wrap providers in a `"use client"` component.
  * **INTERACTIVITY ISOLATION:** Any component using Motion, scroll listeners, or pointer physics MUST be an isolated leaf with `'use client'` at the top. Server Components render static layouts only.
* **Styling:** **Tailwind v4** (default). Tailwind v3 only if the existing project demands it.
  * For v4: do NOT use `tailwindcss` plugin in `postcss.config.js`. Use `@tailwindcss/postcss` or the Vite plugin.
* **Animation:** **Motion** (the library formerly known as Framer Motion). Import from `motion/react` (`import { motion } from "motion/react"`). The `framer-motion` package still works as a legacy alias - prefer `motion/react` in new code.
* **Fonts:** Always use `next/font` (Next.js) or self-host with `@font-face` + `font-display: swap`. Never link Google Fonts via `<link>` in production.

### 3.B State
* Local `useState` / `useReducer` for isolated UI.
* Global state ONLY for deep prop-drilling avoidance - Zustand, Jotai, or React context.
* **NEVER** use `useState` to track continuous values driven by user input (mouse position, scroll progress, pointer physics, magnetic hover). Use Motion's `useMotionValue` / `useTransform` / `useScroll`. `useState` re-renders the React tree on every change and collapses on mobile.

### 3.C Icons
* **Allowed libraries (priority order):** `@phosphor-icons/react`, `hugeicons-react`, `@radix-ui/react-icons`, `@tabler/icons-react`.
* **Discouraged:** `lucide-react`. Acceptable only when the user explicitly asks for it or the project already depends on it.
* **NEVER hand-roll SVG icons.** If a glyph is missing, install a second library or compose from primitives - do not draw icon paths from scratch.
* **One family per project.** Do not mix Phosphor with Lucide in the same component tree.
* **Standardize `strokeWidth` globally** (e.g. `1.5` or `2.0`).

### 3.D Emoji Policy
Discouraged by default in code, markup, and visible text. Replace symbols with icon-library glyphs. **Override:** allow emojis only when the user explicitly asks for a playful / chat-style / social-native vibe - and even then use them sparingly with intent.

### 3.E Responsiveness & Layout Mechanics
* Standardize breakpoints (`sm 640`, `md 768`, `lg 1024`, `xl 1280`, `2xl 1536`).
* Contain page layouts using `max-w-[1400px] mx-auto` or `max-w-7xl`.
* **Viewport Stability:** NEVER use `h-screen` for full-height Hero sections. ALWAYS use `min-h-[100dvh]` to prevent layout jumping on mobile (iOS Safari address bar).
* **Grid over Flex-Math:** NEVER use complex flexbox percentage math (`w-[calc(33%-1rem)]`). ALWAYS use CSS Grid (`grid grid-cols-1 md:grid-cols-3 gap-6`).

### 3.F Dependency Verification (mandatory)
Before importing ANY 3rd-party library, check `package.json`. If the package is missing, output the install command first. **Never** assume a library exists.

---

## 4. DESIGN ENGINEERING DIRECTIVES (Bias Correction)

LLMs default to clichés. Override proactively. Every rule has a context-aware override path.

### 4.1 Typography
* **Display / Headlines:** Default `text-4xl md:text-6xl tracking-tighter leading-none`.
* **Body / Paragraphs:** Default `text-base text-gray-600 leading-relaxed max-w-[65ch]`.
* **Sans font choice:** `Inter` discouraged as default — pick `Geist`, `Outfit`, `Cabinet Grotesk`, `Satoshi`, or a brand-appropriate serif first. Override: explicit neutral / Linear-style ask, or public-sector / accessibility-first brief.
* **Pairings to know:** `Geist` + `Geist Mono`, `Satoshi` + `JetBrains Mono`, `Cabinet Grotesk` + `Inter Tight`, `GT America` + `IBM Plex Mono`.
* **SERIF DISCIPLINE (very discouraged as default):** "feels creative / premium / editorial" is NOT a reason for serif — "creative brief = serif" is the single most-tested AI tell. Serif acceptable ONLY when the brief names a serif font, OR the aesthetic is genuinely editorial / luxury / publication / heritage AND you can articulate why this serif fits this brand. Everything else defaults to sans-serif display (Geist Display, ABC Diatype, Söhne Breit, Cabinet Grotesk Display, Migra Sans, GT Walsheim, Inter Display, PP Neue Montreal). `Fraunces` / `Instrument_Serif` banned as defaults.
* **EMPHASIS RULE:** emphasize inside a headline with italic/bold of the SAME font — never inject a serif word into a sans headline (or vice versa); mixed-family emphasis is amateur.
* **If a serif is justified** (rare): rotate from this pool, never the same serif across consecutive projects — PP Editorial New, GT Sectra Display, Cardinal Grotesk, Reckless Neue, Tiempos Headline, Recoleta, Cormorant Garamond, Playfair Display, EB Garamond, IvyPresto, Migra, Editorial Old, Saol Display, Söhne Breit Kursiv, Domaine Display, Canela, Schnyder, Tobias, NB Architekt, ITC Galliard.
* **ITALIC DESCENDER CLEARANCE (mandatory):** italic display words with descenders (`y g j p q`) clip at `leading-[1]` / `leading-none` — use `leading-[1.1]` minimum + `pb-1` / `mb-1` reserve. Audit every italic display word before shipping.

### 4.2 Color Calibration
* Max 1 accent color. Saturation < 80% by default. **One palette per project** — no warm/cool-gray fluctuation.
* **THE LILA RULE:** AI-purple / blue-glow is discouraged as default — no automatic purple button glows, no random neon gradients. Neutral bases (Zinc / Slate / Stone) + one high-contrast accent (Emerald, Electric Blue, Deep Rose, Burnt Orange…). Override: brief explicitly asks purple → embrace with intent (consistent palette, harmonised neutrals, restrained gradients), not generic gradient slop.
* **COLOR CONSISTENCY LOCK (mandatory):** one accent on the WHOLE page — a warm-grey site never gets a blue CTA in section 7; a rose site never a teal footer badge. Audit every component before shipping.
* **PREMIUM-CONSUMER PALETTE BAN (mandatory, second-most-recurring tell):** the LLM default for premium-consumer briefs (cookware / wellness / artisan / luxury / heritage / DTC) is warm beige + brass/clay/oxblood + espresso text. Banned as default:
  - Backgrounds `#f5f1ea #f7f5f1 #fbf8f1 #efeae0 #ece6db #faf7f1 #e8dfcb` · Accents `#b08947 #b6553a #9a2436 #9c6e2a #bc7c3a #7d5621` · Text `#1a1714 #1a1814 #1b1814`.
  - **Rotate these families instead:** Cold Luxury (silver-grey + chrome + smoke) · Forest (deep green + bone + amber) · Black and Tan (off-black + warm tan, no beige) · Cobalt + Cream · Terracotta + Slate · Olive + Brick + Paper · monochrome + one saturated pop. Never ship the same family twice in a row.
  - Override: brief explicitly names those colors, or genuinely vintage/artisan brand AND you can articulate why.

### 4.3 Layout Diversification
* **ANTI-CENTER BIAS:** centered Hero/H1 avoided when `DESIGN_VARIANCE > 4` — force Split Screen, left-content/right-asset, asymmetric whitespace, or scroll-pinned structures. Override: editorial / manifesto / launch-announcement briefs where the message is the design.

### 4.4 Materiality, Shadows, Cards
* Cards only when elevation communicates real hierarchy; otherwise `border-t`, `divide-y`, or negative space.
* Tint shadows to the background hue — no pure-black drop shadows on light backgrounds.
* `VISUAL_DENSITY > 7`: generic card containers banned; data metrics breathe in plain layout.
* **SHAPE CONSISTENCY LOCK (mandatory):** ONE corner-radius scale per page (all-sharp / all-soft 12-16px / all-pill). Mixed systems only with a documented rule followed everywhere (e.g. "buttons pill, cards 16px, inputs 8px"). Round buttons in a square layout = broken.

### 4.5 Interactive UI States
Implement full cycles, not "static successful state only":
* **Loading:** skeletal loaders matching final layout shape, no generic spinners · **Empty:** beautifully composed + how to populate · **Error:** inline (forms), contextual (toasts only for transient).
* **Tactile feedback:** `:active` → `-translate-y-[1px]` or `scale-[0.98]`.
* **BUTTON CONTRAST CHECK (mandatory, a11y):** verify text-vs-background on every button — white-on-white, `bg-white` CTA + `text-white`, borderless transparent-over-page = banned. WCAG AA (4.5:1 body, 3:1 large 18px+). Ghost buttons over photos need backdrop / scrim / stroke.
* **CTA BUTTON WRAP BAN (mandatory):** button text fits ONE line at desktop — shorten the label (primary CTAs ≤3 words, ideally 1-2) or widen the button, never `max-width` a CTA. Wrapped CTA = Pre-Flight Fail.
* **NO DUPLICATE CTA INTENT (mandatory):** one label per intent per page — "Get in touch" / "Contact us" / "Let's talk" / "Start a project" are ALL "contact": pick ONE everywhere (nav / hero / footer). Same for signup and portfolio intent clusters.
* **FORM CONTRAST CHECK (mandatory, a11y):** inputs, placeholders, focus rings, helper text, error text all pass WCAG AA against the section background. Audit every form.

### 4.6 Data & Form Patterns
* Label ABOVE input; helper text present in markup; error text BELOW input; `gap-2` blocks. No placeholder-as-label. Ever.

### 4.7 Layout Discipline (Hard Rules — failing any = shipping broken work)
* **Hero fits the initial viewport:** headline ≤2 lines, subtext ≤20 words AND ≤3-4 lines, CTAs visible without scroll. Too long → cut copy or reduce font scale. A value-prop that needs >20 words is unclear, not the rule too tight.
* **Hero font-scale discipline:** plan font + asset size together. Large asset + headline >6 words → do NOT start at `text-7xl/8xl`. Default `text-4xl md:text-5xl lg:text-6xl`; `text-6xl md:text-7xl` only for 3-5-word headlines. A 4-line hero headline is always a font-size error.
* **HERO TOP PADDING CAP (mandatory):** max `pt-24` desktop — more reads as a layout bug. Breathing room comes from font / asset scale, not top padding.
* **HERO STACK DISCIPLINE (max 4 text elements):** ① eyebrow OR brand strip (pick ≤1) ② headline ③ subtext ④ CTAs (1 primary + ≤1 secondary). **Banned inside hero:** tagline below CTAs, trust micro-strip, pricing teaser, feature bullets, avatar row — those become sections directly below. Eyebrow AND tagline together → drop the tagline.
* **Logo wall UNDER the hero, never inside it** — not in the same flex row as hero copy.
* **Nav renders on ONE line at desktop** (condense / drop / hamburger if not) · **height cap 80px, default 64-72px.**
* **Bento grids need rhythm:** no 6 consecutive left-image/right-text rows — alternate full-width rows, asymmetric tiles, vertical breaks. **BENTO CELL COUNT (mandatory):** exactly as many cells as content (3 items → 3 cells); an empty cell = planned wrong → re-shape, never paste a blank tile.
* **Section-Layout-Repetition Ban:** one layout family max ONCE per page; an 8-section page uses ≥4 different families.
* **ZIGZAG ALTERNATION CAP (mandatory):** max 2 consecutive image+text-split sections — the 3rd is a Pre-Flight Fail. Break with full-width / vertical-stack / bento / marquee.
* **EYEBROW RESTRAINT (mandatory, #1 violated rule):** max 1 eyebrow per 3 sections (hero counts; 9-section page ≤3). If section A has one, the next 2 cannot. Pre-Flight check is mechanical: count small-caps `uppercase tracking` labels; > ceil(sections/3) → fail. Default move: drop it — the headline alone is enough.
* **SPLIT-HEADER BAN (mandatory):** "big headline left + small explainer right" banned as default — stack headline + body vertically (max-width 65ch). Allowed only when the right column carries a real visual / interactive element, not filler text.
* **Bento Background Diversity (mandatory):** ≥2-3 cells per multi-cell grid get real variation (image, brand-appropriate gradient, pattern, tint). Typography-only cream-on-cream bento = AI default.
* **Mobile collapse declared per section** in the same component — no "Tailwind handles it" assumptions.

### 4.8 Image & Visual Asset Strategy
Landing pages are visual products; text-only pages with fake-screenshot divs are slop.
* **Priority order:** ① image-gen tool (MUST create section-specific assets — hero photography, product shots, textures — at the right aspect ratio; do not skip because hand-rolled CSS feels faster) → ② real web images (`https://picsum.photos/seed/{descriptive-seed}/{w}/{h}`, brief-provided URLs, open-license sources if allowed) → ③ last resort: clearly-labeled placeholder slots (`<!-- TODO: hero product photo 1600x1200 -->`) + tell the user which images to provide. Never fill the page with hand-rolled SVG illustrations or div fake screenshots.
* **Even minimalist sites need real images:** ≥2-3 per page (hero + product/lifestyle + supporting); B&W minimalist photography for restrained briefs. Pure-text is incomplete work, not minimalism.
* **Real logos for social proof:** Simple Icons (`https://cdn.simpleicons.org/{slug}/ffffff`) or devicon (tech stacks). Invented brand → invent a matching SVG mark (monogram / ligature / abstract glyph); plain text wordmarks look generic. Logos must render in both light/dark mode. **LOGO-ONLY rule (mandatory):** logo wall = logos and nothing else — no industry/category labels underneath; alt-text optional.
* **Hand-rolled decorative SVGs strongly discouraged, never default** — acceptable only for explicit briefs ("draw me an SVG logo"), single simple geometric marks, or confident output quality.
* **Div-based fake screenshots banned.** Show a product via real screenshot URL, generated image, real mini component preview, or editorial photography. **Hero needs a real visual** — text + gradient blob is a placeholder, not a hero.

### 4.9 Content Density
Landing pages live on the first impression. Cut ruthlessly.
* **Section shape default:** headline ≤8 words + sub-paragraph ≤25 words + one visual asset OR one CTA.
* **No data-dump sections:** 20-row tables / 30-row award lists / giant pricing matrices → top 3-5 highlights + "View full list" link, marquee / carousel for breadth, or a different page if the data IS the product.
* **Lists >5 items need a different component, not a longer list:** 2-column grouped split · card grid · tabs/accordion · horizontal scroll-snap pills · carousel · marquee. A 10-row hairline spec list is the worst default — group into 2-3 chunks with sparse dividers or move to card-per-spec.
* **Spec sheets (the Marrow pattern):** `border-b` under every row is banned for cookware / hardware / apparel / artisan briefs. Alternatives: 2-col spec cards (name + large display value + one-line "why it matters") · scroll-snap horizontal pills · 3 clustered chunks with one soft divider each ("Materials" / "Cooking" / "Warranty") · featured-vs-rest (3-4 hero spec tiles + "View full specifications" disclosure).
* **COPY SELF-AUDIT (mandatory before ship):** re-read every visible string (headlines, subheads, eyebrows, buttons, body, captions, alt text, footer, errors); flag & rewrite: grammatically broken, unclear referents, hallucination-flavored ("elegant nothing" phrases, cute-but-wrong wordplay), or LLM-trying-to-sound-thoughtful (fake-craftsman labels, mock-poetic micro-meta). Unsure → replace with a plain functional sentence. AI-cute copy is worse than boring copy.
* **Fake-precise numbers banned** (`92%`, `4.1×`, `48k`, `5.8 mm`): fine only from real data (brief / brand / public metrics) or explicitly labeled mock — never AI-invented spec aesthetics.
* **One copy register per page** — no mixing technical mono, editorial prose, and marketing punch unless the brand voice explicitly calls for it.

### 4.10 Quotes & Testimonials
* Quote body ≤3 lines, never 6 (small footer-style testimonials may stretch slightly — spirit: "fits in a glance"). Longer → cut; a landing-page quote is a snippet.
* No em-dashes in quote text (Section 9.G bans them entirely).
* Attribution: name + role + optionally company. Never name only ("- Sarah").
* Real typographic quotes (" ") or none at all — not straight ASCII (").

### 4.11 Page Theme Lock
ONE theme per page; sections do not invert. Dark page = ALL sections dark — no light warm-paper section sandwiched between dark ones. Exception: an explicit "Color Block Story" / deliberate single theme switch with a strong transition — allowed once per page, never random alternation. Same-family background tints fine (`bg-zinc-950` + `bg-zinc-900`); `bg-amber-50` mid-page on a `bg-zinc-950` site is broken. Design-system theming (Radix Themes, shadcn `<Theme>`) is set ONCE at `layout.tsx` / page root.
---

## 5. CONTEXT-AWARE PROACTIVITY

These are tools, not defaults. Use them when the design read calls for them. **None of these fire automatically.**

* **Liquid Glass / Glassmorphism:** premium consumer, Apple-adjacent, luxury, media-overlay vibes; NOT dashboards, public-sector, "boring B2B." Beyond `backdrop-blur`: 1px inner border (`border-white/10`) + subtle inner shadow (`shadow-[inset_0_1px_0_rgba(255,255,255,0.1)]`); solid-fill fallback under `prefers-reduced-transparency`.
* **Magnetic Micro-physics:** `MOTION_INTENSITY > 5` AND premium / playful / agency brief. EXCLUSIVELY Motion's `useMotionValue` / `useTransform` outside the render cycle — never `useState` (Section 3.B).
* **Perpetual Micro-Interactions** (Pulse, Typewriter, Float, Shimmer, Carousel): `MOTION_INTENSITY > 5` AND the section actively benefits (status indicators, live feeds, AI-feel). Informational sections stay still — not every card needs a loop. Spring Physics (`type: "spring", stiffness: 100, damping: 20`), no linear easing.
* **"Motion claimed, motion shown."** `MOTION_INTENSITY > 4` → the page must actually move: hero entry transitions, scroll-reveal on key sections, hover physics on CTAs at minimum. A static page claiming `MOTION_INTENSITY: 7` is broken. Cannot ship working motion → drop the dial to 3, ship clean static. Never half-build breaking motion (cut-off ScrollTriggers, jumpy enters, missing cleanups).
* **MOTION MUST BE MOTIVATED (mandatory).** Every animation must answer "what does it communicate?" — hierarchy, storytelling, feedback, or state transition. "It looked cool" / "GSAP is available" are invalid reasons. Each ScrollTrigger / marquee / pinned section needs a one-sentence reason or it gets dropped.
* **MARQUEE MAX-ONE-PER-PAGE (mandatory).** Text marquees ("logos endlessly scrolling", "manifesto scrolling sideways") at most ONCE per page — two reads as lazy filler. Pick the one section where it serves the content; the rest get different layouts.
* **GSAP Sticky-Stack / Horizontal-Pan:** must be a REAL sticky-stack / pinned pan, not a sequential reveal. Canonical skeletons: `reference/motion-skeletons.md` — read before implementing. Shared signature failure: trigger fires before the section is pinned → fix `start: "top top"`, pin the wrapper, scrub the inner track.

### 5.A Canonical Motion Skeletons (externalized - read before implementing)
Sticky-Stack / Horizontal-Pan / Scroll-Reveal Stagger 三个模式的完整代码骨架（安装、HTML 结构、GSAP trigger 配置）外置于 `reference/motion-skeletons.md`——**实现任一模式前完整读取对应骨架并照抄 trigger 配置**（`start: "top top"`、pin、scrub 参数是踩坑收敛值），勿凭记忆重写。
### 5.D Forbidden Animation Patterns

* **`window.addEventListener("scroll", ...)`** is banned. It runs on every scroll frame, jank-prone, no batching. Use Motion's `useScroll()`, GSAP's `ScrollTrigger`, IntersectionObserver, or CSS `scroll-driven animations` (`animation-timeline: view()`).
* **Custom scroll progress calculations using `window.scrollY`** in React state. Same reason. Re-renders on every frame.
* **`requestAnimationFrame` loops that touch React state.** Use motion values (`useMotionValue` + `useTransform`) instead.
* **Layout Transitions:** Use Motion's `layout` and `layoutId` props for visible state changes (re-ordering lists, expanding modals, shared elements between routes). Do not wrap static content in `layout` props "for safety" - it costs measurement work.
* **Staggered Orchestration:** Use `staggerChildren` (Motion) or CSS cascade (`animation-delay: calc(var(--index) * 100ms)`) for reveal moments where sequence matters. For `staggerChildren`, parent (`variants`) and children MUST share the same Client Component tree.

---

## 6. PERFORMANCE & ACCESSIBILITY GUARDRAILS

### 6.A Hardware Acceleration
* Animate ONLY `transform` and `opacity`. Never animate `top`, `left`, `width`, `height`.
* Use `will-change: transform` sparingly - only on elements that will actually animate.

### 6.B Reduced Motion (mandatory)
* **Any motion above `MOTION_INTENSITY > 3` MUST honor `prefers-reduced-motion`.** This is non-negotiable.
* In Motion: wrap with `useReducedMotion()` and degrade to static.
* In CSS: gate animations behind `@media (prefers-reduced-motion: no-preference)` or provide an override block under `@media (prefers-reduced-motion: reduce)` that disables.
* Infinite loops, parallax, scroll-hijack, and magnetic physics MUST collapse to static / instant under reduced motion.

### 6.C Dark Mode (mandatory for any consumer-facing page)
* Design for **both modes from the start**. Never ship light-only or dark-only without explicit user instruction.
* Use Tailwind `dark:` variant OR CSS variables for tokens. Pick one strategy per project.
* **Do not prescribe specific dark-mode colors here.** The brief decides. Maintain visual hierarchy, brand identity, and WCAG AA contrast (AAA for body) across both modes.
* Respect `prefers-color-scheme: dark`. Default to system preference unless the brand insists on one mode.

### 6.D Core Web Vitals Targets
* **LCP** < 2.5s. Hero image must be `next/image priority` or preloaded.
* **INP** < 200ms. Heavy work off main thread.
* **CLS** < 0.1. Reserve space for images, fonts, embeds.
* Run Lighthouse before declaring a page done.

### 6.E DOM Cost
* Apply grain / noise filters EXCLUSIVELY to fixed, `pointer-events-none` pseudo-elements (e.g., `fixed inset-0 z-[60] pointer-events-none`). NEVER on scrolling containers - continuous GPU repaints destroy mobile FPS.
* Be aware of bundle size. Motion is not tiny. Three.js is large. Lazy-load anything that's not above-the-fold.

### 6.F Z-Index Restraint
NEVER spam arbitrary `z-50` or `z-10`. Use z-index strictly for systemic layer contexts (sticky navbars, modals, overlays, grain). Document the z-index scale in a project constants file.

---

## 7. DIAL DEFINITIONS (Technical Reference)

### DESIGN_VARIANCE (Level 1-10)
* **1-3 (Predictable):** Symmetrical CSS Grid (12-col, equal fr-units), equal paddings, centered alignment.
* **4-7 (Offset):** `margin-top: -2rem` overlaps, varied image aspect ratios (4:3 next to 16:9), left-aligned headers over center-aligned data.
* **8-10 (Asymmetric):** Masonry layouts, CSS Grid with fractional units (`grid-template-columns: 2fr 1fr 1fr`), massive empty zones (`padding-left: 20vw`).
* **MOBILE OVERRIDE:** For levels 4-10, asymmetric layouts above `md:` MUST collapse to strict single-column (`w-full`, `px-4`, `py-8`) on viewports `< 768px`.

### MOTION_INTENSITY (Level 1-10)
* **1-3 (Static):** No automatic animations. CSS `:hover` and `:active` states only. `prefers-reduced-motion` is the default mode anyway.
* **4-7 (Fluid CSS):** `transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1)`. `animation-delay` cascades for load-ins. Focus on `transform` and `opacity`.
* **8-10 (Advanced Choreography):** Complex scroll-triggered reveals, parallax, scroll-driven animation (CSS `animation-timeline` or GSAP ScrollTrigger). Use Motion hooks. **NEVER use `window.addEventListener('scroll')`** - it is a hard ban, not a "prefer-not." See Section 5.D for the allowed alternatives.

### VISUAL_DENSITY (Level 1-10)
* **1-3 (Art Gallery):** Lots of white space. Huge section gaps (`py-32` to `py-48`). Expensive, clean.
* **4-7 (Daily App):** Standard web app spacing (`py-16` to `py-24`).
* **8-10 (Cockpit):** Tight paddings. No card boxes; 1px lines separate data. Mandatory: `font-mono` for all numbers.

---

## 8. DARK MODE PROTOCOL

Dual-mode by default. Never assume light-only unless the brief is print-emulating editorial.

### 8.A Token Strategy (pick one, stick to it)
* **Tailwind `dark:` variant** (default for utility-first projects): every color utility paired with its dark variant (`bg-white dark:bg-zinc-950`, `text-gray-900 dark:text-gray-100`).
* **CSS variables** (for shadcn/ui, Radix Themes, or component libraries with theming): define semantic tokens (`--surface`, `--surface-elevated`, `--text-primary`, `--accent`) and swap values under `[data-theme="dark"]` or `@media (prefers-color-scheme: dark)`.

### 8.B Do Not Prescribe Specific Colors Here
The brief and brand decide. This skill enforces only:
* **Contrast** - WCAG AA minimum for body text, AAA target for hero copy.
* **Hierarchy parity** - visual hierarchy that works in light must work in dark. If a CTA pops in light, it pops in dark.
* **Brand fidelity** - primary brand color stays recognisable. Don't desaturate the brand into a dark mode.
* **No pure `#000000` and no pure `#ffffff`** - use off-black (zinc-950, near-black warm gray) and off-white. Pure values kill depth.

### 8.C Default Mode
Respect `prefers-color-scheme` unless the brand insists. Add a manual toggle if either mode would lose key brand expression.

### 8.D Test in Both Modes Before Finishing
Open the page in both modes during development. Do not ship a page you've only seen in one mode.

---

## 9. AI TELLS (Forbidden Patterns)

Avoid these signatures unless the brief explicitly asks for them.

### 9.A Visual & CSS
* **NO neon / outer glows** by default — inner borders or subtle tinted shadows.
* **NO pure black (`#000000`)** — off-black, zinc-950, charcoal.
* **NO oversaturated accents** — desaturate to blend with neutrals.
* **NO excessive gradient text** on large headers.
* **NO custom mouse cursors** — outdated, accessibility- and perf-hostile.

### 9.B Typography
* **AVOID Inter as default** (Section 4.1; override path exists).
* **NO oversized H1s that just scream** — control hierarchy with weight + color, not raw scale.
* **Serif for editorial / luxury / publication only**, never dashboards.

### 9.C Layout & Spacing
* Mathematically consistent padding/margins; no awkward floating gaps.
* **NO 3-column equal feature cards** — use 2-column zig-zag, asymmetric grid, scroll-pinned, or horizontal-scroll alternatives.

### 9.D Content & Data ("Jane Doe" Effect)
* **NO generic names** ("John Doe", "Sarah Chan") → creative, realistic, locale-appropriate.
* **NO generic avatars** (SVG "egg", Lucide user icons) → believable photo placeholders or specific styling.
* **NO fake-perfect numbers** (`99.99%`, `50%`, `1234567`) → organic messy data (`47.2%`, `+1 (312) 847-1928`).
* **NO startup-slop brand names** ("Acme", "Nexus", "SmartFlow") → contextual names that sound real.
* **NO filler verbs** ("Elevate", "Seamless", "Unleash", "Next-Gen", "Revolutionize") → concrete verbs only.

### 9.E External Resources & Components
* **NO hand-rolled SVG icons** — Phosphor / HugeIcons / Radix / Tabler; Lucide on explicit request only. Decorative SVGs strongly discouraged (4.8).
* **NO div-based fake screenshots** — full ban in 9.F.
* **NO broken Unsplash links** — `https://picsum.photos/seed/{descriptive-string}/{w}/{h}`, generated placeholders, or actual assets.
* **shadcn/ui** allowed but NEVER in default state — customize radii, colors, shadows, typography to the project aesthetic. Code ships visually clean and meticulously refined.

### 9.F Production-Test Tells (banned outright)

Real LLM-test signatures of "trying to look designed." Hard bans unless the brief explicitly calls for one.

**Hero & top-of-page**
* **NO version labels in the hero** (`V0.6`, `BETA`, `INVITE-ONLY PREVIEW`, `EARLY ACCESS`, `ALPHA`) — only for briefs explicitly about launch / preview status.
* **NO "Brand · No. 01"-style sub-eyebrows** ("Marrow · No. 01 · The 6-quart"). Skip.

**Section numbering & micro-labels**
* **NO section-number eyebrows** (`00 / INDEX`, `001 · Capabilities`, `06 · how it works`) — eyebrows name the topic in plain language, never enumerate.
* **NO `01 / 4` pagination on images or bento tiles.**
* **NO `Scroll · 001 Capabilities`-style scroll cues** — a simple arrow or "Scroll" is enough, no section-number prefix.
* **NO "Index of Work, 2018-2026"-style range labels** as eyebrows — say what the section is.

**Separators & dots**
* **The middle-dot (`·`) is rationed: max 1 per line** in metadata strips — never the default separator for everything; prefer line breaks, hairlines, or columns.
* **NO decorative colored status dots** on lists/nav/badges — acceptable ONLY for real semantic state (server status, availability flag), sparingly (this ban is absolute: repeated in Locale section below intentionally).

**Em-dashes & typography flourishes**
* **Em-dash (`—`): completely banned everywhere** — the full non-negotiable rule is 9.G below.
* **NO `<br>`-broken-and-italicized headlines** as a default "design move" ("for thirty\<br\>*years.*") — headlines read naturally first.
* **NO vertical rotated text** ("INDEX OF WORK 2018-2026" at 90°) — agency cliché; only for explicit agency / Awwwards / experimental briefs serving real composition.
* **NO crosshair / hairline grid lines as decoration** — only when they organize real content.

**Fake product previews**
* **NO div-based fake product UI anywhere (hero worst)** — fake task lists / terminals / dashboards from styled divs is the #1 LLM-design Tell. Real screenshot, generated image, real mini component preview, or none.
* **NO fake version footers inside fake screenshots** ("v0.6.2-rc.1", "last sync 4s ago · main").

**Marketing-copy Tells**
* **NO "Quietly in use at" / "Quietly trusted by"** — "Trusted by", "Used at", "Customers include", or no heading.
* **NO poetic section labels** ("From the field", "Field notes", "On our desks", "Loose plates") — plain functional labels ("Testimonials", "Latest writing") or none.
* **NO mock-humble industry-references in body copy.**
* **NO micro-meta-sentences under eyebrows** — Eyebrow + Headline + Body is enough.
* **NO generic step labels** ("Stage 1/2/3", "Phase 01/02/03", "Pass One/Two/Three") — the step content IS the label; if progression needs showing, use the verb-noun directly ("Install", "Configure", "Ship").

**Pills, labels and version stamps**
* **NO pills/labels/tags overlaid on images** (`Brand · 02`, `PLATE · BRAND`) — image speaks alone or caption below (outside the image).
* **NO photo-credit captions as decoration** (`Field study no. 12 · Ines Caetano`, `Plate 03 · House archive`) — credit only a real photographer of a real photo; otherwise functional one-liner or none.
* **NO version footers on marketing pages** (`v1.4.2`, `Build 0048`) — devtool fixtures, not landing-page content.
* **NO "Reservation 412 of 800" live-stock counters** — only for explicit limited-run waitlists with real data.

**Decoration text strips**
* **NO decoration text strip at hero bottom** (`BRAND. MOTION. SPATIAL.`, `TYPE / FORM / MOTION`, `ESTD. 2018 · LISBON`) — only when it carries real navigable links or real status info.
* **NO floating top-right sub-text in section headings** — put sub-text under the headline or build a clean aligned 2-column header; a tiny corner paragraph is the Tell.

**Lists, dividers and scoring**
* **NO `border-t` + `border-b` on every row** of long lists / spec tables — pick one border, use sparsely (alternatives in 4.9).
* **NO scoring/progress bars with filled background tracks** — number + small icon, or tiny inline bar WITHOUT a track.

**Locale, time, scroll cues**
* **Locale / city / time / weather strips banned for 99% of briefs** ("Lisbon, working with founders", "Lisbon 14:23 · 18°C") — allowed ONLY for globally-distributed-studio / travel / physical-venue briefs; a single footer contact address is fine, atmospheric strips are not.
* **Scroll cues banned** (`Scroll`, `↓ scroll`, "Scroll to explore", mouse-wheel icons) — if they have not scrolled yet they are looking at the hero; they know what scroll is.
* **ZERO decorative status dots by default** — same rule as above (real semantic state only, max one per page section).

### 9.G EM-DASH BAN (the single most-violated Tell)

**Em-dash (`—`) is COMPLETELY banned — zero allowance.** No "limited use", no "natural language frequency", no "body copy is fine". Banned in headlines, eyebrows, labels, pills, buttons, captions, nav, body copy, quotes, attribution, alt text. Replacements:
* Headlines/labels → period, comma, line break, or hairline.
* Body copy → restructure: two sentences, comma, parentheses, or colon.
* Quote attribution → spaced hyphen (` - `) or line break + smaller name.
* En-dash (`–`) as separator is equally banned — date / number ranges (`2018-2026`, `€40-80k`) use a plain hyphen.

Permitted dash characters: regular hyphen `-` (compound words, ranges, markup dividers) and the math minus (`-5°C`). A single visible `—` or `–` fails the Pre-Flight Check and must be rewritten. Binary rule: zero (historically ignored when phrased as "use sparingly").

---

## 10. REFERENCE VOCABULARY (externalized)
模式命名词汇表外置于 `reference/pattern-vocabulary.md`：§4/§5/§11 引用布局模式名、或需向用户准确描述布局方案时读取，用既有命名，勿自造近义词。
## 11. REDESIGN PROTOCOL

This skill handles **greenfield builds AND redesigns**. Misclassifying the mode is the single biggest source of bad redesign output.

### 11.A Detect the Mode (first action)
* **Greenfield** - no existing site, or full overhaul approved. Dial baseline from Section 1.
* **Redesign - Preserve** - modernise without breaking the brand. Audit first, extract brand tokens, evolve gradually.
* **Redesign - Overhaul** - new visual language on top of existing content. Treat as greenfield for visuals; preserve content and IA.

If ambiguous, ask **once**: *"Should this redesign preserve the existing brand, or are we starting visually from scratch?"*

### 11.B Audit Before Touching
Document the current state before proposing changes:
* **Brand tokens** - primary / accent colors, type stack, logo treatment, radii.
* **Information architecture** - page tree, primary nav, key conversion paths.
* **Content blocks** - what exists, what's doing work, what's filler.
* **Patterns to preserve** - signature interactions, recognisable hero, copy voice.
* **Patterns to retire** - AI-slop tells, broken layouts, dead links, generic stock imagery, perf traps.
* **Dial reading of the existing site** - infer current `DESIGN_VARIANCE` / `MOTION_INTENSITY` / `VISUAL_DENSITY`. That's your starting point, not the baseline.
* **SEO baseline** - current ranking pages, meta titles, structured data, OG cards. **SEO migration is the #1 redesign risk.**

### 11.C Preservation Rules
* **Do not change information architecture** unless asked. Keep page slugs, anchor IDs, primary nav labels stable for SEO and muscle memory.
* **Extract brand colors before applying Section 4.2.** A brand that is already purple stays purple - apply the LILA RULE's override.
* **Preserve copy voice** unless asked for a rewrite. Visual modernisation ≠ content rewrite.
* **Honor existing accessibility wins.** Do not regress focus states, alt text, keyboard nav, contrast.
* **Respect existing analytics events.** Do not rename buttons, form fields, section IDs that downstream tracking depends on.

### 11.D Modernisation Levers (priority order)
Apply in order - stop when the brief is satisfied:
1. **Typography refresh** - biggest visual lift per unit of risk.
2. **Spacing & rhythm** - increase section padding, fix vertical rhythm.
3. **Color recalibration** - desaturate, unify neutrals, keep brand accent.
4. **Motion layer** - add `MOTION_INTENSITY`-appropriate micro-interactions to existing components.
5. **Hero & key-section recomposition** - restructure top-of-funnel using Section 10 vocabulary.
6. **Full block replacement** - only when the existing block is unsalvageable.

### 11.E Decision Tree: Targeted Evolution vs Full Redesign
* IA, content, and SEO sound → **targeted evolution** (Levers 1-4). ~70% of value at ~40% of risk.
* Visual debt is structural (broken IA, no design system, broken mobile) → **full redesign** with strict content preservation.
* Brand itself is changing → **greenfield**.

### 11.F What Never Changes Silently
Never modify without explicit user approval:
* URL structure / route slugs.
* Primary nav labels.
* Form field names or order (breaks analytics + autofill).
* Brand logo or wordmark.
* Existing legal / consent / cookie copy.

---

## 12. COMPONENT APPROACH (no generic block library - by design)

预置代码只存在于**机械层**：`showcase/_skeleton.html`（deck 舞台机械）与 `reference/motion-skeletons.md`（GSAP 动效骨架）。通用版式/装饰积木（hero / pricing / bento…）**刻意不做**：可复用的页面区块配方会把每个项目推向同一模板——正是 §4.7 版式去重、§9 AI-Tells 与 check-structure 反趋同门要防的病。风格层的"积木"由素材库承担（每套 DESIGN.md 的 components / signature moves）。若未来 longform 路径出现组件级重复失败，以 `reference/` 模式片段形式补充，不建独立 blocks/ 架构。
## 13. OUT OF SCOPE

This skill is NOT for:
* Dashboards / dense product UI / admin panels (use Fluent, Carbon, Atlassian, or Polaris from Section 2.A).
* Data tables (use TanStack Table or AG Grid).
* Multi-step forms / wizards (use Form-specific patterns; this skill won't make them better).
* Code editors (use Monaco / CodeMirror with their official skinning).
* Native mobile (use Apple HIG / Material directly).
* Realtime collab UIs (presence, cursors, OT-aware - different problem class).

If the brief is one of the above, **say so explicitly**, point to the right tool, and only apply this skill's marketing-page / about-page / landing-page parts to the surfaces where they apply.

---

## 14. FINAL PRE-FLIGHT CHECK

Run this matrix before outputting code. This is the last filter.

**THIS IS NOT OPTIONAL. Run every box. If any box fails, the output is not done.**

- [ ] **Brief inference** declared (Section 0.B one-liner)?
- [ ] **Dial values** explicit and reasoned from the brief, not silently using baseline?
- [ ] **Design system** chosen from Section 2 if applicable, or aesthetic labeled honestly?
- [ ] **Redesign mode** detected and audit performed (if applicable, Section 11)?
- [ ] **ZERO em-dashes (`—`) anywhere on the page.** Headlines, eyebrows, pills, body, quotes, attribution, captions, buttons, alt text. Zero. (Section 9.G - non-negotiable.)
- [ ] **Page Theme Lock**: ONE theme (light, dark, or auto) for the whole page. No section flips to inverted mode mid-page (Section 4.11)?
- [ ] **Color Consistency Lock**: one accent color used identically across all sections (Section 4.2)?
- [ ] **Shape Consistency Lock**: one corner-radius system applied consistently (Section 4.4)?
- [ ] **Button Contrast Check**: every CTA text is readable against its background (no white-on-white, WCAG AA 4.5:1)?
- [ ] **CTA Button Wrap**: no CTA label wraps to 2+ lines at desktop?
- [ ] **Form Contrast Check**: form inputs, placeholders, focus rings, labels all pass WCAG AA against the section background?
- [ ] **Serif discipline**: if a serif is used, it is NOT Fraunces or Instrument_Serif (or it is, with explicit brand justification)? Different serif from your previous project?
- [ ] **Premium-consumer palette check**: if the brief is premium-consumer (cookware / wellness / artisan / luxury), the palette is NOT the AI-default beige+brass+oxblood+espresso family? Different family from your previous premium-consumer project?
- [ ] **Italic descender clearance**: every italic word with `y g j p q` has `leading-[1.1]` min + `pb-1` reserve?
- [ ] **Hero fits the viewport**: headline ≤ 2 lines, subtext ≤ 20 words AND ≤ 4 lines, CTA visible without scroll, font scale planned around image?
- [ ] **Hero top padding**: max `pt-24` at desktop, hero content does not float halfway down the viewport?
- [ ] **Hero stack discipline**: max 4 text elements in hero (eyebrow OR brand strip, headline, subtext, CTAs)? No tiny tagline below CTAs, no trust micro-strip in hero?
- [ ] **EYEBROW COUNT (mechanical)**: count instances of `uppercase tracking` micro-labels above section headlines across all components. Count ≤ ceil(sectionCount / 3)? Hero counts as 1.
- [ ] **Split-Header Ban**: no "left big headline + right small explainer paragraph" pattern as a section header (vertical stack instead)?
- [ ] **Zigzag Alternation Cap**: no 3+ consecutive sections with the same image+text-split layout?
- [ ] **No Duplicate CTA Intent**: no two CTAs with the same intent ("Get in touch" + "Let's talk" both on page = Fail)?
- [ ] **Logo wall = logo only**: no industry / category labels printed below logos?
- [ ] **Bento Background Diversity**: at least 2-3 bento cells have real visual variation (image, gradient, pattern), not all white-on-white text cards?
- [ ] **"Used by / Trusted by" logo wall** lives UNDER the hero, not inside it, uses REAL SVG logos (Simple Icons / devicon) or generated SVG marks, NOT plain text wordmarks?
- [ ] **Copy Self-Audit**: every visible string re-read, no grammatically-broken or AI-hallucinated phrases ("free on its past" type) shipped?
- [ ] **Motion motivated**: every animation can be justified in one sentence (hierarchy / storytelling / feedback / state transition), no GSAP-for-show?
- [ ] **Marquee max-one-per-page**: no two horizontal marquees on the same page?
- [ ] **Navigation on ONE line** at desktop, height ≤ 80px?
- [ ] **Section-Layout-Repetition** check: no two sections share the same layout family (at least 4 different families across 8 sections)?
- [ ] **Bento has rhythm AND exact cell count** (N items → N cells, no empty cells in middle or at end)?
- [ ] **Long lists use the right UI component** (not default `<ul>` with `divide-y` for > 5 items - see Section 4.9 alternatives)?
- [ ] **Real images used** (gen-tool first, then Picsum-seed, then explicit placeholder slots) - NO div-based fake screenshots, NO hand-rolled decorative SVGs, NO pure-text minimalism?
- [ ] **No pills/labels overlaid on images** (no `Plate · Brand`, no `Field notes - journal`)?
- [ ] **No photo-credit captions as decoration** (`Field study no. 12 · Ines Caetano`)?
- [ ] **No version footers** (`v1.4.2`, `Build 0048`) on marketing pages?
- [ ] **No micro-meta-sentences** under eyebrows ("Each of these is a feature we ship today...")?
- [ ] **No decoration text strip at hero bottom** (`BRAND. MOTION. SPATIAL.`)?
- [ ] **No floating top-right sub-text** in section headings?
- [ ] **No scoring/progress bars with filled background tracks** as comparison visuals?
- [ ] **No locale / city-name / time / weather strips** unless brief is genuinely globally-distributed or place-focused?
- [ ] **No scroll cues** (`Scroll`, `↓ scroll`, `Scroll to explore`)?
- [ ] **No version labels in hero** (V0.6, BETA, INVITE-ONLY) unless the brief is a launch?
- [ ] **No section-numbering eyebrows** (`00 / INDEX`, `001 · Capabilities`, `06 · how it works`)?
- [ ] **No decorative dots** (zero by default, only for real semantic state)?
- [ ] **No `border-t` + `border-b` on every row** of long lists / spec tables?
- [ ] **Content density** sane: no 20-row data tables, no fake-precise specs without justification, ≤ 25-word sub-paragraphs by default?
- [ ] **Quotes ≤ 3 lines** of body, attribution clean (no em-dash)?
- [ ] **Motion claimed = motion shown**: if `MOTION_INTENSITY > 4`, page actually animates, not just claimed?
- [ ] **GSAP sticky-stack / horizontal-pan** implemented per `reference/motion-skeletons.md` canonical skeleton (`start: "top top"`, `pin: true`, correct scrub)?
- [ ] **No `window.addEventListener('scroll')`** - using Motion `useScroll()` / ScrollTrigger / IntersectionObserver / CSS scroll-driven animations only?
- [ ] **Reduced motion** wrapped for everything `MOTION_INTENSITY > 3`?
- [ ] **Dark mode** tokens defined and tested in both modes?
- [ ] **Mobile collapse** explicit (`w-full`, `px-4`, `max-w-7xl mx-auto`) for high-variance layouts?
- [ ] **Viewport stability**: `min-h-[100dvh]`, never `h-screen`?
- [ ] **`useEffect` animations** have strict cleanup functions?
- [ ] **Empty / loading / error** states provided?
- [ ] **Cards omitted** in favor of spacing where possible?
- [ ] **Icons** from an allowed library only (Phosphor / HugeIcons / Radix / Tabler), no hand-rolled SVG paths?
- [ ] **Motion** isolated in client-leaf components with `'use client'` at the top, memoized?
- [ ] **No AI Tells** from Section 9 (Inter as default, AI-purple, three-equal cards, Jane Doe, Acme, "Quietly in use at")?
- [ ] **Core Web Vitals** plausibly hit (LCP < 2.5s, INP < 200ms, CLS < 0.1)?
- [ ] **One design system** per project (no Material + shadcn mixed)?

If a single checkbox cannot be honestly ticked, the page is not done. Fix it before delivering.

---

## 15. DECK MODE (Fixed-Stage Slides) - Incremental Rules

Applied when the brief is a presentation deck or a fixed set of slides (see 0.E). DECK MODE rules override Sections 1-14 wherever they conflict. Output is a single-file standalone HTML (no build step), 1920x1080 stage, 8 slides by default, fit-scaled to any viewport.

### 15.1 Default Page Plan (8 slides)
1. Cover (brand wordmark + hero statement + primary CTA)
2. Agenda / principles
3-5. Feature / capability pages (2-3 pages, flow layout)
6. Data or quote page (stats, tables, testimonial)
7. Product / example page (console, UI mock, case)
8. Closing CTA (repeat wordmark + final action)
Adjust page count to the brief, but every slide must satisfy 15.3-15.6.

### 15.2 Deterministic Stage (non-negotiable)
- Fixed stage 1920x1080. One `<section class="slide">` per page: `position:absolute; inset:0; width:1920px; height:1080px; overflow:hidden`.
- Fit to viewport with ONE JS helper: `factor = min(vw/1920, vh/1080)`, center via `transform: translate(x,y) scale(factor)` on a stage wrapper. Never size the stage in vw/vh units.
- Slide switching: toggle `.active` / `.visible` classes (visibility + opacity + pointer-events), NEVER `display:none`.
- Navigation: `?slide=N` deep link, keys ← → Space Home End, touch swipe, `prefers-reduced-motion`, `@media print` renders all slides.
- Speaker notes (presenter mode, recommended): slides may carry a `data-note` per slide; pressing `N` toggles an overlay showing the current slide's note (time + page + note). Optional presenter-sync via `postMessage`/`StorageEvent` for a second window. Keep the notes OUT of the visible slide composition (they are chrome-layer, not content).
- Deck chrome: brand wordmark inside each slide at top 56px / left 120px; bottom-center clickable dot-progress navigation wrapped in a pill capsule (one dot per slide; active dot solid + slightly enlarged), NO on-screen keyboard hint text. Rules for the capsule:
  - Width is content-driven (`fit-content`): it grows automatically as slide count changes.
  - Color adapts to the slide background: capsule background = theme's main body-text color at ~8% alpha + same-color hairline border; dots inherit that color. Light background -> dark navigation; dark / saturated background -> light navigation. Source of truth is the theme's body/primary text variable, never a hardcoded hex.
  - `.nav-dot` is a `<button>`: it MUST set `color: inherit`, otherwise `currentColor` resolves to the UA default black and breaks contrast on dark themes.
  - Inject the theme body-text color explicitly on the pill container (`color: var(--color-...)`): do NOT rely on inheriting from the chrome bar's own color, which is a muted gray that washes the capsule out on light backgrounds.
  - Treat the capsule as a three-token surface, not a single `currentColor` effect: expose `--nav-pill-fg`, `--nav-pill-bg`, and `--nav-pill-border`, plus dark-tone fallbacks `--nav-pill-fg-dark`, `--nav-pill-bg-dark`, and `--nav-pill-border-dark`. Provide an `rgba()` fallback before the `color-mix()` enhancement; do not assume `color-mix()` support.
  - For a deck whose slides switch between light, dark, saturated, gradient, or image-led backgrounds, mark the affected slide with `data-nav-tone="dark"`. The controller must mirror that state to `.dot-nav[data-tone="dark"]`, so the capsule remains readable while preserving the series palette. Do not infer a single tone from the first slide and reuse it for the whole deck. If a deck uses only one tone, it still must declare the semantic tokens explicitly rather than relying on UA defaults.
  - Add a restrained `backdrop-filter` and shadow only as legibility aids. Under `prefers-reduced-transparency: reduce`, disable blur and use an opaque theme surface. The capsule must remain compact chrome, not become a card or a second content panel.
  - Class must be namespaced (`.nav-dot`) to avoid clashing with in-page decorative dots.
  - **CAPSULE RENDERING HARD RULE (2026-08-21, 30 套全量踩坑)**：胶囊背景/描边用 `color-mix(in srgb, currentColor calc(var(--nav-pill-alpha) * 100%), transparent)`。**color-mix 的混合比例必须是百分比**——直接写 `var(--nav-pill-alpha)`（值 `0.08`，无单位数字）或裸数字，整条声明会 invalid-at-computed-value，背景/描边退回全透明，胶囊视觉消失（只剩裸圆点）。`rgba()` 里的 0-1 数字合法，不受此限。`check-decks.py` 已含对应断言（每页 `.dot-nav` 背景 alpha>0.01 且描边 ≥1px）。
- 以上舞台结构（stage/缩放/切页/导航胶囊/print/reduced-motion）的事实骨架参考：`showcase/_skeleton.html`（373 行可运行骨架，新 deck 从它起步改造，勿凭记忆重写舞台机械）。

### 15.3 Value-Layer Fidelity Boundary (highest-leverage rule)
- `tokens.json` is the ONLY numeric source. `variables.css` / `theme.css` are implementation references. `DESIGN.md` is the fact source. Never design from screenshots or intuition.
- Palette, radii, font names: use EXACTLY the source tokens, 1:1. Typography sizes and spacing: multiply by 2 (web design → stage). Line-height: use the source `--leading-body` UNMODIFIED, applied to EVERY body-like class (`.body`, `.body-muted`, `.body-on-color`, `.card-body`, ...). Fixing only the main `.body` class is a known regression.
- Fonts: load the DESIGN.md substitute via Google Fonts with the fallbacks listed in the source; on load failure fall back to those substitutes, never to the default sans.
- 素材模式生成的 deck 必须在 `<head>` 写来源标记 `<meta name="design-source" content="<style-slug>">`：包外目录 deck 靠它被 check-decks.py 用素材权威行高校验（缺标记时降级为 deck 自身声明自洽检查）。
- **Boundary vs freedom**: this section only guards the fidelity of the TOKENS (what the palette / type / radii ARE). HOW to compose colors, assign type roles, and land the visual voice is the model's creative call under Section 16 - do not freeze it here.

### 15.4 Layout Hard Rules
- Flow layout inside slides. NO absolute-positioned content (known canvas overflow bug).
- Height budget: content must not cross y=900. Bottom 160px is a safety zone reserved for chrome.
- Absolute decorations (bubbles, triangles, shapes) must be checked for geometric overlap with the content block.
- Radii, shadows, button-corner direction follow the DESIGN.md signature literally.
- Remember line-height increases push card bottoms down, re-verify 15.6.2 after any line-height change.
- Budget the height IN THE FIRST DRAFT: display-scale headlines (e.g. 90px source x2 = 180px) spanning two lines, and dense multi-card/multi-table grids, are the highest-frequency overflow points. Compress margins and paddings up front, leave margin before the QA pass.

### 15.5 Story-Reveal Motion (v5 editorial expo - reference-deck-verified)
Transition-driven, driven by `.slide.visible` (NOT CSS `animation` + JS re-trigger):
- No slide-level translate or transition: the slide appears instantly, then its elements tell the story one by one.
- Reveal base state: `opacity:0; transform: translateY(28px)`. `.slide.visible .reveal` → `opacity:1; transform: translateY(0)`. Transition: `opacity/transform 0.7s cubic-bezier(0.16, 1, 0.3, 1)` (ease-out expo). Defined once as CSS tokens `--ease-out-expo` / `--duration-normal` in `:root`.
- Stagger via `transition-delay` on `.slide.visible .reveal.dN`: d1 0.12s / d2 0.24s / d3 0.36s / d4 0.48s (0.12s steps). Sequence matters: hero title → subhead → CTA; list items top-to-bottom; card grids left-to-right; all via d1-d4 (or finer by theme).
- Leaving a slide simply removes `.visible` — the reverse transition (elements slide down 28px and fade out) IS the exit animation. No extra code, no JS re-trigger needed in showSlide beyond toggling `.active` / `.visible`.
- Data-viz on entry: SVG line charts draw left-to-right (`.chart-line` with `pathLength="1"`, `stroke-dasharray:1` / `stroke-dashoffset:1 → 0` on `.visible`, ~1.4s delay 0.5s); ring charts fill clockwise.
- Interaction (hover on buttons / cards / link-arrow) must override the reveal transition to snappy timing (`.slide.visible [class*="btn"], .slide.visible .artifact, .slide.visible .link-arrow { transition: ... 0.2s ease }`).
- FORBIDDEN: large-delay chunked stagger ("block by block"), CSS `animation`-based reveals (forces JS re-trigger hacks), scroll-driven reveals.
- Banners / marquees: static large centered text only. NEVER scrolling marquees (unreadable at any speed).
- `prefers-reduced-motion`: collapse all animations/transitions to instant.

### 15.6 Mandatory QA Gates (run all four; none may be skipped)
1. **Value-layer check**: every color used in the HTML must be inside the source palette (tokens.json colors). This catches the biggest failure mode (inventing palettes). Reference implementation: `python showcase/check-values.py <slug 或 deck 目录>`（静态扫描，无需浏览器；包外 deck 需 `--style <slug>` 或 `design-source` 标记定素材基准，无自洽降级）. In **自由发挥模式** this gate downgrades to "declared-token self-consistency" - every color/font used must be inside the `freeplay-declaration.md` ②③ declared token sets (no stray colors/fonts beyond what you declared; the deck must match its own declaration).
2. **Automated deck check**: reference implementation `showcase/check-decks.py <slug 或 deck 目录>`（file:// 直读，无需起 HTTP 服务；需 playwright + Chrome）. It asserts per slide: every body-like computed line-height == the leading baseline (±0.02), visible content bottom <= 900, and nav-pill visibility/contrast. It excludes decor elements (hero-art / glow-* / bar-* / marquee) and fixed chrome. 行高基准解析：showcase 套（slug）取素材 `variables.css` 的 `--leading-body`（权威，不变）；包外用户 deck 依次取 `--style <slug>` → deck `<head>` 的 `<meta name="design-source">` 标记（15.3 契约）→ deck 自身 `:root --leading-body`（自洽降级，输出注明）。In **自由发挥模式** there is no source `--leading-body`; the line-height target is the declaration's own body line-height, and the safety-zone y<=900 check still runs — pass `--freeplay`（声明文件优先读 deck 旁 `freeplay-declaration.md`，回退包内模板）for this mode.
3. **Visual QA (capability-adaptive)**: Chrome headless `?slide=N` screenshots at 1920x1080 (工具 `python showcase/shot-all-slides.py <slug 或 deck 目录>`，file:// 直读无需起服务；showcase 套截到 `showcase/<slug>/screenshots/`，包外 deck 截到 deck 旁 `screenshots/`), then an inspection by whoever CAN see images: a native multimodal main model inspects directly; a text-only main model must delegate to a vision-capable sub-agent (e.g. a vision-reader). Never skip the visual pass just because the main model can't see. Covers palette adherence, signature moves, overflow below y=900, crop / overlap, and the bottom capsule on at least one light slide, one dark/saturated slide, and one gradient/photo-led slide. Confirm that the capsule has a visible surface boundary, that inactive dots remain legible, and that the active dot is distinguishable without overpowering the material style.
Arbitration (applies to ANY vision source - multimodal model or sub-agent): color / corner-radius / line-spacing judgments are UNRELIABLE (bone-white vs white confusion, 8px radius misread, 1.0 line-height reported as "comfortable"). Confirm via CSS computed values + pixel measurement before changing code.
4. **Structure anti-convergence**: run `python showcase/check-structure.py [<slug 或 deck 目录>]`（静态分析；包外 deck 需 `--style <slug>` 或 `design-source` 标记定契约基准）. It inspects middle slides 2-6 and requires at least two distinct, style-specific DOM/CSS signals; generic `card`, `quote`, `stat`, `frame`, and wordmark scaffolding does not count. The allowed middle-expression families are: data = real data cards/charts; newspaper = multi-column layout; illustration = full illustration plus side notes; product = product entity/UI artifact; playful = stickers, annotations, hand-drawn arrows; industrial = numbering, spec tables, engineering callouts. A single quote or breathing-space slide may be a deliberate rhythm change; the check warns only when more than half of the middle slides lose identifiable signals.

### 15.7 Deck-Specific Tells (banned in DECK MODE)
- Invented palette colors outside tokens.json (the #1 rework cause)
- Content crossing y=900 or overflowing the 1920x1080 canvas
- Decorative shapes overlapping text
- Body line-height drifting from the source `--leading-body` (including sibling classes)
- Scrolling banners, chunked stagger reveals

### 15.8 Customization Contract (clone-friendly CONFIG block)
Every generated deck MUST expose its adjustable parameters as named CSS custom properties, grouped in ONE clearly-marked `/* ════ CONFIG ... ════ */` block at the top of the `<style>` (right after the value-layer `:root`), each line carrying a short Chinese comment that names the parameter and gives the common range. Cloners edit ONLY that block and refresh - no build step.

Fixed token contract (names identical across all decks; defaults = the verified reference feeling):
- **Motion**: `--motion-ease` (default `cubic-bezier(0.16,1,0.3,1)`), `--motion-duration` (0.7s), `--motion-distance` (28px), `--motion-stagger-step` (0.12s)
- **Nav pill**: `--nav-dot-size` (14px), `--nav-dot-gap` (18px), `--nav-pill-pad-y` (14px), `--nav-pill-pad-x` (28px), `--nav-pill-alpha` (0.08), `--nav-pill-border-alpha` (0.28), `--nav-pill-shadow-alpha` (0.12), `--nav-pill-blur` (10px), `--nav-active-scale` (1.15), `--nav-hover-scale` (1.35). The semantic surface tokens (`--nav-pill-*`) must remain in the same CONFIG block when a deck needs brand-specific tuning.
- **Layout**: `--safety-bottom` (160px), `--frame-pad-top` (112px), `--frame-pad-x` (120px)
- **Data-viz**: `--chart-draw-duration` (1.4s)

Value-layer tokens from tokens.json stay 1:1 and do NOT go into CONFIG (they are the material contract; editing them breaks source fidelity). `.reveal`, `.slide`, and `.nav-dot` rule bodies must reference the CONFIG variables (`var(--motion-*)`, `var(--nav-*)`, `var(--safety-bottom)` ...), not hardcoded numbers.

### 15.9 Share & Export (P2 — deck delivery, reference implementation in showcase/)
Deck delivery happens in three dialects; pick by audience:

1. **本地导出 PDF** — `python showcase/export-pdf.py <slug 或 deck 目录>` → `.pdf`。showcase 样品按 slug（产物在 `showcase/exports/`）；**用户自己的 deck** 传包外任意含 index.html 的目录路径，产物落在 deck 旁边。deck 经 file:// 直读，无需起服务；`../fonts` 相对引用按目录解析（字体库从 `showcase/fonts/` 拷到 deck 同级，与部署暂存同结构）。8 页 16:9 落版（骨架 `@media print` 每 slide 一页，脚本注入 `@page size` 保证不缩放不裁切）。适合打印、评审、存档。
2. **本地导出 PPTX** — `python showcase/export-pptx.py <slug 或 deck 目录>` → `.pptx`，输出位置规则同上。逐页截 1920×1080 全幅图嵌 16:9 幻灯片，与浏览器所见 1:1。适合发给不改代码的同事继续编辑。
3. **公开 URL 分享** — 动手前**先完整读取 `deploy-guide.md`**（部署规范/AI 代理执行手册，本节仅要点摘要）：环境自备自检、Vercel / 飞书妙搭两条出口的完整流程、字体改造与失败处理都在该文档。要点：
   - **Vercel**：默认部署**用户自己的 deck**（暂存 `<deck>/ + fonts/` 保持 `../fonts` 相对结构后 `vercel deploy --prod --yes`）；样品整站在 `showcase/` 内部署（`.vercelignore` 排除 exports/本地截图；根落地页 `showcase/index.html` 自动跳图廊）。
   - **飞书妙搭**：单 deck 创意模式应用（`+create --app-type html` → `+init` → push `sprint/default` → `+release-create` / `+release-get` 轮询 → `/page/<meta_token>` 链接，开发态=发布态）。**字体必须先换官方镜像** `https://miaoda.feishu.cn/fonts/css2`（平台资源不进 git；样品查 `deck-font-map.json`、用户 deck 自动探测字族并与 fonts.css 求交；斜体族用 `ital,wght` 双轴；未知字族不进查询，否则 css2 整条 400 全字体失败）。`+html-publish` 为旧链路勿用；重部署复用应用不重复 `+create`。
   - 登录授权（`vercel login` / `lark-cli auth login --domain apps`）属用户操作；部署前 deck 必须已过 15.6 QA。

**字体自托管（强制，2026-08-19 起）**：deck 字体一律用本地共享字体库，禁止 Google Fonts 外链。原因：外链依赖观看者网络能否到达 `fonts.googleapis.com`/`fonts.gstatic.com`，国内/飞书生态观看者会回退系统字体，视觉掉档。实现：
- 共享库 `showcase/fonts/`：62 个 latin 子集 `.woff2` + `fonts.css`（62 个 `@font-face`，只取 latin，内容为英文省体积）。覆盖 30 套实际用到的全部 23 个字族（Inter/JetBrains Mono/Archivo/Archivo Black/Anton/Bebas Neue/Fraunces/Source Serif 4/EB Garamond/Caveat/DM Sans/Alfa Slab One/Manrope/Bowlby One SC/Open Sans/Roboto Condensed/Nunito/Raleway/Space Grotesk/Noto Sans/Press Start 2P/VT323/Literata）。
- 每个 deck 的 `<head>` 用 `<link rel="stylesheet" href="../fonts/fonts.css">` 引用（相对路径，`file://` 和 Vercel/妙搭都可用）。字体选择仍每套各异的品牌替代字体（素材 DESIGN.md 的 substitute 规则），只是文件不再依赖 Google。
- 重建工具：`python showcase/fonts_download.py`（重新下载/增量）+ `python showcase/fonts_rewrite.py`（改写 deck 外链为本地引用）。
- 改字体后必须重跑 QA：`check-values.py` + `check-decks.py` + `gallery-shots.py`（重截 gallery 封面）+ build-index.py（图廊回填）。截图用 `document.fonts.ready` 等待加载完成。

---

## 16. STYLE CONTRACT (creative freedom - where the model decides)

Section 15 locks the skeleton: page plan, stage, navigation, motion, layout safety, QA, CONFIG. The STYLE CONTRACT is NOT another rulebook. It is the agreement on what the model MUST respect while playing and where it has true freedom. Sections 15 and 16 together define a deck's output contract.

### 16.1 What the model MUST respect (binding, from the material)
- Style source of truth = the material `DESIGN.md` (facts) + `tokens.json` (only numeric source). Never screenshots, never echoing another style, never the model's own generic default. Anticipate the expected output is a deck that READS as that exact brand, not "a nice deck".
- Palette, type, radii, shadows come EXACTLY from the source tokens (1:1; sizes/spacing x2). Zero invented colors or fonts.
- 氛围与装饰手法可对照真实品牌官网的表现学习（`brand-style-reference.md` 的沉淀规则：官网是"表现标杆"、DESIGN.md 是"事实源"，学手法不照搬布局；背景纹理是 30 套普遍缺失项，优先从该报告找补）。
- The material's USAGE constraints are the style's voice and are binding, not suggestions. Extract them from DESIGN.md Do's/Don'ts and obey. Examples that shipped: IKEA link-blue only for links / yellow only for activation; Steep sienna only on peach surfaces and chart strokes, max one peach card per page; Flying Papers serif 400-only with isolated italic phrases, accent card one per row; Raycast deep monitor system with a single signature pop color.

### 16.2 Where the model is FREE TO PLAY (do NOT over-specify)
- **Color composition**: how to use the palette inside its rules - emphasis order, surface hierarchy, where the one accent lands, contrast layering. Skill never dictating which accent on which page.
- **Typographic voice**: role split of the substitute fonts (headline / body / micro-label), letter-spacing feel, editorial vs technical tone - decided from reading DESIGN.md.
- **Page composition & "signature moves"**: italics placement, card geometry, data-viz style for that brand, layout personality - the model's judgment from the material.
- **Copywriting / content voice** inside the 8-page plan: tone, microstructure, what each section says.

### 16.3 Keeping freedom disciplined
- Before code, write a 3-line "Style Read": palette voice / typographic voice / signature moves, each traceable to a DESIGN.md line (mirrors 0.B for the material).
- In **自由发挥模式** the Style Read IS the `freeplay-declaration.md` (0.E) - no external DESIGN.md to trace to, so the declaration's own ②③④ sections are the trace anchor.
- Every decorative decision must trace to source basis. If a decoration has no source line, drop it - restraint is the move (most brands here are restrained for reasons).
- If a visual call cannot be sourced or justified, prefer the source's default restraint.

### 16.4 Anti-slop guard (style layer)
The deck must NOT converge to a generic AI look: no AI-purple, no default glassmorphism, no invented palette, no "three equal cards" if the source does not say so, no interpolation between styles. Enforcement = 15.6 gate 1 (value-layer ⊆ tokens) + the source usage constraints + 16.3 traceability.
Anti-convergence warning (Zara-style self-reminder): when generating a BATCH of styles (e.g. the whole library), models tend to converge toward one comfortable look across generations. This is the core risk of a style library - every deck must stay distinguishable. Before each deck, re-read 16.3 Style Read and confirm the palette voice / typographic voice / signature moves genuinely differ from the previous deck's. If two adjacent decks read as "the same design," redo the stylistic calls.
Structural anti-convergence: each style must declare at least two distinct middle-slide signals in `metadata/structure-contracts.json`, and the implementation must express its declared family rather than falling back to a shared card/grid recipe. Different families intentionally use different middle expressions: data cards/charts, newspaper columns, illustration with side notes, product/UI artifacts, playful stickers and annotations, or industrial numbered specifications and engineering callouts.

### 16.5 CJK / Chinese Fallback Contract
English-first decks work as-is. When deck content is Chinese or mixed CJK, apply a fallback system so the material's typographic voice survives the script change:
- **Font mapping (per role)**: map each substitute font to a CJK-capable pairing drawn from the material's voice - display serif/sans → 思源宋体/思源黑体 (Noto Serif SC / Noto Sans SC) or a brand-appropriate display face (e.g. 站酷小薇体 for warm/editorial); body sans → 思源黑体 (Noto Sans SC); mono → keep the Latin mono for digits/latin + a CJK fallback (most monos lack CJK). Weights must match the material's weight budget (e.g. Steep serif 400-only → Noto Serif SC 400).
- **Metric adjustments**: line-height bumps for CJK (~1.75-1.85 vs the Latin 1.35-1.5); letter-spacing returns to 0 (no negative tracking on CJK); NO `text-transform: uppercase` on CJK text; NO italic emphasis on CJK (use weight or color instead - mirrors Zara's rule).
- **Spacing convention**: 盘古之白 - insert a space between CJK and Latin/digits (`使用 Claude`, not `使用Claude`).
- **Loading**: add the CJK font to the Google Fonts `<link>` with `display=swap`, keeping the Latin substitute as primary so Latin glyphs render from the branded face and CJK auto-falls to the SC font.
- **Re-verify**: after switching language, re-run 15.6 gates - the CJK line-height bump moves card bottoms and can push content past y=900.

---

# APPENDICES (externalized to reference/)
- **设计系统安装命令** → `reference/design-systems.md`：§2 选定设计系统、装依赖前读（命令是 reality anchor，防幻觉版本号）。
- **Canonical Sources** → `reference/canonical-sources.md`：自造任何通用组件（按钮/表格/toast/导航…）前，先读对应官方源。
- **Apple Liquid Glass 诚实近似** → `reference/liquid-glass.md`：brief 要求玻璃拟态 / Apple 风 / backdrop-blur 时读（标注过的近似方案，非官方实现）。
