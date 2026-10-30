---
name: writing-for-agents
description: 'Use when authoring or restructuring an agent-consumed document, a SKILL.md or skill directory, writing skills, or deciding a skill split-or-monolith disclosure question. Not for prose style: use unslop.'
---

# Writing for agents

One property decides whether a document works: a cold agent takes the same process every run. The packaging differs across a skill, an AGENTS.md, and a pointer-reached doc; the writing does not. The theory behind the craft lives in `references/authoring-levers.md`; reach for it when a claim below is not enough to act on.

## The job

You reshape how an agent behaves through its reading material. Three shapes of request arrive here; name which one you hold before touching anything.

A document reshape edits one agent-consumed file in place. A skill build creates or changes a skill directory on disk. A disclosure question decides whether a skill stays whole or splits. Reviews and disclosure answers change nothing beyond the decision record.

Every shape stays local and reversible: the target document, its skill directory, and the repository-owned registration or attribution surfaces those artifacts require. Roll back through version control or undo. This work never publishes, installs, commits, or mutates remote state; a request that wants publication or destruction stops at the local artifact unless the user separately authorizes that operation as its own act.

## Read the target first

Read the whole target before editing. Decide what it contains (ordered actions, consulted definitions and facts, or both) and what kind of document it is: skill, AGENTS.md/CLAUDE.md, or pointer-reached doc.

When the caller hands you a completed-task bundle with the exact skill slugs it invoked, treat those slugs as the boundary: reshape only the named skill directories, present each finding as a one-skill proposal, and wait for explicit approval of each proposal before editing. Log a backlog item only where the caller names an authorized destination; otherwise record it as rejected or deferred with the reason.

When the request preserves wording (a rename, a port, a carryover), write down the source baseline, the exact permitted rename pairs, and the regions that must stay byte-identical before you rewrite. Keep headings and their order, anchors, list and numbered-step nesting, table shape, code, commands, paths, URLs, identifiers, quoted triggers, and machine-consumed literals exactly as they are unless the request names a permitted change. Judge the result against an ordered structural model that includes numbered steps, and map every obligation to its subject, condition, exception, order, and proof. A positive rephrasing must carry the full force of an explicit ban; never soften a hard prohibition into a preference. Equal lengths, matching token sets, and modal counts prove nothing. Compare the exact regions byte for byte, report every permitted difference and every unresolved obligation, and recheck changed headings, link targets, anchors, and reachable references before claiming preservation.

When the request only shortens descriptions across named files, bind each edit to the description value and the repository's actual metadata limits. Every supported trigger, routing verb, exclusion, authority line, and distinct negative route survives; quoted trigger literals stay exact. Parse the resulting frontmatter under the repository's YAML rules and confirm nothing outside the description moved. Resolve each route to its real target, bare-word slugs and supported wildcards included, and never accept a plausible phrase as a skill name. Give each changed description a fresh read-only review beside its baseline and body, checking for lost triggers, narrowed exclusions, broadened claims, ambiguous routing, and sibling-copy mistakes. Treat suggested fixes as unverified candidates under the same checks, report partial coverage as partial, and leave the repository's generated-surface convention alone rather than hand-editing generated metadata.

## Put every piece where the agent reaches it

Rank material by how immediately the agent needs it. Steps the agent performs in order stay in the file as the primary tier. Definitions, rules, and facts consulted on demand sit in the file as reference or move behind a context pointer into a separate file that loads only when the pointer fires. Every piece of material gets exactly one level: the top stays legible and nothing the agent needs hides behind a pointer.

Push down what only some branches reach; keep what every branch needs inline. Keep a concept's definition, rules, and caveats under one heading instead of scattered. In-file reference that ought to be disclosed buries the steps and turns attending to them into a coin-flip.

## Write pointers that fire

A pointer's wording, not its target, decides when the agent reaches the material. Say what the material is, then list the branches that trigger reaching it. Lead with the word the agent already uses, give one trigger per branch, merge synonyms that rename a single branch, and cut identity the body already carries. A must-have target behind weak wording is a wording bug: sharpen the pointer first and inline the material only if sharpening fails.

## Give each step a finish line

Every step ends on a condition under which the agent can tell done from not-done, and the condition demands the thorough work the step exists for. A vague bound invites the agent to rush toward the visible later steps. Sharpen the bound first; only when it stays irreducibly fuzzy and you observe the rush, move the sequence across a real context boundary such as a hand-off or a subagent dispatch. An inline call leaves the later steps in context and changes nothing.

## Anchor with words the model already knows

A compact concept from pretraining, repeated as a token rather than restated as a sentence, anchors a whole region of behaviour in the fewest tokens. Prefer a word the model already carries; a coined word earns its keep only with a clear definition. The same word anchors twice: in the body it steadies execution, in a pointer it steadies invocation, because prompts, docs, and codebase share the language. Collapse restatements into the token, and steer toward the wanted behaviour in positive words rather than reciting the banned one.

## Keep one home per idea

Each meaning lives in exactly one authoritative place, so a behaviour change is a one-place edit. The environment counts as a place too: scripts, configs, directory layout, `--help` output. A document that restates one is a cache, and a cache earns its load only when the lookup is expensive (the unwritten convention, the reason behind a choice, the gotcha no config confesses). Delete every sentence that passes the no-op test: an instruction the model already obeys by default costs attention and buys nothing. Left alone, documents gather sediment, stale layers kept because adding felt safe and removing felt risky; core down to what is live.

## When the target is a skill

Choose how the skill fires. A model-invoked skill carries a model-facing description so the agent reaches it on its own and other skills can reach it; that description is permanent context load, paid for discoverability. A user-invoked skill sets `disable-model-invocation: true`, carries only a human-facing summary, costs no context load, and only the human typing its name can fire it. Pick model invocation only when the agent must fire the skill itself or another skill must reach it; when it fires solely by hand, keep it user-invoked. Shared reference that two user-invoked skills both need lives in neither. With no model-facing descriptions neither can fire the other, so it becomes a plain file outside the skill system that any skill points at. Justify each split by independent reach or by a sequence that rushes, and when user-invoked skills multiply past recall, gather them under one user-invoked router that names each skill and when to reach for it. The full mechanics live in `references/skill-mechanics.md`; load it when the document is a skill.

When the request writes a skill directory, the ordered write path lives in `references/authoring-procedure.md`; load it then and follow it from classification through validation. Directory names, frontmatter fields, reference load conditions, script behaviour, registration rows, and the repository's native validation each get checked at the end, and each failure is repaired at its source rather than worked around.

## When the question is split or monolith

Diagnose first whether the complaint is triggering or disclosure. Triggering is whether the model invokes the skill at all; it runs on the description, and no file split repairs it. When the request conflates the two, say so as the first finding and fix the description before touching structure.

Default to one file. Split only when SKILL.md runs long with natural branches, eval evidence shows context spent on sections most runs ignore, or bulky content serves narrow conditions. Where a split earns its keep, cut along the axis the invocations actually follow: one intent per variant, workflow apart from reference data, or depth tiers behind sharp observable conditions. Never split by topic when invocations ignore topic, never split to hit a length without a branching condition, never bury rare-but-critical content in a reference, and never ship cosmetic files with no load condition.

Dress every reference for reliable loading: an observable signal for when it loads, one sentence per pointer, a filename that states the condition, a table of contents past roughly three hundred lines, and a merge when two references co-load in most runs. Deterministic work such as validation, transforms, or schema generation belongs in `scripts/`, not `references/`. Weigh each candidate: content loaded in nearly every run moves inline, content almost never loaded goes away or inlines, the middle range splits, and a load the agent fetches but never uses signals a broken pointer.

Prove the architecture with runs, not instinct. Query each variant, each edge branch, each lookup category, plus one common-path query that loads zero references and off-topic queries that must not trigger. Instrument files loaded, tokens, and time on identical eval sets, and compare candidates on cost, quality, and path coverage with reliability outranking efficiency. Without instrumentation, recommend measuring before committing to a split; when the split costs more tokens than the monolith, revert and record the overhead as evidence; when no architecture converges, deliver the monolith with the eval evidence explaining why.

Hand back the decision in this order: diagnosis of triggering versus disclosure with evidence, verdict of split or monolith with rationale, the chosen axis with pointer hygiene or the monolith rationale with pruning notes, and the evaluation plan of query set, instrumentation, metrics, and decision thresholds.

## Every document stands alone

The finished document restates each safety, authority, execution, and proof rule its workflow needs. It never sends the agent elsewhere for runtime behaviour: no pointer to AGENTS.md, a system prompt, a rule file, another skill, or an optional peer step.

## When it goes wrong

Sprawl means the document is too long even with every line live: disclose reference behind pointers and divide by branch or sequence so each path carries only what it needs. Duplication means one meaning in two places: collapse to the single home. A dangling pointer means its target moved or vanished: update or remove it the same run. Premature completion means the agent ends steps early: sharpen the finish line before restructuring. When the document cannot be made predictable, return the lever that failed with the evidence instead of weakening any check.

## What to hand back

For a document or skill reshape, return the authored document with every line earning its place by changing routing, authority, reads and writes, procedure, success proof, failure handling, or attribution, with no stale duplication, no unreachable pointers, and no runtime routing into peer skills. For a written skill directory, add the changed paths, the user job each skill now owns, merge or deletion decisions, attribution changes, and the exact validation evidence. For a disclosure question, return the decision record in the order named above. Use the request's own semantic names for documents, phases, and tasks throughout, and open no new record beyond these returns except a generalized invariant the work genuinely uncovered.

## Reach for more only when

| File | Load when |
|---|---|
| `references/authoring-levers.md` | A claim above is not enough to act on and you need the reasoning behind it |
| `references/skill-mechanics.md` | The document is a skill and you are choosing invocation or splitting |
| `references/authoring-procedure.md` | The request writes a skill directory and you need the ordered write path |
