# Retro report: [<mode>] [<scope>]

Scope: [session, period with start and end dates, milestone, cycle objective plus final artifact, or target path with fixed pass scope]
Sources consulted: [each source with what it supplied]
Sources unavailable: [each gap with its reason, or "none"]

Keep only the routed mode's section below. Delete the other four.

## Environment findings (environment mode only)

Severity-ranked friction candidates. Standing is confirmed, inferred, or unverified.

- [Finding, one line]
  Type: [tool-failure | slow-retry | missing-context | state-loss | navigation-overhead | unclear-feedback]
  Evidence: [verbatim session excerpt]
  Severity: [high | medium | low]
  Standing: [confirmed | inferred | unverified]
  Removed by fix: [friction this elimination removes]

When no friction is observed, this section carries exactly "No environment friction detected." with zero candidates.

## Engineering verdict (engineering mode only)

Period: [start date to end date]

Team and contributor breakdowns, each line with its source:

- [Team or contributor]: [commits, PRs, review participation, issue resolution, CI pass or fail rate] (source: [repository | tracker | review logs])

Habits, evidenced versus inferred:

- [Habit, one line]
  Evidence: [commit range, PR link, CI history, or review thread]
  Standing: [confirmed | inferred]

Summary: [one line]

## Learning verdict (learning mode only)

Evidence review, one row per milestone criterion:

- [Criterion]: [met | partially met | unmet]
  Evidence: [cited artifact]

Gap analysis:

- [Gap, one line]
  Expected: [what the milestone required]
  Observed: [what the evidence shows]

Strategy assessment:

- [Strategy or resource]: [effective | ineffective]
  Basis: [evidence]

Adjusted plan:

- Continue: [what, with motivating evidence]
- Change: [what, with motivating evidence]
- Drop: [what, with motivating evidence]
- Add: [what, with motivating evidence]

Next milestone: [specific, measurable goal]
Success criteria: [explicit, checkable criteria]

## Next-cycle verdict (next-cycle mode only)

Working assets: [contracts, schemas, tests, services, vocabulary, examples that earned reuse, each with evidence]

Misleading progress: [scaffolds, panels, abstractions that only looked productive, each with evidence]

Negative corpus: [failed paths recorded as training data, each with the specific reason it failed and when it would be worth trying again]

Lessons, pattern-level, specifics kept as evidence:

- [Lesson as pattern, one line]
  Evidence: [specifics that showed it]

Anti-patterns and gates:

- [Anti-pattern as concrete failure mode]
  Gate: [hard check that catches it, or advice only where no check exists]
  Evidence: [observed failure]

Decision: [keep | iterate | restart, with what carries forward; a restart carries the lessons and leaves the failed code behind]

## Rationale verdict (rationale mode only)

Target: [path]

Pass scope: [whole system or named subsystem; areas outside the fixed pass are listed under Remaining scope, not as entries]

Gap enumeration, one row per area where the code cannot explain why, organized by topic:

- [Area or decision, one line]
  Evidence: [confirmed | inferred | unknown]
  Status: [active | superseded | open | needs-review]
  Source: [commit hash, issue link, file reference, or maintainer statement; Verification: corroborated | uncorroborated | contradicted, with what contradicts and why, where a concrete artifact exists]
  Rejected alternatives: [why each lost, or "nothing else was considered"]
  Conflict: [both sides when sources disagree, flagged open; or "none"]

Unknowns: [items beyond evidence, each with its specific needs-maintainer question; "nobody remembers" is recorded as unknown, never guessed]

Remaining scope: [areas outside the fixed pass, or "none"]

Capture recommendation: [topic-file writes recommended to compound under the keep-why fold; this skill writes none]

## Gaps (all modes)

[Unverified items with downgraded priority, unresolvable questions with the specific fact needed, remaining scope outside this pass. "None" only when every finding is confirmed and every source was available.]

## Capture pointers (all modes)

[Learnings recommended to compound or autolearn; rationale topic records recommended to compound. Names the owning skill per pointer; this skill writes none of those surfaces.]
