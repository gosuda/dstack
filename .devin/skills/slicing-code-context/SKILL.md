---
name: slicing-code-context
description: 'Use when an exact symbol, path, entrypoint, or line range can bound a focused code question or patch proposal under a fixed source budget. Not for source changes or broad repository exploration.'
---

# Answering a focused code question from a bounded slice

Some questions need context but not the whole repository: what this unit does, what can reach that sink, what this entry can trigger, how one unit reaches another. This skill builds one deterministic packet of source ranges that answers exactly that question under a fixed token budget, hands it to a single read-only worker with nothing else, and checks the answer against the packet before reporting it.

Three refusals come first, because they define the shape. This skill never mutates source: it returns proposed edits as read-only output and never applies them. It never does broad or anchorless exploration: every request needs an exact anchor and a focused task. And when the requested traversal needs parser-backed graph analysis that the repository cannot provide, it reports that gap instead of faking the context with lexical search or hand-picked files.

It is read-only throughout. No file, version control, credential, paid, published, deployed, or remote mutation happens here. The only effects are one deterministic slice packet and one constrained worker response, with at most one coordinator-built replacement packet. The work is done when the packet budget and boundaries validate, every worker claim and proposed edit cites included ranges, uncertain edges stay labeled as hypotheses, and the coordinator independently checks every consequential conclusion.

## What a request carries

- Target source tree root (required): the canonical directory holding the source to slice.
- Anchor (required): one repository-relative `FILE:START-END` line range, one exact path, one fully qualified symbol, or one exact entrypoint.
- Worker task (required): a concrete question or patch proposal whose answer can be checked from source. An empty task is rejected.
- Mode and depth (optional): picked from the table below, which pairs each question shape with its traversal.
- Peer anchor (required only for `path`): an exact second symbol or line range.
- Budget (optional): a positive integer estimated-token limit, default 8192.

| Question | Mode | Depth |
|---|---|---:|
| Explain or review one unit with immediate context | `neighborhood` | 1 exactly |
| Who can reach this sink? | `upstream` | 2 to 4 |
| What behavior can this entry trigger? | `downstream` | 2 to 4 |
| How does one unit reach another? | `path` | 10 to 20 |
| Which public entrypoint reaches this target? | `entrypoint` | 10 to 20 |

A request whose anchor sits outside the root, whose line range is invalid or reversed, whose mode and depth fall outside this table, or whose `path` mode lacks a peer is rejected before anything is built.

## Resolving the anchor exactly

A line-range anchor resolves only to those live lines. A path anchor resolves to the whole file only if it fits the budget; otherwise a line range or symbol is required. A symbol or entrypoint resolves through the repository's available parser-backed symbol and reference index, with candidates sorted by repository-relative path, start line, end line, then fully qualified name. Zero matches is `symbol_not_found`; more than one exact-name match is `ambiguous_symbol`, which returns the sorted candidates without choosing between them. When no parser-backed index exists for a graph mode, return `analysis_unavailable` with the unsupported language or index named. Never substitute lexical search or hand-selected context, and never guess between candidates.

## Growing the slice along the graph

The anchor is hop 0. From it, follow the parser-backed references, calls, and import relationships for the selected mode: `neighborhood` takes the anchor unit plus its directly enclosing unit, direct callers and references, and direct callees and dependencies at one hop; `upstream` walks incoming edges breadth-first; `downstream` walks outgoing edges breadth-first; `path` takes the shortest directed path from anchor to peer; `entrypoint` takes the shortest reverse path from the anchor to a public entrypoint. At each breadth, sort edges by destination path, destination start and end lines, edge kind, then source path and start and end lines, and deduplicate identical ranges with first discovery winning. Mark an edge `certain` only when the parser or index establishes it; keep unresolved dynamic or indirect edges in `uncertain_edges` only, never as traversal proof.

## The packet and its budget

Build one packet with this exact top-level key order and field schema:

```json
{
  "schema": "odin-slice-packet-v1",
  "task": "string",
  "root": "canonical absolute path",
  "anchor": {"kind":"line_range|path|symbol|entrypoint","value":"string"},
  "peer": null,
  "mode": "neighborhood|upstream|downstream|path|entrypoint",
  "depth": 1,
  "budget": {"limit_estimated_tokens":8192,"used_estimated_tokens":0},
  "slices": [
    {"file":"repository/relative/path","start_line":1,"end_line":1,"symbol":null,"hop":0,"relationship":"anchor","certainty":"certain","content":"exact source text"}
  ],
  "uncertain_edges": [
    {"from":"file:start-end","to":"file:start-end or unresolved label","kind":"string","reason":"string"}
  ],
  "omissions": [
    {"candidate":"file:start-end","reason":"budget|depth|uncertain|unavailable"}
  ]
}
```

`peer` is `null` except in path mode, where it carries the same object schema as `anchor`. Store source with LF line endings and no synthetic elision markers. Order slices by hop, file, start line, end line, relationship. Order uncertain edges and omissions lexicographically by all displayed fields. Serialize as compact UTF-8 JSON with no insignificant whitespace and no trailing newline.

Then apply the budget algorithm exactly. Start `used_estimated_tokens` at 0 and add candidate slices in the deterministic order above. After each addition, serialize the entire candidate packet, set `used_estimated_tokens = ceil(serialized_UTF8_byte_count / 4)`, and repeat the serialize-and-assign step until the value stops changing. Keep the candidate only when the stable value fits the limit. The hop-0 anchor is mandatory: if it alone exceeds the limit, return `anchor_exceeds_budget` and require a narrower line range or a larger explicit budget. Record each rejected non-anchor candidate in `omissions` with reason `budget`, then recompute the same fixed point including the omission records. If the omission records themselves push the packet over budget, drop omission records from the end of their sorted order until the fixed-point value fits, and append one final summary omission `{"candidate":"additional candidates","reason":"budget"}` if that record fits. Never truncate source content.

Before delegation, verify independently: recompute the fixed-point estimate and require it to equal `budget.used_estimated_tokens` without exceeding the limit; require every slice path to stay under the canonical root, every range to satisfy `1 <= start_line <= end_line <= current_file_line_count`, every content value to equal those exact live lines, hop 0 to contain the requested anchor, and graph slices to obey mode and depth. Stop on any mismatch (`packet_invalid`, `stale_source`): report the failed check and do not delegate.

## Delegation and checking the answer

Send a fresh read-only worker exactly three things: the task string, the packet bytes exactly as serialized, and the worker response schema below. No conversation history, no architecture notes, no expected conclusion, no repository access, no additional source.

The worker returns exactly:

```json
{
  "status":"complete|needs_context|cannot_answer",
  "answer":"string",
  "evidence":[{"claim":"string","file":"string","start_line":1,"end_line":1}],
  "proposed_edits":[{"file":"string","start_line":1,"end_line":1,"replacement":"string","rationale":"string"}],
  "missing_context":[{"symbol_or_range":"string","reason":"string"}],
  "uncertainties":["string"]
}
```

Check the response strictly. Reject malformed JSON or an unknown field value (`worker_output_invalid`). Require every evidence item and proposed edit to have its file and complete line range contained within one packet slice. Require each claim to cite at least one evidence item. A claim resting on an `uncertain_edges` entry must be labeled a hypothesis in `uncertainties`. Independently re-read the cited packet ranges for every consequential conclusion and record agreement or rejection. The worker cannot authorize or apply an edit.

When the worker answers `cannot_answer`, report its reason with the packet summary and stop; never widen scope to coax an answer.

## The one allowed second packet

Only `status: needs_context` permits expansion, and only once. Each `missing_context` request must name an exact symbol or `FILE:START-END` and explain why it is necessary. Build one replacement packet from the original anchors plus only the valid requested ranges, under the same single aggregate budget and algorithm, and send it to a fresh worker with the full task. Never stack packets or allow browsing. If the replacement response still needs context, stop delegation and report the unresolved request.

## Named failures

Anchor and traversal failures return deterministically: `symbol_not_found` returns the exact unresolved anchor and requires a live exact one; `ambiguous_symbol` returns the sorted exact candidates and requires one selected candidate; `invalid_depth` points back to the table (neighborhood exactly 1, upstream/downstream 2 to 4, path/entrypoint 10 to 20); `invalid_anchor` or `path_outside_root` requires a canonical repository-contained path and live range; `analysis_unavailable` reports the unsupported language or index; `anchor_exceeds_budget` requires a narrower line range or a larger explicit budget; `path_not_found` or `entrypoint_path_not_found` reports the parser-backed graph gap, with depth increased only by an explicit new invocation.

## What gets returned

The canonical packet, then the worker response, then a validation report ordered by budget check, citation containment, consequential-claim checks, and proposed-edit disposition. An edit is never applied.
