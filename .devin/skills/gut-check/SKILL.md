---
name: gut-check
description: 'Use when a user asks for a gut-check on a decision or action, or asks whether enough is known to proceed. Not for numeric confidence scoring.'
---

# Say whether there is enough to proceed

You read the situation as it stands and return one plain verdict: proceed, proceed with a caveat, pause, or blocked. You assess only the decision or action the user asked about. You never widen into dimensions outside that question, and you never score confidence with numbers. The assessment stays prose.

By default you change nothing. When the user explicitly requests an output file, you may write that one named local artifact, and only when the path does not already exist. An existing path is refused, never overwritten; ask for a different path. Rolling back means deleting the file you wrote. You touch no version control, credentials, paid services, published or deployed surfaces, or remote systems.

## What you refuse

Numeric confidence scores have no place here. If the evidence is thin, say the confidence is lacking in words; do not dress a gap up as likely or probably resolvable to dodge a pause or a blocked verdict. Do not assess anything outside the user's stated question.

## Reading the situation

Name the specific decision, plan, or action the user's words frame. Then list the concrete facts that bear on it: confirmed source evidence, direct tool outputs, and explicit user assertions found in this session. State only what the evidence supports; do not infer or assume the rest.

Next to the facts, name each concrete gap: missing credentials, absent files, unverified assumptions, required human input, blocked tool access. Give every gap one of two labels:

| Label | Meaning |
|---|---|
| Executable | A concrete next step the user can take now resolves it. |
| Blocked | It needs an external dependency or a capability not currently available. |

Write the assessment in two parts, known and unknown, with no numeric score anywhere. Name each known fact that bears on the decision. Name each gap specifically, without generalizing or hedging.

## Giving the verdict

End with one terminal recommendation and its justification:

| Verdict | When it applies |
|---|---|
| Proceed | No gaps, or only trivial ones. |
| Proceed with caveat | The gaps are executable, and you name the caveat as a fact. |
| Pause | At least one decisive gap is executable, and you name its resolution. |
| Blocked | At least one decisive gap is blocked. Name the missing capability or dependency rather than softening the call to a pause. |

When the user's ask frames no actionable decision or action, say what you need framed and stop without producing an assessment. When the workspace hides what you need, name exactly what is missing and stop; do not simulate the data. Written to a file only when the user explicitly requested one, the result holds known, unknown, and the single recommendation, in that order.
