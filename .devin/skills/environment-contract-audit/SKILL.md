---
name: environment-contract-audit
description: 'Use when environment-dependent code, templates, or deployment configuration changes, or when runtime configuration is missing. Produces a bidirectionally reconciled environment-variable contract.'
---

# Environment contract audit

When code, templates, or deployment configuration depends on environment variables, something has to check both directions: everything the code consumes must actually be supplied somewhere, everything supplied must actually be consumed, and each variable must sit at the right required/optional and public/secret scope. That check is this audit. Reach for it whenever environment-dependent code, templates, or deployment configuration changes, or when runtime configuration is missing at startup.
## The two sides you need

You cannot reconcile with only one side in hand. Gather both before you start:

- The declared surfaces: the code, templates, runtime config files, and deployment config under audit, named by the user or inferred from the change diff.
- The supply sources: env files, CI secret definitions, deployment manifests, and anywhere else variable values come from.

## Working through the variables

1. Walk the declared surfaces and list every environment variable referenced. Mark each one required or optional, and public or secret. You are finished with this pass when the full inventory exists with both scope annotations on every entry.
2. For each variable, check the supply side (env files, CI secrets, deployment config) against the consumption side (code reads, template interpolations). Flag three kinds of mismatch: consumed but not supplied, supplied but not consumed, and scope mismatches where a secret is consumed where a public value is expected or vice versa. This pass is done when every variable has both a supply-side and a consumption-side status recorded.
3. Decide the fix for each mismatch: add the missing supply, remove the dead reference, correct the scope, or document the intentional override. This pass is done when every mismatch has a named resolution.
4. Write up the reconciled contract: a table with each variable's name, required/optional scope, public/secret scope, supply source, consumption sites, and resolution status. You are done when the table is complete and every variable is accounted for.

One permission rule governs step 3: touching a production secret, credential, or remote configuration needs one human-gated ask or question call first. Without that explicit approval you stay read-only. No file, VCS, credential, paid, published, deployed, or remote mutation is allowed. Prose consent, invocation consent, consent from a prior run, and discoveries made after starting do not count as approval.

## When to stop instead

- You cannot tell where a variable is supplied or consumed from the declared surfaces. Stop and report the exact blocker rather than guessing a resolution.
- Fixing a mismatch would put a secret or credential into a public scope or another place that leaks it. Stop before the exposure, and report the risk together with the correct secret scope.

Your boundary is the declared code, templates, runtime config, and deployment-config surfaces; do not wander past them looking for extra variables to reconcile.

## What you hand back

A bidirectionally reconciled environment-variable contract: the table of every referenced variable with its scopes, supply source, consumption sites, and resolution status. Close with exactly one reading of the situation: `reconciled` when every variable is supplied and documented at the correct scope, `partial` when some mismatches remain but each has a named resolution, `blocked` when an exact blocker prevented reconciliation, or `unsafe-exposure` when a secret would have been exposed and you stopped before mutating anything.
