# Canonical learning-record contract: `odin-learning/v1`

Sole authored owner. `autolearn` carries a generator-owned byte-identical copy of this file and never edits record fields independently. The bundled `scripts/validate-record.py` implements this contract and fails closed on anything it cannot parse.

Every canonical record is Markdown with YAML frontmatter between exact `---` lines (UTF-8, no BOM). JSON frontmatter is rejected. The validator proves parser safety and field validity; it does not prove that a learning was worth recording.

## Common fields

Every canonical record requires:

```yaml
schema: odin-learning/v1
record_kind: rationale
date: 2026-10-01
```

`schema` is always the exact literal `odin-learning/v1`. `record_kind` selects the branch. `date` is required for both branches and must already be a valid ISO `YYYY-MM-DD` calendar date. `schema` version, accepted fields, and enums are fixed by the machine contract below and never extended by prose.

Direct captures use the capture-run date. Migrations preserve the legacy source date and never substitute the current date, filesystem mtime, commit date, or session timestamp. A missing or invalid source date leaves that source `unmigrated`. `date`, `source`, and `origin_records` are provenance metadata recording where and when the invariant was observed; they never fabricate a timeless claim and never substitute for enforcement.

## Rationale branch

`record_kind: rationale` and its `type` values (`pattern`, `caveat`, `reference`, `decision`, `concept`, `fix`, `lesson`, `workaround`, `incident`, `constraint`) are serialization categories, not permission for narrative junk. They never authorize temporal decision diaries, what-we-learned-today notes, activity logs, or abandoned-attempt stories. Admission is governed by the owning skill invariant gate; the validator proves parser safety and field validity, never that a learning was worth recording. `record_kind: rationale` preserves a reusable scope-qualified invariant captured by `compound`.

Required:

```yaml
schema: odin-learning/v1
record_kind: rationale
date: 2026-10-01
type: caveat
confidence: high
source: session context 2026-10-29
```

| Field | Type | Rule |
|---|---|---|
| `type` | enum | `pattern`, `caveat`, `reference`, `decision`, `concept`, `fix`, `lesson`, `workaround`, `incident`, `constraint` |
| `confidence` | enum | `high`, `medium`, `low`: author certainty stated by the source |
| `source` | string | Non-empty origin: session context, PR, issue, or codebase area |
| `tags` | array | Optional; if present, 1-8, lowercase hyphen-separated: `^[a-z0-9]+(-[a-z0-9]+)*$` |
| `status` | enum | Optional: `active`, `stale`, `superseded` |
| `evidence` | enum | Optional, separate from `confidence`: `observed`, `corroborated`, `single-source`, `unknown` |
| `retire_when` | string | Optional, non-empty condition under which the record should be revisited |
| `last_updated` | date | Optional ISO date of a later in-place update |
| `origin_records` | list | Required for migrated records, omitted for direct captures (see Provenance) |

Legacy mapping is exact:

| Legacy value | Canonical `type` |
|---|---|
| `pattern` | `pattern` |
| `caveat` | `caveat` |
| `reference` | `reference` |
| `decision` | `decision` |
| `concept` | `concept` |
| `fix` | `fix` |
| `lesson` | `lesson` |

An unsupported legacy `type` leaves the source `unmigrated`. It is never silently mapped to a neighboring type. `type: caveat` is first-class and never converted into another type.

A rationale record must not require or emit solution-branch fields (`title`, `category`, `module`, `problem_type`, `component`, `severity`, `symptoms`, `root_cause`, `resolution_type`, `applies_when`). Legacy frontmatter `Context`/`Implication` move into body sections; they are not canonical frontmatter fields.

Rationale body sections, only as applicable to the admitted invariant (delete the rest, never add diary or narrative sections):

```markdown
## Scope
## Enforcement
## Counterexample
```

The `#` title states the invariant; the body carries scope, enforcement, and counterexample only. An honestly-unobserved counterexample shape stays in the body as `unknown:` or `undefined:`; those markers never appear as YAML field values and never stand in for missing enforcement.

## Solution branch

`record_kind: solution` is a serialization category for bug or knowledge solutions captured by `autolearn`, not permission for narrative junk: it never authorizes incident retellings, trivia, or session history as records. Admission is governed by the owning skill gate; the validator proves parser safety and field validity, never that a solution was worth recording.

Required:

```yaml
schema: odin-learning/v1
record_kind: solution
date: 2026-10-01
title: Clear problem or topic title
category: build-errors
module: build
problem_type: build_error
component: build-graph
severity: high
```

| Field | Type | Rule |
|---|---|---|
| `title` | string | Non-empty problem or topic title |
| `category` | enum | Directory basename matching the `problem_type` row in the category map |
| `module` | string | Non-empty module or area |
| `problem_type` | enum | One of the track table below; determines the track |
| `component` | string | Non-empty component or subsystem; keep consistent within a repo |
| `severity` | enum | `critical`, `high`, `medium`, `low` |
| `symptoms` | array | Bug track required, 1-5 non-empty items; knowledge track optional; if present, 1-5 non-empty items |
| `root_cause` | enum | Bug track required; knowledge track optional when a specific cause is known |
| `resolution_type` | enum | Bug track required; knowledge track optional when a change was applied |
| `applies_when` | array | Optional; if present, 1-5 non-empty conditions |
| `tags` | array | Optional; if present, 1-8, same hyphen rule as rationale |
| `related_components` | array | Optional, non-empty items |
| `status` | enum | Optional: `active`, `stale` |
| `stale_reason` | string | Required when marking `status: stale` without a successor |
| `stale_date` | date | Required alongside `stale_reason` |
| `last_updated` | date | Optional ISO date of an in-place update |
| `supersedes` | string | Optional prior path replaced by this successor |
| `evidence` | enum | Optional: `observed`, `corroborated`, `single-source`, `unknown` |
| `origin_records` | list | Required for migrated records, omitted for direct captures |

Track table (`problem_type` decides the track; `best_practice` is the knowledge fallback):

| Track | `problem_type` values |
|---|---|
| Bug | `build_error`, `test_failure`, `runtime_error`, `performance_issue`, `database_issue`, `security_issue`, `ui_bug`, `integration_issue`, `logic_error` |
| Knowledge | `best_practice`, `documentation_gap`, `workflow_issue`, `developer_experience`, `architecture_pattern`, `design_pattern`, `tooling_decision`, `convention` |

`root_cause` enum: `missing_association`, `missing_include`, `missing_index`, `wrong_api`, `scope_issue`, `thread_violation`, `async_timing`, `memory_leak`, `config_error`, `logic_error`, `test_isolation`, `missing_validation`, `missing_permission`, `missing_workflow_step`, `inadequate_documentation`, `missing_tooling`, `incomplete_setup`.

`resolution_type` enum: `code_fix`, `migration`, `config_change`, `test_fix`, `dependency_update`, `environment_setup`, `workflow_improvement`, `documentation_update`, `tooling_addition`, `seed_data_update`.

Category map (`problem_type` to `docs/solutions/` directory basename):

| `problem_type` | `category` |
|---|---|
| `build_error` | `build-errors` |
| `test_failure` | `test-failures` |
| `runtime_error` | `runtime-errors` |
| `performance_issue` | `performance-issues` |
| `database_issue` | `database-issues` |
| `security_issue` | `security-issues` |
| `ui_bug` | `ui-bugs` |
| `integration_issue` | `integration-issues` |
| `logic_error` | `logic-errors` |
| `best_practice` | `best-practices` |
| `documentation_gap` | `documentation-gaps` |
| `workflow_issue` | `workflow-issues` |
| `developer_experience` | `developer-experience` |
| `architecture_pattern` | `architecture-patterns` |
| `design_pattern` | `design-patterns` |
| `tooling_decision` | `tooling-decisions` |
| `convention` | `conventions` |

A solution record must not contain rationale-only `type` or `confidence`. The validator rejects both on solution records, and migration never carries them over. Pre-existing knowledge-track docs carrying bug-track fields are harmless; leave them unless rewriting the doc for other reasons.

Solution body uses the track sections from the owning solution skill's `assets/solution-template.md` (`autolearn`; `compound` writes rationale records only and never emits a solution body) (bug: Problem, Symptoms, What Did Not Work, Solution, Why This Works, Prevention; knowledge: Context, Guidance, Why This Matters, When To Apply, Examples). Delete sections with no real content instead of leaving placeholders.

## Origin records

Every migrated record contains a non-empty ordered list:

```yaml
origin_records:
  - path: docs/solutions/old-slug.md
    sha256: 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
    migration_origin: legacy-compound-v0
    historical: true
```

Each item requires all four keys: `path` (pre-cutover source locator, non-empty), `sha256` (lowercase hex digest of the original UTF-8 bytes before any parse, `^[0-9a-f]{64}$`), `migration_origin` (one of `legacy-compound-v0`, `legacy-autolearn-v0`, `legacy-keep-why-v0`, `canonical-rationale-v1`, `canonical-solution-v1`), `historical: true` (boolean, never the string `"true"`). `historical: true` marks a preserved pre-cutover locator; a later clean cutover may remove that old path without invalidating the digest.

Rules: read original bytes first; never fabricate an origin for a direct capture; carry the union forward when a migrated record is replaced; deduplicate only identical `(path, sha256, migration_origin, historical)` tuples. A destination missing any input tuple is `unmigrated: provenance merge incomplete`.

## Legacy detection and mapping

- `legacy-compound-v0`: no `schema` marker plus compound fields. Convert to rationale. A record without `source` or without a valid date is `unmigrated`.
- `legacy-autolearn-v0`: no `schema` marker plus solution fields (`title`, `category`, `module`, `problem_type`, `component`, `severity`). Convert to solution. A record without a valid date is `unmigrated`.
- `legacy-keep-why-v0`: only when explicitly scoped. Rationale fields plus valid date and source convert to rationale; complete solution metadata converts to solution. An ambiguous, undated, source-less, or confidence-less rationale entry stays `unmigrated` unless the operator supplies an explicit per-file mapping.
- Unrecognized unmarked files are `unmigrated` and left unchanged.
- An explicit operator mapping for missing fields is a one-time migration input, never a durable store; it must supply every missing required field and is shown before writing.

Cross-branch conversion (rationale to solution or the reverse) is blocked by default. It proceeds only with `consent:cross-branch` plus a complete lossless field and body mapping that places every source field, provenance object, section, and verification claim. Without both, both inputs stay unchanged.

## Machine contract

The validator reads the YAML block below. Human prose above and this block must stay in sync; a record valid under one and invalid under the other is a schema defect, not a record defect.

```yaml
# machine-contract odin-learning/v1
schema_value: odin-learning/v1
record_kinds:
  - rationale
  - solution
rationale_required:
  - schema
  - record_kind
  - date
  - type
  - confidence
  - source
rationale_optional:
  - tags
  - status
  - evidence
  - retire_when
  - last_updated
  - origin_records
rationale_type_enum:
  - pattern
  - caveat
  - reference
  - decision
  - concept
  - fix
  - lesson
  - workaround
  - incident
  - constraint
rationale_confidence_enum:
  - high
  - medium
  - low
rationale_status_enum:
  - active
  - stale
  - superseded
rationale_evidence_enum:
  - observed
  - corroborated
  - single-source
  - unknown
solution_required:
  - schema
  - record_kind
  - date
  - title
  - category
  - module
  - problem_type
  - component
  - severity
solution_optional:
  - symptoms
  - root_cause
  - resolution_type
  - applies_when
  - tags
  - related_components
  - status
  - stale_reason
  - stale_date
  - last_updated
  - supersedes
  - evidence
  - origin_records
problem_type_enum:
  - build_error
  - test_failure
  - runtime_error
  - performance_issue
  - database_issue
  - security_issue
  - ui_bug
  - integration_issue
  - logic_error
  - best_practice
  - documentation_gap
  - workflow_issue
  - developer_experience
  - architecture_pattern
  - design_pattern
  - tooling_decision
  - convention
bug_track:
  - build_error
  - test_failure
  - runtime_error
  - performance_issue
  - database_issue
  - security_issue
  - ui_bug
  - integration_issue
  - logic_error
root_cause_enum:
  - missing_association
  - missing_include
  - missing_index
  - wrong_api
  - scope_issue
  - thread_violation
  - async_timing
  - memory_leak
  - config_error
  - logic_error
  - test_isolation
  - missing_validation
  - missing_permission
  - missing_workflow_step
  - inadequate_documentation
  - missing_tooling
  - incomplete_setup
resolution_type_enum:
  - code_fix
  - migration
  - config_change
  - test_fix
  - dependency_update
  - environment_setup
  - workflow_improvement
  - documentation_update
  - tooling_addition
  - seed_data_update
severity_enum:
  - critical
  - high
  - medium
  - low
category_enum:
  - build-errors
  - test-failures
  - runtime-errors
  - performance-issues
  - database-issues
  - security-issues
  - ui-bugs
  - integration-issues
  - logic-errors
  - best-practices
  - documentation-gaps
  - workflow-issues
  - developer-experience
  - architecture-patterns
  - design-patterns
  - tooling-decisions
  - conventions
solution_status_enum:
  - active
  - stale
solution_evidence_enum:
  - observed
  - corroborated
  - single-source
  - unknown
migration_origin_enum:
  - legacy-compound-v0
  - legacy-autolearn-v0
  - legacy-keep-why-v0
  - canonical-rationale-v1
  - canonical-solution-v1
origin_required:
  - path
  - sha256
  - migration_origin
  - historical
category_map:
  - build_error=build-errors
  - test_failure=test-failures
  - runtime_error=runtime-errors
  - performance_issue=performance-issues
  - database_issue=database-issues
  - security_issue=security-issues
  - ui_bug=ui-bugs
  - integration_issue=integration-issues
  - logic_error=logic-errors
  - best_practice=best-practices
  - documentation_gap=documentation-gaps
  - workflow_issue=workflow-issues
  - developer_experience=developer-experience
  - architecture_pattern=architecture-patterns
  - design_pattern=design-patterns
  - tooling_decision=tooling-decisions
  - convention=conventions
```

## Parser validation

Every canonical write, update, replacement, consolidation, or migration destination must pass. From the owning skill directory, pass the record by absolute path (a repository-relative `docs/...` path resolves only from the repository root, not from the skill directory):

```bash
python3 scripts/validate-record.py /path/to/repo/docs/solutions/<area>/<slug>.md
```

Exit 0 is parser-safe and schema-valid. Exit 1 names the failing field. Exit 2 is a usage or schema-load error. A non-zero exit blocks the write.
