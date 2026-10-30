---
name: graph-backbone
description: 'Use when defining, revising, or gate-replanning the project structural backbone in project-root graph.yaml. Not for remote, credential, publish, deploy, or irreversible changes.'
---

# Keep the project backbone

The structural backbone of the project lives in one file, the project-root `graph.yaml`, and you are its only writer. Nothing else in the repository changes under this skill. You create the backbone, append topology revisions to it, or replan focus nodes under a declared gate. You never execute graph nodes, touch remote systems, or mutate version control. If anything goes wrong after a write, you restore the checkpoint bytes (or remove the file you created) and say what happened.

## Set the write boundary first

Resolve the project root to an absolute path and bind your write set to its single `graph.yaml`. Checkpoint the file byte for byte before changing anything; a missing file counts as the creation checkpoint. No write target outside `graph.yaml` opens at any point.

Outside this procedure, only the designated read-only status consumer reads the file. No other workflow reads or writes it, and no code-changing workflow depends on it.

## Classify the request before mutating

Label the operation create, topology change, or focus replan before you touch the file. Any node addition, removal, identifier change, or type change, and any edge addition, removal, endpoint change, or type change, counts as a topology change. A focus replan alters only an existing gate's focus-node data.

You need the project root, the one operation, and, for creation or topology change, the complete proposed node and edge sets plus a unique non-empty revision identifier. A focus replan needs the declared gate and its permitted focus-node IDs. A topology change also needs the project's append-only transition-ledger representation when `graph.yaml` does not already make it unambiguous. Treat an existing `graph.yaml` as required input for revision or replanning, and as optional input for creation.

## Validate against the schema

Read `references/graph-schema.md`, then parse the existing file when one is present. Require `schema`, `revision`, `nodes`, and `edges`; require schema `odin.graph/v1` and a non-empty revision; require unique non-empty node IDs with non-empty labels; require every edge endpoint to name an existing node. Reject an unknown schema version, node type, edge type, duplicate node ID, or dangling edge, and name the violation.

The closed type lists are:

| Element | Allowed values |
|---|---|
| Node types | `Invariant`, `Surface`, `Store`, `Hazard`, `Decision` |
| Edge types | `constrains`, `reads`, `writes`, `fails-when` |

Preserve every unknown top-level and per-record field without interpreting, normalizing, reordering, or deleting it.

## Approve the frozen backbone, then write

For creation or topology change, compile the complete proposed graph against the schema checks above. Freeze the revision, nodes, and edges, display that frozen set, and wait for human approval of that set. Never infer approval from the initial request. For a topology change, assign the approved topology a new revision and append its transition through the file's established append-only ledger representation; never rewrite or remove an earlier transition. If the ledger representation is absent or ambiguous, stop before mutating rather than inventing one.

For a gate replan, keep revision, nodes, edges, and ledger byte-identical to the checkpoint. Confirm the named gate exists and authorizes every changed focus-node ID, then alter only that gate's existing focus-node data. Stop when the gate or its focus representation is missing or ambiguous.

Before writing, replay the same classified operation from the checkpoint and require the second serialization to be byte-identical to the first. On a mismatch, stop with the checkpoint restored. After writing, read the file back and repeat the full schema, topology-immutability, metadata-preservation, ledger, gate-scope, and deterministic-replay checks. The graph may order subsequent plan sequence, but this procedure neither executes that plan nor authorizes mutation beyond `graph.yaml`.

## Name the failure and recover

| Failure | What it means and what you do |
|---|---|
| `invalid-input` | Operation inputs are missing. Change nothing and name what is missing. |
| `schema-rejected` | A closed-schema or graph-integrity check failed. Change nothing and name the violation. |
| `approval-withheld` | The frozen backbone was not approved. Change nothing. |
| `gate-violation` | The gate is absent or a focus change falls outside it. Change nothing. |
| `ledger-undefined` | The revision ledger is absent or ambiguous. Stop before mutation rather than inventing one. |
| `nondeterministic-replay` | The two serializations differ. Stop with the checkpoint restored. |
| `write-verification-failed` | The write or read-back failed. Restore the checkpoint bytes, or remove `graph.yaml` when this run created it. Never leave a partial revision, widen the write set, invent metadata or evidence, swallow an error, or claim success. |

Each failure result names the class, operation, failing check, observed evidence, and recovery performed. When the checkpoint cannot be verified as restored, return `blocked` with the remaining local difference.

On success, return the complete project-root `graph.yaml` with a `created`, `revision-appended`, or `focus-replanned` result holding the revision, the approved write set, the gate when one applies, validation results, the replay digest, and the rollback checkpoint identity.
