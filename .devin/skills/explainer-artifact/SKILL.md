---
name: explainer-artifact
description: 'Use when asked to create an explainer document for a concept, diff, idea, or work recap. Drafts and verifies it in a scratch directory. Not for one-screen explanations: use explain-concept.'
disable-model-invocation: true
---

# Drafting an explainer the user can keep

You produce a durable explainer document for a concept, diff, idea, or work recap window, verify its structure, show it to the user, and stop. You write only inside one isolated scratch run directory under `/tmp/dstack-$(id -u)/explainer-artifact/`. Deleting the run directory rolls back the run. No remote mutation occurs. A human performs any publication or remote relocation.

A run that ends without an artifact still counts as done: an operational question answered in chat, an empty recap window, or a bare invocation the user did not answer.

## Sorting the request

Classify the request into one input shape (concept, diff, idea, or work recap window) plus its audience. Classify plain language with no token by meaning. Use the invocation content or the current prompt; the audience defaults to the user and the output format defaults to HTML unless intake resolved `output:md`.

Routing guards apply here:

- A verdict question ("Should we adopt X?") is not taught.
- A request to document a solved problem for future work is not taught.
- An idea input is explained as given, with its implications and trade offs. Never expand it into options or a requirements dialogue.
- A diagnostic question ("why is this failing?") is answered in chat rather than taught.
- Concept versus diff tiebreak: when a phrase names both a concept and a repo path, prefer diff when a ref is supplied and concept otherwise.

## Asking when nothing was supplied

On a bare invocation, ask one blocking question ("What should I explain?"), offering a shortcut option for a recap of recent work in this repo alongside free text. Produce no default artifact unprompted. If the user does not answer, the run ends as done with no artifact.

## Opening the run directory

Create the run directory with this block as written, since the checks refuse a scratch root not owned by the agent or one reached through a symlink:

```bash
SCRATCH_ROOT="/tmp/dstack-$(id -u)";
[ ! -L "$SCRATCH_ROOT" ] && (umask 077; mkdir -p "$SCRATCH_ROOT") 2>/dev/null && [ ! -L "$SCRATCH_ROOT" ] && [ -O "$SCRATCH_ROOT" ] && [ -w "$SCRATCH_ROOT" ] || SCRATCH_ROOT="${TMPDIR:-/tmp}/dstack-$(id -u)";
if [ -L "$SCRATCH_ROOT" ]; then echo "unsafe scratch root symlink: $SCRATCH_ROOT" >&2; exit 1; fi;
(umask 077; mkdir -p "$SCRATCH_ROOT") || exit 1;
if [ -L "$SCRATCH_ROOT" ] || [ ! -O "$SCRATCH_ROOT" ]; then echo "scratch root is not owned by the current user: $SCRATCH_ROOT" >&2; exit 1; fi;
chmod 700 "$SCRATCH_ROOT" || exit 1;
RUN_DIR="$SCRATCH_ROOT/explainer-artifact/$(date +%Y%m%d)-$(openssl rand -hex 3)";
(umask 077; mkdir -p "$RUN_DIR") || exit 1; chmod 700 "$RUN_DIR" || exit 1;
echo "$RUN_DIR";
```

If this block exits with an unsafe scratch root error, no artifact is written. The user supplies or fixes the scratch root and the run is retried.

## Gathering grounding material

Sufficiency criteria per shape:

- Concept: at least one source citation per major claim, or the claim is marked unanchored. Gather from `CORPUS.md` when it exists, or ask once which source to ground in.
- Diff: the ref resolves to one or more commits. For an empty range (the ref resolves to no commits, for example `main..HEAD` with uncommitted work): say what the ref resolved to, name the nearest real candidate (the working tree, the last commit), and use it only after the user agrees. When the user cannot be asked, use it and state the substitution in the artifact `Subject`.
- Idea: the idea is stated in the user words. No external sourcing is required.
- Recap: the window resolves to repository activity. Do not pre-scan or characterize the window in the main conversation before the artifact is composed. For an empty window: say so, offer to widen it, write no artifact, and end after the user responds. This is a done run, not a failure.

In diff mode, gather silently. Nothing learned while gathering reaches the user until the ordering rule below is satisfied.

## Offering a check in

Judge whether the material warrants a check in (a substantial change or concept the user is likely to need to recall). Offer it with the blocking question tool, recording the user exact choice as Just the explainer or Quiz me. Only Quiz me enables the prediction and exercise mechanics. Just the explainer skips both but still composes and presents the report. If the warrant test skips the offer, proceed without either mechanic. Do not offer it again after the user declines. In diff mode, word the offer without describing the change content or purpose, so the offer does not pre-leak the reveal.

## Holding the reveal under quiz me

With Quiz me selected in diff mode, no interpretive content, explanation, annotation, diagram, or surfaced opportunity appears before the user prediction turn ends. Show only the raw change reference (the diff or its stat summary), ask for the prediction ("What do you think this change does, and why was it made?"), and end the turn there. When no blocking tool exists, ask in chat and stop. Compose the explainer only after the prediction lands. The reveal names the gaps between the prediction and what the change does.

## Composing and verifying the artifact

Write the artifact to `$RUN_DIR/explainer.html` (or `explainer.md`) before anything else happens with it. Default format is a single self contained HTML file. Voice is personal by default, adapted for another reader on request at unchanged depth. Then establish the checked state:

- Structural check: the file parses as valid HTML (or valid Markdown); no unresolved template placeholders remain; all internal section anchors resolve.
- Link check: every external link in the artifact either resolves to a live URL or is marked `[unchecked]` next to the link text.

If the structural check fails, fix the artifact and re-check once. If it still fails, report the structural error and do not present the artifact as checked.

## Running exercises

Pose exercises in chat only when the recorded choice was Quiz me, one at a time, using the blocking question tool where its option shape fits and free chat where the answer is narrative. Check each answer, correct it, and name the gap it exposed. Never put exercises inside the artifact. When the choice was Just the explainer, skip this step.

## Closing with the destination

Ask for the destination once with the blocking question tool. Never publish without human interaction or infer consent: a destination the user named up front is a choice of destination, not consent to publish. For any destination requiring publication or remote relocation, present the full warning, require explicit confirmation after the user has seen it, and stop. Hand publication or relocation to the human rather than executing it. If the consent sequence cannot be completed, do not publish. A failed publish never deletes the artifact. Report the local `$RUN_DIR/explainer.html` path with publication as an unexecuted human handoff. When no interaction is possible at this ask, do not hang or discard the artifact. It is displayed and stable at its path. Report the local path and end.
