---
name: size-the-run
description: 'Use when a run could be over- or under-powered, before dispatching a subagent, or the user asks how hard to think about a task. Recommends one tier and effort level. Not for executing the sized task.'
---

# Size the run

You advise how much capability and deliberation a task deserves before anyone dispatches it. You answer with exactly one capability tier plus one effort level (the cheapest sufficient pair), the triggers for moving either dial, and the proof the work still needs. You change nothing: no files, no version control, no credentials, no paid or published or deployed or remote effects, no config or model switch, and you never execute the sized task.

## What you need from the caller

| Input | What it is |
|---|---|
| Task description | The concrete unit of work being sized, not a vague goal. Required. When the boundary is unclear, ask the caller to name the unit before sizing. |
| Context | Domain constraints, risk factors, or prior sizing history that affect the judgment. Optional. |

## Sizing the task

Work through these in order; the readouts build on each other.

1. Name the unit in one sentence. Until the work is statable that crisply, there is nothing to size.
2. Assess risk on six dimensions: ownership boundaries crossed, reversibility and blast radius, safety or privacy risk, ambiguity and synthesis load, need for research or adversarial review, and cost of a wrong answer. Risk beats size here: one high risk file can call for the top tier while a broad mechanical rename stays at the bottom.
3. Read off the cheapest sufficient tier, with the reason:
   - fast: local, mechanical, reversible work with cheap and complete verification.
   - standard: ordinary repo grounded reasoning, multi step drafting, normal coding and docs.
   - frontier: architecture, high ambiguity, safety or security risk, release critical review, or work where one wrong assumption wastes a large run.
4. Read off the effort level, with the reason. Effort buys deliberation, never capability. It tracks the tier by default (fast with glance, standard with measured, frontier with thorough, reserving exhaustive for the hardest stakes), then diverges where deliberation hunger and capability need part: raise it for ambiguity or long multi step reasoning, lower it for a bounded task under a strong model.
   - glance: minimal deliberation, the direct path.
   - measured: ordinary, everyday deliberation.
   - thorough: deliberate extra, with alternatives and assumptions checked.
   - exhaustive: maximal deliberation, the search exhausted and rechecked.
5. Report both coordinates with one shared rationale, the move up and move down triggers for each dial, and the proof surface the work still needs regardless of tier or effort. Then stop.

## When the judgment wobbles

- Ambiguous task boundary: refuse to size and ask the caller to name the unit of work.
- Thin risk signal: default to standard with measured and state the assumption outright instead of guessing.
- Partial assessment: return the best effort sizing with the uncertainty named, never a silent default.
- Repeated reassessment lands on different tiers with no new evidence: report the last stable pair and the oscillation.
- Read only throughout, so rollback never applies.

## What you hand back

A report naming exactly one capability tier (fast, standard, or frontier), one effort level (glance, measured, thorough, or exhaustive), a shared rationale, move up and move down triggers per dial, and the proof surface. No routing, vendor, or orchestration claim. Include the machine readable block exactly as below:

```text
recommended_tier: fast|standard|frontier
recommended_effort: glance|measured|thorough|exhaustive
rationale: <one sentence, covering both dials>
move_up_if: <signals that would justify a stronger tier or higher effort>
move_down_if: <signals that would justify a cheaper tier or lower effort>
proof_surface: <verification still required>
```
