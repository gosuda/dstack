# Slop patterns for docs purge

Use with `SKILL.md` step 2. The evidence tests in `SKILL.md` decide whether a passage is a finding; this catalog names the wording pattern and the fix. For document-level ownership, staleness, and pointer rules, `SKILL.md` governs.

Source: `ce-noslop` `SKILL.md`, `references/patterns.md`, and `references/terminology.md` from `EveryInc/compound-engineering-plugin` at `fbd794f329f5b65d0ea00a5e6487336c385ff2be`. Rule numbers below preserve the upstream stable ids. MIT, Copyright (c) 2025 Every. This file rebuilds only the purge-relevant subset for bounded Markdown-tree cleanup. Chat authoring modes, channel-marketing routing, and strategy behavior were not imported.

A single device is a choice, not a tell. Flag a passage when patterns accumulate or a deterministic check confirms the claim is unsupported, and never flag text inside quotation marks, titles, or code, a term the domain uses for one exact meaning, deliberate repetition for emphasis, a scope statement, a safety notice, a real correction, one short sentence for emphasis, or a heading or sign-off in a letter.

## Mapping from purge classes to pattern rules

| Purge class | Rules | Fix |
|---|---|---|
| Empty ceremony: importance claims, significance tails, promotion | 1 puffery, 2 trailing -ing analysis, 3 promotional adjectives, 5 formulaic outlook | Delete the claim or clause and keep the fact; keep one real limitation or plan stated plainly |
| Empty ceremony: unsupported attribution and setup | 4 vague attribution, 6 setup-reversal copy, 7 faux insight, 8 metadiscourse, 9 rejected alternative no one raised | Name the source or cut the claim; never invent a source; cut the setup and state the real constraint |
| Jargon and mechanism | 10 model vocabulary (including `delve`, `leverage`, `tapestry`, `showcase`, `garner`, `intricate`), 11 dressed-up copulas, 20 borrowed metaphors for ordinary operations, 21 feeling instead of mechanism | Use the plain word for the actual claim; name the operation or the thing; name what the reader can do or check |
| Noise: structure and filler | 12 not-X-but-Y, 13 forced triads, 14 synonym cycling, 15 span that is really a list, 16 filler, 17 stacked hedges, 18 adverbs doing the work of a verb, 19 nominalizations | State the thing directly; keep only true and specific items; pick one term and repeat it; prefer the verb; supply the number when the adverb carries the meaning |
| Tautology, fragments, order | 22 dense sentences, 24 buried decision, 25 heading restated in first sentence, 26 summary-recap ending, 27 dramatic fragments, 28 colon reveal | One idea per sentence; conclusion then reason then background; delete the restatement; rewrite fragment rows as sentences; reserve the colon for a list or a quote |
| Formatting noise | 29 rhythm-crutch dash, 30 bold label restating its line, 31 bold sprinkled for emphasis, 32 title-case headings, 33 decorative emoji, 34 bullets where prose reads better, 35 mixed straight and curly quotes | Use a period or a comma; convert restating labels to prose; use sentence case; remove decorative emoji; let format follow content |
| Chat and report artifacts | 36 chatbot openers and closers, 37 sycophancy, 38 announcing the next point, 39 process narration in a report, 40 knowledge-limit gap-filling, 41 manufactured thoroughness | Remove openers, closers, and narration; state what was decided and why; state what the source does not show or cut the sentence; never present a guess as a fact |
| Actor and reader | 23 passive hiding the actor, plus reader, decision-first, one-idea, and portability tests | Name the actor when the source says who; keep the passive only when naming adds nothing; gloss identifiers or name the consequence so a reader without the document or code can act; carry the outcome in the first sentence |
| Opaque schemes and labels | opaque labels (such as A0, DEL1, ENG-01, DES-02, T3, or invented letter-number codes) | Replace with a short semantic readable name describing the work; build a link map before mass renames; preserve externally fixed machine or standard identifiers, legal notices, and numbered procedure steps; if intent cannot be recovered, report without altering |

Promotional and model-vocabulary examples that the voice gate bans as prose are named here only in code spans and are stripped before that gate runs: `seamless`, `seamlessly`, `delve`, `delving`, `holistic`, `synergy`, `underscoring`, `leveraging`.

## Terminology

Keep exact identifiers, paths, commands, thresholds, and technical terms needed for precision. Explain an unfamiliar technical term when the reader needs it to understand or act.

By default, every human-facing filename, heading, section, phase, task label, and finding label must use a short semantic readable name describing the work. Replace opaque schemes such as A0, DEL1, ENG-01, DES-02, T3, or invented letter-number codes with the concise semantic name stating the action or consequence they mean.

Preserve externally fixed machine or standard identifiers (such as RFC numbers, CVE IDs, protocol constants, git commit hashes, and API symbols), legal notices, and numbered procedure steps (such as step 1, 2, 3 in an ordered sequence).

Require a link map before any mass rename. The link map must record every occurrence of the label or filename, all incoming Markdown links, outgoing targets, heading anchors, and relative paths across the documentation tree, ensuring all references update simultaneously.

Detect opaque labels by scanning human-facing filenames, headings, sections, phases, task labels, and finding labels for:
- Single letters followed by numbers (such as A0, T3).
- Capitalized acronym prefixes followed by numeric counters or hyphens (such as DEL1, ENG-01, DES-02).
- Synthetic alphanumeric codes or letter-number combinations that lack plain descriptive language.

On a hit:
1. Check whether the token is a preserved machine identifier, legal notice, or numbered procedure step. If preserved, leave it intact.
2. If the token is human-facing and opaque, inspect the surrounding section, task description, or repository context to identify the concrete work or purpose.
3. If semantic intent is clear, construct the link map and rename the label across all occurrences and references to the short semantic readable name.
4. If semantic intent cannot be recovered from the documentation tree or repository evidence, do not invent an arbitrary name. Leave the existing label unchanged, classify the candidate as an unrecovered finding with MEDIUM certainty, and record it in the purge report for human clarification.

Never touch code blocks, quoted text, frontmatter, link targets, identifiers, or a caller-required token unless the user names that content as the thing to fix.
