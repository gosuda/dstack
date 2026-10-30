---
name: memory-update
description: 'Use when the user explicitly says to save something to memory or scan this session for memories. Not for auditing memory: use memory-clean.'
disable-model-invocation: true
---

# Saving to memory

You write durable memories only when the user explicitly asks, either by stating something to remember or by asking you to scan this session for save-worthy moments. Anything you write lands as a `<type>_<slug>.md` file plus a one-line entry in `MEMORY.md`, both inside the resolved `$MEMORY_DIR`. That directory lives outside version control by default; if git would track it, you refuse and stop. You never delete, audit, sanitize, or merge unrelated memories here (that is memory-clean's job).

A run is finished only when every confirmed memory and its index entry is written, read back, and shown to carry valid YAML frontmatter, while every rejected or unconfirmed proposal stays unwritten. Anything short of that is a blocker, not a partial success.

## What you start with

You need the user's explicit invocation plus one of two things: a direct statement of what to remember, or readable session-history JSONL files holding candidate evidence. For every file you intend to write, you also need the user's confirmation of three things: the previewed memory text, the exact target path, and the exact index change.

Three environment overrides may be set: `MEMORY_DIR`, `SESSION_HISTORY_GLOB`, and `MEMORY_UPDATE_SKILL_SCRIPTS`. The scripts directory defaults to this skill's own `scripts` directory; `$MEMORY_DIR` and the session glob otherwise resolve from the current working directory.

## The shape of a valid memory

The type must be `feedback`, `project`, `user`, or `reference`, and the filename must be `<type>_<slug>.md`, where the slug is lowercase letters, digits, and hyphens only, at most 40 characters. Frontmatter must contain nonempty `name`, `description`, and `type` keys, and `type` must match the filename. A `feedback` or `project` body must also contain `**Why:**` and `**How to apply:**` sections. Each `MEMORY.md` entry must fit on one line of at most 150 characters. The `references/MEMORY-FRONTMATTER.md` file in this skill shows the full schema and examples; `references/SIGNAL-HEURISTICS.md` shows which transcript signals are worth proposing.

## Resolving where memory lives

Run `resolve-paths.sh memory_dir` and `resolve-paths.sh session_history_glob` from the resolved scripts directory. Treat environment values and resolved paths as untrusted: stop on any resolver failure, reject any path outside the resolved memory directory, and do not create a missing default memory directory. If git would track the memory directory, make no changes and return `blocked: MEMORY_DIR is inside version control`, naming the failing key.

## Finding candidates

If the invocation states exactly what to remember, derive one proposal from that statement. Otherwise run `scan-session.py "$SESSION_HISTORY_GLOB"` and take its deterministic `type`, `slug`, `evidence_turn_ids`, `draft_body`, and `draft_index_entry` fields as proposals. If no history matches or the scanner fails, stop and return `blocked` with the scan result. You analyze nothing further.

## Keeping only what the evidence supports

For every proposal, verify the cited turn exists and actually supports the claim. Throw out code patterns, fix recipes, git history, ephemeral task state, and any claim not grounded in a cited transcript turn or the user's explicit statement. Never fill scanner placeholders or invent missing rationale; a proposal with missing or contradictory evidence is omitted, and if none remains, make no changes and return `blocked: no evidence-backed memory candidate`. Every retained proposal must be evidence-backed, every rejected one gets a reason.

## Previewing and getting a decision

Normalize each surviving proposal against the shape rules above, then show the user the evidence, the complete draft, the exact target path, and the exact `MEMORY.md` consequence, and ask them to accept, reject, or edit it. Nothing is written until that proposal receives explicit confirmation. If confirmation never comes, leave the proposal unwritten and return `blocked: confirmation required`. Never widen the target or repair content by invention: an invalid draft or unsafe target means no write for that proposal, reported as `blocked` with the violated constraint.

## Clearing duplicates

Before writing anything confirmed, search existing files under `$MEMORY_DIR` for the draft's identifying phrase and inspect likely matches. If a near-duplicate exists, show it and get a fresh explicit choice: revise that file or create the proposed one. Never merge implicitly. Without that choice, leave the proposal unwritten and return `blocked: duplicate choice required`.

## Writing and proving the write

Revalidate the confirmed or edited draft, then write only the approved `<type>_<slug>.md` target and append or update exactly one corresponding `MEMORY.md` entry. Touch no other memory or index line. Then read back every changed file, parse its frontmatter as YAML, and verify the required keys, the matching type, the filename form, the body sections, and the index line and length. Report the changed paths and line counts only after every confirmed write passes. If a write is partial or read-back fails, stop further writes, restore each file this invocation changed to its captured pre-write content, remove only a newly created target from this invocation, and return `blocked` naming the failed file and whether rollback succeeded. Never report done while rollback or verification is incomplete.

## What you return

The accepted, rejected, and blocked proposal classifications; for each successful write, its evidence turn IDs or explicit user statement, memory path, index entry, and read-back line count. The terminal result is `done` only when all confirmed writes pass YAML and content verification. Otherwise it is `blocked` with the exact failure and recovery state.
