---
name: state-machine-workflow
description: 'Use when work has distinct modes and the user wants states, events, guards, outcomes, illegal transitions, not a prose todo list. Not for remote, credential, publish, deploy, or irreversible changes.'
---

# State machine workflow

Some work is not a todo list. The system sits in one mode at a time and moves between modes on events. When that is the shape of the problem, write it down as a state machine: every mode named, every move guarded, every forbidden shortcut called out, so the result can be encoded directly in types, a state-machine library, or a runtime enum.

This skill writes one specification file to the project and nothing else. It never touches remote systems. Rolling back is deleting that file.

## What you need before you start

You need a description of the domain, process, or system being modeled: who owns the states and where the boundary sits. Optionally, an existing list of states or transitions to refine, or an existing state-machine file to extend. If the domain is too vague to enumerate states from (no named entity, no boundary, no modes), stop and ask the user to supply them. Do not invent scope.

## Building the machine

Work through these in order. Each step has a bar for moving on. Do not skip ahead past an unresolved step.

1. Confirm the scope with the user first. Name the system boundary and the entity or process that owns the states, and move on once the user confirms the boundary.
2. List every distinct mode the system can occupy. Name each state as a noun or adjective-noun pair describing the mode, not the action that caused it. Give each an entry condition and at least one outgoing transition, and move on once every state has both.
3. For each state, list every valid move to another state with all five fields: source state, destination state, triggering event, the guard condition that must hold for it to fire, and the outcome or side effect it produces. If two guards contradict each other or a state turns out unreachable, surface the contradiction with a proposed resolution and do not write until it is resolved.
4. For terminal and milestone states, name the concrete observable result: a file written, a decision recorded, a value returned, a signal emitted. Vague outcomes do not count.
5. For every pair of states where a direct transition must never occur, name the pair and say why it is forbidden. These guard against invalid shortcuts.
6. Check four things: every state has at least one outgoing transition (no dead states except explicit terminal states); every path from the initial state reaches a terminal or outcome state; no two transitions from the same state share an identical event and guard; every guard references a condition observable within the scoped domain. Fix failures before continuing.
7. Show the full specification as a structured table or diagram (states, transitions, guards, illegal transitions) and ask the user to confirm. If the user rejects the enumeration, revise from their feedback. Never write a specification the user has not approved.
8. Write the specification to the project using the format it already prefers (Markdown table, Mermaid diagram, or code). With no preference, write a Markdown file with sections for states, transitions, guards, outcomes, and illegal transitions.

If only part of the machine is complete and approved, write only that part and mark the rest as open. Never present unfinished states or transitions as stubs or placeholders.

## What you hand back

The specification file: all states with entry conditions, all transitions with source, destination, event, guard, and outcome, all terminal outcomes, and all illegal transitions with rationale. It should be sufficient to encode directly.
