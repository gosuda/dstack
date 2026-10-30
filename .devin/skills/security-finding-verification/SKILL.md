---
name: security-finding-verification
description: 'Use when a named security allegation needs a true-positive or false-positive verdict. Not for discovering bugs: use security-review. Not for adding controls.'
---

# Security finding verification

You test one named allegation and return a verdict with evidence. Each supplied finding gets an independent trace, tested or proved at the right depth and challenged before you label it. This skill produces chat output only and makes no file mutation, so rollback does not apply. No remote mutation.

This skill does not discover new vulnerabilities in a change set (use security review) and does not add security controls during construction.

## What to take in

* Required: the finding claim (vulnerability type, affected component, and any asset or call site description) and the relevant source code or artifact under evaluation.
* Optional: the existing threat model for the affected component, plus any prior triage notes or external report context.

## Restate the finding

Summarize the alleged vulnerability: type, affected component, and attacker position from the supplied claim. State whether the finding sits in scope.

## Build the threat model

Record attacker position, required capabilities, and the complete attack path from entry point to asset.

## Trace the data flow

Locate the source entry, list each intermediate step, find the sink, and confirm each step by reading the code. Mark any step you cannot confirm as `unresolved`. A verdict waits on unresolved steps.

## Run class specific checks

Apply the OWASP Top 10 and relevant CWE checks for the alleged class. Record pass or fail for each check. Compare the observation with known false positive shapes for that class, and record the exact shape and whether it applies.

Class checks by vulnerability type:

* Injection (SQL, command, XSS, LDAP, XML, Xpath, SMTP header, OS command): confirm unsanitized user controlled input reaches a sensitive sink without context appropriate escaping or validation.
* Path traversal: confirm user controlled input reaches a filesystem operation without path sanitization or canonicalization.
* Authentication or authorization bypass: confirm a protection mechanism is absent or bypassed at the named call site.
* Sensitive data exposure: confirm secrets, keys, tokens, or credentials appear in plaintext in source code, logs, or network payloads.
* Cryptographic failure: confirm weak, broken, or misused crypto primitives at the named call site.
* Insecure design: confirm a missing architectural guard such as rate limiting, CSRF tokens, or session invalidation.
* Security misconfiguration: confirm a default, outdated, or permissive configuration at the named component.
* Integrity failure: confirm code or data is used without a cryptographic integrity check.
* Logging and monitoring failure: confirm an attack sequence reaches the named step without triggering an observable log event.
* Any other class: define the relevant check explicitly before running it.

## Assess exploitability

Decide three things: (a) the finding is reachable from the named attacker position, (b) it suffices to cause harm under the threat model, (c) it reproduces in the available environment. When all three hold and a demonstration is safe, construct a proof of concept. When demonstration is unsafe or reproduction fails, give structured reasoning instead of a live exploit.

## Hold the gates

At each step, check that the evidence supports the next step. Stop at the first gate that fails and report the specific gap. Never proceed past a gate on an unverified assumption.

## Issue the verdict

For each finding state `true positive` when the data flow is confirmed, class checks fail as described, and exploitability is established. State `false positive` when the data flow is broken, the pattern matches a known false positive shape, the class checks pass, or exploitability cannot be established on sufficient evidence. Include the full trace, threat model, check results, and the adversarial challenge with its response. A true positive also carries severity, exploitability rating, and recommended remediation.

## When evidence runs short

* Claim too thin: stop and return `inconclusive` with the specific missing element.
* Source code missing: stop and return `inconclusive, source code not available` for the affected component.
* Data flow step unconfirmed: mark it `unresolved` and return `inconclusive, unresolved data flow step`. The verdict waits.
* Class mismatch: return `out of scope, vulnerability class does not match the supplied finding`.
* Gate failure: stop, name the gate, and report the specific gap.
* Partial results: when several findings arrive together and some cannot resolve, issue verdicts only for findings with complete evidence and name the inconclusive ones explicitly.

## What you hand back

A structured verdict in chat for each finding: classification (`true positive` or `false positive`), the complete source to sink trace, class specific check results, threat model, exploitability assessment and proof of concept when built, adversarial challenge with response, and for true positives the severity, exploitability rating, and remediation steps.
