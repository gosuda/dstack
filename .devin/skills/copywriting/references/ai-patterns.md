# AI writing patterns

Read this in page mode when the user asks for AI-tell removal, and when auditing copy for `[AI-ISM]` flags. Run the pass before the seven sweeps. A word that the voice file or shipped copy uses as a signature is exempt from every list here.

## Words

Tier 1 words are always replaced when auditing. The banned words in the main skill file count as Tier 1 too; they are the only words banned outright in new copy.

`delve`, `landscape` (as a metaphor), `tapestry`, `realm`, `paradigm`, `embark`, `beacon`, `testament to`, `robust`, `comprehensive`, `cutting-edge`, `leverage` (as a verb), `pivotal`, `underscores`, `meticulous`, `seamless`, `game-changer`, `utilise`, `nestled`, `vibrant`, `deep dive`, `unpack`, `showcase`, `unlock`, `intricate`, `holistic`, `actionable`, `impactful`, `learnings`, `thought leadership`, `best practices`, `synergy`, `in order to`, `due to the fact that`, `serve as`, `commence`, `keen` (as an intensifier).

Tier 2 words are flagged when two or more appear in one paragraph.

`harness`, `navigate`, `foster`, `elevate`, `unleash`, `streamline`, `empower`, `bolster`, `spearhead`, `resonate`, `revolutionise`, `facilitate`, `underpin`, `nuanced`, `crucial`, `ecosystem` (as a metaphor), `myriad`, `plethora`, `catalyse`, `transformative`, `cornerstone`, `paramount`, `burgeoning`, `nascent`, `overarching`.

Tier 3 words are flagged only at high density, around 3 percent of the words in a passage or more.

`significant`, `innovative`, `effective`, `dynamic`, `compelling`, `unprecedented`, `exceptional`, `remarkable`, `sophisticated`, `world-class`, `state-of-the-art`.

## Structures

| Pattern | Examples or test |
|---|---|
| Formulaic opening | "In the rapidly evolving world of..." |
| Rhetorical-question opener | A question the reader was not asking |
| Engagement hook | "Here's the thing", "Plot twist:" |
| Copula avoidance | "serves as", "features", "boasts" where "is" or "has" would do |
| Synonym cycling | The same thing renamed every sentence |
| Vague attribution | "Experts believe", "Studies show" |
| Significance inflation | Ordinary facts framed as milestones |
| False range | "From startups to enterprises" covering nothing in between |
| Dash stand-ins | Any em dash, en dash used as a dash, `--`, or spaced hyphen. One occurrence is a failure |

## Chatbot artefacts

Remove these entirely: "I hope this helps", "Great question", "Let's dive in" and any other "let's" plus verb transition, leaked chain of thought ("Let me think step by step", "Step 1:"), and acknowledgement loops.

## Drafting tells

These survive a word-level pass, so check for them separately.

| Tell | What it looks like |
|---|---|
| Prompt echo | The draft reuses the brief's own phrasing |
| Generic default | A real number or name the user supplied is replaced by a category placeholder |
| Uniform confidence | Every line lands at the same pitch |

## Severity

| Level | Patterns | When to fix |
|---|---|---|
| P0, credibility killers | Knowledge-cutoff disclaimers, chatbot artefacts, vague attributions, significance inflation, a supplied specific replaced by a generic default | Immediately |
| P1 | Prompt echo, Tier 1 words, template phrases, "let's" openers, formulaic openings, engagement hooks, bold overuse, any em dash | Before publishing |
| P2 | Generic conclusions, compulsive rule of three, uniform paragraph length, announced honesty, copula avoidance, overused transitions, Tier 2 clusters | When time allows |

Copy with no P0 or P1 hits left is publishable.
