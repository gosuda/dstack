---
name: humanizer-simple-english-asd-ste100
description: 'Use when asked to rewrite technical English for STE compliance, stripping ambiguity and AI-style patterns. English only; not for Korean: use humanizer-korean-plain or humanizer-korean-ste.'
---

# Humanizer Simple English ASD-STE100

Rewrites technical English toward ASD-STE100: short, explicit, one-meaning sentences that keep exactly what the source said. Read-only work. The rewritten text comes back in chat; nothing is written to files, and this skill never touches VCS, credentials, paid services, published pages, deploys, or remote systems.

## When to reach for it

Use it when the user asks for a technical English rewrite, STE compliance, a controlled-language pass, disambiguation, or de-slopping of a manual or document. Source text is required, inline or as a file path the user names.

Do not use it for creative or persuasive copy where voice is the mechanism. If the source is marketing or literary prose, say so plainly: "STE is not applicable to creative or persuasive copy; this text uses voice and nuance as its mechanism and should not be flattened." Do not use it for Korean text; hand Korean to the Korean humanizers instead.

## Pick rewrite or write

State the chosen mode in one line before doing anything else.

- `rewrite` is the default for explanatory prose. Apply the structural rules fully; treat the lexical rules as advisory, flagging departures without enforcing them.
- `write` is the default for procedures and error strings. Apply every rule below fully.

If the user names a mode, honor it. If they do not, infer it from the document type as above. An optional `rule_table` flag (default off) adds a before/after violation table after the rewritten text when set to `true`.

## Read the source first

Walk the text sentence by sentence and note every rule violation before rewriting anything. Do not start rewriting until you know what the text must still say afterward. For a long document, divide it into exact, non-overlapping sections and account for every section in the return; copy tables, code, and other non-prose regions unchanged.

## Structural rules, always on

These hold in both modes:

| Rule | Do | Do not |
|---|---|---|
| Active voice (Rule 3.6) | "The agent deletes the file." | "The file is deleted," unless the actor is genuinely unknown |
| No phrasal verbs (Rule 9.3) | "Remove the panel." / "Start the job." | "Take off the panel." / "Spin up the job." |
| One instruction per sentence (Rule 5.2) | "Open the file. Read line 3." | "Open the file and read line 3, then check if it matches." |
| Sentence length | At most 20 words for procedures, 25 for descriptions | Compound sentences with piled-up clauses |
| No semicolons (Rule 8.1) | Split into separate sentences | Any semicolon |
| Noun clusters (Rule 2.1) | At most 3 stacked words ("fuel pump valve") | 4 or more stacked nouns |
| No ellipsis | Keep subject, verb, and article explicit | Drop words to save space |
| Paragraph limits | One topic per paragraph | Multi-topic paragraphs |
| Lists for sequences | Numbered or bulleted list for 3 or more steps | A sequence buried inside prose |

## Lexical rules and what can actually be checked

In `write` mode these bind; in `rewrite` mode flag the departure and leave the wording alone:

| Rule | Direction |
|---|---|
| One word, one meaning | Same word for the same concept throughout; never rotate synonyms |
| Verb, not noun (Rule 3.7) | "Analyze the log." not "Perform an analysis of the log." |
| Simple tenses (Rule 3.2) | Infinitive, imperative, simple present, simple past, simple future; avoid present perfect unless current relevance is asserted |
| Domain terms | Keep necessary technical nouns; define each once if it is not common English |

No ASD-STE100 dictionary ships with this skill, so full dictionary certification is not claimed. Structural compliance is fully verifiable here; lexical departures beyond the table above are reported as unverified, with the reason stated, rather than certified.

## Keep meaning and modality intact

Hedges ("may", "could", "is likely to") carry the author's confidence. Never promote a hedge into a fact to make a sentence shorter; keep the longer form and flag the trade-off.

For normative documents, every requirement keeps its subject, modality, condition, exception, ordering, and consequence. Keep identifiers, numbers and bounds, error codes, references, citations, backtick tokens, uppercase states, anchors, tables, and code exact unless the user explicitly asked to change them. A sentence split may repeat a modal but must never detach it from the clause it governs. Keep domain terms and intentional restatements that independently implementable sections need. Never delete apparent redundancy as part of a style pass, and never add a fact the source did not state. Requirements are compared one by one: equal token, numeric, or modal counts can still hide a reversed prohibition or a requirement given to the wrong actor. This pass creates no scratch files and does not install or commit anything.

## What you hand back

Return the complete rewritten text in chat, with unresolved ambiguities and lexical residuals named alongside it. If the `rule_table` flag is on, append the markdown table of violations found. If the input already complies, say so and return it unchanged. If the source text is empty or absent, return "No source text provided." If a rewrite would need a fact the source lacks, keep the original phrasing, flag the gap, and note the ambiguity instead of inventing the fact. For a long, partly compliant text, return the compliant portion with residuals flagged rather than returning nothing.

The rewrite is finished when the returned document carries no structural STE violations and every lexical departure is named.
