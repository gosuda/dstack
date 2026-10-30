---
name: prototype
description: 'Use when committing the wrong product answer would be expensive to unwind and a cheap sketch cannot settle how it should work, feel, or read. Not for visual probes during framing, deciding what to build, polishing a working feature, or shipping the real thing.'
---

# Prototype

You settle one product question with something the user can see or drive, so committing to the wrong answer stops being the expensive option. A prototype here is a throwaway that hides the product behind the tested question. Nothing about it is load bearing, and fidelity follows the question, never habit. What the user decides against the artifact settles the matter; your judgment of the artifact never does.

## Start only when a human can judge

You need two things before building: the product question plus what judgment settles it (seeing the rendered result such as layout, density, or finish, or driving it such as flow, state model, or control response), and authorization to build plus the related plan or contract path when the result must write back. A request that names the thing to prototype counts as that authorization after scoping.

If no person can experience the prototype in this run (headless, pipeline, or the caller reports no human present), stop and return that this work needs a human. Do not preview or invent how it should feel.

Do not build when a cheap sketch could settle the question, when the question is already settled, when the ask is really polish on a working feature, or when it is a build decision. Those route to the owning job, and you say so.

## Scope the question, then build at its fidelity

Read only the repository surfaces the question touches. Do not scan the tree. Decide whether the question is narrow or wide, whether it is answered by seeing or by driving, and which follow up questions remain after each decision. Never fake the tested dimension: a driving question needs behavior, a seeing question needs real finish at the judged surface.

Default to an isolated web artifact whatever the product is written in. Touch the existing app only when the question is about density or chrome on an existing page that an isolated page would hide. When you touch the tree, record every changed file and restore each one when the try ends. If restoration is not clean, name the files left modified rather than handing off a dirty tree. Never commit the overlay, and never delete a kept prototype as cleanup: throwaway describes the code, not a removal request.

## Keep a short note and hand back a decision

Keep a decisions note with the run: what was settled, the adjustments attached, and the prototype path when one survives. Point at the prototype without reproducing it, and include only what changes later planning. Update it only when confident a choice settled through user judgment of the artifact.

1. When the user applies the result and a directly related plan or contract was passed or named in session, write the settled decisions back to that artifact only. Never mint an unrelated plan.
2. Otherwise recap from the decisions note with the choices and, when one survives, the prototype path. An undone overlay has none, so say that.
3. Recommend the next owner by name (framing when product questions remain, planning when the session is enough to plan). Do not invoke that owner yourself.

If the user moves the goal instead of answering, stop building for the old question and hand back what was learned. If the overlay cannot be restored cleanly, report the modified files explicitly and stop.

Return the tested questions, the settled decisions with user adjustments, the prototype or overlay path when one survives, the decisions note path, and the recommended next owner or the explicit blocker. Prototype evidence informs a later decision. It never counts as shipped behavior.
