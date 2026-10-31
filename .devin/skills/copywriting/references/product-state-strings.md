# Product-state strings

Read this in page mode for error, empty, success, loading, and permission strings, for action labels, and before using the `[STATE-COPY]` flag. When you flag a string, name the rule id it breaks. Persuasion frameworks do not apply to these strings; tone still follows the reader-state table in the main skill file.

## Rules

| Rule id | Applies to | Rule |
|---|---|---|
| `rule/destructive-names-action` | Destructive CTAs | Verb plus noun naming the exact object: "Delete project" |
| `rule/no-confirm-ok-labels` | Consequential actions | Never label them Confirm, OK, Yes, or a bare verb |
| `rule/canonical-verb` | All actions | One verb per operation, used consistently, chosen for its consequence (see below) |
| `rule/error-states-recovery` | Errors | Say what happened, why when known, and the recovery action. Never show a raw exception or a bare "Something went wrong". Keep field-level and surface-level errors separate, and preserve everything the user typed |
| `rule/success-state-specific` | Success | Confirm in the past tense what happened to which object, in proportion to the action |
| `rule/empty-state-action` | Empty states | Name the object and offer the first action, with no dead ends (see the three types below) |
| `rule/loading-state-specific` | Loading | Say what is loading and, for long operations, roughly how long. Keep the label of the control that triggered it stable |
| `rule/permission-benefit-first` | Permission requests | State the user benefit before the ask, and ask in context when the feature is first used |
| `rule/reads-without-seeing` | All strings | The copy works when heard. Field errors read sensibly after their label. Link and button text names the destination or action. No directional words such as "above", "below", or "here" |

## Canonical verbs

| Verb | Consequence |
|---|---|
| Delete | Permanent |
| Remove | Detaches without destroying |
| Archive | Hides, reversibly |
| Discard | Drops unsaved edits |
| Cancel | Abandons an action in progress |

## Empty-state types

| Type | What the string does |
|---|---|
| Never had any | Guides the first step |
| Filtered to zero | Offers to clear the filter |
| User cleared | Confirms completion. This is the one empty state that needs no CTA |

## Length budgets

Size for the tightest surface first, and leave 30 to 40 percent headroom for translation.

| Surface | Budget |
|---|---|
| Button or CTA | 2 to 4 words |
| Title | 3 to 6 words |
| Error message | 12 to 18 words, including the recovery step |
| Any sentence the user must act on | 14 words at most; 8 or fewer reads at full comprehension |
