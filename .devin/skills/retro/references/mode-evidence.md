# Mode evidence

Shared rules first, then the five distinct evidence paths.

## Shared rules

- Cite the source behind every finding: transcript excerpt, commit range, issue link, artifact path, named record, or maintainer statement.
- Standing: confirmed (the evidence states it), inferred (reasonably derived, labeled as such), unverified (no traceable support, downgraded priority, lives under Gaps).
- Severity: high (blocks progress or understanding of critical behavior), medium (degrades efficiency or correctness), low (minor friction).
- Rank: severity first; evidence strength breaks ties. Merge duplicates instead of listing near-copies.
- Recommendation shape: the concrete change, the cost or friction it removes, the evidence behind it.
- Never: numeric scores or invented metrics, inferred environments, invented telemetry, code treated as proof of motive.

## environment

- Required: the session transcript or state record, containing observable agent-environment interaction.
- Optional: environment context, used only if supplied. Never infer it.
- Friction types: tool-failure, slow-retry, missing-context, state-loss, navigation-overhead, unclear-feedback.
- No artifact supplied: report "No session artifact supplied." and stop.
- No friction observed: report "No environment friction detected." with zero candidates. Do not fabricate candidates.

## engineering

- Required: the period, resolved to explicit start and end dates. No period means no gathering and no file.
- Primary sources: the local repository for commits, pull requests, and CI runs; connected trackers for issues and tickets; repository review logs over tracker-exported review data. A secondary source covering the same activity is cited as corroboration only.
- Breakdowns per team or contributor: commit count, PR count, review participation, issue resolution, CI pass or fail rate, each with its source attribution.
- Habits carry evidence citations; inferences are labeled as inferences.
- Every unreachable source is a named gap with its reason, and every finding it would have supported stays unevidenced.

## learning

- Required: the milestone definition and at least one progress artifact (exercises, notes, project artifacts, session records). Absent or thin evidence stops the run with the gap named.
- Classify each milestone criterion as met, partially met, or unmet, citing the artifact behind the call.
- Gaps state expected versus observed. Strategies and resources are judged effective or not only on the supplied evidence.
- Adjustments say what to continue, change, drop, and add, each with its motivating evidence.
- The next milestone is specific and measurable with explicit success criteria.
- Conflicting evidence surfaces both readings and asks for the specific clarification. Scope beyond the milestone stops with a recommendation for a separate retro.

## next-cycle

- Required: the cycle objective and the final artifact. Either missing stops the run as blocked.
- Optional, cited when present: QA output, user complaints, screenshots, transcripts, diffs, planning notes.
- Separate working assets (contracts, schemas, tests, services, vocabulary, examples that earned reuse) from misleading progress (scaffolds, panels, abstractions that only looked productive). Failed paths are recorded in the report as negative corpus, not deleted.
- Escalate specifics to the pattern class before writing the lesson; specifics stay as evidence. A lesson that fixes one reported case is reworked or dropped.
- Each anti-pattern names a concrete failure mode and the gate that catches it. Repeated or high-impact failures get hard gates, not advice.
- Vague direction becomes architecture vocabulary a fresh reader can use.
- Ends with an explicit keep, iterate, or restart decision; a restart carries the lessons and leaves the failed code behind.
- Provenance stays in the memo. Shipped artifacts must not describe their development history.

## rationale

- Required: the target path and a fixed pass scope (the whole system or one named subsystem). Never widen the scope mid-pass; areas outside it are reported as remaining scope, not entries.
- Inventory existing documentation first (README, docs, design notes, decision records, existing rationale files). Adopt the project's terminology and file conventions. This inventory informs the analysis only; retro writes no files but the report.
- Scan for gaps: candidates where the code cannot explain why. Surprising, defensive, or redundant code; compatibility workarounds; boundaries that do not follow from the domain; magic numbers; rejected alternatives named in commits or issues but unexplained; incident-shaped changes with no documentation; constraints invisible in the code; areas one contributor understands; docs that state what but never why. The scan produces the gap list only; no explanations are written during the scan.
- Large scopes are ordered damage-first: auth, data integrity, incident-touched code, unusual or defensive code, then low-bus-factor areas. Every prioritized area is enumerated.
- Resolve each candidate through this search order: (a) history (log, blame, messages); (b) tracker and PR threads; (c) existing docs, however stale; (d) the code itself. Code is the weakest source for why: it identifies candidates and corroborates shape, never authors rationale.
- Keep search order separate from trust order. Discovery sources carry the least authority. Confirmed comes only from maintained docs, an accepted decision record, or a maintainer stating it directly. When sources disagree, record both sides and flag the conflict open. Never declare one source authoritative and rewrite the other.
- Classify every entry on two axes. Evidence: confirmed, inferred, or unknown. Unverified standing is recorded as unknown with a needs-maintainer note, never a guess. Status: active, superseded, open, or needs-review. Open means the entry's own question is unresolved; unknown is an Evidence level, not a Status. Where a concrete artifact backs the claim, record Source (commit hash, issue link, file reference) and Verification (corroborated, uncorroborated, or contradicted, with what contradicts and why).
- Ask the human only what the evidence cannot answer, and ask specifically ("why does the sync step wait for the snapshot before applying buffered events?"), never generically. "Nobody remembers" is a complete answer: record unknown.
- Organize entries by topic (auth, sync), never by source file or commit. A correction that restored something to its intended state involved no real alternative: one line, not a manufactured decision entry. Full decision, alternatives, and reason structure is reserved for choices a reader would genuinely ask why about; self-evident conventions get one sentence.
- Exclude credentials, personal information, private local detail, and session narrative from anything recommended for committing. Topic-file capture is recommended to compound under the keep-why fold; this skill writes none of those surfaces.
