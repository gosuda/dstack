---
name: figure-it-out
description: 'Use when non-trivial work should run a matched playbook to verified real-surface completion, or a bespoke workflow when none fits. Not for remote, credential, publish, deploy, or irreversible changes.'
---

# Figure it out

Non-trivial work goes wrong when the agent improvises: invented commands, a second convention beside the repo's own, a green checkmark standing in for the thing the user will actually touch. This skill prevents that. You classify the task against the 23-playbook index in `references/playbooks.md`, run the one playbook that fits end to end, and prove it on the real surface the user will use. When no playbook fits, you design the smallest bespoke workflow that could satisfy a falsifiable success predicate and prove that instead. Either way the run leaves a reviewable trail.

Everything here happens locally in the working tree, where version control is the rollback. Every remote or irreversible action, push, PR creation or any other PR workflow mutation, release, deployment, credential use, branch or worktree deletion, is human-gated: preview it with its exact consequence and get explicit approval for that action before it. Approval for one action never authorizes another.

## What you need before starting

The task itself, including the falsifiable success predicate when you suspect no playbook will fit; the real product surface the result must be verified against, and the tools available; optionally a `playbook-name`, one of the 23 names in `references/playbooks.md` (a valid explicit name wins; otherwise you infer it from the requested outcome); and optionally any existing playbooks or prior workflows worth considering alongside the index.

## Matching the task to a playbook

Select exactly one playbook per requested outcome from the index, classifying by the requested outcome rather than an isolated keyword, and state the rationale (independently requested outcomes may yield ordered names, as the trail below allows):

- unknown cause → `investigation`; defect → `bug-fix`; measured slowness → `perf-issue`; iterative metric improvement → `hillclimb`;
- live-process evidence → `runtime-forensics`; event or span chronology → `trace-forensics`;
- new behavior → `feature`; behavior-preserving restructuring → `refactoring`; throwaway question-answering build → `prototype`; reference-image parity → `visual-parity`;
- agent skill creation → `authoring-a-skill`; model or system measurement → `eval`;
- watching a changing process until a supplied terminal condition → `watch-for` (mode until);
- release or deployment → `shipping`; one delegated unattended objective → `autonomous-run`;
- independently owned units with dependency-aware dispatch → `cloud-task-orchestrator`;
- a complete plan derived, implemented, reviewed, and shipped under approval → `autopilot-full`; ordered layers implemented bottom-up against layer contracts → `autopilot-stack`;
- prior work resumed by reconstructing completed, pending, and blocked state → `session-pickup`; stopping at a consistent boundary with a recorded handoff → `pause-safely`;
- required outcomes spanning dependency-ordered phases → `multi-phase-plan`; worktree and branch inventory with approved disposal → `worktree-cleanup`; a reviewed pull request opened against a base → `opening-a-pr`.

When the classification is genuinely ambiguous, state the competing outcomes and stop rather than silently choosing the cheaper contract. An invalid or unmatched name changes nothing: report it with the 23 valid names and the unmatched outcome. When no playbook fits at all, proceed to the bespoke workflow below; and when a playbook turns out to fit after bespoke work already started, stop the bespoke workflow and defer to the playbook rather than duplicating it.

## Running the matched playbook

State the selected playbook, its concrete target, and its real-surface done check before changing anything. Inspect the repository or running surface just enough to identify its existing commands and conventions; never invent a command or establish a second convention. Then execute the playbook's required actions as defined in `references/playbooks.md`: the host's native primitive for agent, worktree, or PR operations when one exists, otherwise the repository's established git operation for worktrees, the host agent dispatch surface for workers, and `gh` for PR workflow.

Preview each remote or irreversible action with its exact consequence and wait for explicit human approval, one action at a time. Run the playbook's stated done check after all integration. When it fails, keep repairing within scope or return the precise failure. Compilation, a worker report, a checked box, or source inspection never substitutes for the required real-surface observation.

## Designing a bespoke workflow when none fits

Define a falsifiable success predicate first: a check that can fail on the real product, never a tautology. A predicate that cannot fail stops the run until a real one exists. Then design the smallest workflow that could reach it, naming each lever, script, command, probe, or local artifact, with its input and its expected output. State the rollback path for every local artifact the workflow will write before writing any of them.

Build and run each lever in order, recording the command, the real output, and whether it advanced the predicate. When a lever's output contradicts its expected output, record the contradiction and stop advancing: revise the lever or the workflow and re-run from the changed step. Verify the predicate against the real product at the end, never a mock or proxy. When the required operation has no established mechanism, report the unavailable operation as blocked rather than inventing a command, API, path, or peer-skill dependency.

## Recovering without pretending

A failed check or a predicate that fails on the real product keeps its failing observation in the trail: repair the source, rerun the same real-surface check, and roll local artifacts back along their stated rollback paths when the surface is left worse than found. Never claim done while the check is red. An unexpected reversible mutation restores the last known consistent local state before returning. An unauthorized remote or irreversible action stops the run before it, with the exact blocked action and its consequence named. Partial execution ends as reported work, never as done: the completed actions or the failed lever, the current surface state, the failed check, and the next executable action.

## What you hand back

A reviewable trail with `status` (`done`, `blocked`, or `failed`). A playbook run carries the selected `playbook` (or the ordered names for independently requested outcomes), its concrete target, the `actions` completed, the `verification` naming the real surface exercised and the observed result for each playbook, and the `approval` record of each remote or irreversible action approved and performed, or the exact pending action. A bespoke run carries the falsifiable predicate, the bespoke workflow with each named lever, the real output of every lever run, and the final predicate verification result, verified or not verified. Add `next-action` only when blocked or failed. `done` holds only when every selected playbook completed with its real-surface done check passed, or the bespoke predicate is verified on the real product.
