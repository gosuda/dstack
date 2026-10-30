# Mapping a study corpus

A corpus map is the inventory a teacher works from: every readable file listed, every teachable concept named once, each concept pointing at the exact passage it came from. Re-running the map overwrites `CORPUS.md` whole; never merge with a prior version.

## The file you produce

```md
# Corpus: {name}

corpus_root: {absolute path}
mapped: {YYYY-MM-DD}

## Sources

| File | Kind | Cite from |
|---|---|---|
| {rel-path} | {kind} | {anchors or reference only} |

## Concepts

1. **{Term}** — {one sentence}. Needs: {prereqs or none}. Source: `{anchor}`
```

## Naming what each source is

Use one of these kinds in the Sources table:

| Kind | Meaning |
|---|---|
| textbook | Structured chapter or section exposition. |
| paper | Peer-reviewed publication or preprint that makes claims suitable for a research venue. |
| practitioner book | Field guide, handbook, or how-to. |
| work document | Notes, memos, or onboarding docs authored on the job. |
| notes | The learner's own capture, which may be fragmentary. |

Mark a file `reference only` in its Sources row when it orients but teaches no distinct concept.

## Pointing at the exact passage

Every concept line carries exactly one anchor. A concept taught in two places cites the earlier introduction.

- Preferred: `<path-relative-to-corpus-root>#<heading-slug>`, for example `ch03-locks.md#deadlock`.
- Fallback when the source has no headings: `<path>:<start>-<end>`, for example `notes/raw.md:12-34`.

## Keeping the map honest

- Keep the Sources row count equal to the readable-file count; every readable file appears.
- List unreadable files under `## Unreadable` with the file name and why each could not be read.
- Order Concepts by prerequisite: no concept appears before a concept it needs.
- When two concepts need each other, keep the one the corpus introduces first in place and append `cycle: see {other}` on the other's line.
