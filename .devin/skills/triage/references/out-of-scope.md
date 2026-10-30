# Out-of-scope knowledge base

The `.out-of-scope/` directory in a repository stores persistent records of rejected feature requests for two purposes: institutional memory (why a feature was rejected, so the reasoning survives the closed issue) and deduplication (a new request matching a prior rejection surfaces the previous decision instead of relitigating it).

## Directory structure

```text
.out-of-scope/
├── dark-mode.md
├── plugin-system.md
└── graphql-api.md
```

One file per concept, never per issue. Multiple issues requesting the same thing group under one file.

## File format

Each file carries a `# Concept Name` heading, a `Decision:` line, a `Reason:` line, and a `Prior requests:` list with issue links, written as a short design note with paragraphs, code samples, or examples so a newcomer understands the reasoning on first read.

```markdown
# Dark Mode

Decision: Declined, this project does not support user-facing theming.

Reason: The rendering pipeline assumes a single palette resolved at build time.
Supporting runtime themes would require a context provider wrapping the
whole tree plus per-component resolution and a persistence layer, which
does not align with this project focus on content authoring.

## Prior requests

- #42: "Add dark mode support"
- #87: "Night theme"
```

Name the file with a short kebab-case concept name recognizable without opening it. Write substantive reasons (project scope, technical constraints, strategic choices with references). Never record temporary circumstances; a deferral is never a rejection.

## Checking during triage

During context gathering, read all files in `.out-of-scope/` and match by concept similarity, never by keyword. On a match, surface it to the maintainer with the reason and ask whether they confirm, reconsider, or disagree. On confirm, append the new issue to `Prior requests` and close. On reconsider, delete or update the concept file and triage normally. On disagree, triage normally as a distinct request.

## Writing during triage

Write only when an enhancement is rejected as `wontfix`. Rejected pull requests follow the same rule as issues. Never write here for already-implemented `wontfix`; a built feature is never a rejection, and recording it would poison future dedup checks. Flow: maintainer decides, check for a matching concept file, append or create, post the comment linking the file, close with the `wontfix` role.

## Updating or removing

When the maintainer changes their mind about a rejected concept, delete the `.out-of-scope/` file. Old issues stay historical records and are never reopened. The new issue that triggered reconsideration proceeds through normal triage.
