# Rationale template

Copy this template to `docs/solutions/rationale/<slug>.md`, where `<slug>` is a sanitized semantic name for the invariant (no ADR numbers, dates, or hashes). Replace every bracketed placeholder and delete sections with no real content. The template itself is not a record: validate only after all placeholders are replaced.

```markdown
---
schema: odin-learning/v1
record_kind: rationale
date: [YYYY-MM-DD]
type: [pattern | caveat | reference | decision | concept | fix | lesson | workaround | incident | constraint]
confidence: [high | medium | low]
source: [session context, PR, issue, or codebase area]
tags:
  - [keyword-one]
  - [keyword-two]
status: [active]
evidence: [observed | corroborated | single-source | unknown]
retire_when: [condition that should trigger a revisit, or delete this line]
---

# [Invariant statement: reusable mechanism that must always or never hold, never an incident retelling]

## Scope
[Supported scope: where the invariant holds and where it does not; never beyond the corroborating evidence. Repo-local quirks marked local; general claims only with corroboration]

## Enforcement
[Guardrail, check, or test that exercises the invariant and would fail on violation; never a test that merely asserts mocked or fixture output. Reusable inputs are allowed when the test still proves the invariant]

## Counterexample
[Concrete violation and its material consequence: the significant failure prevented or the recurring decision improved. Use unknown: only for an honestly-unobserved violation shape, never as a stand-in for missing enforcement]
```

After assembling, run from the skill directory against the absolute record path (the `docs/...` destination lives in the operating repository, not inside the skill directory):

```bash
python3 scripts/validate-record.py /path/to/repo/docs/solutions/rationale/<slug>.md
```

A non-zero exit blocks publication. `type: caveat` stays `caveat`; never convert it into another type to look more classified.
