---
name: retro
description: 'Use when a finished session, period, milestone, or cycle needs an evidence-backed look-back, or an existing system needs its unexplained rationale recovered. Not for saving learnings into docs: use compound or autolearn.'
---

# Look back with evidence

A retro explains finished work: what helped, what hurt, and what to keep. It never saves learnings itself. Findings that deserve to live on become pointers to compound or autolearn, which own capture. It never writes docs/solutions/, CONCEPTS.md, or rationale topic files.

This skill is read-only, except for one file write and only when the user explicitly asks for a file report. No version control, credential, paid, published, deployed, or remote mutation follows from running it. If the user wants the report as a file, write it to the path they name. When they ask for a file but name no path, use `reports/retro-<mode>-<slug>.md`. Otherwise the report stays in chat.

## Run one mode at a time

Pick exactly one mode from the request and stay inside it. A request that names no mode gets one clarifying question covering the five modes and what each needs, not five reports.

| Mode | What it examines | What you need before starting |
|---|---|---|
| environment | A finished session, for agent-environment friction | The session transcript or state record, with observable agent-environment interaction in it |
| engineering | A named period, from repository and tracker telemetry | The period resolved to an explicit start and end date |
| learning | A milestone, from progress evidence | The milestone definition and at least one progress artifact such as exercises, notes, project artifacts, or session records |
| next-cycle | A finished cycle, distilled into lessons, anti-patterns, gates, and a decision | The cycle objective and the final artifact |
| rationale | An existing system, for unexplained why knowledge | The target path and a fixed pass scope: the whole system or one named subsystem, never widened mid-pass |

How each mode gathers evidence, which sources outrank which, and how findings are prioritized lives in `references/mode-evidence.md`. Follow it for the routed mode and ignore the other four.

## Gather only what the mode needs

Do not start gathering until the mode and its required scope are settled. Missing required scope stops the run before any finding is drafted, and nothing is written. Confirm you are read-only unless a file report was requested.

Cite every source you consult and record every unavailable source as a gap with its reason. Never infer an environment, invent telemetry, or treat code as proof of motive.

The shared evidence rules apply to every mode. Each finding carries a source, a standing, and a severity.

| Standing | Meaning |
|---|---|
| confirmed | The evidence states it |
| inferred | Reasonably derived and labeled as such |
| unverified | No traceable support; downgraded priority and lives under Gaps |

| Severity | Meaning |
|---|---|
| high | Blocks progress or understanding of critical behavior |
| medium | Degrades efficiency or correctness |
| low | Minor friction |

Rank by severity first, evidence strength second. Merge duplicates instead of listing near copies. Findings with no traceable evidence are dropped, or kept under Gaps as unverified. No numeric scores or invented metrics.

## Turn specifics into patterns before recommending

Cluster individual complaints and incidents upward into the shared pattern. The pattern becomes the finding and the specifics stay as evidence. A recommendation that fixes only the reported case is rework waiting to happen, so escalate it to the class or drop it. Each surviving recommendation names the concrete change, the cost or friction it removes, and the evidence behind it, ordered by severity then evidence strength.

Each mode then gets its own verdict, built from the pattern findings above.

### Environment verdict

The ranked friction candidates are the verdict; no separate breakdown is needed. When no friction is observed, say so plainly with zero candidates rather than inventing any.

### Engineering verdict

Name team or contributor breakdowns (commits, PRs, review participation, issue resolution, CI pass or fail rate) with each line carrying its source. The local repository is primary for commits, pull requests, and CI runs, connected trackers cover issues and tickets, and repository review logs outrank tracker exported review data. A secondary source covering the same activity is cited as corroboration only. Habits carry evidence citations and inferences are labeled as inferences, and every unreachable source becomes a named gap with its reason while each finding it would have supported stays unevidenced.

### Learning verdict

Review evidence one row per milestone criterion, calling each met, partially met, or unmet with the artifact behind the call, and stop with the gap named when evidence is absent or thin. Gaps state expected versus observed. Strategies and resources are judged effective or not only on the supplied evidence. Adjustments say what to continue, change, drop, and add, each with its motivating evidence. The next milestone is specific and measurable with explicit success criteria. Conflicting evidence surfaces both readings and asks for the specific clarification, and scope beyond the milestone stops with a recommendation for a separate retro.

### Next-cycle verdict

Separate working assets (contracts, schemas, tests, services, vocabulary, examples that earned reuse) from misleading progress (scaffolds, panels, abstractions that only looked productive), record failed paths in the report as negative corpus without deleting them, name each anti-pattern as a concrete failure mode with the gate that catches it, prefer hard gates over advice for repeated or high impact failures, turn vague direction into vocabulary a fresh reader can use, and end with an explicit keep, iterate, or restart decision. A restart carries the lessons and leaves the failed code behind, and shipped artifacts never describe their development history.

### Rationale verdict

Start by inventorying existing documentation (README, docs, design notes, decision records, existing rationale files) and adopting the project terminology and file conventions; that inventory informs the analysis only, since retro writes no files but the report. Scan for gaps where the code cannot explain why (surprising, defensive, or redundant code, compatibility workarounds, boundaries that do not follow from the domain, magic numbers, rejected alternatives named in commits or issues but unexplained, incident shaped changes with no documentation, constraints invisible in the code, areas one contributor understands, docs that state what but never why) and produce the gap list before explaining anything. Large scopes are ordered damage first (auth, data integrity, incident touched code, unusual or defensive code, then low bus factor areas) with every prioritized area enumerated. Each candidate resolves through history first (log, blame, messages), then tracker and PR threads, then existing docs however stale, then the code itself, which is the weakest source for why: it identifies candidates and corroborates shape but never authors rationale. Search order stays separate from trust order. Confirmed comes only from maintained docs, an accepted decision record, or a maintainer stating it directly. When sources disagree, both sides are recorded and the conflict flagged open. Every entry carries Evidence (confirmed, inferred, or unknown) and Status (active, superseded, open, or needs-review), with Source (commit hash, issue link, file reference) and Verification (corroborated, uncorroborated, or contradicted, with what contradicts and why) wherever a concrete artifact backs the claim. Unverified standing is recorded as unknown with a `needs-maintainer` note, never a guess, and open means the entry's own question is unresolved. The human is asked only what the evidence cannot answer, asked specifically, and "nobody remembers" is recorded as unknown. Entries are organized by topic, never by source file or commit. A correction that restored something to its intended state involved no real alternative and gets one line, not a manufactured decision entry; full decision, alternatives, and reason structure is reserved for choices a reader would genuinely ask why about, and self evident conventions get one sentence. Credentials, personal information, private local detail, and session narrative stay out of anything recommended for committing, and areas outside the fixed pass are reported as remaining scope, not entries.

Emit the report in chat following `templates/retro-report.md`, keeping only the routed mode's section and deleting the other four. Write the file only when asked; any file write matches the chat report. A fresh reader should be able to tell what to preserve, discard, and check first without reading the source session. Every finding cites traceable evidence with an honest standing, recommendations are ranked, and unavailable sources and unverified items appear as gaps, never filled by invention.

## Stop honestly when the run cannot proceed

Missing required scope stops the run before gathering, with what is missing stated. An unavailable source becomes a named gap; continue on what is evidenced and never fabricate activity, issues, or rationale. Ambiguous or conflicting evidence marks the finding unverified or records both sides. Ask for the specific missing fact, never a generic explanation, and "nobody remembers" is a complete answer. Scope widening mid-run stops the run: report the widening and recommend a separate retro for the added scope. A guessed entry discovered late is demoted to unverified and the report corrected before finishing. Rollback, if a file was written, is deleting that file; nothing else was mutated.

## What retired into this skill

Retro is the only surviving retrospective entry point, with no aliases kept. Agent environment friction taxonomy, severity ranking, and evidence validation came from the agent environment retrospective. Period telemetry, source precedence, breakdowns, and gap accounting came from the engineering retrospective. Criterion classification, strategy assessment, adjusted plan, and measurable next milestone came from the learning retrospective. Lesson extraction, asset separation, pattern escalation, and anti-pattern plus gate discipline came from cycle memo, whose build and versioning machinery stays with the work owners. The explicit keep, iterate, or restart decision came from the cross run playbook, which likewise does not run cycles here. Rationale gap scanning, evidence search and trust order, Evidence and Status classification, conflict flagging, and the unknown discipline came from keep why; its topic file capture moved to compound under the keep why fold. The skill doctor decode the transcript plus evidence cited per turn discipline is carried by the shared evidence rules; its numeric scores and scratch HTML report were grading, not retrospective analysis, and were not carried.

Compound and autolearn keep the capture jobs, and compound additionally receives the keep why topic file capture. Retro recommends capture; it never writes those surfaces.

## What you hand back

A report with the scope, sources consulted, sources unavailable, the routed mode's required sections, ranked recommendations, explicit gaps, and capture pointers naming the owning skill per pointer. File form goes to the user named path, or to `reports/retro-<mode>-<slug>.md` when a file was asked for without a path.
