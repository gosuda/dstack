---
name: artifact-arena
description: 'Use when asked to run /artifact-arena to generate and judge competing artifact implementations. Not for remote, credential, publish, deploy, or irreversible changes.'
disable-model-invocation: true
---

# Letting competing implementations fight it out

The user invokes `/artifact-arena` with one artifact in mind. You spawn several candidates that each build it in isolation, have them cross-judged, pick the most maintainable base, graft the best ideas from the losers into it by hand, and verify the synthesis exactly as it would be verified outside the arena. Everything stays local -- candidate worktrees and the synthesis artifact -- with rollback being discarding them. No remote, credential, VCS, or published state is ever mutated.

## Setting a fair fight

State the artifact each candidate must produce as a single contract. From it derive a rubric of 3-6 concrete gradeable criteria, each naming an observable behavior rather than a vague quality. The rubric is the judge's and your tool; candidates see only the task prompt, never the rubric. Give each candidate its own output path -- a git worktree where possible, otherwise a unique local directory -- because candidates sharing one path is shared mutable state and corrupts the result. Alongside the prompt you need the candidate count N (minimum 2), and optionally a model pool and a shared grounding path every candidate reads first; without a pool use available models, preferring a different family for the cross-judge than the parent.

## Running the contest, in order

1. Fan out: spawn all N candidates in one batch, each receiving the task prompt, the grounding path if supplied, and its own output path, and each producing both the artifact and a short rationale naming the alternatives it considered and rejected. The rationale is mandatory -- without it the grafting later is guesswork. A candidate that produces nothing is recorded as a dropout and the arena continues with N-1.
2. Cross-judge: once every candidate has finished -- never while they are still writing, or the judge reads partial output -- spawn one read-only judge, on a different model family from the parent's when possible. It sees the rubric and the candidates by path label, scores each criterion per candidate, and recommends a base with its rationale.
3. Pick the base: read every candidate end to end and score each against the rubric criterion by criterion, never on overall feel. Where you and the judge agree, the pick is confirmed; where you disagree, the rubric was ambiguous or one scorer is biased, so read both rationales and resolve before proceeding. Choose the candidate a future maintainer can extend most easily without breaking invariants, preferring the cleaner boundary or smaller surface on a tie.
4. Graft: walk each losing candidate once more and take what is worth porting -- usually one or two things per candidate -- folding each graft in by hand, re-derived from first principles so the result holds one coherent mental model rather than pasted seams. Record what was grafted from which candidate and what was rejected and why. If every candidate converged on the same shape, say so and ship the consensus with no graft.
5. Verify: run the same verification the artifact would face outside the arena. A failure the arena missed means one of two things -- a candidate already caught it and the graft was missed, so return to grafting, or the frame itself was wrong, so reframe and re-run from the start. Never paper over the failure, and never ship a synthesis that has not passed verification. Then leave one synthesis note alongside the artifact at the base path naming the base candidate, each graft with its source candidate, each rejection with its reason, any dropouts, the cross-judge verdict, and the verification result.

## When the arena cannot crown a winner

Fewer than two candidates producing output means there is nothing to judge: report blocked with the dropout reasons. Losing candidates that diverge wildly instead of converging mean the task was under-specified: reframe and re-run rather than averaging incompatible shapes. A cross-judge that disagrees with you gets its rationale read and resolved, or the rubric reframed when the rubric itself was ambiguous.
