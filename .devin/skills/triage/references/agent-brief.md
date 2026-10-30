# Writing agent briefs

An agent brief is the authoritative specification an agent works from when an item moves to `ready-for-agent`. For an issue that means building the change from nothing; for a pull request it means what is left to do to the existing diff: finish it, close gaps, or address review points. The original body and discussion are context; the brief is the contract.

## Principles

Durability over precision. The item may sit in `ready-for-agent` for days or weeks while the codebase changes, so write the brief to stay useful: describe interfaces, types, and behavioral contracts; name the types, function signatures, or configuration shapes the agent should look for or change. Never reference file paths or line numbers; they go stale.

Behavioral, never procedural. Describe what the system should do, never how to implement it. Good: the configuration type accepts an optional schedule field of a stated shape. Bad: open a named file and edit a named line.

Complete acceptance criteria. Every brief carries concrete, independently testable criteria. Good: the list command with a stated flag returns well-formed output on success and error paths with unchanged exit codes. Bad: the feature works correctly.

Explicit scope boundaries. State what is out of scope so the agent never gold-plates or assumes adjacent features.

## Template

```markdown
## Agent Brief

**Category:** bug / enhancement
**Summary:** one-line description of what needs to happen

**Current behavior:**
What happens now. For bugs, the broken behavior. For enhancements, the status quo. For a pull request, the state of the diff and what remains.

**Desired behavior:**
What happens after the work is complete. Specific edge cases and error conditions included.

**Key interfaces:**
- `TypeName`: what needs to change and why
- `functionName()` return type: current versus desired behavior
- Configuration shape: any new options needed

**Acceptance criteria:**
- [ ] Specific, testable criterion 1
- [ ] Specific, testable criterion 2

**Out of scope:**
- Thing that must not be changed or addressed here
- Adjacent feature that seems related but is separate
```

## Bad brief

A brief with no category, a vague summary, file paths with line numbers, no acceptance criteria, no scope boundaries, and no current versus desired behavior distinction is rejected. Rewrite it before the item moves to `ready-for-agent`.
