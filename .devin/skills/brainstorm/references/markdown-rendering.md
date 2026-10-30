# Markdown Rendering

This is a format-rendering reference, it describes how to render any artifact in markdown, independent of which skill is producing it.

It is paired with a section contract (`brainstorm-sections.md`, etc.) that describes *what* the artifact contains. This reference describes *how* markdown specifically presents it. The same content rendered by different skills shares the same markdown principles.

## Hard invariants

These hold regardless of which skill produced the artifact.

- YAML frontmatter at the top of the file. Standard `---` delimited block containing the artifact's stable metadata (title, date, type, etc.: exact fields are per-skill, defined in the section contract).
- ASCII identifiers in anchors. Markdown headings auto-generate anchors from the heading text. Keep headings ASCII so anchors are predictable (`#implementation-units`, not `#implementación-units`).
- Repo-relative paths for file references. Always. Never absolute paths: they break portability across machines, worktrees, teammates.
- No HTML mixed in. Keep the markdown pure. No `<div>`, no `<details>`, no inline `<style>`. If a layout idea only works as HTML, defer it to the HTML rendering. Markdown stays markdown.
- No fixed-width line wrapping. Do not hard-wrap prose to a column (e.g. 80 chars). Write one sentence per line, or let each paragraph flow as a single line. The artifact is read rendered and shared, where fixed wraps add nothing and only produce noisy mid-sentence diffs; markdown joins soft line breaks within a paragraph, so wrapping never changes the rendered output.
- DStack plan sections use stable headings. For plan artifacts, render the required sections with exact ASCII headings so agents can find them by heading scan: `## Goal Capsule`, `## DStack spec outline`, `## Planning Outline`, `## Implementation Units`, `## Verification Contract`, `## Definition of Done`, and optional `## Appendix`. Requirements-only artifacts omit the plan-only sections rather than emitting empty placeholders. These stable headings are the wayfinding contract.
- Goal Capsule is top-loaded. It appears before DStack spec outline and long appendices for fast orientation: not a hidden machine copy.

## Format principles

These shape what "good" markdown looks like; the agent applies them per artifact based on content shape.

### Semantic naming and heading format

Headings, requirements, units, flows, and decisions MUST use concise, meaningful names representing their actual purpose, never opaque prefix+counter codes (`R1`, `U1`, `A1`, `F1`, `AE1`, `KTD-N`, `R<N>`, `U<N>`) or parenthesized opaque codes in human headings and labels.

```markdown
- Session pagination: The plan returns paginated sessions.   ← right (purpose-named)
- R1. The plan returns paginated sessions.                   ← wrong (opaque counter prefix)
```

Same applies to unit headings: `### Unit: Cloak detection in preflight contract` or `### Cloak detection in preflight contract` (never `### U1. Cloak detection in preflight contract`).
### Content shape: prose vs bullets vs tables

The same content can be rendered three ways; the agent picks per content shape, not by template default.

- **Prose** when the content has narrative flow (motivation, decision rationale, problem framing). Bullets fragment narrative into disconnected pieces.
- **Bullets** when items share a parallel shape but each carries enough prose to not fit a table cell.
- **Tables** when 5+ items share uniform structure (`ID + body`, `name + value`, `decision + rationale`, `risk + mitigation`). Tables scan faster at that scale and unlock additional columns (status, traceability, severity) that bullets cannot accommodate cleanly.

The test: which shape would a reader scan fastest for this content? If items have parallel structure and 5+ instances, table. If items are 3-5 and each has a few lines of prose, bullets. If the content is a single narrative thought, prose.

### Bold leader labels within bullets

When a bullet has substructure that benefits from named fields (Key Flows with Trigger / Actors / Steps / Outcome, Acceptance Examples with Covers / Given / When / Then), use bold leader labels at the start of nested bullets, not deeper heading levels.

```markdown
- Anonymous capture
  - **Trigger:** Agent enters Step 2a with no session.
  - **Actors:** Unauthenticated visitor, Background sync worker
  - **Steps:** Preflight detects cloak; agent launches; capture proceeds.
  - **Covered by:** Session pagination, Token-bucket rate limiting, Preflight cloak detection
```

This gives the bullet structure without needing H4/H5 headings that would clutter the doc and break TOC generation.

### Section separators

For substantial artifacts, use horizontal rules (`---`) between top-level H2 sections. Omit for short docs where separators would dominate.

### Tables for genuinely comparative info only

Use tables for the uniform-shape case in "Content shape" above. Don't use tables to render content lists that are really bullets, markdown tables are noisier in raw form and worse for diffs.

## Section anatomy

How section types commonly render in markdown. These are patterns, not contracts, the agent picks the shape that fits the content.

- Goal Capsule: bullets or a small table for objective, authority, execution profile, stop conditions, and tail ownership.
- DStack spec outline: H2 section containing Summary, Problem Frame, Requirements, and product-scope subsections. Put Requirements under `### Requirements` so review tools can distinguish Product Requirements from implementation detail.
- Planning Outline: H2 section for technical design decisions, assumptions, and sequencing.
- Summary / Problem Frame: prose paragraphs.
- Requirements: bullets or subheadings with concise meaningful purpose names and semantic anchors, never opaque `R<N>.` prefixes. When requirements span more than one concern, grouping under bold inline headers is the default shape, not optional polish (group by capability, not by discussion order); render a flat list only when every requirement is about the same thing. When requirements have status, traceability, or severity that warrant additional columns, escalate to a table using purpose names for rows.
- Implementation Units: H3 heading per unit naming its concrete purpose (e.g. `### Unit: Cloak detection in preflight contract`), never `U<N>.` prefixes. Fields (Goal, Files, Patterns, Test Scenarios, Verification) render as bullets with bold leader labels, or as sub-headings if the field has multi-paragraph content.
- Verification Contract / Definition of Done: use tables when commands, applicability, unit references, and done signals share a uniform shape. Reference units by their purpose names rather than numeric counters. Name concrete repo commands such as `bun test` rather than generic "run tests" when the repo has known commands.
- Key Technical Decisions: bullets or cards with bold decision name + prose rationale, never numbered `KTD-N` prefixes.
- Key Flows / Acceptance Examples: bullets with descriptive flow/scenario names and bold leader labels (Trigger / Actors / Steps / Outcome / Covers / Given-When-Then). Actors and covered requirements are referenced by their semantic names.
- Scope Boundaries: bullets, optionally split into "Deferred for later" / "Outside this product's identity" sub-headings when the positioning distinction matters.

The agent picks more elaborate or simpler shapes based on what each specific artifact's content needs.

## Diagrams

When the section contract calls for a diagram (architecture, sequence, flowchart, state machine, swim lane, data-flow), author it as a Mermaid source in `assets/` beside the document, rendered to a committed SVG and embedded with a caption.

````markdown
![Approval path from draft to publish](assets/approval-path.svg)

> A draft needs one reviewer; anything touching billing needs two.
````

The source that produced it lives at `assets/approval-path.mmd` and is committed with the SVG.

Markdown's diagram affordances are limited compared to HTML. For quantitative comparisons (bar charts, scatter plots) markdown has no native equivalent, use a table with the data and let prose or caption carry the interpretation. The richer visualization happens in the HTML rendering.

For a **UI/layout shape** that would be a wireframe in HTML, markdown has no inline-SVG wireframe affordance. Render the region composition as a nomnoml layout diagram (or describe it in prose), never hand-draw a box-drawing/ASCII wireframe; it violates the no-box-drawing-characters rule and reads poorly. The wireframe proper is an HTML-only affordance.

## Inline code and code blocks

- **Inline code** for identifiers (variable names, function names, flag names, file paths, technical symbols that are not section anchors).
- **Fenced code blocks** with language tag for code, shell commands, API request/response samples. Always specify the language for syntax highlighting and accessibility.

````markdown
The flag `--cdp-url` accepts a URL.

```bash
browser-use --cdp-url http://localhost:9222
```
````

## No process exhaust

Engineering process metadata stays out of the artifact:

- No "captured at Phase X" notes
- No `## Next Steps` pointing to the next skill
- No italic provenance lines ("*Brainstorm completed 2026-05-13*")
- No engineering-flow shepherding ("Now read this file:", "Next, run that command:")

This information belongs in commit messages, tool output, and agent transcripts, not in the artifact a reader returns to weeks later.

## Frontmatter shape

Per-skill frontmatter fields are defined in each skill's section contract (`brainstorm-sections.md` lists brainstorm frontmatter). Common rules:

- YAML at the top of the file, delimited by `---` on its own line above and below.
- Field names in lowercase snake_case (`created_at`, `topic`, not `CreatedAt`, `Topic`).
- **No status / lifecycle field.** Artifacts are point-in-time records, not tracked work items. Do not introduce a mutable `status` field or an `active → completed` lifecycle: whether the work shipped is derived from git, not stored in the doc.
- Stable across artifact revisions: never rename or repurpose a field.

## Post-write audit

Before declaring the markdown file written, scan it for these common slips:

- Headings, requirements, units, flows, and decisions use concise meaningful purpose names, never visible R1/U1/A1/F1/AE1/KTD-N display counters.
- No HTML elements mixed in.
- All file paths are repo-relative.
- Horizontal rule separators between H2s (for Standard / Deep artifacts).
- No process exhaust (Phase X notes, Next Steps pointers, provenance lines).
- Tables only where 5+ uniform-shape items justify them.
- Frontmatter has all the per-skill required fields with reasonable values.
