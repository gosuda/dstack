---
name: ideate-multiple-agents
description: 'Use when the user wants divergent ideas or an independently generated candidate pool grounded in the working repository. Requires at least two successful independent generation workers, a full-pool critic, and a separate reviewer. Not for refining one supplied idea: use brainstorm.'
---

# Grow ideas from independent workers

You produce a pool of divergent candidates for an identifiable subject, grounded in the working repository, where no worker sees another worker's output until the critic does. One agent role-playing several seats never counts. Neither does having the coordinator, an explorer, the critic, or the reviewer stand in as a generator. Without a real subagent facility that runs separate workers and returns their outputs, report `blocked: independent-generation-unavailable` and stop. Do not substitute single-agent ideation.

Everyone except the coordinator stays read-only: research, generators, critic, and reviewer change nothing. The coordinator writes only `docs/ideation/<slug>.md` and, when the subject line starts with `format:html`, the matching `docs/ideation/<slug>.html`. No implementation, version control, credential, paid, published, deployed, or remote mutation happens here.

## Fixing the subject and the output paths

Parse the subject and the optional leading `format:html` flag, and reject unsupported flags. Build `<slug>` by lowercasing the subject, replacing each run of non-alphanumeric characters with one hyphen, and trimming leading and trailing hyphens. Reject an empty subject or an empty slug, and reject any target that escapes `docs/ideation/`.

Fix the output set before writing anything. When either requested target already exists, report `blocked: target-exists` and stop. Never overwrite the file and never pick another path on your own.

## Framing the problem before generating

Write a solution-neutral frame first, in the form of a "How might we..." question that carries no proposed implementation. Name the target user or actor whose job or constraint matters. State the observable result that shows an idea is useful. State the binding constraints that shape the work.

When the target user or the observable success cannot be established from the supplied context or repository evidence, stop with `blocked: intent-underdefined`. Ask only for the missing intent input. Never generate candidates against an invented audience or success criterion.

## Grounding in the repository

Read the smallest relevant repository surfaces and record the existing architecture, patterns, and constraints with `file:line` citations. Match the scouting effort to the subject: one read-only explorer for one known concern, three parallel explorers for multiple or uncertain concerns, five for a cross-module or architectural subject. Explorer work supplies evidence only; it never counts toward the generation minimum. When the evidence cannot identify the subject, report `blocked: subject-unidentified` and stop.

## Running the generators

Create at least two generation assignments that cross repository-relevant topic axes with different frames, such as user workflow, architecture, reliability, small changes with large effect, or constraint removal. Record each worker's id, axis, frame, scope, and expected return. Give every worker the same grounding summary and constraints but a distinct assignment. Never pass another generator's candidates, the coordinator's preferred answer, or an emerging shortlist into a worker. Assignments must differ in the work they ask for, not in persona names alone.

Launch the generation workers together and ask each for roughly six to eight concise candidates. Each candidate holds an idea, why the idea exists, its evidence basis, its user-facing value, its hardest feasibility risk, and its differentiating decision or capability. A basis is a repository `file:line` anchor or an `external:<source>` marker for a source actually inspected. Treat the existing fact and the proposed change as separate things: evidence that an opportunity exists never proves a future result. Assign stable candidate ids from worker id plus local sequence, and preserve every returned candidate in the raw pool, including unsupported, duplicate, or malformed ones.

A generation worker counts as successful only when it is a distinct worker that completed its assignment and returned at least one usable candidate with an idea, a rationale, and an inspected supporting basis. Criticism, an empty response, or ungrounded suggestion does not qualify. Wait for every assigned worker to return or reach an explicit failed state, and record failures and partial outputs. A worker that returned candidates and then failed keeps those candidates in the raw pool, but its partial result never counts as a successful completion. When an assignment needs replacement, give a separate generator the same uncovered axis without exposing the pool.

Continue only when at least two successful workers with distinct assignments hold and the assigned axes are covered. Otherwise report `incomplete: independent-generation` with the successful count, the failed assignments, and the partial pool. Never produce a success artifact on fewer, and never narrow the assignment set to hide the shortfall.

## Critic, then an independent reviewer

Hand one separate read-only critic the grounding summary, the assignment inventory, the complete raw pool, and the worker outcomes. The critic returns `survive` or `reject` with a reason for every candidate id, with no filtering beforehand. A candidate survives only when its cited basis supports the opportunity, it names a user-facing value, it is feasible in this repository, it changes a meaningful decision, and it is not a restatement of another survivor. Unsupported candidates stay visible as rejections. A duplicate rejection names the retained candidate id.

Then hand a separate read-only reviewer the same grounding and raw pool plus every critic verdict and the generation inventory. The reviewer is neither a generator nor the critic. The reviewer audits generation independence, assignment coverage, citation accuracy, scope, consistency, and candidate accounting, then returns one final `survive` or `reject` verdict with a reason for every raw candidate id. The reviewer may correct the critic and states why. The reviewer's survivor set stands. The coordinator never rescues a rejection or drops a survivor on preference.

A missing, invented, or repeated candidate id, a missing reason, or an unsupported survivor makes the round `non-converged: incomplete-adjudication`. Send it back for correction; when correction is unavailable, stop before writing any success artifact. A critic or reviewer that is unavailable ends the run as incomplete with the pool and the missing role named. The coordinator never impersonates either role.

Judge candidates on user-facing value, the concrete pain or job relieved, the hardest feasibility dependency, and the differentiating decision or capability. Reject any candidate that cannot name a user-facing value or only restates an existing survivor. Keep a high-value but difficult candidate only when its feasibility risk is explicit and the reviewer states why the risk is worth it.

## Giving every survivor a direction card

Each survivor gets a direction card with the problem statement, the recommended direction, user value, feasibility with the hardest risk, differentiation, key assumptions to validate, MVP scope limited to one user job and the riskiest assumption, what is explicitly not being done with a reason for each exclusion, and open questions. A survivor without a complete card is not ready for intent clarification: complete the card or reject the candidate with a reason.

## Assembling and writing the result

Assemble the canonical Markdown with the subject, the problem frame, grounding context and citations, topic axes with generation frames and worker identities and outcomes, survivors (each with candidate id, direction card, rationale, evidence, and final verdict reason), and rejected candidates (each with candidate id, proposal, available evidence or its explicit absence, and final rejection reason). Every raw candidate appears exactly once across the survivor and rejection sections. Keep the full critic and reviewer verdicts in an accounting table keyed by candidate id; the table may reference the candidate sections rather than repeat their prose. Require raw count to equal survivor count plus rejection count. Zero survivors is a valid adjudicated result, never permission to invent a winner; ask whether to revise the subject or constraints instead of asking the user to pick from an empty set.

Create `docs/ideation/` when needed, write only the fixed targets, and read the result back to confirm candidate accounting and evidence completeness. When HTML was requested, render one self-contained HTML view of the canonical Markdown without adding or omitting substance, and check parity on headings, problem frame, worker outcomes, ids, survivors, direction cards, rejections, reasons, citations, and next step. Markdown stays canonical; an HTML mismatch is reported as `non-converged: html-parity` with no claim that the requested set is complete.

Close by reporting the output set, the successful generation-worker count, raw candidate count, survivor count, rejection count, and any recorded worker failures. Ask which surviving direction best matches the user's intent, or whether to revise the subject when none survived. Stop there: never plan, implement, stage, or commit a survivor.

When a run ends incomplete, name the unmet precondition, the affected workers or candidate ids, the partial evidence available, and what unblocks it. Never claim successful independent ideation from an incomplete run. On a write or read-back failure, report the paths created and the failure, and remove only newly created incomplete output files owned by this run after preserving user-requested diagnostics. Never delete pre-existing files. A missing citation or unsupported basis never becomes an invented one: keep the candidate and require an explained rejection.
