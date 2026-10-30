# Authoring levers

The reasoning behind the craft in `SKILL.md`. Load this file when a claim there is not enough to act on.

## Context pointers

A context pointer is a reference held in the agent's context that names out-of-context material and states when to reach it. A skill description is one. A line in AGENTS.md naming a doc is the same object.

The wording decides when the agent reaches the material and how reliably. A must-have target behind weak wording is a wording bug: sharpen the pointer first, and inline the material only if sharpening fails.

A pointer carries two things: what the material is, and which branches trigger reaching it. Every word of an always-loaded pointer costs on every turn, so it earns harder pruning than the body. Lead with the operative word, give one trigger per branch, merge synonyms that rename a single branch, and cut identity the body already carries.

## The two loads

Every document and pointer spends one of two budgets.

Context load is the cost of always-loaded material on the agent's window: an AGENTS.md line, a skill description, anything sitting in context every turn, spending tokens and attention whether or not it fires.

Cognitive load is the cost on the human: which documents exist, and when to reach for each. The human is the index. Spend it where human judgement matters and remove it where it does not.

Material behind a pointer escapes context load at the price of the pointer's own line. Material with no pointer at all rides entirely on the human remembering it.

## The information hierarchy

A document mixes two content types freely: steps, the ordered actions the agent performs, and reference, the definitions, rules, and facts consulted on demand.

The core decision is where each piece sits. An in-file step is the primary tier: what the agent does, in order. An in-file reference is consulted on demand. A disclosed reference moves to a separate file behind a pointer and loads only when the pointer fires.

Push too little down and the top bloats. Push too much and material the agent needs goes into hiding.

## Progressive disclosure and co-location

Progressive disclosure moves material down the ladder, out of the main file and behind a pointer, so the top stays legible. Branching is the cleanest test: inline what every branch needs, push behind a pointer what only some branches reach. When a document has steps, reference that should be disclosed buries them and turns attending to them into a coin flip.

Co-location keeps a concept's definition, rules, and caveats under one heading rather than scattered.

Sprawl is the failure mode: a document too long even when every line is live and unique. The ladder is the cure.

## Completion criteria

Every step ends on the condition that tells the agent the work is done.

Clarity asks whether the agent can tell done from not done. A vague bound invites early finishing, because the visible later steps pull forward and only the criterion's clarity resists. Sharpen the bound first, and only when it stays irreducibly fuzzy and you observe the rush, move the sequence across a real context boundary such as a hand-off or a subagent dispatch. An inline call leaves the later steps in context and changes nothing.

Demand asks how much the criterion requires. A bound that names every affected item forces thorough work where a bound that asks for a list does not. Demand drives the digging the agent does inside the work, and it is the lever most worth pulling.

## When to split

Splitting one document into two spends one of the two loads, so split only when the cut earns it.

Split by sequence where a run of steps lets the later steps tempt the agent to rush the one in front of it. Merging sequences back exposes each step to what follows, which invites the same early finishing.

Split by invocation when a distinct leading word should trigger the material on its own, when a trigger word actually appears in prompts, or when another skill must reach it. The new always-loaded description costs context load regardless, so that independent reach has to be worth it.

## Leading words

A leading word is a compact concept already living in pretraining that the agent thinks with while running the document. Repeated as a token, never restated as a sentence, it gathers a working definition across uses and anchors a whole region of behaviour in the fewest tokens.

Prefer a word that already exists. A coined word works only with a clear definition, and it recruits no priors.

The same word anchors twice. In the body it steadies execution: the agent reaches for the same behaviour every time the word appears. In a pointer it steadies invocation: when the word lives in prompts, docs, and codebase alike, the agent links that shared language to the material and reaches it more reliably.

## Pruning

Keep each meaning in a single authoritative place, so changing the behaviour is a one-place edit. Duplication, the same meaning in more than one place, costs maintenance and tokens.

The environment is an authoritative place too: package scripts, config files, directory layout, help output. A document that restates one is a cache, a copy of a lookup, earning its load only when the lookup is expensive. Cache what the agent cannot find by looking: the unwritten convention, the reason behind a choice, the gotcha no config confesses.

Check every line for relevance. Ask whether it still bears on what the document does. Shorter documents stay relevant more easily.

Without a pruning discipline the default fate is sediment: stale layers kept because adding felt safe and removing felt risky. Core down through them to what is still live, and delete sentences that fail the no-op test.
