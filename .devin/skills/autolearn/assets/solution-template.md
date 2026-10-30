# Solution doc templates

Pick the template for the `problem_type` track (see `references/schema.md`). Each doc records one generalized, well-abstracted invariant: a reusable mechanism (never an incident, project name, command, version, or path) with stated supported scope, actual enforcement or proof, and a material consequence (prevents a plausible significant failure or improves a recurring decision). Incident details may inform extraction but never ship as session diary. Durable bodies carry only invariant, supported scope, material consequence, enforcement or independent proof, and necessary counterexample or limits. Tiny one-off fixes, trivia, and session history never qualify; no non-trivial-fix shortcut; no speculative universal truths. Replace every bracketed placeholder. Delete sections with no real content instead of leaving placeholders. Never add, rename, or drop frontmatter fields: the stored `odin-learning/v1` shape is fixed. The template itself is not a record: run the validator only after all placeholders are replaced.

## Bug track

For: `build_error`, `test_failure`, `runtime_error`, `performance_issue`, `database_issue`, `security_issue`, `ui_bug`, `integration_issue`, `logic_error`

```markdown
---
schema: odin-learning/v1
record_kind: solution
date: [YYYY-MM-DD]
title: [Clear invariant title]
category: [directory basename from the schema category map]
module: [Module or area]
problem_type: [schema enum]
component: [component or subsystem]
severity: [critical | high | medium | low]
symptoms:
  - [Observable symptom 1]
root_cause: [schema enum]
resolution_type: [schema enum]
tags:
  - [keyword-one]
---

# [Clear invariant title: reusable mechanism that must hold, never an incident retelling]

## Invariant
[The reusable mechanism: what must always or never hold, never an incident retelling, project name, command, version, or path.]

## Scope
[Supported scope: where the invariant holds and where it does not, grounded in evidence without overgeneralizing.]

## Material Consequence
[What breaks when the invariant is ignored: the plausible significant failure prevented or recurring decision improved.]

## Enforcement
[Concrete guardrail, check, or independent proof that exercises the invariant and fails on violation; never a mock echo, fixture snapshot, or weak test.]

## Counterexample
[Necessary counterexample or limits: concrete violation conditions, boundary cases, or known limits where the invariant does not apply.]
```

## Knowledge track

For: `best_practice`, `documentation_gap`, `workflow_issue`, `developer_experience`, `architecture_pattern`, `design_pattern`, `tooling_decision`, `convention`

```markdown
---
schema: odin-learning/v1
record_kind: solution
date: [YYYY-MM-DD]
title: [Clear invariant title]
category: [directory basename from the schema category map]
module: [Module or area]
problem_type: [schema enum]
component: [component or subsystem]
severity: [critical | high | medium | low]
applies_when:
  - [Condition where this applies]
tags:
  - [keyword-one]
---

# [Clear invariant title: reusable practice that must hold, never an incident retelling]

## Invariant
[The reusable invariant mechanism: what must always or never hold, never an incident retelling, project name, command, version, or path.]

## Scope
[Supported scope: where this invariant applies and where it does not, grounded in evidence without overgeneralizing.]

## Material Consequence
[What breaks or degrades when ignored: the plausible significant failure prevented or recurring decision improved.]

## Enforcement
[Concrete guardrail, check, or independent proof that exercises the invariant and fails on violation; never an unverified claim or weak test.]

## Counterexample
[Necessary counterexample or limits: concrete violation conditions, boundary cases, or known limits where the invariant does not apply.]
```

After assembling, run from the skill directory:

```bash
python3 scripts/validate-record.py docs/solutions/<category>/<slug>.md
```

A non-zero exit blocks publication. Quote any value containing `: ` or starting with a reserved indicator, then re-run until exit 0.
