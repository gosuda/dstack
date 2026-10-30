---
name: visual-diff-review
description: 'Use when asked to review a diff and produce a 7-section visual page. Not for interactive review walks or PR-specific review: use show-review.'
---

# Drawing the change on one page

You take a branch, commit, range, PR, or working tree, compare it against its base (`main` or `master` unless the user names another), and render the review as a single self-contained page at `diagrams/visual-diff-review.html` that you then open. The page carries seven sections in order -- Overview, Before State, After State, Risk Assessment, Coupling Analysis, Merge Recommendation, Evidence Log -- and every section cites its evidence or admits it has none. You touch nothing remote; the only mutation is that local page, and you state the rollback (delete or re-render the page) before writing it.

## Building the seven sections, in order

1. Resolve the named target to its base and extract the full diff. If the name does not resolve, report the exact name that failed and stop rather than widening scope; if the diff is empty, say no changes were found and stop.
2. Enumerate every affected file and component and classify the change surface. This is the scope everything later cites.
3. For each hunk, describe behavior before and after in concrete terms -- what the code did, what it does now.
4. Assess correctness, performance, security, and compatibility, each with evidence from the diff.
5. Name the cross-component dependencies and side-effect surfaces inside the diff.
6. Recommend merge, defer, or reject, grounded in the specific evidence from the earlier sections.
7. Write the page to `diagrams/visual-diff-review.html` and open it, or report the path if opening is unavailable. A filesystem error on write ends the run: report the error, roll back any partial file, and do not proceed to open.

## When evidence runs out

A section you cannot support is marked `INSUFFICIENT EVIDENCE` and the review continues -- citations are never fabricated. A partially complete page is acceptable only when each incomplete section is labeled that way; silence is not a partial result.
