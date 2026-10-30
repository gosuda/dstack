# Learning record format

Learning records live in `./learning-records/` and use concise semantic insight filenames: `<insight-slug>.md` (for example, `mechanical-tension-drives-hypertrophy.md` or `prior-js-promises.md`). Create the directory lazily, only when the first record is earned. Existing stored learning records (including legacy numbered paths such as `0001-slug.md`) remain untouched; do not migrate or rename historical files.

Learning state is operational evidence for the next teaching decision, not a project ADR or timeless universal truth. Each record captures a non-obvious lesson, a key insight, or a piece of stated prior knowledge backed by actual evidence that steers future sessions. Together they feed the zone-of-proximal-development calculation behind what to teach next.

## The shape of a record

```md
# {Concise semantic insight title of what was learned or established}

{1-3 sentences: what was learned (or what prior knowledge was established), and why it matters for future sessions.}
```

The heading must be a concise semantic insight title that names what was learned (for example, `# Mechanical tension drives hypertrophy` or `# Prior experience: JavaScript async/await`), never a bare counter, generic label, or ID like `# LR-0001`. That is the whole format. A record can be a single paragraph. Its value is stating _that_ something is now known and _why_ that changes what comes next, not filling out sections.

## Sections worth adding only sometimes

Most records need none of these. Add one only when it carries genuine weight.

- Status frontmatter (`active | superseded by [Meaningful Title](path.md)`). Use it when an earlier understanding turned out wrong and a later record replaces it. Always link using a meaningful human title naming the superseding insight (for example, `Status: superseded by [Mechanical tension drives hypertrophy](mechanical-tension-drives-hypertrophy.md)` or, when pointing to an existing legacy record, `Status: superseded by [Original Understanding](0001-legacy-topic.md)`). Never use a bare ID or counter like `LR-0002`.
- Evidence: how the user showed the understanding (a question answered, an exercise completed, prior experience cited). Worth keeping when the claim might get revisited later.
- Implications: what this unlocks or rules out for future sessions. Worth keeping when the consequence is not obvious.

## Naming a record

Name each new record with a concise semantic slug that identifies the insight or established understanding (for example, `mechanical-tension-drives-hypertrophy.md` or `prior-js-promises.md`). Do not increment counters or prefix filenames with sequential numbers like `0001-` or `LR-NNNN`. Pick a name descriptive enough that scanning `./learning-records/` reveals the learner's current operational state without opening the files. If two records touch the same concept, qualify the specific insight or context rather than adding an arbitrary number. Existing stored records retain their historical filenames and IDs without migration.

## Earning a record: when to write one

Write one when any of these holds:

1. The user showed genuine understanding of something non-trivial. Look for evidence they can use the concept correctly, not mere exposure. This decides what to teach next.
2. The user disclosed prior knowledge ("I already know X"). Record it with the depth claimed, so future sessions never re-teach it.
3. A misconception was corrected. The user believed something wrong and now sees why. Record the correction, because it predicts where related topics will stumble.
4. The mission shifted in response to learning. The user found they care about something different than they first thought. Confirm the new direction with the user first, then cross-link the workspace mission (using relative generated-record link pattern `[Mission](../MISSION.md)` from within `./learning-records/`) and update it.

### What never earns one

- Material merely covered. Coverage is not learning. Wait for evidence.
- Anything already captured tersely in the workspace glossary (using relative generated-record link pattern `[Glossary](../GLOSSARY.md)` from within `./learning-records/`) as a term definition. Never duplicate it.
- Session-by-session activity logs or tiny learn spam. Records are decision-grade operational insights, not a journal, play-by-play log, or trivial checklist.

## When understanding changes

When a later record contradicts an earlier one (understanding deepened or corrected), mark the old record `Status: superseded by [New Insight Title](target.md)` (or, if referencing an existing legacy record, `[Target Title](0001-slug.md)`). Always use a meaningful human link title naming the insight, never a bare ID or counter. Retain existing stored paths, identifiers, and provenance links without user data migration. Never delete an old record. The history of how understanding evolved is itself useful operational signal.
