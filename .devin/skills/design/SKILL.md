---
name: design
description: 'Use when starting UI work, defining palettes or tokens, fixing AI-generic UI, or persisting a design system to DESIGN.md (modes: implement, persist). Not for live URLs.'
---

# Design

Direction comes before tokens, and tokens come before code. The picked direction is the contract. Restraint is the default, and decoration earns its place only when a named surface goal demands it. Aim for balance, neither maximalism nor minimalism.

This skill runs in one of two modes. Implement mode (the default when unstated) carries a direction through to working UI. Persist mode proposes a system, previews it, and persists it to DESIGN.md only after the user approves. Implement mode is done when one defensible direction lives consistently across palette, typography, spacing, density, and motion, and the audit passes clean. Persist mode is done when the approved system sits in DESIGN.md. All writes stay local to the current project directory, and persist mode additionally writes DESIGN.md, its CLAUDE.md pointers, and preview artifacts. Roll back through version control. Nothing here mutates a remote.

## Start from the surface and its constraints

Name the surface under design (landing, dashboard, settings, docs, one-screen tool, TUI, CLI, or desktop app) and the runtime in play (vanilla CSS and HTML, React with Tailwind or shadcn, Bubble Tea or Ratatui or Textual, clap or cobra or cmdliner or typer, Tauri or Slint or egui or Iced, Qt or QML). State the primary user and the density target, noting assumptions where the caller supplied neither. Load any existing project context (PRD, brand brief, design tokens, component library, an existing DESIGN.md to extend) when present. In persist mode, read the existing DESIGN.md, tokens, and brand guidance first, and name missing context instead of inventing it. Never infer a design from defaults when the brief or the target surface is missing. Stop and request the missing input instead. Name the runtime before deriving tokens in implement mode, and never implement against an assumed runtime. Stop and ask when it is unidentified.

First, frame the surface. Identify the register first: brand (marketing, landing, campaign, long-form, portfolio, where design is the product) or product (app UI, admin, dashboard, tool, where design serves the product). Use the first match among these cues:

| Priority | Cue |
|---|---|
| 1 | Wording in the task ("landing page" or "campaign hero" points to brand; "dashboard" or "settings panel" points to product) |
| 2 | The surface in focus or route segment (`/marketing/*` versus `/app/*`) |
| 3 | The register field in project context |

Then capture the surface, primary user, density target, and motion budget in milliseconds, and write one sentence of physical scene (who, where, ambient light, mood) that forces the dark or light decision. Category names alone never force that answer.

**Which reference to load.** The charter below is the whole audit; the reference files carry depth. Load by surface: web or React surfaces, `references/web.md` and `references/react.md`; TUI or CLI surfaces, `references/tui.md` and `references/cli.md`; desktop surfaces (Tauri, Slint, egui, Iced, Qt), `references/desktop.md` and, for Qt, `references/qt.md`; motion questions, `references/motion.md`; direction breadth, `references/diversity.md` and `references/paradigms.md`; any Chinese, Japanese, or Korean content, `references/cjk.md`, then the single-locale file (`references/chinese.md`, `references/japanese.md`, `references/korean.md`); tokens and theming, `references/design-systems.md`; audits and critique, `references/anti-slop.md` for the full tell catalogue plus `references/soul.md`, `references/personas.md`, `references/cognitive-load.md`, `references/interaction-design.md`, and `references/ux-writing.md` as the surface demands. Per-locale files do not backlink; always re-enter through this list.

## Diverge, then converge on one direction

Dispatch one exploration per direction, three to four directions in parallel, each with a constraint that forces contrast (post-minimalism versus neo-brutalism versus Material 3 versus Fluent, or named taste anchors pulling in opposite directions). Useful diversity techniques include verbalized sampling, actor-critic per candidate, persona injection, temperature shifts, most-unlikely reframing, and an anti-pattern catalog. When two directions read alike, the field is too thin to pick from. Re-dispatch with sharpened, opposing constraints until contrast is real. A direction set is ready when no two directions read alike under a headline-swap test.

Give every direction the same fixed shape:

| Field | What it carries |
|---|---|
| Name | One or two words |
| Taste anchors | One or two named references (Linear, Stripe, Things 3, Rosé Pine, Are.na) |
| Palette stub | Four to six OKLCH swatches, never the default Tailwind ramp |
| Type pair | Display plus text, named families |
| Spacing subset | Committed values from the scale (for example 4/8/16/24/48) |
| Motion | Budget in milliseconds with one easing curve |
| Component primitives | Persist mode only: the shared primitives the system will offer |
| Interaction states | Persist mode only: how those primitives behave across states |

Pick through per-axis single-select questions, one axis each for direction, density, motion budget, and type pair. The recommended option carries `(Recommended)` and sits first, and ticking it accepts the default. Never use multiSelect for axis-with-default override semantics, since it collapses independent decisions into one ambiguous checklist. Reserve multiSelect for additive picks only. Selection is complete when one option is chosen per axis and the picked direction is named.

Derive tokens from the picked direction. Cover color, type, space, radius, shadow, and motion, each as a referenced token, never hardcoded. Pick the color strategy before picking colors:

| Strategy | Coverage | Home |
|---|---|---|
| Restrained | Tinted neutrals plus one accent at 10 percent surface coverage or less | Product default |
| Committed | One saturated color carrying 30 to 60 percent of the surface | Brand default for identity pages |
| Full palette | Three or four named roles, each deliberate | Brand campaigns, product data visualization |
| Drenched | The surface is the color | Brand heroes, campaign pages |

The 10 percent accent cap belongs to Restrained only. Express tokens in the runtime native system: CSS custom properties for web, theme or design-token objects for React, style structs for TUI and desktop, palette constants for CLI. Component code references tokens, and tokens always precede component code. A new spacing value, a third type family, or a hardcoded color appearing mid-build signals drift. Revert to the committed set instead of patching around it.

## Build it or persist it

In implement mode, build against the runtime, hold the cross-surface invariants below on every runtime, and audit the result against the anti-slop charter. The work is done when the implementation references the committed tokens and the audit flags no tell and no invariant violation. When the audit fails, the done condition does not hold. Fix the tell at its source rather than compensating with more decoration. Never present an unaudited or half-implemented direction as done. State which steps are complete and which remain.

In persist mode, produce a preview the user can react to (mockups or a self-contained HTML preview for the target surface) that reflects the proposed tokens, not generic defaults. Present the proposal and preview, request approval, and write nothing to DESIGN.md before approval arrives, since approval is the gate. On approval, persist the system in DESIGN.md (tokens, component primitives, application rules), add CLAUDE.md pointers naming DESIGN.md as the design source of truth, and keep the preview artifacts alongside DESIGN.md. On rejection, revise the system and preview, then re-present, and never persist an unapproved system. When no approval arrives within the session, leave DESIGN.md unchanged and mark produced artifacts unapproved, since they are not the source of truth.

## Invariants held on every runtime

- Color is an input, never a default. Derive a custom OKLCH palette from the picked direction, never the default Tailwind, Material, or Bootstrap ramp.
- The spacing scale is 4/8/12/16/24/32/48/64. Pick a subset matching the density target, commit to it, and hold it. A new value mid-build is a smell.
- Use at most two type families: display plus text. A third is a smell unless the direction explicitly demands it (for example a mono accent for code).
- Budget motion in milliseconds with one easing curve per surface. Name the transitioned properties (for example `transition: opacity 120ms ease, transform 120ms ease`) so layout and paint never animate together. A blanket `transition: all` is forbidden.
- Put semantic structure before class names: `nav`, `main`, and `article` first, utility classes second. Class soup over weak structure is slop.

## Anti-slop charter used by the audit

Signs of the AI-generic look:

- Purple-blue or purple-pink gradient, which betrays a self-generated palette.
- Inter alone as the type system, the default of every template, with no commitment and no contrast.
- Centered hero plus three-column feature grid, the landing-page silhouette that reads as preset.
- Glassmorphism on every surface, where translucence loses meaning because nothing stays opaque.
- Uniform `rounded-lg` on every element, where radius without hierarchy is decoration, not signal.
- Uniform `shadow-md` across the surface, where elevation conveys nothing.
- Blanket `transition: all`, which animates layout, color, and transform together and guarantees jank.
- `font-family: system-ui`, which abdicates the type decision.
- Default Tailwind palette (slate-500, blue-500), the costume of framework defaults.
- Colored card borders asserting structure, since borders are the wrong tool for hierarchy.
- Emoji icons in production UI, which are hostile to accessibility, fragile across locales, and read as draft.

Signs of overkill compensation, the louder cousin of slop:

- Sprites on every empty pixel, decorating where information density is missing.
- A gradient on every section background, where every section marked important means none is.
- Animation on every element entrance, which spends a budget that should be spent once.
- Multi-paradigm mash (neo-brutalism shadow on a glass card on a Material 3 button), where paradigm conflict reads as confusion, not eclecticism.
- Decorative noise compensating for a thin idea. When the surface earns its weight, restraint amplifies it.
