---
name: dedup-skills
description: 'Use when asked to deduplicate a skill tree, fold overlapping skills, or cut the skill count: analyze, gate per family, then fold. Not for prompt-doctrine cascades: use cascade-dedup.'
disable-model-invocation: true
---

# Dedup skills

You shrink a skill tree by folding skills that do the same job with a parameter changed. The work runs in three movements: you map the tree and propose families, the human approves or strikes each family, and only then you fold what was approved. The analyze pass writes nothing but the fold ledger. The fold pass runs only on an explicit user command naming approved families, and lands one commit per family. There is no remote mutation at any point; rollback is `git revert` of that family's commit.

A fold means the survivor absorbs the members' unique steps, the member directories are deleted, pointers are rewritten, attribution and the changelog move with the text, and generated surfaces are re-rendered. A run is complete when every family in the ledger carries a decision, every approved family is folded in its own commit, the checker reports no dangling pointer, and the removed and remaining counts are measured rather than projected.

You need three things before starting. The target tree path, defaulting to `plugins/`, where every `<plugin>/skills/<slug>/SKILL.md` counts as a skill. The tree's attribution file (`licenses/NOTICE` or equivalent), read in full before scanning; a license-covered skill folds like any other, except the attribution travels with the absorbed text. And optionally a reduction floor, a count or percent the fold must clear. The floor never loosens the fold criteria: if defensible families cannot reach it, you report the shortfall at the gate instead of broadening a family or relaxing consent.

## Skills that do one job with a parameter changed

Two skills belong in one family when a user asking for one would accept the other's procedure with a single parameter changed. Three evidence sets, in priority order, say so: pointer neighbors, where descriptions route to each other through `Not for <x>: use <y>` (adjacency is evidence, never proof, and a component chaining distinct jobs such as implement, test, and ticket is several families or none); parameter siblings, where slugs differ along one axis (`from-<seat>-perspective`, `watch-<mode>`, `culture-<situation>`) and the procedures match except for that parameter; and mode siblings, where descriptions differ only by a mode word (`exhaustive`, `batch`, `interview`) over one procedure.

The survivor is the member with the most general name. A member's unique steps enter the survivor as an input or a named mode, never as a second procedure. No alias directory, stub `SKILL.md`, or redirect survives a fold.

## Mapping the tree and proposing families

Enumerate the tree first: every skill directory with its plugin, its frontmatter description, and whether the attribution file names it. The count you get here is the baseline every later percent is computed against.

Then build the pointer graph from every description's `use <slug>` targets and list its connected components. Propose families from the three evidence sets above. For each family record the survivor, every member path, the `Vendored: <source>` annotation for each license-covered member, the unique steps the survivor absorbs, the steps you drop and why, and every description whose pointer must be rewritten. Reject a candidate whose members do different jobs and record the rejection in one line.

Write the fold ledger with a `Projected remaining: <n>` header and one `## Family <name>` section per family, rejected candidates included. If a floor was supplied and the projection misses it, state the shortfall in the header.

When a reduction floor is in play, keep the arithmetic honest. Record the exact measured tree and baseline count, and distinguish "at least p percent removed" from "more than p percent removed": for baseline n and remaining count r, evaluate 100*(n-r) >= p*n or 100*(n-r) > p*n exactly as requested. Pointer components, shared prefixes, and body similarity surface candidates; none of them proves two procedures are interchangeable with one parameter changed. Estimate the achievable reduction from defensible families only, with license obligations and unresolved membership decisions left visible, and re-measure after execution.

## Asking the human, one family at a time

Present the ledger and stop. Ask one question per family (approve or strike), and record each answer as a `Decision: approved|struck` line in that family's section. Nothing in the tree changes during this phase. If the user ends the gate with families undecided, report them as open and fold only what was approved.

## Folding what was approved

Before each approved fold, re-read the survivor, the members, and the live inbound routes; a research recommendation is not family approval. Derive pointer targets from the tree's actual routing grammar, including unhyphenated names and supported wildcards, and re-derive them after authoring, since the change itself can introduce new targets. Every surviving route must reach a skill that stays invocable through that route; never disable or delete a route's target without repairing the caller in the same family change. Inventory the scripts, references, and assets the survivor still needs, move them into its ownership, and repair relative paths before removing member directories. Transfer attribution and applicable license obligations with the absorbed text, remembering that attribution alone does not satisfy every license. When workers fan out, give them disjoint named content paths; the orchestrator alone owns shared attribution, generated surfaces, deletion, verification, and commits, and serializes those operations after content writers have stopped.

For each approved family in ledger order: rewrite the survivor so its description names the absorbed seats or modes inside the description cap and its procedure carries the absorbed steps as inputs or modes; delete every member directory; rewrite every pointer the ledger listed; drop retired names from the attribution lists and add the source of any absorbed licensed text to the survivor's entry; add the retired slug and survivor to the changelog's retired-skill table; re-render generated surfaces; run the tree's checks; commit as `Fold <members> into <survivor>`.

Then measure: count skill directories, compute the percent removed against the step-1 count, and confirm the checker reports no dangling pointer.

## When the fold cannot proceed as planned

An empty or missing target tree means stop before scanning and report that no skill was found; no ledger is written. A candidate whose members do different jobs is rejected in the ledger with its reason, never folded to reach a floor. A floor unreachable from defensible families is stated in the ledger header and at the gate, and the user either lowers the floor or accepts the shortfall; the fold criteria do not move. A gate that ends with undecided families leaves them reported as open. A fold commit that fails the tree's checks is fixed inside that commit before the next family starts; if the family cannot pass, revert its commit and mark the family `Decision: struck` with the failing check named.

## What you hand back

The analyze pass leaves the fold ledger with its projected count against the floor. The gate leaves one recorded decision per family. The fold pass leaves one commit per approved family, the measured remaining count and percent removed, the checker result, and the list of struck or open families.
