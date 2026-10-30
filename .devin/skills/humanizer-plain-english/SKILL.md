---
name: humanizer-plain-english
description: 'Use when asked to make English plain, clear, natural, and readable while keeping its meaning and voice. Not for ASD-STE100 controlled-language compliance: use humanizer-simple-english-asd-ste100. Not for stripping AI tells from otherwise fine prose: use unslop.'
---

# Plain English humanizer
Good prose reads like good design: nothing showy, nothing missing, plain words carrying their full weight, never flattened into sameness. This skill takes tangled or stuffy English and returns the same meaning in language a busy reader can find, follow, and act on.

## When this fits

Reach for this skill when the user asks to make English plainer, clearer, more natural, more readable, or more human for docs, messages, explanations, guides, or any passage where understanding matters more than certification. The goal is comprehension, not compliance: the reader should know what is true, what to do, and what happens next.

## What you give me

The source text, inline or as a file path, is required. One bounded piece per run: a passage, a page, a short document. Say who it is for and what they need to do with it when that is not obvious from the text itself.

When there is no source text, or the file is empty or unreadable, stop and say there is no material to work with. Never invent facts to fill the gap.

## How the rewrite works

Read the whole passage first so the rewrite keeps everything the source promised: its facts, numbers, names, and references; its qualifications and hedges; its obligations and permissions; its technical meaning; and the author's own voice. A plainer sentence that says something stronger, weaker, or different from the original is a failure, not a simplification.

Then rewrite for the reader in front of you:

- Keep every word the reader needs. Plain English here is not a restricted word list, a CEFR grade quota, or ASD-STE100 certification. Technical terms, precise nouns, and necessary vocabulary stay; an unfamiliar term gets a short definition where it first appears rather than being swapped for a vaguer word.
- Prefer short, clear clauses over long fused sentences. Break a sentence the reader must backtrack through into two. One idea carries each sentence; one topic carries each paragraph.
- Use the active voice wherever the actor matters, and name the actor. Keep the passive only when the actor is genuinely unknown or beside the point.
- Choose concrete verbs over abstract ones: use instead of utilize, help instead of facilitate, cut filler such as in order to, due to the fact that, it is important to note that.
- Give the reader somewhere to stand: useful headings, a list for three or more steps or options, the action stated before its background. Cut filler, stacked qualifiers, and jargon that a plainer concrete word already says. Never force symmetry: no matching paragraph templates, no triplets for their own sake, no identical sentence openings unless they carry a real comparison.
- Make the text findable and actionable: keep identifiers, codes, paths, numbers with units, and references exact; keep modal verbs (must, should, may) attached to the clause they govern; end procedural passages with the reader knowing what to do next.

## What you get back

The rewritten text, returned to chat, with the original's meaning intact and any ambiguity the source left unresolved called out beside it rather than papered over. When the input is already plain, say so and return it unchanged. This skill reads and returns; it writes no files, publishes nothing, and changes nothing outside the conversation. Saving the result somewhere is a separate request the user makes explicitly.

## When the stricter sibling fits better

Some documents do not want natural prose. They want controlled language. Safety instructions, maintenance procedures, and normative requirements live under ASD-STE100: a fixed word list with one meaning per word, sentence-length caps, one instruction per sentence, and verifiable compliance. When the user asks for STE compliance, controlled technical English, disambiguation under STE rules, or a certifiable manual, that work belongs in humanizer-simple-english-asd-ste100, judged by its own rules. The two skills share a read-only habit but neither runs the other; route by naming the right one, not by invoking it.

Unslop is the other neighbor: it strips AI tells and chatbot mannerisms from prose that is otherwise sound. Use this skill when the problem is comprehension itself (structure, sentence weight, abstraction), not just surface polish.

## What this never does

Never add a fact the source did not state, promote a hedge into a certainty, soften a requirement into a suggestion, or trade the author's voice for house style. Never claim a restricted-vocabulary standard, a reading-level score, or any certification this rewrite does not carry. When a sentence cannot be made plainer without guessing, keep the original phrasing and flag what is missing.
