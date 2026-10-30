# Refresh: maintain `docs/solutions/` against the current code

Owner. autolearn/SKILL.md section 6 inlines the refresh loop. Do not recopy.

Read this for `autolearn mode:refresh [scope]`. Bounded refresh only: record only invariants, never implicitly delete or migrate stored records. Section 6 of autolearn/SKILL.md governs scope, delete authority, citation checks, validation, provenance, and headless stale marking; this file does not restate them. Classify every candidate doc into exactly one outcome (in headless runs the owner stale disposition also applies):

| Outcome | Meaning | Default action |
|---------|---------|----------------|
| **Keep** | Generalized invariant still accurate, material, enforced or proven | No edit. Report reviewed-and-trustworthy. |
| **Update** | Core invariant mechanism correct, references drifted | Evidence-backed in-place edits |
| **Consolidate** | Two+ docs overlap heavily, both correct | Merge unique content into the canonical doc, repoint references, delete the subsumed one only with explicit authority |
| **Replace** | Old guidance is now misleading, better invariant answer known | Write a validated successor (bundled validator exits 0), then delete the old |
| **Delete** | Domain gone, fully redundant, inbound references absent or decorative | Delete only with explicit authority; never archive into `_archived/` |

## Execution notes

- No candidate docs at all → report it and point the user at create mode.
- Pick the lightest interaction path: Focused (1-2 files) → investigate, then recommend; Batch (up to ~8 mostly-independent docs) → grouped recommendations; Broad (9+, ambiguous, or repo-wide) → triage first (inventory frontmatter, cluster by area, spot-check whether referenced files still exist), then investigate in batches.
- Investigators are read-only subagents: return path, evidence, recommended action, confidence, open questions; never write. Deletes, commits, and frontmatter metadata stay with the orchestrator. The one writing subagent is the Replace successor-drafter; even there the orchestrator validates the result, deletes the old file, and commits.
- Tag memory-sourced findings `(auto memory [claude])`.
- Consolidate reverse case: a doc that grew to cover several genuinely independent problems is a split candidate.
- Replace successor-drafter input: the old doc's full content, an investigation-evidence summary (what changed, what the code does now, why the old guidance misleads), the target path + category, and the contents of `references/schema.md` + `assets/solution-template.md` (never invented from memory). Successors state the generalized mechanism with supported scope, enforcement or proof, and material consequence. `supersedes: [old-filename]` in the successor is optional.

## Interactive questions

Most Updates and Consolidations apply directly without asking. Ask only when: the right action is genuinely ambiguous; about to Delete without explicit authority; about to Consolidate with no clear-cut canonical; about to Replace. One question at a time, prefer multiple choice, lead with the recommended option.

## Commit

One concern per commit, DStack `Op:` trailer in the body.
