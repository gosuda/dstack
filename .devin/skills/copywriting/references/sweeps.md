# The seven sweeps

Read this in page mode, fixing branch, after the value proposition is set (and after the AI-pattern pass, when one was requested). Run the sweeps in order. Each targets a distinct failure, and every finding is collected before anything is fixed. On a point edit, sweep the target only.

| Order | Sweep | What to check | Flags |
|---|---|---|---|
| 1 | Clarity | Confusing structure, unclear pronouns, undefined jargon, claims readable two ways | `[JARGON]`, `[VAGUE]` |
| 2 | Voice and tone | Formal and casual shifts, register mismatch. Find the dominant voice and standardise to it; under the restoration posture, that voice is the one to preserve | `[VOICE-DRIFT]` on the line that reads as a different brand, not where the same brand meets a different moment |
| 3 | So what | Every claim answers "why should the reader care?" | `[DEAD-WEIGHT]`, `[FEATURE-NOT-BENEFIT]` |
| 4 | Prove it | Every claim is backed by a named testimonial, case study, stat, or third-party validation | `[NO-PROOF]`. Use `[PLACEHOLDER: add proof: stat / testimonial / example]` when the proof is unknown |
| 5 | Specificity | Vague time, quantity, and outcome replaced with concrete detail | `[VAGUE]` |
| 6 | Emotion | The pain the reader already feels is named before the outcome is sold, and the copy mirrors the reader's state at this point on the page | `[PAIN-NOT-NAMED]` |
| 7 | Zero risk | Friction at and near CTAs: unanswered objections, missing trust signals, unclear next step, no risk reversal | `[WEAK-CTA]` on any CTA standing alone without a qualifier or trust signal |

## Framework check

Alongside the sweeps, check each major copy block against the nine frameworks in `frameworks-and-pages.md`. This is where `[WHAT-NOT-WHY]`, `[TELL-NOT-SHOW]`, and `[PASSIVE]` usually come from. Carry forward only the highest-impact findings into the 3 to 7 flags.

## Hyphenation

After the rewrites, fix compound modifiers without flagging them:

- Hyphenate a multi-word modifier before the noun it describes: "a 7-day free trial", "real-time updates", "`{{days}}-day free trial`".
- Leave it open when it stands alone as a noun phrase: "The trial lasts 7 days."
- Never hyphenate an adverb ending in "-ly": "a fully managed service".
