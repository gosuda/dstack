# Review output template

Use this skeleton for deep-mode review output. Copy the section structure. The example shows one good rendering, not the only permitted layout. Shape each finding for the reader's next action. Group findings by severity, not by persona.

## Example

```markdown
## Code Review Results

**Scope:** merge-base with the review base branch -> working tree (14 files, 342 lines)
**Intent:** Add order export endpoint with CSV and JSON format support
**Mode:** deep

**Personas:** correctness, testing, maintainability, security, api-contract
- security -- new public endpoint accepts user-provided format parameter
- api-contract -- new /api/orders/export route with response schema

### P0 -- Critical

| # | File | Issue | Persona | Confidence |
|---|------|-------|---------|------------|
| 1 | `orders_controller.rb:42` | User-supplied ID in lookup, no ownership check | security | high |

- **#1** -- `find(params[:id])` on the export path has no `where(account: current_account)` scope, so any authenticated user can export another account's orders. Scope the lookup to the current account.

### P1 -- High

| # | File | Issue | Persona | Confidence |
|---|------|-------|---------|------------|
| 2 | `export_service.rb:87` | Loads all orders into memory -- unbounded | performance | high |

- **#2** -- `Order.where(...).to_a` materializes the full result set; a large account OOMs the worker. Stream with `find_each` or paginate.

### P2 -- Moderate

| # | File | Issue | Persona | Confidence |
|---|------|-------|---------|------------|
| 3 | `export_service.rb:45` | No error handling for CSV serialization failure | correctness | med |

### P3 -- Low

| # | File | Issue | Persona | Confidence |
|---|------|-------|---------|------------|
| 4 | `export_helper.rb:12` | Format detection could use an early return | maintainability | med |

### Actionable Findings

| # | File | Issue | Route | Notes |
|---|------|-------|-------|-------|
| 1 | `orders_controller.rb:42` | Ownership check missing on export lookup | `gated -> audit-project` | `suggested-route` present -- caller decides whether to apply |
| 2 | `export_service.rb:87` | Unbounded memory on export | `safe -> apply` | Mechanical: add `find_each` |

### Pre-existing Issues

| # | File | Issue | Persona |
|---|------|-------|---------|
| 1 | `orders_controller.rb:12` | Broad rescue masking failed permission check | correctness |

### Coverage

- Suppressed: 2 findings below the confidence gate
- Residual risks: No rate limiting on export endpoint
- Testing gaps: No test for concurrent export requests

---

> **Verdict:** Ready with fixes
>
> **Reasoning:** 1 critical auth bypass must be fixed. The memory issue (P1) should be addressed for production safety.
>
> **Fix order:** P0 auth bypass -> P1 memory -> P2 error handling if straightforward
```

## Rules that shape the report

- ASCII-safe only. Never use box-drawing characters or per-item horizontal-rule separators between entries. Never use Unicode arrows or middot. Use `->` for arrows and `--` for dashes. Do not paste file contents or re-print the diff. Cite `file:line`.
- Escape literal `|` in table cells. Any `|` inside a finding title, issue description, code snippet, or example must be written as `\|` so column boundaries come only from unescaped pipes.
- Severity-grouped sections: `### P0 -- Critical`, `### P1 -- High`, `### P2 -- Moderate`, `### P3 -- Low`. Omit empty severity levels.
- Stable sequential finding numbers. Assign finding numbers once after sorting, continue them across severity sections, and reuse those same numbers when findings reappear in Actionable Findings.
- Always include a `file:line` location for code review issues.
- Persona column shows which persona or personas flagged the issue. Multiple personas means cross-persona agreement.
- Confidence column shows `high`, `med`, or `low`.
- No Route column in per-severity tables. The route appears only in the Actionable Findings table.
- Detail line per finding, as needed. Keep the scannable table line short. Put why it matters plus the needed response in a per-finding detail line keyed by stable `#`: `- **#N** -- <why it matters + what response it needs>`.
- Actionable Findings section: include it when the actionable queue is non-empty. It always precedes Pre-existing and Coverage.
- Pre-existing section: separate table with no confidence column.
- Coverage section: suppressed count, residual risks, testing gaps.
- Verdict blockquote is always last and self-sufficient. It holds verdict, reasoning, and fix order. Use blockquotes for all three.
- Horizontal rule (`---`) separates findings from verdict.
- `###` headers for each section.
