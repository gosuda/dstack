---
name: prism
description: 'Use when one reviewer angle is insufficient or the user suspects a direction is tunnel-visioned or inherited its framing. Modes: artifact, direction. Not for source or remote-system changes.'
---

# Prism

This skill stress tests a target from several independent angles so a question framed one way can be checked against genuinely different failure modes. It reports divergence first and treats agreement as reassurance, never proof. There is no vote, no averaging, and no verified verdict.

It is read-only. It writes nothing and rolls back nothing, makes no remote changes, and creates or changes no files. Its report goes to chat only. The only fresh work it spawns is bounded zero-context sub-reads used as inputs to classification.

## What you hand it

| Input | Meaning |
|---|---|
| Target (required) | The artifact to review, or the direction of work to stress test (plan, approach, or framing) |
| Mode | `artifact` (default, for reviewing a concrete artifact) or `direction` (for asking whether current work is tunnel-visioned or inherited its framing) |
| Lenses or viewpoints | Review lenses in artifact mode, distinct viewpoints in direction mode (opposing assumption, adjacent domain, historical failure mode, resource constraint, user-population segment). Optional. If omitted, they are derived from the target genuinely distinct failure modes |
| Context | Background material that may inform the reads without constraining them to a single frame. Optional and used only when available and attributable. Nothing missing is invented |
| Decision | A decision the review must inform. Optional |
| Read count | Between 2 and 5, default 3. Optional. The same model may serve all reads, since the point is framing blind spots rather than cross-model truth |

## How the review runs

The skill reads the target end to end before picking lenses. In direction mode that means the direction statement with its surrounding context. Supplied context counts as evidence only when available and attributable.

It then picks two to five lenses, each covering a distinct failure mode. Proposals testing the same failure mode are merged, and the artifact determines the count rather than a fixed default. In direction mode the viewpoints must be distinct (such as opposing assumption, adjacent domain, historical failure mode, resource constraint, or user-population segment), and no read may copy or restate another. If two distinct lenses or reads cannot be found, it returns `blocked: independent lenses unavailable`, reports the single read with its classification, explains why a multi-lens verdict would be false precision, and never pads the set with variations of one viewpoint.

Next it strips the framing down to the underlying goal, constraints, and known facts. In artifact mode that means restating the bare review question in neutral terms that drop the session loaded vocabulary (keeping a term denotation when load-bearing, dropping the framing that points at one answer). In direction mode that means removing leading, suggestive, and conclusory language from the direction statement while preserving the decision substance. If artifact-mode framing cannot be separated, the skill reports that and stops instead of fanning out a still-loaded question. In direction mode it proceeds with the original statement and notes which bait elements could not be removed.

It then fans out 2 to 5 fresh zero-context reads of the stripped question or direction, default 3, each evaluated independently through one lens. A read that refuses or returns empty is reported as a divergence lead, never retried with re-primed prompts.

## How it judges what comes back

Each lens gets exactly one verdict (`pass`, `fail`, or `unclear`) with the single most load-bearing reason supported by the target or supplied context. Conflicting verdicts are never averaged or flattened. Thin evidence gets `unclear` rather than a firm label.

Each perspective then gets exactly one classification:

| Label | Meaning |
|---|---|
| `divergent-incompatible` | Challenges a premise the direction depends on, or identifies a framing flaw, hidden assumption, or outcome contradicting the intent |
| `divergent-compatible` | Adds, reframes, or proposes a meaningfully different path or emphasis without discarding the direction |
| `convergent` | Independently arrives at the same framing or verdict |
| `ambiguous` | Cannot be classified with confidence, with a one-sentence explanation of why |

Labels are never force-fit. Uncertainty stays `ambiguous` with the missing evidence named.

Reads sharing an underlying assumption, evidence source, or structural concern are clustered under a named root as evidence. Reads with no shared root form single-member clusters.

## How it reports

Order follows the mode. Artifact mode reports incompatible divergence, then compatible divergence, then convergence. Direction mode reports ambiguous clusters first, then incompatible, then compatible, then convergent, ordering within each cluster by relevance to the core claim. Convergence is labeled reassurance, never proof. In direction mode, convergent reads are noted as confirming the framing was inherited, not chosen. No consensus, agreement, majority, or weight wording is used for the reads collectively. Any such sentence is rewritten with per-read or per-cluster attribution.

The report closes with one decisive resolving question whose answer would settle the deepest disagreement. Under full convergence it states the shared verdict and marks the question `none (no lens conflict)`. Unresolved disagreement is returned as conflicting verdicts plus the single resolving question, which counts as a valid partial result. A partial run otherwise returns every read obtained with its classification, never a fabricated read or an upgraded proof claim.

The report carries these sections in this order, in chat:

| Section | Content |
|---|---|
| Stripped target | Bare review question (artifact) or stripped direction statement (direction) |
| Lenses | Each lens or viewpoint and the failure mode it targets |
| Verdicts | Per lens: verdict (`pass` / `fail` / `unclear`), load-bearing reason, and classification |
| Divergences | Roots with divergent perspectives clustered underneath, in the mode order above |
| Convergence | Convergent perspectives as reassurance, never proof, with the inherited-framing note in direction mode |
| Decisive question | Single resolving question, or `none (no lens conflict)` with the shared verdict |
| Status | `complete` when all lenses evaluated and all perspectives classified, `partial` when some reads were obtained but not all, `blocked` when the target is missing, independent lenses are unavailable, or artifact-mode framing cannot be stripped |

Before sending, the skill checks that every lens appears once, every verdict has evidence, every perspective is classified, and the grouping follows from the verdicts. A missing or unreadable target stops the run with `blocked` naming the artifact or access needed. No guessed target is substituted.
