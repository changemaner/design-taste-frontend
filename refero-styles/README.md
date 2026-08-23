# refero-styles — Materials & Attribution

This directory contains 30 sets of design tokens (DESIGN.md / tokens.json / variables.css / theme.css), each extracted from a real brand's **public web pages** (collected via [Refero](https://refero.design)) and reorganized for design study and AI-assisted design work.

## Disclaimer — Style Reference, Not Affiliated

- These materials are **style references only**. This project is **not affiliated with, endorsed by, or sponsored by** any of the brands named here (directories, token names, or documentation).
- All brand names, logos, color identities, and trademarks belong to their respective owners. No ownership is claimed, and none are transferred by this repository's license.
- The materials in this directory are **not covered by the repository's MIT license**. They are distributed for study and as design references; if you plan commercial use that mirrors a specific brand's identity, clear it with the brand yourself first.
- Outputs generated with this skill are "inspired by" a style. Do not present them as official brand material.
- Token values were extracted from public pages and may drift from the brands' current design systems; provided as-is, without warranty.

## Layout

```
refero-styles/
└── <Brand>/            # one directory per style (see ../metadata/style-map.json for slugs)
    ├── DESIGN.md       # narrative fact source: palette, type system, signature moves
    ├── tokens.json     # machine-readable value layer (the ONLY numeric source)
    ├── variables.css   # CSS custom properties (implementation reference)
    └── theme.css       # Tailwind v4 @theme format (implementation reference)
```

Adding new styles: see `../annotation-guide.md` for the annotation vocabulary and field rules.
