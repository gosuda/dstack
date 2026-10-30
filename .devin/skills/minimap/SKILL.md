---
name: minimap
description: 'Use when the user needs a compact read-only current-work view from Git state, recorded test evidence, and optional graph.yaml. Not for tasks that need source or remote-system changes.'
---

# Minimap

This skill gives you one compact view of where current work stands. It joins what Git says, what the last recorded test result says, and what the project graph says, then sorts every claim into conquered, disputed, or fog. Use it when someone explicitly asks for a current work view, including at a phase boundary.

It is read-only and runs no tests. It never writes, stages, commits, or changes any file, branch, credential, payment, publication, deployment, or remote state. It emits one view and writes nothing.

## What it needs in hand

- A repository or worktree root, inferred from the current directory when unambiguous. Only that root is inspected or reported.
- The readable Git evidence for that root: current commit SHA, tree identity, tracked dirty paths, conflicts, and relevant branch or upstream state.
- The latest test result already recorded by the repository or supplied by the caller. A usable result names its checks and outcomes and carries a commit identifier or tree digest. An absent or unordered result is allowed and simply yields fog. This skill never creates or refreshes a result.
- Optionally, a project root `graph.yaml`. Absence is allowed and yields fog for graph knowledge while Git and test claims still render. The schema reference at `references/graph-schema.md` is always read before any `graph.yaml` validation, so validation never uses an unstated schema.

## How it snapshots the tree

It resolves one repository root and reads the Git evidence (commit SHA, tree identity, dirty path list, conflict list, branch and upstream state) without mutation. Then it locates the latest recorded test result using its explicit completion time or the repository defined ordering. If no unique latest result can be established, it records the reason and treats test knowledge as missing. It never runs a test or invents an ordering.

The recorded result is accepted only when it names its checks and outcomes and carries a commit identifier or tree digest. That binding is compared against the current commit or tree. A matching binding is current. A well formed but nonmatching binding is stale, and stays in the picture as contradiction evidence rather than current proof. A malformed result is rejected with the reason recorded.

Read `references/graph-schema.md` first. If `graph.yaml` exists at the root, read it without modification and check it against schema `odin.graph/v1` with a non-empty revision, unique non-empty node IDs, non-empty labels, and edges whose endpoints exist. Only these types are accepted.

| Kind | Accepted values |
|---|---|
| Node | `Invariant`, `Surface`, `Store`, `Hazard`, `Decision` |
| Edge | `constrains`, `reads`, `writes`, `fails-when` |

Unknown schema versions, node types, edge types, duplicate node IDs, and dangling edges are rejected with the specific violation named. Unknown top-level and per-record fields are ignored. Nodes and edges are treated as immutable assertions within their declared revision. Topology is never inferred, replanned, or altered.

## How it turns evidence into claims

It forms the smallest complete claim set from current Git facts, each recorded check outcome, and each valid graph node or edge relevant to the requested work. Every claim keeps its source identity (Git fact, test outcome, or graph node or edge). When `graph.yaml` is absent, a graph knowledge claim is added rather than silently omitting that source. No claim is invented, and no applicability link is asserted without input support.

Each claim then joins all applicable evidence, with no source given global precedence:

- Disputed, when applicable sources contradict, when proof is stale, or when dirty state touches the paths or tree the claim covers.
- Fog, when applicable evidence is missing (including the absent graph and the absent or unordered test result).
- Conquered, only when all applicable evidence is current and agrees.

Every claim gets exactly one class with a concise justification naming the evidence joined.

## The one view it returns

The complete result is a single compact view with exactly the three class headings, kept even when empty: `conquered`, `disputed`, `fog`. Every claim appears under exactly one heading with its source identities and one concise join justification. There is no second campaign or status map.

## When it returns blocked instead

It returns no partial minimap in these cases, with one exact `blocked: <failure-class>` result naming the failing input and reason:

| Failure | Meaning |
|---|---|
| `blocked: git-unavailable` | Repository root or required Git evidence cannot be read. Retry only after the root or read access is corrected. |
| `blocked: invalid-recorded-test-result` | A present selected artifact cannot be parsed into named checks, outcomes, and a commit or tree binding. Correct or replace the artifact outside this run. A genuinely absent or non-uniquely ordered artifact is not this failure. It yields fog. |
| `blocked: invalid-graph` | A present `graph.yaml` violates the accepted schema. Correct the graph outside this read-only run, then retry. Absence is not invalid. It yields fog. |
| `blocked: evidence-read-failure` | An input changed during the snapshot or cannot be read completely. Retry from a fresh read-only snapshot. |

No rollback applies because nothing is mutated. It never suppresses a failure and never reports the view as done unless every emitted claim has exactly one justified class.
