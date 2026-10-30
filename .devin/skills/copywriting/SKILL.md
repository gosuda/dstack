---
name: copywriting
description: 'Use when asked to write or fix product/marketing copy, landing pages, UI strings, brand voice, AI tells, an end-of-article CTA, or a hook/lede. Not for whole articles.'
---

# Copywriting

Write or fix product and marketing copy in one of three modes. The skill infers the mode from the ask and never asks which one: a bottom-of-article call-to-action routes to `cta`; a hook, lede, or accroche for long-form content routes to `hook`; everything else routes to `page`. An explicit mode argument overrides auto-detection. Page mode is reversible local work: it creates or edits copy and brand voice files in the working tree with version control as the rollback, and never mutates anything remote. Cta and hook modes write nothing outside the conversation.

## Inputs to settle first

- Mode page: the copy to fix, or a page type and goal. Copy that exists (or was pasted) takes the editing branch; nothing written yet takes the writing branch. For a genuinely ambiguous request ("improve this" with no copy in scope), ask one question, then commit.
- Mode cta: article context, primary objective, audience and relationship, funnel stage, and mechanism preference, collected in the interview below.
- Mode hook: topic, audience, target language (EN, FR, or both), approximate length, and publication venue; plus an optional existing draft opening, treated as Option 0 and never silently discarded.
- Optional inputs, settled before writing: page purpose, audience, product, traffic source, and any voice file (`VOICE.md`, `BRAND.md`, `docs/voice.md`). When an input is missing, infer it and name the inference so the user can correct it against real copy.

## Writing new copy

Gather context before writing. Settle four fields from the user or from files, and infer and name any field the files do not settle: (1) page purpose, the one action this page drives; (2) audience, the specific reader, their job title, pain, and what they have already tried; (3) product, what it does and the concrete user outcome; (4) traffic source, where the reader comes from. Traffic source sets temperature: cold needs more Why, warm can lead with How or What.

State the brief, then keep going. Mark every inferred field so the user corrects it against copy, not against a question. Stop and ask before writing only when a wrong guess makes the work useless or unsafe: the copy ships in this turn with no review, or the goal is genuinely unknown and each candidate goal produces different copy.

Discover brand voice from the first matching source, then stop: (1) a voice file in the repo (`VOICE.md`, `BRAND.md`, `docs/voice.md`), which is authoritative when it exists; (2) existing copy such as README headers, copy files, or shipped marketing pages; (3) inference (B2B SaaS direct and confident, consumer apps warmer, developer tools terse and honest). A discovered voice outranks the word lists: if the voice file or shipped copy uses a listed word as a signature, keep it. Locale and spelling convention come from the voice. When no voice file exists and the product will need one, offer to write `VOICE.md` alongside the copy using the voice chart structure below. Voice is constant (the brand personality) while tone adapts to the reader's state:

| Reader state | Tone | Example |
|---|---|---|
| Frustrated (error, failure, block) | Empathetic, solution-first, never blaming | "Payment failed. Your card was declined. Try a different card." |
| Confused (first use, complex feature) | Patient, one step at a time | "Connect your bank to see spending insights. We'll walk you through it." |
| Confident (routine task, return visit) | Efficient, minimal | "Saved" |
| Cautious (high stakes, data loss) | Serious, transparent, no nudging | "Delete account? You'll lose all data and this can't be undone." |
| Successful (completion) | Positive, proportional, brief | "Your changes are live." |

A tone shift is not voice drift. Drift is when the copy reads as a different brand, not the same brand in a different moment.

Choose a framework and load page norms. Route on what the copy is. Product-state copy (an error, empty, success, loading, or permission string) or an action label takes the UI state copy rules below and stops there; persuasion frameworks do not apply to a button that deletes something. Marketing copy picks its lead framework from the brief and layers freely:

| Situation | Lead framework |
|---|---|
| Cold traffic, unfamiliar product | Why/How/What (Simon Sinek) |
| Feature-heavy product | Benefit Not Feature |
| High-trust audience, low awareness | Show Don't Tell |
| Transactional page, known intent | CTA Clarity |
| Long-form sales page | Problem → Agitate → Solution (PAS) |

The nine frameworks: **Why/How/What** (lead with Why, not What; order Why, How, What), **PAS** (name the pain, amplify the cost, present the solution), **AIDA** (Attention, Interest, Desire, Action for cold traffic), **StoryBrand** (customer is hero, product is guide; never make the product the hero), **BAB** (Before, After, Bridge; warmer and aspirational where PAS is confrontational), **Show Don't Tell** (replace adjectives with a specific fact, number, or scenario), **Benefit Not Feature** (lead with the outcome for the user; mention the mechanism only after the benefit is clear), **Sentence Economy** (every sentence earns its space; cut openers like "In order to" or "It is important to note that"), **CTA Clarity** (action verb plus what they get plus qualifier; never two CTAs with the same verb on one screen). For a known page type, apply its norms:

- Homepage: establish what the product is and who it is for; pick the highest-value segment and write for them. Sections in order: hero (lead with Why), social proof above fold, problem/pain, solution/benefits (one benefit per point), how it works, testimonials, final CTA. Do not add a secondary CTA that dilutes the primary action.
- Landing page: drive one action; message must match what brought the reader. Headline mirrors the ad or email promise. PAS for problem-aware traffic, AIDA for cold. One CTA only; strip navigation and footer links.
- Pricing page: help visitors choose. Name plans by buyer type, not tier ("Solo / Team / Company" beats "Basic / Pro / Enterprise"). Sections: value restatement, plan comparison (2 to 4 plans), feature differentiators, FAQ, social proof by tier, risk reversal near the CTA.
- Feature page: connect a feature to an outcome for visitors already evaluating. Feature, Benefit, Outcome chain. Skip broad setup; go straight to the specific outcome with a number or example.
- About page: build trust; every element passes the "so what does this mean for me?" test. Mission as a customer benefit, origin story tied to the customer's frustration, human team, 3 to 5 customer-relevant values, a CTA pointing to the product.

Write 2 to 3 alternatives labeled Option A, B, C. Three for a page, hero, or campaign; two for a single string like a CTA or subject line. Each applies the chosen framework visibly, leads with Why, uses no banned word, includes a headline, subhead, and at least one CTA, and is structurally different, not the same idea with new adjectives. Then recommend: pick one, state which and why in one sentence, and give one specific edit note per unpicked option.

Verify every line before handing back. Each line of every option: leads with Why, names a concrete outcome, no banned word, no em dash or stand-in. Each option whole: it does not hand the brief's wording back (prompt echo), and every specific the user supplied appears rather than a stock default. New copy containing a banned word is not an option to present; rewrite it first.

## Fixing existing copy

Set the edit posture first. **Point edit:** the user named one line, word, or section; change only the target plus minimum connective tissue; never turn a point edit into a page audit. **Restoration:** the copy has a clear voice, angle, or opinion; preserve its vocabulary level, emphasis, omissions, sentence shape, and positioning; fix specific failures without rebalancing the argument. **Rebuild:** the copy is generic, contradictory, or has no perspective; reconstruct from the brief, but never invent proof.

Read all copy-bearing files. Scan every reader-facing surface: README headers, landing components, hero, CTAs, product descriptions, feature lists, onboarding strings, meta descriptions, email subjects. Read the voice file too if one exists; it settles register and locale and overrides the word lists for any word it names as a signature. Ask which files if unclear; never audit copy not read in context.

Set the value proposition in one sentence before auditing: "[User] can now [do X] without [old pain]." Every flag and rewrite serves it. If the sentence cannot be written confidently, ask; the copy is unfixable until the value proposition is clear.

Audit against the persuasion frameworks. Check every major copy block against the nine frameworks and carry forward only the highest-impact problems; the flag budget is set below.

Remove AI writing patterns (run this first, before the sweeps, when the user asked for AI pattern removal). Flag each AI-ism with `[AI-ISM]` plus its type. **Tier 1 words** (always replace): delve, landscape (metaphor), tapestry, realm, paradigm, embark, beacon, testament to, robust, comprehensive, cutting-edge, leverage (verb), pivotal, underscores, meticulous, seamless, game-changer, utilise, nestled, vibrant, deep dive, unpack, showcase, unlock, intricate, holistic, actionable, impactful, learnings, thought leadership, best practices, synergy, in order to, due to the fact that, serve as, commence, keen (as intensifier). **Tier 2 clusters** (flag when 2 or more appear in one paragraph): harness, navigate, foster, elevate, unleash, streamline, empower, bolster, spearhead, resonate, revolutionise, facilitate, underpin, nuanced, crucial, ecosystem (metaphor), myriad, plethora, catalyse, transformative, cornerstone, paramount, burgeoning, nascent, overarching. **Tier 3** (flag only at high density, around 3 percent or more): significant, innovative, effective, dynamic, compelling, unprecedented, exceptional, remarkable, sophisticated, world-class, state-of-the-art. **Structural patterns:** formulaic openings ("In the rapidly evolving world of..."), rhetorical-question openers, engagement hooks ("Here's the thing", "Plot twist:"), copula avoidance ("serves as", "features", "boasts"), synonym cycling, vague attributions ("Experts believe"), significance inflation, false ranges, em dashes and `--`/spaced-hyphen stand-ins (zero, in headings and body alike; a single occurrence is a failure). **Chatbot artefacts** (remove entirely): "I hope this helps", "Great question", "Let's dive in", any "let's plus verb" transition, chain-of-thought leaking ("Let me think step by step", "Step 1:"), acknowledgement loops. **Drafting tells** (these survive a word-level pass, so check separately): prompt echo (the draft reuses the brief's own phrasing), generic default over the supplied specific (a real number or name replaced by a category placeholder), uniform confidence (every line lands at the same pitch). **Severity triage:** P0 (credibility killers: cutoff disclaimers, chatbot artefacts, vague attributions, significance inflation, a supplied specific replaced by a generic default) fix immediately; P1 (prompt echo, Tier 1 words, template phrases, "let's" openers, formulaic openings, engagement hooks, bold overuse, any em dash) fix before publishing; P2 (generic conclusions, compulsive rule of three, uniform paragraph length, announced honesty, copula avoidance, overused transitions, Tier 2 clusters) fix when time allows. A clean P0 plus P1 pass is publishable.

Run seven sweeps in order, each targeting a distinct failure mode, flagging everything before fixing. (1) **Clarity:** confusing structure, unclear pronouns, undefined jargon, claims readable two ways. Flags `[JARGON]`, `[VAGUE]`. (2) **Voice and tone:** formal/casual shifts, register mismatch; identify the dominant voice and standardise to it. Flag `[VOICE-DRIFT]` on the line that reads as a different brand, not where the same brand meets a different moment. (3) **So what:** every claim answers "why should the reader care?". Flags `[DEAD-WEIGHT]`, `[FEATURE-NOT-BENEFIT]`. (4) **Prove it:** back every claim with a named testimonial, case study, stat, or third-party validation. Flag `[NO-PROOF]`; use `[PLACEHOLDER: add proof: stat / testimonial / example]` when the proof is unknown. (5) **Specificity:** replace vague time, quantity, and outcome with concrete detail. Flag `[VAGUE]`. (6) **Emotion:** name the pain the reader already feels before selling the outcome; mirror the reader's actual state at this point in the page. Flag `[PAIN-NOT-NAMED]`. (7) **Zero risk:** remove friction at and near CTAs; address objections, add trust signals, clarify the next step, add risk reversal. Flag `[WEAK-CTA]` on any CTA standing alone without a qualifier or trust signal. Finish with the compound adjective hyphenation pass: hyphenate a multi-word modifier before the noun it describes ("a 7-day free trial", "real-time updates", "`{{days}}-day free trial`"); leave it open when it stands alone as a noun phrase ("The trial lasts 7 days"); never hyphenate an `-ly` adverb ("a fully managed service"). Fix hyphenation silently rather than flagging it.

Flag the weakest elements with inline labels, using exactly these labels: `[WHAT-NOT-WHY]` (leads with product, not motivation), `[FEATURE-NOT-BENEFIT]`, `[TELL-NOT-SHOW]` (adjective claim without proof), `[VAGUE]`, `[PASSIVE]`, `[VOICE-DRIFT]`, `[PAIN-NOT-NAMED]`, `[DEAD-WEIGHT]`, `[JARGON]`, `[NO-PROOF]`, `[WEAK-CTA]`, `[STATE-COPY]` (vague, leaky, or dead-end state string, or a destructive CTA labeled Confirm/OK/bare verb; apply the UI state copy rules below before using this label), `[AI-ISM]`. Flag the 3 to 7 weakest elements, prioritised by impact; over-flagging dilutes into a list nobody acts on. One occurrence is one flag; do not stack `[TELL-NOT-SHOW]` and `[AI-ISM]` on the same word.

Rewrite the flagged sections. Cut hard (same meaning in half the words). Lead with Why, not What. Name the concrete outcome, not the capability. Replace adjectives with proof. Make CTAs outcome-specific. Every sentence adds new information or gets cut. A CTA stays short. When replacing AI-isms, rewrite the sentence; do not swap the flagged word for a synonym.

Output a before/after diff. For each flagged section, show the original, the labels, the rewritten text, and one sentence explaining the change. End with a summary: issue count, top pattern, and confidence (note if copy context was limited). Verify each "After" line: leads with Why, names a concrete outcome, no banned word, no em dash or stand-in, and every fact, number, and link from the "Before" still present. Then apply the leave-it-alone test: every change must fix a named failure from the audit; if it is merely different, restore the original.

## End-of-article call-to-action

The archetype decision tree, the exact recommendation structure, and the operating principles live in `references/cta-playbook.md`.

Interview first. Ask the five inputs in order, one at a time with 2 to 4 tappable options, skipping any already supplied; fall back to free text only when the answer cannot be enumerated. (1) Article context: personal or independent blog or essay, newsletter or paid publication, brand or company content-marketing blog, other. (2) Primary objective: newsletter or email subscription, social follow, lead generation (gated asset), product or service signup or free trial, demo or sales call booking, direct purchase, community join, engagement (reply, comment, share), reader support (paid sub or tip), try-it or direct action, other; if the user lists more than one, ask which is primary, because choosing multiple objectives is the dominant cause of CTA failure. (3) Audience and relationship: first-time visitor, returning reader not subscribed, existing subscriber or customer, mixed or unknown. (4) Funnel stage: TOFU (discovery, no buying intent), MOFU (evaluating, comparing), BOFU (ready to act), not applicable. (5) Mechanism preference, asked only if a mechanism could legitimately help (for skeptical or repeat-reader audiences default to none or value-only without asking): none or value-only, curiosity gap, reciprocity (free asset first), discount or offer, urgency (real deadline), scarcity or FOMO, social proof. Capture volunteered constraints (length limit, brand voice, no popups, language, formality).

Diagnose by mapping the inputs to one archetype via the decision tree in `references/cta-playbook.md`. Then compose the recommendation in the exact structure given there: archetype with rationale, content copy (headline, body, button, risk reversal), form (placement, visual weight, layout, proof), mechanism, A/B test plan, and a WCAG 2.2 accessibility check. After the recommendation, list 2 to 3 anti-patterns the user is at risk of given their inputs, as a contrarian check. Failure modes to call out by name: multiple competing CTAs, generic "Subscribe for more" or "Learn More", mechanism mismatch (urgency or scarcity where none exists), SaaS landing-page voice on a personal essay, proofless ask, "Book a Demo" on TOFU content, open-ended reply questions on social. Enforce the operating principles during composition: one primary CTA per post, publication voice, specificity over cleverness, proof co-located with the ask, mechanisms only when the context supports them, and pushback on bad asks.

Adapt copy to the user's stated brand voice, the article's language (never default to English), the publication's existing cadence, and the reader's expertise level. Honor formality cues (tu/vous, du/Sie) and flag the choice. If non-English, translate the content section but keep structure headings in English. Close by suggesting 2 to 3 follow-ups: steelman the opposite CTA, a variant for a different audience or platform, or an end-to-end article review for CTA-supporting signals.

## Hooks and ledes

A hook's only job is to make the reader want sentence 2, through one of five levers (a strong hook usually pulls two at once): open a gap, break a prediction, drop into a scene, promise a payoff, borrow weight. The five levers in detail, the type-fit table, the 18-hook catalog, the anti-pattern cull, and language handling live in `references/hook-catalog.md`.

Confirm the brief before generating; ask if a material input field is missing. Pick 3 to 4 hooks from the catalog that are genuinely different, meaning different levers, not three flavors of the same technique. Diversification rule: across the options include at minimum one intellectual hook (contrarian, definition reversal, historical analogy, curiosity gap), one sensory hook (in medias res, concrete detail), and one reader-direct hook (conditional, direct problem, promise). Write 2 candidates per hook, specific to the user's article. The two candidates within one hook explore different angles (different anecdote, statistic, or scene), not rewordings of each other. Apply the quality gates to every candidate: specific beats abstract (replace "many companies" with "Stripe, Shopify, Vercel"; replace "recently" with a date; replace "studies show" with the actual finding or cut the claim); the first sentence must force the second (read each candidate cold; if sentence 2 would not be clicked after sentence 1, rewrite); match technique to article type using the type-fit table. Run the anti-pattern cull on every candidate and rewrite matches before presenting.

Present using the output format, ask the user through the question tool, and wait. Do not pick for them. If the user says "more" or "none", produce 3 different hooks (different techniques), not new candidates for the same hooks. If the user says "blend 1A and 2B", write one combined hook and check in again before proceeding. After the pick, name in one sentence what the choice commits the rest of the article to. A contrarian hook commits paragraphs 2 and 3 to defending the non-consensus claim. A scene opener commits the next section to resolving or productively delaying the scene.

## Product-state strings

For error, empty, success, loading, and permission strings, and for the `[STATE-COPY]` label, these rules apply:

- Destructive CTAs (`rule/destructive-names-action`, `rule/no-confirm-ok-labels`): Verb plus Noun naming the exact object ("Delete project", not "Confirm" or "OK"). Never label a consequential action Confirm, OK, Yes, or a bare verb.
- Canonical verbs (`rule/canonical-verb`): one verb per operation, used consistently; pick the verb whose consequence matches (Delete is permanent, Remove detaches without destroying, Archive reversibly hides, Discard drops unsaved edits, Cancel abandons an in-progress action).
- Error (`rule/error-states-recovery`): state what happened, why when known, and the recovery action; never raw exceptions or a bare "Something went wrong". Separate field-level from surface-level errors; preserve everything the user typed.
- Success (`rule/success-state-specific`): confirm in past tense what happened to which object, proportional to the action.
- Empty (`rule/empty-state-action`): name the object and offer the first action; no dead ends. Three types: never-had-any (guide the first step), filtered-to-zero (clear the filter), user-cleared (confirm completion; the one empty state that needs no CTA).
- Loading (`rule/loading-state-specific`): say what loads and, for long operations, roughly how long; keep the triggering control's label stable.
- Permission (`rule/permission-benefit-first`): state the user benefit before the permission ask; ask in context when the feature is first used.
- Copy without the screen (`rule/reads-without-seeing`): copy must work when heard; field errors read sensibly after their label; link and button text names the destination or action; no directional words ("above", "below", "here").
- Length budgets (size for the tightest surface first; leave 30 to 40 percent headroom for translation): button or CTA 2 to 4 words; title 3 to 6 words; error message 12 to 18 words including the recovery step; any sentence the user must act on 14 words (8 reads at full comprehension).

## Words I never write

The never-write set, absolute unless a voice file names one as a signature: delve, leverage (verb), robust, seamless, holistic, paradigm, game-changing, cutting-edge, innovative, synergy, revolutionary, effortless, world-class, powerful, showcase, unlock. Also ban **"simple"** as a claim ("our simple onboarding"): never earned upfront, reads as an unkept promise.

## Voice chart, when offering to write VOICE.md

Three to five concepts. Each concept has three parts: (1) a brand principle, one word or short phrase; (2) two or three adjectives naming how it shows up in writing; (3) a Do and Don't pair of real interface or page strings. The Don't side is the useful half: make it the plausible near-miss the team actually ships, not a strawman. Start from shipped copy, not brand values. Record locale and spelling convention, house spellings, and any word the brand uses deliberately that a generic list would flag. Name what the voice is not ("Confident, not boastful").

## When I stop instead

- Invented audience or goal. Copy written without a goal and value proposition reads well and solves the wrong problem. If a context field cannot be settled from files or the user, infer it and name the inference; never present an inference as a fact. Stop and ask only when a wrong guess makes the work useless or unsafe.
- Invented proof. Never fabricate a number, testimonial, or statistic. Use `[PLACEHOLDER: add proof: ...]` and let the user supply it.
- Locale or voice regression. A US-spelling rewrite on an en-AU product ships as a regression across every string it touches. Check existing copy and the voice file before switching spelling or tone; a discovered voice outranks the word lists.
- Point-edit scope creep. Do not turn a named point edit into a page audit; change only the target plus minimum connective tissue.
- Restoration over-reach. Do not rebalance the argument or replace a clear lead with a cleverer one; fix named failures only.
- AI-ism reintroduced or specific dropped. A rewrite that reintroduces an AI tell, or quietly drops a fact, number, or link from the original, is a regression; restore and rewrite again.
- Non-convergent result. If the value proposition cannot be stated in one sentence, the copy is unfixable until it is clarified; report this blocked state with the unresolved value proposition rather than shipping copy that does not serve one.
- Missing cta inputs. If any of the five required inputs cannot be obtained, stop and report which input is missing rather than guessing; a CTA designed on assumed inputs produces the universal failure mode (generic "Subscribe for more").
- Multiple primary objectives (cta). If the user insists on more than one primary objective after pushback, flag it as a failure mode, deliver the strongest single-primary recommendation, and note the competing objectives as anti-patterns.
- No valid archetype (cta). If the input combination maps to no archetype (for example, product or demo on a personal blog where the author is not the product), report the conflict and propose the closest valid alternative. Do not fabricate an archetype.
- Missing hook brief. If topic, audience, language, length, or publication venue is unclear and material, stop and ask before generating. Do not invent a brief.
- Anti-pattern match (hook). If a candidate matches the cull list, rewrite it before presenting. Never present a matched candidate.
- No genuine choice (hook). If the 3 to 4 options collapse to flavors of one technique, regenerate across different levers per the diversification rule before presenting.
- Unverifiable statistic or quote (hook). If a candidate leans on a number or quote that cannot be cited accurately, replace it with a verifiable detail or cut the claim. Do not present an unsupported authority hook.
- Partial results are never presented as done. The done predicate (free of AI-isms, matches the voice, fits the page type) must hold for every line handed back; lines that fail it are rewritten or withheld. Cta mode returns either the full structure or the blocked result naming the missing input; hook mode never presents fewer than 3 distinct options, and stops with the blocker named if 3 cannot be produced.
- Cta and hook modes write nothing outside the conversation; recovery is re-running the interview or regenerating in conversation.

## What you get back

Page mode, writing branch: the brief with marked inferences, 2 to 3 labeled alternatives, the recommendation, edit notes, and the pass result. Page mode, editing branch: before/after diffs with labels, rationale, issue count, top pattern, and confidence. Then `VOICE.md` only when offered and accepted. Cta mode: a single in-conversation recommendation with archetype selection and rationale, copy (headline, body, button, risk reversal), form (placement, visual weight, layout, proof), mechanism, A/B test plan, WCAG 2.2 accessibility check, 2 to 3 anti-pattern warnings, and 2 to 3 suggested next moves. Hook mode: working title, 3 to 4 numbered hook types with two A/B candidates each, the user's selection prompt, and after selection the chosen hook plus one sentence naming what it commits the opening to.
