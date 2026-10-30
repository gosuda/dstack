---
name: design-gate-brainstorming
description: 'Use when creative work is requested with no approved design, or a raw idea or repository must be developed into an approved design document. Not for work with an approved design in context.'
---

# Design gate brainstorming

Creative work waits for an approved design. When a feature, component, or behavior change arrives with no approved design in context, stop before implementing and work the design first. If an approved design is already present, stand down, as this skill does not route.

Everything here is local and reversible. The idea path saves a design document, a builder profile, and session analytics records. The architectural path writes a spec document and may dispatch a spec-reviewer subagent. The bounded path keeps the design in chat. The spike path produces a recommendation only, and any code it sketches is labeled throwaway. Opening a URL is a read, so never mutate a remote resource. Roll back by deleting the files this run wrote.

## Pick exactly one path

Name the path before doing anything else. When the request does not clearly fit one, ask the user to choose rather than defaulting silently.

| Path | When it fits | What it produces |
|---|---|---|
| Idea | The input is a raw idea or a repository to develop, with no change to existing work named | A saved design document |
| Spike | The question is exploratory or the design space is unknown | A recommendation only, with any code labeled throwaway and never committed as durable work |
| Bounded | The change fits one component or a small, well understood surface | An in-chat design covering goal, constraints, key decisions, and open questions |
| Architectural | The change crosses module boundaries, alters a contract, or has durable blast radius | A spec document saved to a local file under the project, covering problem, constraints, design, alternatives considered, and risks |

## Work the idea path

Gather context from the supplied idea or repository. Run the startup diagnostic first: name the problem, the intended audience, and the hard constraints. Then run the builder brainstorm: enumerate candidate approaches, select the strongest against the diagnostic, and record why it won.

Draft the design document around problem, approach, scope, and open questions. Before saving anything, redaction-check the draft by scanning for secrets, credentials, and private data, and remove or redact every match. A draft that still contains a secret is never saved. Redact it or ask a human to remove it, then re-run the check.

Save the redaction-checked design, the builder profile (who is building, with the constraints and preferences observed this session), and the session analytics records (source kind, diagnostic summary, selected approach, confidence tier) to local files. If the idea or repository is missing, stop and ask for it, and write no file. If the repository is unreadable or a URL open fails, record the gap, proceed with what is available, and mark the confidence tier down. If only some sections are complete, save just those, mark the incomplete ones explicitly, and never fabricate the rest.

## Work the architectural path

Self-review the spec against its own acceptance criteria, then dispatch a spec-reviewer subagent if one is available, and revise until self-review is clean. If no reviewer is available, proceed on self-review alone and note the missing review in the handoff. A spec that cannot reach a clean state is never handed off. Stop and report what blocks it instead.

## Close every path with approval

Present the result and ask the user for explicit approval before any implementation. The idea path closes in tiers: a summary of the saved design, a confidence tier, and an offer of the next skill for the build phase.

Record the decision as approved, approved-with-changes, or rejected. Nothing implements until approval is recorded, and a rejection or change request means revising the design or recommendation and asking again, never implementing through it. Then make the terminal handoff. Idea and architectural paths hand the approved document to the plan writer. The bounded path's approved in-chat design and the spike path's recommendation are themselves the terminal output.
