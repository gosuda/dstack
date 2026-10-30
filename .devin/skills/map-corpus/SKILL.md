---
name: map-corpus
description: 'Use when the user points to a study-material folder and asks to make it teachable. Not for remote, credential, publish, deploy, or irreversible changes.'
---

# Map corpus

You turn a folder of study material into a teachable map: a single `CORPUS.md` at the workspace root that inventories every file, names what the material teaches, and orders ideas so prerequisites come first. You never change anything inside the corpus folder itself, and the only file you write is workspace-root `CORPUS.md` (restoring the prior file, or deleting a newly created one, rolls the run back).

You need the corpus folder path and the workspace root where `CORPUS.md` will live. If the corpus path is missing, ask once; if it stays unavailable, stop blocked. An existing `CORPUS.md` may be replaced, but only once the new map is complete and verified.

## Fixing the two paths

Expand `~`, resolve the corpus folder to an absolute path, and confirm it exists and is a directory. Resolve the output path too, and confirm it is exactly workspace-root `CORPUS.md` without touching the corpus root. If the corpus is missing, not a directory, or the output path resolves anywhere else (or writing it would modify the corpus root), write nothing and return `blocked` with both resolved paths and the failed validation.

## Reading everything without changing anything

Recursively list every file under the corpus root and attempt to read each one as-is: no conversion, no modification. Mark each file readable or unreadable and keep the observed reason for every unreadable one. Unreadable files get no conversion attempt and no converter recommendation; a map built from the readable remainder is still valid, but only if every unreadable file is disclosed with its reason.

## Recording sources and concepts

For every readable file, write one source row with its path relative to the corpus root, its material kind, and either the headings worth citing or `reference only`. The row count must equal the readable file count, and no absolute path may appear in a row or a citation.

Then name what the readable material teaches. For each concept, keep the source's own term where one exists, add a one-sentence definition, list its prerequisites, and give at least one citation anchor. Every readable file must be accounted for: either it contributes a concept or its source row says `reference only`. Form citations as `<path-relative-to-corpus-root>#<heading-slug>`, falling back to `<path-relative-to-corpus-root>:<start>-<end>` only when the source has no headings.

## Ordering ideas for learning

Lay the concepts out as one flat numbered list with every prerequisite placed before its dependents. When two concepts depend on each other, put first whichever the corpus introduces first and disclose the cycle on the other concept's line. If the list would grow past roughly forty entries, merge concepts the corpus always teaches together.

## Writing the map

Assemble `CORPUS.md` with these parts in this order: `# Corpus: <name>`; `corpus_root: <absolute path>`; `mapped: <YYYY-MM-DD>`; a `## Sources` table with `File`, `Kind`, and `Cite from` columns; a `## Concepts` numbered list whose entries carry the term, definition, `Needs:`, and `Source:` (using `Needs: none` where there are no prerequisites); and a `## Unreadable` list of each unreadable relative path with its reason, or `None` when everything read cleanly.

Before writing, verify source accounting, concept coverage, citation form, and prerequisite order against the enumerated corpus. If any of those cannot be established from the material, keep any existing `CORPUS.md` untouched, write no partial replacement, and return `blocked` naming the unmet condition. Only when verification passes, wholly replace workspace-root `CORPUS.md`. On success, report the file path with counts of readable sources, unreadable sources, and concepts. If the write itself fails, say so with the error, claim nothing, and restore the prior file when one exists or remove the incomplete new file otherwise.
