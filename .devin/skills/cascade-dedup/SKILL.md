---
name: cascade-dedup
description: 'Use when prompt-doctrine is duplicated, drifted, or conflicting across output-style embeds and external harness AGENTS files. Not for editing the canonical baseline itself.'
disable-model-invocation: true
---

# Cascade dedup

You remove duplicated prompt doctrine across the cascade family without ever weakening the canonical baseline. `system-prompt-baseline.md` is the whole file source of truth and wins every conflict. Nothing about the canonical gets edited here; suspect canonical content stops the run with the discrepancy surfaced.

Preview each consequence before rewriting doctrine at rest, bumping the catalog `releaseVersion`, or touching authorized external harness embeds. All other writes stay reversible local with version control as the rollback. Smoke test doctrine effects in a fresh session, since output styles load at session start.

What you need before starting: the canonical baseline file `system-prompt-baseline.md` (must exist), the six output style embeds (`plugins/dstack-core/output-styles/{axiom-mode,builder,duet,linus,dstack,benchmark}.md`), the two external harness embeds (`~/.omp/agent/AGENTS.md` and `~/.codex/AGENTS.md`), and explicit user authorization recorded in the run before any `benchmark.md` tail repair or external embed edit.

## Mapping zones and verifying the invariant

Each output style divides into two zones. The persona prefix above the charter `<role>` (the second `<role>` in the file) is the strip zone and the only dedup target. The tail from that charter `<role>` to end of file is byte identical with the canonical by invariant and never a dedup target. The `benchmark.md` auto generated margin runner preamble stays untouched, and that file has no eligible strip zone because its persona prefix sits inside the generated block.

Copy the canonical to a temporary file, then diff it against the equal length tail of each output style:

```
diff -q /tmp/canon.md <(tail -c "$(wc -c < /tmp/canon.md)" plugins/dstack-core/output-styles/X.md)
```

Tail drift signals a sync bug rather than duplication. Repair it by replacing the whole tail (charter `<role>` to end of file) with the canonical content as one block. Edits inside the invariant zone stay forbidden. `benchmark.md` repairs wait for explicit authorization recorded in this run; without it, leave the file unchanged and report the needed authorization. Record each diff result.

## Stripping prefixes and ledgering harness divergence

Scan the five hand authored prefixes and skip `benchmark.md`. Classify every sentence as one of four kinds. Normalized text (lowercased tokens, stopwords removed) at Jaccard 0.65 or above against a baseline rule marks a duplicate, so strip it and let the baseline copy stand. Jaccard 0.45 or above with opposing modal verbs (must/never, always/must-not) marks a conflict, so the baseline wins and the prefix line goes or gets rewritten. Persona voice (identity, tone, register) is not a directive, so keep it. Persona specific rules with no baseline pair stay unique directives and are kept. Scores in the 0.45 to 0.65 band without opposing modals stay unique directives for human review; never strip those. Every strip cites its baseline pair.

Handle each external file (`~/.omp/agent/AGENTS.md`, `~/.codex/AGENTS.md`) the same way at two levels: internal duplication within the file at the same thresholds, then directive level comparison against the baseline. Ledger each divergence exactly once. Harness adaptations (wording naming that harness tools or commands) are kept. Accidental drift (same rule, mutated wording) gets aligned to baseline wording. Conflicts resolve for the baseline unless the divergence fits harness specific tooling. Nothing stays unclassified.

## Applying, verifying, then committing

Apply all repo edits (strips, conflict resolutions, tail repairs) plus the `releaseVersion` bump when strips or conflict resolutions occurred. Pure re-syncs with zero strips skip the bump. Let the package surfaces generator (`scripts/render-plugin-surfaces.mjs`) re-render every package surface (`plugins/<id>/plugin.json` and `.claude-plugin/plugin.json`) from that one literal. Any `benchmark.md` change ships only with authorization recorded in this run.

Verify before committing: re-run the invariant diffs until all six tails read byte identical (6/6), and run `prek run --all-files`. A failing diff or check blocks the commit; report the failing check and the responsible file. Only then commit all repo files in one atomic commit including regenerated surfaces. A run that classifies fully but fails verification produces no commit; its divergence ledger and classification record still get reported, and the invariant needs re-verification before any later commit. External files change in place and never commit; close the report with an explicit warning listing each externally edited path for user review.

Failed verification leaves no commit to revert, so discard uncommitted repo edits with `git checkout -- <files>`. External edits have no version control safety net, so record original content before editing and restore from that record on failure.

What you hand back: the 6/6 invariant re-verification diff results, strips per file with baseline pair citations, conflicts resolved with the winner named, kept harness adaptations, the complete divergence ledger with one classification per divergence, every externally edited path flagged for review, the `prek run --all-files` result, and the `releaseVersion` decision (bumped literal plus regenerated surfaces, or the no bump rationale). Repo changes land as one atomic commit; external edits land in place and never commit.
