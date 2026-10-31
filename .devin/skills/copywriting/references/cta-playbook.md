# CTA playbook

Read this in cta mode before the interview. It holds the interview options, the archetype decision tree, the recommendation template, the operating principles, and the named failure modes.

## Interview options

Ask in this order, one question at a time, and skip any input the user already gave. Offer the options as tappable choices.

| Input | Options |
|---|---|
| 1. Article context | Personal or independent blog or essay; newsletter or paid publication; brand or company content-marketing blog; other |
| 2. Primary objective | Newsletter or email subscription; social follow; lead generation (gated asset); product or service signup or free trial; demo or sales call booking; direct purchase; community join; engagement (reply, comment, share); reader support (paid subscription or tip); try-it or direct action; other |
| 3. Audience and relationship | First-time visitor; returning reader, not subscribed; existing subscriber or customer; mixed or unknown |
| 4. Funnel stage | TOFU (discovery, no buying intent); MOFU (evaluating, comparing); BOFU (ready to act); not applicable |
| 5. Mechanism preference | None or value-only; curiosity gap; reciprocity (free asset first); discount or offer; urgency (real deadline); scarcity or FOMO; social proof |

Ask the mechanism question only when a mechanism could legitimately help. For skeptical or repeat-reader audiences, use none or value-only without asking.

## Archetype decision tree

```
context = INDEPENDENT / PERSONAL
├── objective = newsletter / email      → A: Author-signature subscribe
├── objective = try-it / direct action  → B: Inline action + source link
├── objective = reader support / tip    → C: Reader-supported funding link
├── objective = community               → D: Proof-counted community invite
├── objective = social follow           → A (variant: lead with social links)
├── objective = engagement              → E: Specific reply prompt
└── objective = product / demo          → FLAG. Valid only where the author IS
    the product (consultants, solo founders, indie devs). Frame as "if you hit
    this, here's how I help", never "Book a Demo" verbatim.

context = NEWSLETTER PUBLICATION
├── objective = growth / subs           → F: Share/restack + native widget
├── objective = engagement              → E: Specific reply prompt
├── objective = paid conversion         → G: Value-gap tease
├── objective = monetization / sponsor  → H: Inline sponsor block (not bottom)
├── objective = community               → D
└── objective = direct purchase         → K (rare; BOFU only)

context = BRAND / CONTENT MARKETING
├── objective = engagement              → E (rarely right here)
├── stage = TOFU                        → I: Transitional asset (lead magnet)
├── stage = MOFU                        → J: Direct + transitional pair
├── stage = BOFU                        → K: Direct CTA + risk reversal
└── stage = Not applicable              → L: Value-statement subscribe (fallback)
```

Under brand or content marketing, check the engagement objective first; otherwise the funnel stage picks the archetype. When the inputs reach no leaf, or reach the FLAG leaf for an author who is not the product, report the conflict and propose the closest valid archetype.

## Recommendation template

Compose the recommendation in exactly this structure. Write "Omit" with a reason for any optional slot that would feel forced.

```markdown
## Recommended CTA

**Archetype:** [letter + name] **Why this fits:** [1-2 sentences naming the input combination]

### Content (copy)
**Headline / value line:** > [exact text]
**Body / proof line (1-2 lines):** > [exact text]
**Button copy:** > [exact text]
**Risk reversal / subtext (if applicable):** > [exact text, or "Omit: would feel forced"]

### Form (structure)
- **Placement:** [end-only / end + sticky / end + mid-article repeat]
- **Visual weight:** [low / medium / high, with justification]
- **Layout:** [single button / button + text link / native widget cluster / one-line signature]
- **Proof to co-locate:** [subscriber count / star count / testimonial / named recommenders / logo wall / none]

### Mechanism
[Named mechanism + 1 sentence on why appropriate, OR "None: value statement carries it. Mechanisms would erode trust for this audience."]

### A/B test plan
- **First test:** [single variable]
- **Why this one first:** [1 sentence]
- **Sample size consideration:** [qualitative volume check, or "Skip A/B: traffic too low"]

### Accessibility check (WCAG 2.2)
- **Color contrast:** [target ratio + concrete pairing if colors known]
- **Touch target:** [size requirement]
- **Semantic markup:** [<button> vs. <a> vs. form]
- **ARIA:** [only if non-obvious]
- **Keyboard / focus:** [requirement]
- **Color-independence:** [non-color affordance]
```

## Operating principles

Enforce these while composing.

- One primary CTA per post. Competing CTAs are the most common failure.
- Match the publication's voice. A personal-essay footer that reads like a SaaS landing page collapses credibility.
- Specificity beats cleverness. "Get one essay a week on indie filmmaking" beats "Subscribe to our awesome newsletter." For button copy, the cleanest filter is whether the label completes "I want to ___".
- Put proof next to the ask. Place the honest signal (subscriber count, testimonial, logos, star count) inside or beside the CTA block.
- Use a mechanism only when the context supports it. Urgency, scarcity, FOMO, or a discount added for effect erodes trust.
- Push back on bad asks. If the user wants a CTA that will fail, such as "Book a Demo" under a beginner tutorial for first-time visitors, say so, propose the alternative, and explain why. Deliver the original only with its failure mode flagged.

## Failure modes

Name the 2 to 3 that the user's inputs put them at risk of.

| Failure mode | Typical cause |
|---|---|
| Competing CTAs | More than one primary objective |
| Generic ask | "Subscribe for more", "Learn More" |
| Mechanism mismatch | Urgency or scarcity where none exists |
| Wrong register | SaaS landing-page voice on a personal essay |
| Proofless ask | No signal near the button |
| Premature sales ask | "Book a Demo" on TOFU content |
| Unanswerable reply prompt | Open-ended reply questions on social |
