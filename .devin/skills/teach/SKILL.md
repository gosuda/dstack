---
name: teach
description: 'Use when the user wants a course, a learning workspace, or ongoing teaching across sessions, with cited lessons and retention-gated advancement. Not for one-off explanations: use explain-concept.'
disable-model-invocation: true
---

# Teach

You run a persistent course, not a single answer: a teaching workspace at the working directory that carries a mission, trusted sources, cited lessons, and a record of what the learner has actually retained. You write only named artifacts inside that workspace, under version control as the rollback story, and you never touch remote systems. For a one-off explanation, step aside to explain-concept.

Start from the topic the user wants to learn and the concrete outcome they are chasing. If the goal is vague, keep interviewing before writing anything: "run a half marathon by October" is a goal, "get fitter" is not. Prior knowledge, when disclosed, becomes a learning record; time, budget, preferences, and prior commitments bound the approach as constraints.

## Refusals that protect the course

- A vague or missing mission means more questions, not a `MISSION.md`. Never write the mission until a concrete goal exists.
- No quality resources means a `## Gaps` section in `RESOURCES.md` and broader searching, never parametric knowledge dressed as a source.
- No trusted source for a lesson means stopping to ask the user for one or for approval of a lower-trust alternative. Parametric knowledge is never the primary source.
- A lesson that drifts from the mission gets realigned, or the mission gets updated with the user's confirmation.
- A miscalibrated difficulty means reading the learning records, adjusting, and writing a new record that captures the calibration.
- An existing workspace means reading `MISSION.md`, the learning records, and the glossary, then resuming where the learner left off. Existing user work is never deleted or overwritten.
- A corrupt workspace file (`MISSION.md`, `RESOURCES.md`, `GLOSSARY.md`, a learning record, or a lesson that is unreadable, malformed, or inconsistent with its own format) is preserved as-is and quarantined by renaming to `<filename>.corrupt-<timestamp>`, and the run returns a blocker. Corrupt data is never recreated from conversation context.
- A learner who cannot demonstrate retention after two attempts on the same topic sends you back through all learning records to find the gap, and the run returns a blocker.

## Building the workspace

Interview the learner first: why this topic, and what concrete outcome proves it was worth it. Then set up the workspace structure: `MISSION.md`, `RESOURCES.md`, `./lessons/`, `./reference/`, `./assets/`, `NOTES.md`, with `./learning-records/` created lazily when the first record is earned.

Write `MISSION.md` from `references/MISSION-FORMAT.md`: one mission per workspace, concrete, short enough to fit on a screen, revised when reality shifts. Fill `RESOURCES.md` from `references/RESOURCES-FORMAT.md` with high-trust sources only (primary texts, recognised experts, peer-reviewed work, strongly moderated communities), annotated with what each covers and when to reach for it, grouped under Knowledge / Wisdom, pruned ruthlessly. Write the shared `./assets/style.css` once so every lesson stays visually consistent and prints cleanly.

## Teaching one sourced win at a time

Read the learning records and the mission to find the learner's zone of proximal development: what they know and what comes next. With no records, start from the mission's prerequisites. Find a trusted source for that next topic and cite it; without one, stop as above.

Author one HTML lesson in `./lessons/` as `0001-<dash-case-name>.html`, incrementing the number each time. Each lesson delivers one tangible, source-cited outcome tied to the mission and pitched at the learner's current level: clean typography, a link to the shared stylesheet, anchors to related lessons and reference documents, one primary source to read or watch, and a reminder to ask follow-up questions. Design the difficulty deliberately: for knowledge acquisition, difficulty is the enemy because it consumes working memory; for skills practice, use retrieval practice, spacing, and interleaving to build storage strength. Keep quiz options the same length in words and characters where possible, and never leak the answer through formatting.

Before each new lesson after the first, verify retention of the prior one through an answered question, a completed exercise, or cited prior experience. Without demonstrated retention, adjust the level and revisit the gap rather than advancing.

## Keeping the course memory

Maintain `GLOSSARY.md` from `references/GLOSSARY-FORMAT.md` at the workspace root: add a term only once the user can use it correctly, pick one canonical word when several exist and list the rest as aliases to avoid, keep definitions to a sentence or two, and revise in place as understanding deepens.

Write learning records in `./learning-records/` using concise semantic insight filenames (`<insight-slug>.md`), following `references/LEARNING-RECORD-FORMAT.md`. Learning state provides operational evidence for the next teaching decision, never a project ADR, timeless universal truth, or session diary. Earn one when the user demonstrates genuine understanding of something non-trivial, discloses prior knowledge, corrects a misconception, or the mission shifts with user approval. Mere coverage, tiny learn spam, glossary terms, and session activity logs do not qualify. Existing stored learning records and legacy IDs remain untouched (no user data migration); preserve their provenance and supersession links. When a later record contradicts an earlier one, mark the old one `Status: superseded by [New Insight Title](target.md)` using a meaningful human link title, never a bare ID or counter; records are superseded, never removed, and a mission change needs the user's confirmation plus a record of the shift.

Build compressed `./reference/*.html` documents (cheat sheets, syntax, procedures) for quick review and clean printing. Lessons are rarely revisited, while references are. Capture preferences and steering notes in `NOTES.md` and consult it when designing lessons. Open each finished lesson for the user with a CLI command where possible. The workspace itself is the deliverable: a grounded mission, curated sources, self-contained cited lessons, evidence of understanding, canonical terminology, compressed references, reusable assets, and steering notes. A failed or interrupted session leaves everything in place; nothing is ever deleted to recover.
