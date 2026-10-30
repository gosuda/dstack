---
name: handoff
description: 'Use when work reaches a session boundary or the user asks to hand off, delegate, or get a clipboard-ready prompt. Mode brief packages continuity; mode prompt builds the delegation prompt.'
---

# Session continuity and handoff

You carry context across the gaps where sessions end: interruptions, session exits, and explicit requests to hand work to someone (or something) else. While work is underway you keep one small live record. Only when the human explicitly asks for a handoff do you package anything, and you never launch the receiver. Two package shapes exist. Mode `brief` writes a compact continuity brief to a file or stdout. Mode `prompt` assembles a clipboard-ready delegation prompt with no filesystem paths in it.

Follow [resume.md](references/resume.md) whenever you decide whether to resume prior state or start fresh.

## Keep one live record while you work

Your continuity set is three files under `.handoff/continuity/`: `notes.md` for goals, scope, and rationale, `graph.md` for the directed graph of task, decision, and blocker nodes with dependency, sequence, and resolution edges, and `death-point.md` for the last completed action, the exact next action, blockers, timestamp, and status. Before the first write, prove `.handoff/` is ignored; if it is not, add the repository-local exclusion and prove it again. Never stage these files.

When starting fresh, write `death-point.md` first with whatever goal, repository identity, session handle, timestamp, status (`active`), and next action you have, and flush that minimal marker before creating the other two files. Then record the goal, scope, repository identity, session handle, and initial rationale in `notes.md`, build the graph, and bring the death point up to date. When resuming, append a timestamped resumption record, mark the prior death-point node `resumed`, and reconcile current facts without rewriting prior decisions or rationale.

Update all three artifacts before continuing whenever a decision lands, a discovery changes the plan, a task changes state, a blocker changes, a phase ends, interruption threatens, or scope shifts. Record what changed and why it matters; leave out tool chatter and intermediate noise. You are done updating when the changed fact is recorded and all three files are flushed.

Endings get marked, not implied. On interruption or ordinary exit, set the death point to `interrupted` with the last completed action, the exact next action, active blockers, and a timestamp. On goal completion, append the achieved result and residual work to the notes, resolve or classify every open graph node, and set the death point to `completed`. A later session always starts fresh after a `completed` marker.

If the prior state is unusable, preserve it, name the reason (`corrupt`, `stale`, `incomplete`, `completed`, or `wrong project`), and start fresh. A lone valid minimal `death-point.md` is an emergency recovery marker: start fresh from its goal and timestamp, then rebuild notes and graph from current evidence. Any other partial set is not a resumable point, so keep every complete artifact and report which file failed.

## Package only when asked, in the requested mode

Packaging starts from an exact source. Use the supplied source handle when one is given, otherwise the current live state. In mode `brief`, a supplied destination path selects where the brief lands. Reject ambiguity and wrong-project matches, and stop to request an exact handle rather than guessing. Before reading source content into a package, apply the exclude list to the canonical project identity and every candidate path; if any source is excluded, refuse the package and name what matched. A stale index never overrides the current exclude list. If the user gave no task and none is inferable from nearby context, stop and ask for the task; emit no prompt.

When a reference arrives as a bare name or description with no locator, stop and ask for one stable handle (a permalink, resource URI, or file:line reference). Never invent the handle; if none is supplied, mark the reference unresolved and carry that status into the package.

## Mode brief: a portable snapshot under 6,144 bytes

Print the source receipt first: session or harness kind, canonical project identity, short session handle, source timestamp, and computed age (treat future or invalid timestamps as unknown age). Warn visibly about work older than seven days, and disclose it when policy withholds newer matching work and this is only the newest visible source.
Write the brief to the supplied destination path when one is given, otherwise under `.handoff/handoffs/` or to stdout, then close with this line:
Then build one UTF-8 brief of at most 6,144 bytes with typed sections for the source receipt, goal and scope, active files, the task/decision/blocker graph, decisions with rationale, evidence, the next action, and `Where it stopped`. Filter out raw transcript, tool output, command dumps, JSON and CLI walls, system reminders, repeated material, and long token runs; keep conclusions in order. Reserve at least one quarter of the budget for `Where it stopped`, which holds the final substantive noise-filtered exchanges or the death-point facts. When truncation is needed, end that section with `[cut for handoff budget]` and put nothing after the marker; never emit an empty heading. Emit no brief until its byte count fits and every required section is nonempty.

Write the brief under `.handoff/handoffs/` or emit it to stdout, then close with this line:

`Continue from this compact context; do not re-derive completed work.`

Report the path or stdout result with the current continuity status (`fresh`, `resumed`, `interrupted`, or `completed`) and the death-point path. On resume, also name any rejected continuity set and why.

## Mode prompt: a path-free delegation

Name the task in one sentence, noting the inference source when the user gave only a short label. Gather enough to orient a fresh agent (repo or product identity, issue, PR, or branch names or URLs, likely modules, constraints, known symptoms, desired output shape) without doing the receiving agent's review or picking its technical direction.

Assemble the prompt from portable anchors only: repo owner and name, product or module names, issue or PR URLs, branch names, public symbols, command names, config keys, exact error text, docs titles, and search terms. Include no absolute, home-directory, checkout, or repo-relative paths unless the user explicitly requested them; a drafted line containing a filesystem path gets rewritten as a portable anchor before copying, or dropped with a noted omission when it cannot be rewritten. Any drafted claim not checked against the repo, issue, PR, or docs gets removed or marked unverified, never presented as reviewed fact.

The first instruction to the receiving agent is review-and-assess, not a work order: the agent owns that review and decides whether the task is still real, stale, already solved, over-scoped, or better handled differently. State constraints, non-goals, validation expectations, and the desired output shape; require a re-check of live repo, GitHub, and CI state; and ban pushing, merging, closing issues or PRs, labeling, or posting without explicit request. When naming where the next session resumes, prefer an addressable compaction-surviving thread (a comment permalink on the tracked issue or review) over a chat-only relay, and cite the thread handle rather than paraphrasing it. Fill every template field below or mark it as needing user input:

```text
I want to discuss and possibly work on: <short task title>

Context:
- <portable repo/product context>
- <what triggered this task>
- <known current state, branch/issue/PR names or URLs if relevant>
- <important constraints and ownership boundaries>

Before doing any implementation:
- Find the right repository from the current directory, a parent directory, or the usual workspace.
- Read the local agent/repo instructions.
- Inspect the relevant code, docs, tests, recent commits, and linked issue/PR state.
- Decide whether this task is still real, whether the proposed direction is a good idea, and whether a smaller or better fix exists.
- Call out stale assumptions, hidden risks, and anything that should stop the work.

Task:
- <what to investigate or implement if the review supports it>
- <expected behavior or decision criteria>
- <non-goals>

Validation:
- <focused tests, checks, or live proof expected>
- <what evidence should be included>
- <what is explicitly not required>

Output:
- Start with the review findings and recommendation.
- Then give the proposed plan or patch summary.
- If you edit code, keep changes scoped and report exact proof run.
- Do not push, merge, close issues/PRs, label, or post public comments unless explicitly told.
```

Copy the full prompt with a temp file or pipe, never inline shell quoting. On macOS use `pbcopy`; otherwise use the platform clipboard tool (`wl-copy`, `xclip`, `clip.exe`). When none is available, print the prompt and state that clipboard copy was unavailable. Confirm tersely with the task title only; do not paste the full prompt unless the user asks.
