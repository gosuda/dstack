---
name: let-fate-decide
description: 'Use when the user says let fate decide, YOLO, dealer choice, surprise me, whatever, or delegates a vague choice in a casual or playful tone, or when you are about to pick arbitrarily between valid options. Not when instructions are precise, one approach is clearly correct, or the call governs safety, security sign-off, production release, or incident response.'
allowed-tools: Bash Read
---

# Let fate decide

When several valid options tie and the user invites fate to break it (let fate decide, feeling lucky, dealer choice, surprise me, YOLO, heart of the cards, whatever, your call, up to you, idk, wing it, or a shrug that fully delegates), you draw a 12-house Tarot spread with real entropy and let the reading suggest which option to explore first. No approval is needed to draw and interpret. Cards suggest where to look next. Evidence decides what is true. The reading never authorizes anything on its own: the interpretation is always delivered alongside the tool call that acts on the chosen option, never as a text-only turn. A redraw request when nothing in the system changed draws one new spread once; it never re-runs the same approach to chase a preferred card.

For the meaning of each house and card, see [the interpretation guide](references/INTERPRETATION_GUIDE.md), with the matching lens from [technical context lenses](references/TECHNICAL_CONTEXT_LENSES.md) for specialized work. Major Arcana sets each house theme and carries more weight; Minor Arcana supplies detail (Wands for action and drive, Cups for collaboration and feel, Swords for analysis and hard truths, Pentacles for craft and reliability).

## Refusals that need no draw

| The situation | What you do instead |
|---|---|
| Precise instructions, a single obviously correct approach, or a precision-seeking tone | Reject the draw and ask clarifying questions. |
| A safety, security sign-off, production, release, or incident-response decision, or any correctness verdict | Reject the draw as a decision method. A reading may prioritize where to investigate, and must then be followed by source review, tests, proofs, traces, or reproduction. |
| An explicit "do not use Tarot" | Reject the draw. Do not draw. |
| Drawn text contradicting a requirement or a concrete risk | Requirements and evidence win. Record the conflict and proceed on evidence. |
| The urge to redraw until a preferred card appears | Reject it. One draw per decision point. |

## Draw with real entropy over complete assets

Resolve the script from this `SKILL.md` file's installed location, never from the shell working directory. Relative links and JSON `file` paths resolve from the directory containing this `SKILL.md`. Quote the absolute script path in the commands below.

Draw the default spread, 12 Houses of the Zodiac, where each house gets 1 Major Arcana card then 2 Minor Arcana cards, and each of the 36 cards carries an independent reversal flag:

```bash
python3 "<resolved-script-path>"
```

For house and card text inline in the JSON:

```bash
python3 "<resolved-script-path>" --content
```

For a pre-flight asset check:

```bash
python3 "<resolved-script-path>" --verify
```

The script verifies all 92 assets before every draw and refuses to deal when any are missing. The draw succeeds when the script exits 0 and its JSON parses with 12 houses, 36 cards, sequential positions 1 through 36, 12 distinct Major cards, and 24 distinct Minor cards.

Then read every house file and every drawn card's file, honoring each card's orientation (upright or reversed). With `--content` the text is already in the draw output and no further reads are needed. The reading is complete when all 12 houses and all 36 cards have been read in their drawn orientations.

## Synthesize one story across all 12 houses

Weave a single reading across beginning stance, resources, communication, foundations, creativity, practice, partnership, transformation, principle, delivery, community, and blind spot. When time is short, prioritize House 1 for stance, House 6 for execution quality, House 8 for risk, House 10 for delivery, and House 12 for blind spots. State which approach the reading supports, which cards moved the choice, and what to watch. For security, audit, or correctness work the decision is only where to investigate next; evidence from review, testing, reproduction, or formal reasoning still decides whether a risk is real. The reading names a direction with its card reasons and caveats, delivered alongside the tool call that implements the chosen option.

Stop after one draw per decision point. A "try again" with no system change means drawing a new spread once, not re-running the same approach.

## Fail closed, never invent

When the script exits nonzero, reports missing assets, or the entropy source fails, stop and report the error, then skip the reading. Never invent cards, never simulate randomness by hand, and never interpret card names without their files. The whole point is real entropy over complete assets. A draw naming missing files fails closed too: do not fall back to interpreting from names or suits. Restore the assets (see `references/SOURCE-MAP.md`) and redraw.

## What you hand back

The chosen direction with its card reasons and caveats, attached to the tool call that acts on it. For the compact helper form, give `Verdict: {option}` plus one sentence of card reason, or 3 bullets (dominant theme, main risk or blind spot, recommended next action).

## Spread reference

| House | Represents | Question it answers |
|-------|------------|---------------------|
| 1 | Self | How should this work begin? |
| 2 | Resources | What values, assets, or constraints matter? |
| 3 | Communication | What needs clarifying or connecting? |
| 4 | Foundations | What context or dependency underlies the task? |
| 5 | Creativity | Where should experiment or delight shape the work? |
| 6 | Practice | What quality, maintenance, or execution concern matters? |
| 7 | Partnership | Who or what must this integrate with? |
| 8 | Transformation | What risk, shared state, or deep change is present? |
| 9 | Exploration | What principle or broader strategy guides the path? |
| 10 | Calling | What delivery or long-term outcome is served? |
| 11 | Community | What system, network, or shared aspiration is involved? |
| 12 | The Hidden | What blind spot, ending, or unconscious factor matters? |

## Entropy note

Unseeded draws use `secrets.randbelow()` for two independent Fisher-Yates shuffles (Major and Minor decks separately) and `secrets.randbits()` for 36 independent reversal flags: roughly `log2(C(22,12))` bits from Major selection, `log2(C(56,24))` from Minor selection, plus 36 reversal bits, conservatively over 100 bits unordered (ordered house assignment holds more). Exact values print under `entropy_bits`. `--seed` exists for tests only, replays the upstream draw order (Major shuffle, Minor shuffle, reversals in house order) through one isolated PRNG, is labeled in the output, and carries no entropy claim.

## Rationalizations to reject

| Rationalization | Why it fails |
|---|---|
| The cards said so, so it is decided. | Cards inform direction. They never override safety, correctness, or requirements. |
| This reading justifies a pre-existing preference. | Say so honestly when the reading challenges instinct instead. |
| The reversed card means do nothing. | Reversed means blocked, internalized, or inverted. It is not inert. |
| Major Arcana overrides the user. | Requirements always take priority over readings. |
| Keep drawing until the spread agrees. | One draw per decision point. Accept the spread. |
| The reading says the risk is fine. | Only evidence dismisses a security or correctness concern. |
