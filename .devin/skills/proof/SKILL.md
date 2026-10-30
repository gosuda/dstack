---
name: proof
description: 'Use when asked to publish, read, comment on, suggest to, or pull a Proof collaborative markdown document. Not for proofreading, math proofs, or test evidence.'
---

# Sharing a markdown document through Proof

Work with one collaborative markdown document on the hosted Proof service through its HTTP API from `Bash`. The local file stays canonical; a Proof link is a share, never a second knowledge store. The durable learning bundle stays the YAML `docs/solutions/` records owned by `compound`.

Provenance: `EveryInc/compound-engineering-plugin` pinned `fbd794b329f5b65d0ea00a5e6487336c385ff2be`, `skills/ce-proof/SKILL.md` plus `references/api.md` and `references/workflows.md`. Recipes conform to API v3 documented at https://www.proofeditor.ai/agent-docs and the pinned reference. Outward mutating writes require explicit user approval before execution and are never pre-verified with live writes. Identity `ai:compound-engineering` and display `Compound Engineering` are preserved as wire defaults; a caller may pass a distinct sub-agent identity pair when that agent owns the doc. No trademark SVG is reused as branding.

## Which job is this

Pick the narrowest operation for the request: `publish`, `read`, `review`, `comment`, `edit`, `suggest`, `pull`, `title`, or `delete`. Publish is one-way, local file to hosted doc. Read and review start from the live document as source of truth. Edit starts from a fresh read and touches as little as possible. Pull syncs the live markdown down to a local file. Delete only finishes an explicitly ephemeral scratch doc or an explicit user cleanup ask.

This skill owns the share, read, review, edit, and pull plumbing. It does not own durable learning (`compound`, `autolearn`) or local doc authoring (`docs-writing`); PR bodies belong to their own flow, not this one. It publishes source-file bytes; it never hand-writes the shared body.

## What you need up front

You need the local markdown path for publish or pull, or the Proof URL with slug and token for anything touching the hosted doc. You also need the user's explicit go-ahead for that operation: publishing, editing, commenting, suggesting, presence, a title change, a pull that overwrites as a side effect, and deletion each wait for their own explicit invocation, and any sensitive content placed in the doc needs its own explicit approval. Never put secrets, credentials, API keys, private tokens, or sensitive personal data into a Proof doc without that approval, and never silently swap a repo-tracked project doc for a Proof link.

Both credentials live in shell variables or session memory only, never in repo-tracked files, commits, or durable logs. `accessToken` is the everyday bearer; `ownerSecret` is owner-only, required for owner delete while unclaimed, and never appears in user-facing copy. Capture `slug`, `accessToken`, and `ownerSecret` immediately at creation and persist the two credentials for the session separately. Hand humans the tokenized `tokenUrl`, never a bare `/d/<slug>`.

Prefer typed `proof_*` MCP tools when the harness already offers them; otherwise use the HTTP recipes below. In MCP mode the server injects `by`, `X-Agent-Id`, and presence identity. For docs the signer does not own, pass `?token=` as `shareToken` for edits and presence.

## Announce yourself for the session

Presence is an outward network write, so it waits for the same gate as every other operation: bind it only after the user explicitly invoked presence, and skip it for read-only `read` and `review` jobs, which run unannounced. When presence is invoked, bind it with the CE identity defaults:

```bash
TOKEN="xxx"; SLUG="abc123"; AGENT="ai:compound-engineering"
curl -sS -X POST "https://www.proofeditor.ai/api/agent/$SLUG/presence" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Agent-Id: $AGENT" \
  -d '{"name":"Compound Engineering","status":"reading","summary":"Reviewing doc"}'
```

## Publish the file's own bytes

Publish only markdown, and only the bytes of the named local file: read the file in full, encode with `jq --rawfile` so newlines, quotes, and backticks survive, and never hand-write or placeholder the body. When the source is an HTML unified plan, do not upload; return the local browser or open path instead, and label a unified plan title by readiness when known.

```bash
SRC="path/to/plan.md"; TITLE="Plan: Foo"
RESPONSE=$(jq -n --arg title "$TITLE" --rawfile md "$SRC" '{title:$title, markdown:$md}' \
  | curl -sS -X POST https://www.proofeditor.ai/share/markdown \
    -H "Content-Type: application/json" -d @-)
URL=$(printf '%s' "$RESPONSE" | jq -r '.tokenUrl')
SLUG=$(printf '%s' "$RESPONSE" | jq -r '.slug')
TOKEN=$(printf '%s' "$RESPONSE" | jq -r '.accessToken')
OWNER_SECRET=$(printf '%s' "$RESPONSE" | jq -r '.ownerSecret')
```

Keep `OWNER_SECRET` in session memory only. After a planning-handoff publish, surface the URL and return control; do not auto-delete review docs.

## Read and review from the live document

`GET /api/agent/<slug>/v3/document` is the source of truth. Its `comments[]` and `suggestions[]` are the review state: reply, resolve, unresolve, accept, reject, or modify by id. There is no delete-comment operation. An `orphaned: true` thread stays readable and replyable, but its old quote is not a live anchor.

```bash
DOC=$(curl -sS "https://www.proofeditor.ai/api/agent/$SLUG/v3/document" \
  -H "Authorization: Bearer $TOKEN" -H "X-Agent-Id: $AGENT")
```

When `mutationReady` is false and `revision` is null, omit `baseRevision` and re-read shortly.

## Edit with the smallest touch that works

Send `{by, baseRevision?, operations[]}` to `POST /api/agent/<slug>/v3/edit`. Targets are visible text, never raw markdown syntax or block refs. Content operations are `replace` (`find`, `with`, optional `occurrence`/`before`/`after`), `insert` (`markdown`, `after` or `before`), `delete` (`find`), and `set_document` (`markdown`, max 2 MiB). Review operations are `comment` (`on`, `body`, optional `occurrence`), `reply` (`comment` id, `body`, optional `resolve`), `resolve` and `unresolve` (`comment` id), `suggest` (`kind: "insert"|"delete"|"replace"`, `find`, `with`), `accept` and `reject` (`suggestion` id), and `modify_suggestion` (`suggestion` id, `with`). Prefer `replace`, `insert`, or `delete` for prose and `suggest` for visible tracked changes; reserve `set_document` for an explicitly requested whole-doc replacement or a change no narrow operation can express. At most 100 operations per request.

```bash
curl -sS -X POST "https://www.proofeditor.ai/api/agent/$SLUG/v3/edit" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Agent-Id: $AGENT" \
  -H "Idempotency-Key: $(uuidgen)" \
  -d '{"by":"ai:compound-engineering","operations":[{"op":"replace","find":"old visible text","with":"new text"}]}'
```

On `TARGET_AMBIGUOUS`, disambiguate with `occurrence`, `before`, or `after` from `error.candidates`; never silently take the first match. On `retryable: false` fix the request; on `retryable: true` with `error.current`, re-resolve and retry once. On `202`, `PENDING`, or `ok: false` with `partial: true`, re-read before chaining anything and retry only the failed operation with the same `Idempotency-Key`. After one fresh read plus one safe retry, report the bug per the service bridge (`POST https://www.proofeditor.ai/api/bridge/report_bug` with `by`, optional `slug`, and `error` object) rather than looping. A mutation counts as done when it returns `ok: true`, or, on `202` or `partial: true`, when a re-read of `v3/document` confirms it.

## Pull the live text home

Read through the canonical endpoint and land the file with an atomic rename; `jq -jr` preserves trailing newlines without shell interpolation:

```bash
SLUG=<slug>; TOKEN=<accessToken>; LOCAL=<absolute-path>
STATE_TMP=$(mktemp "${TMPDIR:-/tmp}/ce-proof-state.XXXXXX")
curl -sS "https://www.proofeditor.ai/api/agent/$SLUG/v3/document" \
  -H "Authorization: Bearer $TOKEN" -H "X-Agent-Id: $AGENT" > "$STATE_TMP"
TMP="${LOCAL}.proof-sync.$$"
jq -jr '.markdown' "$STATE_TMP" > "$TMP" && mv "$TMP" "$LOCAL"
rm -f "$STATE_TMP"
```

A pull overwrites the named local file. Confirm the path first when the pull is a side effect rather than the request; a silent overwrite is a defect. This pass creates no scratch files beyond the sync temps above and installs or commits nothing.

## Titles and deletion

Set the title only when asked. Delete only when the user asks or when finishing an explicitly ephemeral scratch doc. Deletion needs `ownerSecret` while unclaimed, or the owner session after claim; viewer, commenter, and editor tokens cannot delete. Two responses mean the secret was revoked (`403 DOCUMENT_DELETE_FORBIDDEN/CREDENTIAL_NOT_OWNER`, or `401` on the creation secret): stop using it rather than retrying. `DOCUMENT_HAS_NO_OWNER` means only the original secret can delete. Emptying the markdown does not scrub comment marks; a content wipe is not a privacy cleanup.

```bash
curl -sS -X PUT "https://www.proofeditor.ai/api/documents/$SLUG/title" \
  -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" \
  -d '{"title":"Updated title"}'
curl -sS -X DELETE "https://www.proofeditor.ai/api/documents/$SLUG" \
  -H "Authorization: Bearer $OWNER_SECRET"
```

## Stop instead of guessing

Stop, report the exact code and slug, and leave the doc and local files unchanged on an ambiguous target, a failed mutation after one safe retry, a revoked owner secret, or missing credentials. Refuse a request to place secrets or sensitive data without explicit approval and name the approval it needs. Refuse an empty-markdown wipe asked for as privacy cleanup and offer owner delete instead. Stop before overwriting on a side-effect pull with no confirmed path, and do not upload an HTML unified-plan source.

For normative documents under edit, every requirement keeps its subject, modality, condition, exception, ordering, and consequence. Keep identifiers, numbers and bounds, error codes, references, citations, backtick tokens, uppercase states, anchors, tables, and code exact unless the user explicitly asked to change them. A sentence split may repeat a modal but must never detach it from the clause it governs.

## What you hand back

The tokenized URL or the pulled local path, the confirmed revision or `ok` state, and a short summary of what changed. Review docs linger; deletion happens only on explicit cleanup.
