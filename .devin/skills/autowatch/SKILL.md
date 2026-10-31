---
name: autowatch
description: 'Use when the user explicitly asks for autonomous end-to-end work from request to open pull request or merge request with CI watched to decided. Not for step-by-step supervised work and never as an alias for lfg.'
---

# Autowatch

One request goes in; the finished state its shape calls for comes out. A code change with publication in scope ends as an open PR or MR whose URL you hold, with CI decided, after implementation, simplification, review, residual recording, learning capture, commit, push, and watch. With no remote and consented local-only, the run instead closes as local-only `DONE`, with push, PR or MR creation, and CI watch skipped. Merging stays with the user unless granted for this run.

This skill owns routing, work-source verification, sequencing, residual handoff, and close-out. Implementation, diagnosis, review, thread adjudication, learning curation, commit authoring, PR or MR publication, and the watch cycle belong to their owning skills. Call those owners with bounded packets and read their returns. Never reimplement them.

## What you carry in

Bring the request itself: a feature, bug report, issue reference, plan path, or a result whose owner is a single skill. An assignment of planning or implementation to a model or harness may ride along on the invocation; sanitize it and pass it as a carrier, never search for it on disk. Carry the explicit grants for this run as well: permission to push, to create or edit the PR, to watch with pushes, to publish a Proof share, and, only when separately stated, to merge.

## Pick the route from what the request is

A plan path, or a plan this session wrote, takes the plan route. A concrete report of failing or wrong behavior takes the diagnose route. A change hanging on an unsettled judgment takes the decision route first, and only a verdict supporting the change continues. Product shape with more than one plausible reading takes framing first when a human is present, otherwise planning. A request whose result is not a code change goes to the skill owning that result, and that invocation is the whole run. Every other code change goes to planning. When unsure, take the route that asks more of the evidence. Never search the plans directory for a candidate or act on a discovered file. Never plan from scratch over an existing plan.

Step-by-step supervised work belongs to `plans`, `fix`, or `commit-push-pr` directly, not here. No `lfg` alias is emitted or accepted.

## Earn the work source before building

On the plan route, brief settled decisions and the artifact-root rule, then use the identified plan only when it passes the readiness check. A `blocked` return, or an invalidated settled decision, stops the run with nothing pushed. Only the absence of both a blocker and a reported plan file invokes planning once with the same arguments. On the defect route, the verified diagnosis fix is the implementation. Without a verified work source, stop and state why.

Implement through the owning skill with a return-to-caller packet naming the verified plan path. Only a valid `complete` return advances. Every other status or malformed return stops the pipeline.

## Shape the diff, then prove it reviewable

Simplify the branch diff when the change exceeds a trivial docs-only or sub-10-line edit. Skipping that invocation is allowed only with the reason stated.

Review the branch diff against the plan, omitting the plan link on the defect route. A finding whose evidence shows the settled decision cannot work (infeasible, wrong thing, destructive) stops the pipeline as blocked before any shipping precondition.

Apply eligible review fixes and persist them. Do not proceed while eligible fixes remain uncommitted. Record every unapplied actionable finding, conflict stamp, or flagged decision durably: in the PR or MR body when one will exist, otherwise in tickets or the `DONE` report. Never output `DONE` while residuals live only in memory. A tracker-write failure never blocks `DONE` once the report states it. Do not prompt inside this autonomous run.

## Check the shipping precondition before every push

Run `git remote`. When empty, require explicit consent to proceed local-only. On consent, make every commit the steps call for, then skip push, PR or MR creation and editing, and CI watching entirely, and close as local-only `DONE`. On withheld consent, stop with nothing committed. Never invent a remote, change the URL, or proceed silently. A configured remote alone grants no publication authority.

Capture learning only when the run produced durable reasoning the code, tests, and plan do not carry, by invoking `compound` once in non-interactive mode. `Documentation skipped` is success. The learning lands in the PR or MR at open when one will exist.

## Publish with the grant, watch to decided

Publish through `commit-push-pr` in its full or no-PR mode per the granted scope, with an explicit publication grant. The forge comes from the verified remote or request URL (GitHub PR or GitLab MR). Ambiguity stops the run; the forge is never guessed. Creation and update use body files and non-interactive flags only after the exact approved preview, and no MR command offers a general dry-run. Never push a set the human has not approved in shape. Autowatch carries the invocation grant, not a silent default.

When an open PR or MR exists and watching was granted, watch it with `watch-and-repair-pr` to CI-decided (GitHub checks or the GitLab MR head pipeline). Never reimplement CI watching, poll by hand, or substitute another watcher. Without a grant or without an open PR or MR, record CI as unwatched with its reason.

## Close out with the full accounting

Finish with one line stating `DONE` plus the PR or MR URL when one exists, the CI decision, residuals location, and learning outcome. Or name the exact stop (no work source, blocked review, withheld consent, local-only, missing grant, out of budget) with what was left unpushed and where residuals live. A stop leaves nothing pushed that was not already pushed.

Stop without pushing anything new on a missing work source, a blocked plan or diagnosis, a non-complete implementation return, a blocked review finding, a missing push, PR, MR, watch, publish, or merge grant, an incomplete or malformed child return, an invalidated settled decision, an unmet project shipping gate, or an exhausted budget. Complete all reachable local work, record residuals, and report the missing grant or bound. Never retry by broadening scope.
