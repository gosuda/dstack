---
name: proof
description: 'Use when asked to publish, read, comment on, suggest to, or pull a Proof collaborative markdown document. Not for proofreading, math proofs, or test evidence.'
---

# Sharing a markdown document through Proof

Work with one collaborative markdown document on the hosted Proof service through its HTTP API from `Bash`. The local file stays canonical; a Proof link is a share, never a second knowledge store. The durable learning bundle stays the YAML `docs/solutions/` records owned by `compound`.

## Provenance

Adapted from `EveryInc/compound-engineering-plugin` pinned `fbd794b329f5b65d0ea00a5e6487336c385ff2be`: `skills/ce-proof/SKILL.md` plus `references/api.md` and `references/workflows.md`. Recipes conform to API v3 as documented at https://www.proofeditor.ai/agent-docs and the pinned reference. Outward mutating writes are never pre-verified with live writes. Identity `ai:compound-engineering` and display name `Compound Engineering` are kept as wire defaults; a caller may pass a distinct sub-agent identity pair when that agent owns the doc. No trademark SVG is reused as branding.

## Pick the operation

Choose the narrowest operation for the request:

- `publish`: one-way, local file to hosted doc.
- `read` and `review`: start from the live document as source of truth.
- `comment`, `suggest`, and `edit`: start from a fresh read and touch as little as possible.
- `pull`: sync the live markdown down to a local file.
- `title`: set the title only when asked.
- `delete`: only to finish an explicitly ephemeral scratch doc or on an explicit user cleanup ask.

This skill owns the share, read, review, edit, and pull plumbing. Durable learning belongs to `compound` and `autolearn`, local doc authoring to `docs-writing`, and PR bodies to their own flow. It publishes source-file bytes and never hand-writes the shared body.

## Approval gates

Every outward write waits for the user's explicit go-ahead for that specific operation: publishing, editing, commenting, suggesting, presence, a title change, a pull that overwrites a file as a side effect, and deletion. Sensitive content needs its own explicit approval: never put secrets, credentials, API keys, private tokens, or sensitive personal data into a Proof doc without it. Never silently swap a repo-tracked project doc for a Proof link.

## Inputs and credentials

Publish and pull need the local markdown path. Anything touching the hosted doc needs the Proof URL with its slug and token.

Creation returns `slug`, `accessToken`, and `ownerSecret`. Capture all three immediately and keep the two credentials separately in shell variables or session memory, never in repo-tracked files, commits, or durable logs.

- `accessToken` is the everyday bearer.
- `ownerSecret` is owner-only, required for owner delete while the doc is unclaimed, and never appears in user-facing copy.

Hand humans the tokenized `tokenUrl`, never a bare `/d/<slug>`.

Prefer typed `proof_*` MCP tools when the harness offers them; otherwise use the HTTP recipes below. In MCP mode the server injects `by`, `X-Agent-Id`, and presence identity. For docs the signer does not own, pass the `?token=` value as `shareToken` for edits and presence.

## Presence

Presence is an outward network write behind the same gate as every other operation. Bind it only after the user explicitly invoked presence, and skip it for `read` and `review` jobs, which run unannounced. Use the CE identity defaults:

```bash
TOKEN="xxx"; SLUG="abc123"; AGENT="ai:compound-engineering"
curl -sS -X POST "https://www.proofeditor.ai/api/agent/$SLUG/presence" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Agent-Id: $AGENT" \
  -d '{"name":"Compound Engineering","status":"reading","summary":"Reviewing doc"}'
```

## Publish

Publish only markdown, and only the bytes of the named local file. Read the file in full and encode it with `jq --rawfile` so newlines, quotes, and backticks survive; never hand-write or placeholder the body. When the source is an HTML unified plan, do not upload it; return the local browser or open path instead, and label a unified plan title by readiness when known.

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

## Read and review

`GET /api/agent/<slug>/v3/document` is the source of truth. Its `comments[]` and `suggestions[]` are the review state: reply, resolve, unresolve, accept, reject, or modify by id. There is no delete-comment operation. An `orphaned: true` thread stays readable and replyable, but its old quote is no longer a live anchor.

```bash
DOC=$(curl -sS "https://www.proofeditor.ai/api/agent/$SLUG/v3/document" \
  -H "Authorization: Bearer $TOKEN" -H "X-Agent-Id: $AGENT")
```

When `mutationReady` is false and `revision` is null, omit `baseRevision` and re-read shortly.

## Edit

Send `{by, baseRevision?, operations[]}` to `POST /api/agent/<slug>/v3/edit`, with at most 100 operations per request. Targets are visible text, never raw markdown syntax or block refs.

| Operation | Fields |
|---|---|
| `replace` | `find`, `with`, optional `occurrence`/`before`/`after` |
| `insert` | `markdown`, `after` or `before` |
| `delete` | `find` |
| `set_document` | `markdown`, max 2 MiB |
| `comment` | `on`, `body`, optional `occurrence` |
| `reply` | `comment` id, `body`, optional `resolve` |
| `resolve`, `unresolve` | `comment` id |
| `suggest` | `kind: "insert"\|"delete"\|"replace"`, `find`, `with` |
| `accept`, `reject` | `suggestion` id |
| `modify_suggestion` | `suggestion` id, `with` |

Prefer `replace`, `insert`, or `delete` for prose and `suggest` for visible tracked changes. Reserve `set_document` for an explicitly requested whole-doc replacement or a change no narrow operation can express.

```bash
curl -sS -X POST "https://www.proofeditor.ai/api/agent/$SLUG/v3/edit" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Agent-Id: $AGENT" \
  -H "Idempotency-Key: $(uuidgen)" \
  -d '{"by":"ai:compound-engineering","operations":[{"op":"replace","find":"old visible text","with":"new text"}]}'
```

Edits to a Proof doc preserve meaning: keep identifiers, numbers, bounds, error codes, references, backtick tokens, anchors, tables, and code exact unless the user asked to change them.

## Errors and retries

- `TARGET_AMBIGUOUS`: disambiguate with `occurrence`, `before`, or `after` from `error.candidates`. Never silently take the first match.
- `retryable: false`: fix the request.
- `retryable: true` with `error.current`: re-resolve and retry once.
- `202`, `PENDING`, or `ok: false` with `partial: true`: re-read before chaining anything, and retry only the failed operation with the same `Idempotency-Key`.

After one fresh read plus one safe retry, stop looping and report the bug through the service bridge: `POST https://www.proofeditor.ai/api/bridge/report_bug` with `by`, optional `slug`, and an `error` object.

A mutation is done when it returns `ok: true`, or, after a `202` or `partial: true`, when a re-read of `v3/document` confirms it.

## Pull

Read through the canonical endpoint and land the file with an atomic rename. `jq -jr` preserves trailing newlines without shell interpolation.

```bash
SLUG=<slug>; TOKEN=<accessToken>; AGENT="ai:compound-engineering"; LOCAL=<absolute-path>
STATE_TMP=$(mktemp "${TMPDIR:-/tmp}/ce-proof-state.XXXXXX")
curl -sS "https://www.proofeditor.ai/api/agent/$SLUG/v3/document" \
  -H "Authorization: Bearer $TOKEN" -H "X-Agent-Id: $AGENT" > "$STATE_TMP"
TMP="${LOCAL}.proof-sync.$$"
jq -jr '.markdown' "$STATE_TMP" > "$TMP" && mv "$TMP" "$LOCAL"
rm -f "$STATE_TMP"
```

A pull overwrites the named local file. When the pull is a side effect rather than the request, confirm the path first; a silent overwrite is a defect. The pull creates no scratch files beyond the sync temps above and installs or commits nothing.

## Title and deletion

Set the title only when asked. Delete only when the user asks or when finishing an explicitly ephemeral scratch doc.

Deletion needs `ownerSecret` while the doc is unclaimed, or the owner session after claim; viewer, commenter, and editor tokens cannot delete. `403 DOCUMENT_DELETE_FORBIDDEN/CREDENTIAL_NOT_OWNER`, or `401` on the creation secret, means the secret was revoked: stop using it rather than retrying. `DOCUMENT_HAS_NO_OWNER` means only the original secret can delete. Emptying the markdown does not scrub comment marks, so a content wipe is not a privacy cleanup.

```bash
curl -sS -X PUT "https://www.proofeditor.ai/api/documents/$SLUG/title" \
  -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" \
  -d '{"title":"Updated title"}'
curl -sS -X DELETE "https://www.proofeditor.ai/api/documents/$SLUG" \
  -H "Authorization: Bearer $OWNER_SECRET"
```

## Stop instead of guessing

Stop, report the exact code and slug, and leave the doc and local files unchanged on an ambiguous target, a failed mutation after one safe retry, a revoked owner secret, or missing credentials.

- A request to place secrets or sensitive data without explicit approval: refuse and name the approval it needs.
- An empty-markdown wipe requested as privacy cleanup: refuse and offer owner delete instead.
- A side-effect pull with no confirmed path: stop before overwriting.
- An HTML unified-plan source: do not upload it.

## Output

The tokenized URL or the pulled local path, the confirmed revision or `ok` state, and a short summary of what changed. Review docs linger; deletion happens only on explicit cleanup.
