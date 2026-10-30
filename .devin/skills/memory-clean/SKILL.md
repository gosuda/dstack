---
name: memory-clean
description: 'Use when a human asks to audit memory or find stale or duplicate memories. Not for writing new memories: use memory-update.'
disable-model-invocation: true
---

# Memory clean

Durable memory rots: entries go stale, near-duplicates accumulate, index links dangle, and suspected credentials creep in. This skill audits the memory store, shows the human exactly what it proposes to change, applies only what the human confirms, and proves the result with a fresh audit. Start it only when a human explicitly asks to audit memory or find stale or duplicate memories. Writing new memories belongs to memory-update, not here.

Every repair is human-gated. Preview each target and its consequence, and get explicit confirmation for each repair group before changing data at rest in `$MEMORY_DIR`, which lives outside version control by default. An override the resolver reports git would track is refused. The only other write is the snapshot copy taken first, and rollback restores the store from that snapshot.

## What you need before you start

- The project whose durable memory store is being audited, or an explicit `MEMORY_DIR` override.
- The sibling skill memory-update in the same plugin. The path resolver lives there, so memory-clean cannot run without it.
- Optionally, `SESSION_HISTORY_GLOB` for session-based staleness evidence. `MEMORY_CLEAN_SKILL_SCRIPTS` relocates only the bundled `audit-memory.py`; it never selects the resolver.
- The path resolver must produce an existing memory directory. Session history may be omitted, but then session-based feedback staleness cannot be assessed and must be reported as unavailable.

## Resolving the store location

Run `../memory-update/scripts/resolve-paths.sh memory_dir` and `../memory-update/scripts/resolve-paths.sh session_history_glob`. When `MEMORY_UPDATE_SKILL_SCRIPTS` is set, run `$MEMORY_UPDATE_SKILL_SCRIPTS/resolve-paths.sh` instead; that variable is memory-update's relocate hook, not a clean-skill hook. Reject resolver errors, control characters, forbidden shell metacharacters, and unsafe whitespace rather than interpreting them. The resolver refuses a memory directory git would track. Move on only when both paths resolve without error; otherwise stop with a blocked diagnostic.

## Auditing and repairing in order

1. State the scope boundary: the resolved `$MEMORY_DIR` and nothing else. Do not create new memories, edit another store, redact suspected credentials, or widen the requested scope. This step holds when the boundary is stated and no out-of-scope target is queued.
2. Before any repair, take a timestamped recursive snapshot of `$MEMORY_DIR` in `/tmp` and record its path. This step holds when the snapshot directory exists and its path is recorded, or when the run stops without changing the store.
3. Run `audit-memory.py "$MEMORY_DIR" "$SESSION_HISTORY_GLOB"` and preserve its JSON output. The deterministic audit checks index orphans and dangling links, schema and required sections, index size limits, credential patterns, fix-recipe and path-pinned content, relative dates, body-line Jaccard similarity above 0.70, missing reference targets, past project dates without historical-anchor phrases, and feedback rules contradicted by session evidence. This step holds when the JSON report is captured and preserved regardless of exit status.
4. Render every finding under exactly one severity (critical, warning, informational) with its evidence attached. For each staleness finding, include the reported session identifiers and available contradiction context. Label unavailable session evidence instead of inventing it.
5. Group proposed repairs by mechanism and show an exact preview of each: add an orphan to `MEMORY.md`; remove a dangling index line; merge a near-duplicate pair while naming the superseded file and index update; make a targeted structural edit; or update, archive, or delete a stale memory. Show a file's content before proposing its deletion. For a suspected credential, report the critical finding and make no redaction. Nothing unpreviewed gets queued for repair.
6. Get explicit human confirmation separately for each repair group. Confirmation for one group never authorizes another. Unconfirmed groups stay unchanged. This step holds when every repair group has a confirmed or unconfirmed decision recorded.
7. Apply only confirmed repairs inside `$MEMORY_DIR`, preserving unrelated content. When an applied repair fails partway, stop further mutation and restore every file that group touched from the snapshot before reporting the failure.
8. Re-run the same audit against the same resolved inputs. Success needs zero critical findings. Report all residual warning and informational findings. Do not claim success when the audit fails, evidence is unavailable, or critical findings remain.

## When something goes wrong

- Invalid or missing path: stop before snapshot or mutation and return `blocked` with the resolver diagnostic.
- Memory directory git would track: stop before snapshot or mutation and return `blocked: MEMORY_DIR is inside version control`.
- Snapshot failure: stop without mutation and return `blocked` with the failed snapshot target.
- Audit failure or malformed report: keep any valid partial report, make no repairs, and return `blocked` with the diagnostic. Never infer omitted findings.
- Missing staleness evidence: complete the structural checks, mark session-based staleness unavailable, and return `blocked` rather than treating absence of evidence as freshness.
- Confirmation absent or ambiguous: leave that repair group unchanged and report it as unconfirmed.
- Partial repair failure: stop, restore that group's touched files from the recorded snapshot, and report the attempted changes and the restoration result. When restoration fails, return `blocked` and identify every potentially changed file.
- Critical findings after re-audit: return `non-converged` with the remaining critical findings and residual warnings or information. Do not widen scope or invent a fix.

## What you hand back

The snapshot path, the resolved audit scope, the severity-grouped JSON findings, per-group previews and confirmation decisions, applied and restored file lists, the fresh re-audit result, residual warnings and information, and exactly one terminal classification: `complete`, `blocked`, or `non-converged`. The `complete` reading is valid only when the fresh audit contains zero critical findings.
