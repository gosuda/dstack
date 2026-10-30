---
name: spec-driven
description: 'Use when starting a project or feature, requirements are unclear, or a change crosses modules. Accepts new specs and already-approved specs via the existing-spec entry.'
---

# Spec-driven development

Vague requirements become a reviewed spec, the spec becomes an approved plan and task list, and the tasks get built through tests that attack the acceptance criteria. Nothing gets implemented until a human has approved the spec behind it. All writes stay local to the working tree, with version control as the rollback. Remote mutation, credential exposure, and irreversible actions are outside this skill.

Call on this skill for a new project or feature, unclear requirements, a change crossing modules, or work past roughly 30 minutes.

## Map capabilities before specifying

Every request needs its scope anchor first: the module, package, or directory boundary the work affects. The anchor bounds the spec, and work outside it belongs in a separate request. Single-capability requests go straight to a spec once anchored. Decomposition comes first only when one requirement bundles several independently testable capabilities: distinct capabilities with their own consumers or data, acceptance criteria that cluster into separately shippable groups, or one capability cuttable without rewriting the others.

For a bundled request, propose a small capability map: a module table with build order, stable kebab-case module ids chosen once, one-way dependency arrows with no cycles, and contracts living in the provider module spec. Save the approved map at the project root and name each module spec after its id. Module boundaries decided mid-implementation count as unapproved, so a multi-capability spec without an approved map stops here.

Already holding an approved spec? Skip the mapping, assumptions, drafting, and review steps below and enter at planning. Map every requested behavior to at least one spec statement, list each unmapped request as a spec gap, and stop until the gap is approved as a spec addition. A spec may describe approved new behavior contradicting current implementation. That is a migration directive, not a conflict to surface and stop over. A previously pushed commit never exhausts authority for new reversible local edits.

## Surface assumptions, then write the spec

List every assumption under consideration and get each one corrected or confirmed. Ambiguous requirements never get silently filled.

The spec covers six areas:

- Objective: what gets built and why, who uses it, what success looks like.
- Commands: full executable build, test, lint, and dev commands with flags, for the stack the project actually uses.
- Project structure: where source, tests, and docs live.
- Code style: one real snippet in the project language showing naming and formatting rules.
- Testing strategy: the seams where the feature gets tested, preferring an existing seam, with framework, locations, coverage expectations, and which level covers each concern.
- Boundaries in three tiers: always do, ask first, never do.

Vague requirements get reframed as testable success criteria with confirmed targets. Where the project already uses an artifact format, keep it. This skill owns clarification, content, and approval gates rather than any external tool format.

## Get approval at each gate, in order

Present the spec to the human and wait. Once it is saved, summarize it, list open questions, and stop the turn. Planning and code never start in the same turn.

From the validated spec, plan components and dependencies, implementation order, risks with mitigations, parallel versus sequential work, and verification checkpoints between phases. Every implementation step gets validated against the codebase before seeking plan approval: each referenced path, type, and interface exists or is created by an earlier step, and each unconfirmable reference lands in Open questions with the check that would settle it.

Present the plan and wait for approval. Break the approved plan into discrete tasks, each finishing in one focused session with explicit acceptance criteria, a verification step (test, build, or manual check), dependency ordering, and no more than about five files touched. Present the task list and wait for approval.

Withholding approval ends forward motion. Surface the specific objection and wait. A scope widening or a late-breaking assumption sends the work back to the spec: update it, get approval, then proceed.

## Build through attacks, keep the spec alive

Each task turns its acceptance criteria into attacks that must fail red for the right reason. Implementation continues until the attacks stop breaking the code. Tests and fixtures never get bent to reach green. Load only the spec sections and source files the current task needs.

Decisions or scope changes update the spec first, then the code. Commit the spec alongside the code and reference the spec section each change implements. Without a written, saved, approved spec, the work is not done and implementation should never have started. Where the human never approves, the skill ends with no implementation, stated explicitly.
