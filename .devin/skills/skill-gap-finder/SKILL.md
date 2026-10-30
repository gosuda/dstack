---
name: skill-gap-finder
description: 'Use when the user suspects no installed skill covers a task and wants proof. Names the owning skill or writes a missing-skill brief. Never routes or invokes the matched skill.'
---

# Finding whether a skill already owns the task

You settle one question: does an installed skill already cover this task, or is the gap real? You either name the owning skill or prove nobody owns it. You never invoke the matched skill and never route the user onward. Naming the owner, or writing the gap brief, is where you stop.

This is a read-only job. You consult the installed skill catalog and write nothing persistent. No file, VCS, credential, paid, published, deployed, or remote changes.

## What you need before you start

You need both of these, no exceptions:

- The task description or user request under analysis.
- The installed skill catalog, available at runtime through the host harness.

If the task is ambiguous, stop and ask the user to clarify it before you search. If the catalog cannot be read, stop and report that blocker. Do not guess at coverage from memory.

## Search the catalog like you want to be proved wrong

Pull the core action and the domain out of the task description first. That pair is what you match against, not surface wording.

Then search the catalog exhaustively. Try broad and narrow phrasings of the task so a gap finding means something. A gap declared after one literal search is a false gap. Record the search strategy you used and enumerate the matching set it produced.

## When a skill already owns it

Name the best-matching skill, quote its trigger sentence, and give the selection rationale. Then stop. Do not invoke it and do not route the user to it.

When several skills match equally well, name all of them with their trigger sentences, report the overlap, and let the user decide. Do not break the tie yourself.

When the closest thing is only a near-duplicate, do not fork it and do not stretch its scope. Write a missing-skill brief instead and record the overlap.

## When nothing owns it

Write a missing-skill brief with all three parts:

- The task description.
- The exhaustive search strategy you ran and why it found no match.
- The trigger predicate a new skill would need to cover the task.

Never invent behavior a skill does not have, never fork a near-duplicate, and never widen scope to force a fit. If the search fails, your output is a brief or a clarification request, never a best-effort invocation.
