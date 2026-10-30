# Skill mechanics

What changes when the document is a skill: frontmatter, the invocation choice, and router skills. Everything else about writing it follows the craft in `SKILL.md`.

## How the skill fires

Two choices, trading the two loads.

A model-invoked skill keeps a `description`, so the agent fires it on its own and other skills can reach it. Typing its name still works: model invocation always includes user reach, and a description only adds agent discovery without ever removing the human's. The description is the skill's top-level context pointer, loaded at all times, permanent context load in exchange for discoverability. A model-invoked skill whose content is all reference also serves as one home for shared reference: another skill can invoke it, so reference needed by several skills lives in one place. Mechanics: omit `disable-model-invocation`, and write a model-facing description that carries the trigger branches (the pointer rules in `SKILL.md` apply in full).

A user-invoked skill strips the description from the agent's reach: only the human typing its name fires it, and no other skill can. Zero context load, at the price of cognitive load, since you become the index that remembers it exists. Mechanics: set `disable-model-invocation: true`, and write the `description` as a one-line human-facing summary with trigger lists removed.

Pick model invocation only when the agent must reach the skill on its own or another skill must. When it fires solely by hand, keep it user-invoked and pay no context load.

Shared reference that two user-invoked skills both need lives in neither. With no model-facing descriptions neither can fire the other, so push it to a plain file outside the skill system that any skill points at.

## Splitting by invocation

Split off a model-invoked skill when a distinct leading word should trigger the material on its own, when a trigger word actually appears in your prompts, or when another skill must reach it. The new always-loaded description costs context load, so that independent reach has to be worth it.

## Router skills

When user-invoked skills multiply past what you can remember, cure that piled-up cognitive load with a router skill: one user-invoked skill that names the others and when to reach for each, so the human remembers one skill instead of many. It can only hint, never fire them, since nothing but the human reaches a user-invoked skill.
