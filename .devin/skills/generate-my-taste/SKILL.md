---
name: generate-my-taste
description: 'Use when asked to generate a personal taste skill from local evidence. Not for applying an existing taste register, and only for taste skills.'
disable-model-invocation: true
---

# Generate my taste

You build a personal taste skill from what the user actually does, as evidenced locally. The generator produces `<name>-taste` skills only, nothing else. It writes exactly three files (references first, the skill last), shows a synthesis preview, and writes nothing until the human picks the draft option at the preview gate. A collision writes to a draft path instead of overwriting. Update in place is allowed only for an existing `*-taste` skill the user explicitly selected, and then it replaces only the three generated files while everything else in that skill stays untouched. There is no remote, credential, publish, deploy, or irreversible change; rollback is undo.

Applying an existing taste register is a different job and out of scope here. Generating anything that is not a taste skill is out of scope too.

What you need before starting: a target skill name (optional, defaults to `<user-or-handle>-taste`, and you ask only when it is genuinely ambiguous); an evidence scope (optional, indexed recall first with local files as fallback); a domain set (optional, prose plus code plus design plus decision); anchor picks (optional, defaulting to the top 5 evidence-ranked candidates); and local evidence drawn from these optional sources:

- Indexed memory-search tools exposed by the current harness, or indexed session-history tools exposed by the current harness
- Local memory files under `~/.claude/projects/**/memory/*.md`, plus `~/.claude/CLAUDE.md` and `~/.claude/CLAUDE.local.md`
- Local transcript stores for Claude Code, Codex, Gemini CLI, OpenCode, Amp, Pi, and Cursor

## Naming the skill

Resolve the target name first. Ask Q1 as a single-select only when the name is ambiguous: `<user-or-handle>-taste (Recommended)`, updating an existing `*-taste` skill when that is detected and intended, or a custom name through free-text annotations.

## Reading the evidence

Scan in order, preferring indexed sources and falling back to files: indexed memory-search tools, then indexed session-history tools, then local memory files, then local transcript stores. Every source class is optional. Record a missing class as `not present` or `not readable` and keep going with what is available. Extract compact evidence per signal (a quoted phrase, the source class, a path or index label, and the inferred signal). Never dump exhaustive transcripts.

From the scan, pull three signal kinds: influences, slop signals (Side A), and overkill signals (Side B).

## Keeping only anchors the evidence earns

An influence becomes an anchor only when it has all five of these: a portable principle across at least two domains; recognizable Side A and Side B failure modes; a concrete exemplar; contrast value against neighboring candidates; and a non-random operational framing. An influence from outside the usual pool is included only when it clears the same five; otherwise map the signal to the nearest qualifying influence and cite the mapping.

Confirm 5 anchors, or confirm fewer and report the gap. When fewer than 5 qualifying anchors can be derived, stop and report the missing evidence and the blocked anchor count. Partial results are never written, and no slot markers or fabricated anchors are ever emitted. Slot markers may appear in `assets/`, never in generated output.

## Confirming the open forks

Ask only forks that are still unresolved, at most three questions per ask-user tool call, with the recommended option first and `(Recommended)` appended. Q2 is evidence scope (single-select: ICM plus local files, local files only, or current project only). Q3 is domain set (single-select: four-domain, four-domain with one emphasis, or stop for a custom template). Q4 is anchor picks, and it is the only `multiSelect` exception: set `multiSelect: true`, require exactly 5 picks, present 8 to 12 candidates with the top 5 evidence-ranked first, ask one correction question when more or fewer than 5 are selected, and fall back to the top 5 evidence-ranked candidates when the user accepts without edits. Evidence-backed defaults pass straight to preview without extra questions.

Then derive the preview defaults from the evidence rather than asking more upfront questions: charter Side A and Side B clusters grouped by prose, code, design, and decision; hybrid audit plus anchor mode discipline with slash-arg override, unless the evidence supports audit-only or anchor-only; and draft-by-default collision handling, with update in place only for a detected `*-taste` skill the user selected. When evidence contradicts a default, ask one separate single-select fork after Q4 and before the preview.

## Previewing before writing

Compose the synthesis preview: composed frontmatter (`name` and compact `description`); an evidence summary (source classes scanned, strongest quoted signals, missing optional sources); a 5-anchor table (anchor name, influence, concept, evidence rationale); the Side A charter; the Side B charter; the mode block; the generated file paths; and the collision policy with its ownership boundary. Show it, then gate with a single-select: `Write draft (Recommended)`, `Revise preview`, or `Abort`. On abort, write nothing. On revise, apply the specific corrections and gate again. Nothing is written before this gate returns the draft choice.

## Writing the three files

Create the target directories first, then write in this order: `references/anchors.md`, then `references/charter.md`, then the generated `SKILL.md` last. A collision writes under `~/.claude/claude/skills/<name>-taste.draft/`; a clean write uses `~/.claude/claude/skills/<name>-taste/`. Update in place, only for a detected `*-taste` skill and only when selected, replaces just `SKILL.md`, `references/anchors.md`, and `references/charter.md`, preserving every other file in that skill and every file this generator does not own.

Build the generated `SKILL.md` from `assets/SKILL.template.md` as the skeleton, in this fixed order: frontmatter, posture, modes, two-sided charter, anchors, audit output shape, anchor mode output shape, auto-clarity exception. Emit exactly 5 cross-domain anchors across prose, code, design, and decisions. Audit mode walks all 5 anchors, citing Side A or Side B where violated, and closes with the top 3 fixes. Anchor mode loads the 5 anchors and charter bans as imperatives. The auto-clarity exception suspends the taste register for destructive confirmations, security or data-loss warnings, order-sensitive procedures, and direct clarification requests.

Never generate generic validation openers, hedge prefaces, phrases that invite skipping the discipline, a summary after every answer, a weighted rubric, an exhaustive transcript dump, or unresolved placeholders. Confirm with an anti-slop search that none of these patterns made it into the output.

Ambiguity has one remedy: an unclear name, or an anchor count that is not 5, gets one correction question, never a guess. A missing evidence source is recorded as `not present` or `not readable` and the run proceeds. A collision without update in place selected always takes the draft path, never an overwrite. An off-catalogue influence that fails the five criteria is mapped to the nearest qualifying influence with the mapping cited, never invented into an anchor.

## What you hand back

Three written files at the target or draft path (`references/anchors.md`, `references/charter.md`, and the generated `SKILL.md` last), plus a report listing the written paths and verification notes: evidence source classes scanned, question shapes used, generated skill order, anti-slop search results, compact frontmatter description, and write-safety confirmation.
