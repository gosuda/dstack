---
name: copywriting
description: 'Use when asked to write or fix product/marketing copy, landing pages, UI strings, brand voice, AI tells, an end-of-article CTA, or a hook/lede. Not for whole articles.'
---

# Copywriting

Write or fix product and marketing copy in one of three modes. Infer the mode from the ask and never ask which one. An explicit mode argument overrides the inference.

| Mode | Route here when the ask is | Writes |
|---|---|---|
| `page` | Anything not listed below: homepages, landing, pricing, feature and about pages, product descriptions, UI and product-state strings, brand voice, AI-tell removal | Copy and voice files in the working tree |
| `cta` | A call to action at the bottom of an article, essay, or newsletter issue | Nothing outside the conversation |
| `hook` | A hook, lede, or accroche for long-form content | Nothing outside the conversation |

Page mode is reversible local work. It creates or edits files in the working tree, version control is the rollback, and it never mutates anything remote. In cta and hook modes, recovery means re-running the interview or regenerating in the conversation.

## Page mode

### Choose the branch

If copy exists in scope, in files or pasted into the chat, take the fixing branch. If nothing is written yet, take the writing branch. If the request is ambiguous ("improve this" with no copy in scope), ask one question, then commit to a branch.

### Settle the brief

Both branches start from a four-field brief. Settle each field from the user or from files.

| Field | What it settles |
|---|---|
| Page purpose | The one action this page drives |
| Audience | The specific reader: job title, pain, and what they have already tried |
| Product | What it does and the concrete outcome for the user |
| Traffic source | Where the reader comes from. Cold traffic needs more Why; warm traffic can lead with How or What |

When a field is not settled, infer it and mark it as inferred. State the brief, then keep working, so the user corrects the inference against real copy instead of answering a question first. Never present an inference as a fact. Stop and ask before writing only when a wrong guess makes the work useless or unsafe: the copy ships this turn with no review, or the goal is unknown and each candidate goal produces different copy.

### Find the voice

Take the voice from the first source that exists, then stop looking:

1. A voice file in the repo (`VOICE.md`, `BRAND.md`, `docs/voice.md`). It is authoritative.
2. Existing copy: README headers, copy files, shipped marketing pages.
3. Inference from the product category. B2B SaaS reads direct and confident, consumer apps warmer, developer tools terse and honest.

A discovered voice outranks every word list in this skill. If the voice file or shipped copy uses a listed word as a signature, keep it. Locale and spelling convention come from the voice too; check them before changing spelling or tone, because a US-spelling rewrite on an en-AU product is a regression in every string it touches. When no voice file exists and the product will need one, offer to write `VOICE.md` alongside the copy (see "Voice chart for VOICE.md").

Voice is the constant brand personality. Tone adapts to the reader's state:

| Reader state | Tone | Example |
|---|---|---|
| Frustrated (error, failure, block) | Empathetic, solution-first, never blaming | "Payment failed. Your card was declined. Try a different card." |
| Confused (first use, complex feature) | Patient, one step at a time | "Connect your bank to see spending insights. We'll walk you through it." |
| Confident (routine task, return visit) | Efficient, minimal | "Saved" |
| Cautious (high stakes, data loss) | Serious, transparent, no nudging | "Delete account? You'll lose all data and this can't be undone." |
| Successful (completion) | Positive, proportional, brief | "Your changes are live." |

A tone shift is not voice drift. Drift is copy that reads as a different brand, not the same brand at a different moment.

### Route the copy

Product-state copy (error, empty, success, loading, and permission strings) and action labels follow `references/product-state-strings.md` and nothing else. Persuasion frameworks do not apply to a button that deletes something. Read that file whenever you write, audit, or flag such a string.

Marketing copy picks a lead framework from the brief and may layer others on top:

| Situation | Lead framework |
|---|---|
| Cold traffic, unfamiliar product | Why/How/What |
| Feature-heavy product | Benefit not feature |
| High-trust audience, low awareness | Show don't tell |
| Transactional page, known intent | CTA clarity |
| Long-form sales page | Problem, agitate, solution (PAS) |

Read `references/frameworks-and-pages.md` before writing or auditing marketing copy. It defines the nine frameworks and the norms for homepage, landing, pricing, feature, and about pages.

### Write new copy

1. Write labeled alternatives: Option A, B, and C for a page, hero, or campaign; Option A and B for a single string such as a CTA or subject line.
2. Make each option structurally different, not the same idea with new adjectives. Each one applies the chosen framework visibly. A page, hero, or campaign option includes a headline, a subhead, and at least one CTA; a single-string option is just the string.
3. Run the checks in "Checks before handing back". An option that fails is rewritten before it is shown, never presented with a caveat.
4. Recommend one option in one sentence that says which and why, and give one specific edit note for each option not picked.

### Fix existing copy

First set the edit posture. It limits everything that follows.

| Posture | When | What you may change |
|---|---|---|
| Point edit | The user named one line, word, or section | Only the target plus the minimum connective tissue. Run the steps below on the target alone; never widen a point edit into a page audit |
| Restoration | The copy has a clear voice, angle, or opinion | Fix named failures only. Preserve vocabulary level, emphasis, omissions, sentence shape, and positioning. Do not rebalance the argument or swap a clear lead for a cleverer one |
| Rebuild | The copy is generic, contradictory, or has no perspective | Reconstruct from the brief, but never invent proof |

Then work through these steps:

1. Read every copy-bearing file in scope: README headers, landing components, hero, CTAs, product descriptions, feature lists, onboarding strings, meta descriptions, email subjects, and the voice file if one exists. If it is unclear which files are in scope, ask. Never audit copy you have not read.
2. Write the value proposition in one sentence: "[User] can now [do X] without [old pain]." Every flag and rewrite serves it. If you cannot write it confidently, ask; the copy cannot be fixed until the value proposition is clear.
3. If the user asked for AI-tell removal, run the AI-pattern pass in `references/ai-patterns.md` before anything else.
4. Run the seven sweeps in `references/sweeps.md` in order, and check each major copy block against the nine frameworks. Collect every finding before fixing any.
5. Flag the weakest elements with the labels below.
6. Rewrite the flagged sections. Cut hard, to the same meaning in half the words. Lead with Why where the framework calls for it. Name the concrete outcome, not the capability. Replace adjectives with proof, or with `[PLACEHOLDER: add proof: stat / testimonial / example]` when the proof is unknown. Make CTAs outcome-specific and short. Every sentence adds new information or goes. When replacing an AI-ism, rewrite the sentence instead of swapping in a synonym.
7. Apply the hyphenation rule from `references/sweeps.md` silently. It needs no flag.
8. Output the before/after diff described under "What you get back", then run the checks.

### Flag labels

Use exactly these labels. Flag the 3 to 7 weakest elements, ordered by impact; more than that becomes a list nobody acts on. One occurrence gets one flag, so never stack `[TELL-NOT-SHOW]` and `[AI-ISM]` on the same word.

| Label | Meaning |
|---|---|
| `[WHAT-NOT-WHY]` | Leads with the product instead of the reader's motivation |
| `[FEATURE-NOT-BENEFIT]` | Names a capability without the user outcome |
| `[TELL-NOT-SHOW]` | Adjective claim without a fact, number, or scenario |
| `[VAGUE]` | Unspecific time, quantity, outcome, or a claim readable two ways |
| `[PASSIVE]` | Passive construction that hides who does what |
| `[VOICE-DRIFT]` | The line reads as a different brand |
| `[PAIN-NOT-NAMED]` | Sells the outcome before naming the pain the reader feels |
| `[DEAD-WEIGHT]` | The sentence adds nothing the reader needs |
| `[JARGON]` | Term the reader may not know, left undefined |
| `[NO-PROOF]` | Claim with no testimonial, case study, stat, or third-party validation |
| `[WEAK-CTA]` | CTA with no qualifier or trust signal, or a generic verb |
| `[STATE-COPY]` | Product-state string that breaks a rule in `references/product-state-strings.md`. Name the rule id |
| `[AI-ISM]` | AI writing pattern. Follow the label with its type, for example `[AI-ISM] chatbot artefact` |

When the user asked for AI-tell removal, every P0 and P1 hit from `references/ai-patterns.md` gets fixed. Those fixes do not count against the 3 to 7 budget, and repeated hits of one pattern may share one diff entry.

### Checks before handing back

Run these on every line you wrote or changed, in both branches:

- Options for cold traffic, or built on Why/How/What, lead with Why. Warm and transactional copy may lead with How or What.
- Each marketing line names a concrete outcome. Each product-state string passes its rule.
- No banned word (see "Banned words in your own copy") and no em dash. The en dash, `--`, and the spaced hyphen used as a dash count as em dashes. Zero is the limit, in headings and body alike.
- No prompt echo: the copy does not hand the brief's own phrasing back. Every specific the user supplied (number, name, example) appears instead of a stock default.
- Fixing branch only: every fact, number, and link in the "Before" survives in the "After", and no AI tell came back in. A rewrite that drops a specific or reintroduces a tell is a regression; restore it and rewrite again.
- Fixing branch only, the leave-it-alone test: every change fixes a named flag or the hyphenation rule. A change that is merely different gets reverted to the original.

The done predicate for page mode is that every line handed back is free of AI tells, matches the voice, and fits the page type. A line that fails is rewritten or withheld, never presented as done.

## Banned words in your own copy

These words never appear in copy you write, unless a voice file or shipped copy uses one as a signature: delve, leverage (verb), robust, seamless, holistic, paradigm, game-changing, cutting-edge, innovative, synergy, revolutionary, effortless, world-class, powerful, showcase, unlock. "Simple" is banned as a claim ("our simple onboarding"): it is never earned upfront and reads as a promise the product has to keep.

This list is the whole banned set; a draft containing one of these words is not an option to present. The tiers in `references/ai-patterns.md` are audit rules, not a second ban list: when your own draft trips one, treat it as the same P0, P1, or P2 hit it would be in someone else's copy. When auditing, a word from this list counts as Tier 1 and is always flagged.

## Voice chart for VOICE.md

Write `VOICE.md` only when you offered it and the user accepted. Build it from shipped copy, not from brand values.

1. Choose three to five concepts. Each concept has a brand principle (one word or a short phrase), two or three adjectives for how it shows up in writing, and a Do and Don't pair of real interface or page strings.
2. Make the Don't side the plausible near-miss the team actually ships, not a strawman. It is the useful half.
3. Name what the voice is not ("Confident, not boastful").
4. Record the locale and spelling convention, house spellings, and any word the brand uses deliberately that a generic list would flag.

## Cta mode

Read `references/cta-playbook.md` before starting. It holds the interview options, the archetype decision tree, the recommendation template, the operating principles, and the named failure modes.

1. Interview for five inputs in order, one at a time, skipping any the user already gave: article context, primary objective, audience and relationship, funnel stage, and mechanism preference. Offer 2 to 4 tappable options per question through the question tool, and fall back to free text only when the answer cannot be enumerated. If the user names more than one objective, ask which is primary; competing objectives are the most common cause of CTA failure. Ask about mechanism only when one could legitimately help; for skeptical or repeat-reader audiences, default to none or value-only without asking. Capture any constraint the user volunteers: length, brand voice, no popups, language, formality.
2. Map the inputs to one archetype with the decision tree.
3. Compose the recommendation in the playbook's exact structure, and enforce the operating principles while composing.
4. List 2 to 3 failure modes the user is at risk of, given their inputs, as a contrarian check.
5. Adapt the copy to the stated brand voice, the article's language (never default to English), the publication's cadence, and the reader's expertise. Honor formality cues (tu or vous, du or Sie) and say which you chose. For a non-English article, write the copy in that language and keep the template headings in English.
6. Close with 2 to 3 follow-ups: steelman the opposite CTA, a variant for another audience or platform, or a review of the whole article for signals that support the CTA.

## Hook mode

A hook has one job: make the reader want sentence 2. Read `references/hook-catalog.md` before generating. It holds the five levers, the type-fit table, the 18 hooks, the anti-pattern cull, language handling, and the output format.

1. Confirm the brief: topic, audience, target language (EN, FR, or both), approximate length, and publication venue. If a field that changes the hooks is missing, ask before generating. If the user supplied a draft opening, carry it as Option 0; never silently discard it.
2. Pick 3 to 4 hooks that pull different levers, not three flavors of one technique. Across the set, include at least one intellectual hook (contrarian, definition reversal, historical analogy, curiosity gap), one sensory hook (in medias res, concrete detail), and one reader-direct hook (conditional, direct problem, promise). Check each pick against the type-fit table.
3. Write two candidates per hook, specific to this article. The two explore different angles (a different anecdote, statistic, or scene), not rewordings of one line.
4. Apply the quality gates to every candidate. Specific beats abstract: name "Stripe, Shopify, Vercel" instead of "many companies", give a date instead of "recently", and state the actual finding instead of "studies show", or cut the claim. The first sentence must force the second; read each candidate cold, and if you would not read on after sentence 1, rewrite it. Replace any number or quote you cannot cite accurately with a verifiable detail, or cut it.
5. Run every candidate through the anti-pattern cull and rewrite any match before presenting.
6. Present in the catalog's output format, ask the user to pick through the question tool, and wait. Do not pick for them.
7. If the user says "more" or "none", write 3 new hooks with different techniques, not new candidates for the same hooks. If the user says "blend 1A and 2B", write one combined hook and check in again before going further.
8. After the pick, say in one sentence what the hook commits the rest of the article to. A contrarian hook commits paragraphs 2 and 3 to defending the non-consensus claim; a scene opener commits the next section to resolving or deliberately delaying the scene.

## When to stop instead

Never fabricate a number, testimonial, statistic, or quote in any mode. Use `[PLACEHOLDER: add proof: ...]` and let the user supply it. Never present partial results as done.

| Mode | Condition | What to do |
|---|---|---|
| page | A brief field cannot be settled and a wrong guess makes the work useless or unsafe | Ask. Otherwise infer it, name the inference, and keep going |
| page | The value proposition cannot be written in one sentence | Report the blocked state with the unresolved value proposition instead of shipping copy that serves none |
| cta | Article context, objective, audience, or funnel stage cannot be obtained | Stop and name the missing input. A CTA built on assumed inputs ends up as "Subscribe for more" |
| cta | The user insists on more than one primary objective after pushback | Flag it as a failure mode, deliver the strongest single-primary recommendation, and list the competing objectives as anti-patterns |
| cta | The inputs map to no archetype, such as a product demo on a personal blog where the author is not the product | Report the conflict and propose the closest valid archetype. Never invent one |
| cta | Any part of the recommendation template cannot be filled | Return the blocked result naming what is missing, not a partial template |
| hook | A material brief field is unclear | Ask before generating. Never invent a brief |
| hook | The options collapse into flavors of one technique | Regenerate across different levers before presenting |
| hook | Three distinct hooks cannot be produced | Stop and name the blocker. Never present fewer than 3 options |

## What you get back

| Mode | Output |
|---|---|
| page, writing | The brief with inferred fields marked, 2 to 3 labeled options, the recommendation, edit notes for the options not picked, and the check result |
| page, fixing | For each flagged section: the original, its labels, the rewrite, and one sentence on why it changed. Then a summary with the issue count, the top pattern, and your confidence, noting when copy context was limited |
| page, voice | `VOICE.md`, only when offered and accepted |
| cta | One recommendation in the playbook structure, 2 to 3 anti-pattern warnings, and 2 to 3 suggested next moves |
| hook | The working title, 3 to 4 numbered hooks with A and B candidates each (plus Option 0 if a draft was given), and the selection prompt. After the pick: the chosen hook and one sentence on what it commits the opening to |
