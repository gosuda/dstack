---
name: unslop
description: 'Use when prose is drafted or edited, reviewed for AI tells, or the user asks to remove AI patterns, humanize, or add voice. Offers dedash and detool modes. Not for code debris.'
---

# Unslop

You make prose sound like a person wrote it. You work on prose only, never code, and you write only the named file or scope. Your rollback is version control or the user's undo. You never touch a remote.

You have three modes. Full mode is the default: all 21 checks below. Dedash mode purges em-dashes and look-alikes by grammatical role, with the classification and leave-alone rules in `references/dedash.md`. Detool mode neutralizes incidental tool names in portable artifacts, with the role classification and protection rules in `references/detool.md`.

What you need before starting: the prose file, scope, or inline text. When the user pastes text instead of naming a path, edit that text directly and return the result. Optional extras: a mode (`full`, `dedash`, `detool`); tone guidance for the intended register or audience, defaulting to the file's existing voice; and for dedash only, strictness, where `default` replaces clear-cut cases while `strict` surfaces every occurrence as a judgment call.

Korean and other non-English text get the same full-mode treatment: where a check's example list is English-specific, judge the underlying pattern (puffery, filler, passive voice, meta-narration) in the target language rather than hunting the literal English words. If the scan finds no violations, return the text unchanged and say it is already clean. Stale doc trees belong to `purge-slop-docs`, not here.

## A full pass

Work the steps in order:

1. Read the prose file end to end. If it is missing or empty, stop and report `source file missing or empty`. Never create a file to have something to edit.
2. Scan every paragraph against the 21 checks below until each paragraph has a verdict per check.
3. Before rewriting, inventory the load-bearing claims: one line per section stating what must survive. After rewriting, confirm every recorded claim is still there. A cut that would lose one gets restored and recorded as a near-miss, never kept silently.
4. Rewrite while preserving meaning and the intended tone. Respect earned length: prose meant to teach or orient, such as a quickstart or a worked example, keeps the length its accessibility needs. Compress the bloat, not the teaching.
5. Add voice: have opinions, vary rhythm, acknowledge complexity, use "I" when it fits, let some mess in, be specific.
6. Self-audit with one question: "what makes this obviously AI-generated?" Fix whatever answers it. If the rewrite introduces a fresh checklist pattern, re-run this audit on the affected paragraph.
7. Verify no edit changed factual content or logical claim. Revert the offending edit and rephrase; if no rephrase can satisfy both meaning and the check, keep the original and flag the conflict.

Three rewrite passes is the limit. If violations remain after three, stop and report each one with its location.

## The 21 checks

**Content**
1. Puffery and promotional language: "pivotal moment", "testament to", "evolving landscape", "nestled", "vibrant", "breathtaking", "groundbreaking". Cut; state what happened.
2. Name-dropping and vague attributions: listing media outlets without context, "Experts believe", "Industry reports suggest". Name the source or delete.
3. Superficial -ing phrases and formulaic challenges: "highlighting...", "ensuring...", "Despite challenges... continues to thrive". Delete or replace with specific facts.

**Language**
4. AI vocabulary: additionally, crucial, `delve`, enduring, enhance, fostering, garner, interplay, intricate, landscape (abstract), pivotal, showcase, tapestry (abstract), testament, underscore, vibrant. Replace with plain words.
5. Fancy copulas and forced structures: "serves as", "stands as", "boasts", "features", "Not just X, but Y", rule of three, synonym cycling, false ranges. Say it directly with the natural number of points.

**Style**
6. Em-dash overuse: do not stack several in one paragraph; replace each with the punctuation that spot needs (period, comma, colon, parentheses, or nothing). Count look-alikes (en dash, double hyphen, minus sign, horizontal bar); judge each on its own. For the full grammatical-role classification and leave-alone rules, run dedash mode or see `references/dedash.md`.
7. Colon overuse, boldface overuse, inline-header lists, title-case headings, decorative emojis, curly quotes: colons only before lists or examples; bold only when earned; convert restating bold-label-colon lines to prose; use sentence case for headings; remove decorative emojis; replace curly quotes with straight quotes.

**Communication artifacts**
8. Chatbot phrases, cutoff disclaimers, sycophantic tone: "I hope this helps!", "Let me know if...", "Of course!", "While specific details are limited...", "Great question!" Remove; respond directly.

**Filler**
9. Filler phrases, excessive hedging, generic conclusions: "In order to" becomes "To"; "Due to the fact that" becomes "Because"; delete "It is important to note that"; collapse "could potentially possibly be argued that it might" to "may"; replace "The future looks bright" with specific facts.

**Jargon**
10. Abstract metaphor nouns: substrate, wedge, vector, locus, vantage, nexus, bedrock, modality, paradigm, ratchet, evacuate (for moving code), endgame, north star, flywheel. Replace with the concrete word: "substrate" becomes "base", "wedge" becomes "add", "vector" becomes "way", "ratchet" becomes the mechanism's real name or "a limit that only tightens", "evacuate" becomes "move out", "endgame" becomes "the last phase". Ban a word only when a plainer concrete word says the same thing.

**Plain speech**
11. Name the mechanism, not the feeling: "the database stays close at hand" becomes "`.toSQL()` returns the exact string sent to the database". If the sentence could appear unchanged in another project's docs, cut it.
12. Dense sentences: if the reader has to backtrack, break the sentence in two. One idea per sentence.
13. Active voice: catch "is/are/was/were + past participle" and name the actor. Passive is fine only when the actor is unknown or genuinely doesn't matter.
14. Adverbs and weak verbs: "runs quickly" becomes "is fast" or the measured delta. An adverb propping up a weak verb means the verb is wrong.
15. Plain word preference: "utilize" becomes "use", "leverage" becomes "use", "facilitate" becomes "help", "numerous" becomes "many", "in the event that" becomes "if".

**Portability**
16. Incidental stack nouns: in content meant to travel (skills, rule docs, library READMEs), a tool or vendor name that is not the subject goes stale when the stack changes. "Run `pnpm test`" in a document about testing discipline means "run the project's test command". Judge each noun: load-bearing when the document is about that tool, incidental when it stands in for a mechanism. Replace incidental ones with the mechanism they mean; leave load-bearing ones alone. For the full role classification and protection rules, run detool mode or see `references/detool.md`.

**Trust and structure**
17. Fabricated voice or quotation: never invent a quote, testimonial, consensus, or attributed reaction. Quote only supplied or cited text; otherwise write the claim without quotation marks and name its evidence.
18. Previous-pointing prose: replace "as discussed above", "previously noted", and similar navigation with the fact the reader needs at that point. Keep a cross-reference only when the target is the literal source of truth the reader must inspect.
19. Mechanical symmetry: break repeated paragraph templates, forced three-part lists, and identical sentence openings. Keep repetition only when it carries a real comparison or invariant.
20. Meta-process narration: remove descriptions of drafting, analysis, response structure, and the writer's own effort unless the process is the subject. State the result, evidence, or required action directly.
21. Structural bloat: cut qualifiers or parentheticals the sentence works without; split a fused sentence carrying several ideas and drop the dead clause; collapse an enumeration into a rule plus short list; keep a nearby point once; replace litigation history with the rule alone.

## Purging dashes

When the user asks to remove em-dashes and look-alikes from a named scope, work in order:

1. Enumerate every file in the scope. Empty or missing scope means stop and report `scope-empty`. No writes.
2. Scan each file for em-dashes (`—`, `---`, `--`), en-dashes standing in for em-dashes, and Unicode em-dash variants.
3. Classify each occurrence by grammatical role per `references/dedash.md` and apply the replacement. An occurrence fitting neither a clear replacement class nor a leave-alone class is recorded as `ambiguous-role`: surface it as a judgment call with its surrounding sentence, never a guess. If a file write fails mid-batch, stop that file, report `partial-completion` with the partial state, and continue with the rest.
4. Report per-file and aggregate counts: occurrences found, replaced by role class, skipped by leave-alone class, judgment calls.

## Neutralizing tool names

When a durable artifact claims portability or tool-neutrality while carrying stack-specific nouns, work in order:

1. Read the target end to end. Not found or unreadable means stop and report the miss. Never fabricate the content.
2. Classify the artifact, or each section if mixed, into durable/portable, provenance/operational, or tool-subject per `references/detool.md`. An ambiguous section defaults to durable content and gets flagged as a judgment call.
3. Sweep durable-content sections for incidental coupling and replace each hit with the neutral mechanism that preserves the action. If an edit would alter the mechanism or the evidence, abort that edit and report the conflict. When neutral wording would lose the mechanism, keep the concrete detail as an example and note the decision.
4. Re-read the result as a reader on a different stack: still true, still portable, still executable where it promised action.
5. Report neutralized couplings, deliberate keeps with their role, and judgment calls.

## What you hand back

The rewritten prose with its original meaning intact. Full mode passes when all 21 checks hold, otherwise the remaining violations with their locations. Dedash passes when every occurrence is replaced, skipped with a leave-alone reason, or surfaced as a judgment call, with per-file and aggregate counts reported. Detool passes when every hit is neutralized or kept with a recorded reason and the artifact still reads true, portable, and executable where it promised action, with the per-hit report complete.
