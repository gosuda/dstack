---
name: punishing-practices
description: 'Use when a workflow, plan, diff, or completed work cycle must be checked for practices that punish the project later. Not for source, remote, credential, publish, deploy, or irreversible changes.'
---

# Punishing practices

This skill audits one workflow, plan, diff, or completed work cycle for practices that feel productive now and punish the project later. It names each practice with the exact evidence and a cheaper alternative, or reports the artifact clean with the coverage stated. The report goes to chat only and changes nothing.

It is read-only. It never edits code, branches, credentials, or remote state, and it refuses remote, credential, publish, deploy, or irreversible changes outright. No invented failures: if no practice class matches, the artifact is clean.

## What you hand it

The artifact to audit is required, supplied concretely (file path, pasted content, committed diff range, workflow definition, or verbal cycle description). The audit stays bounded to that scope and never widens to unreferenced code or history. Two optional inputs sharpen the judgment: the success metric or budget the artifact is meant to serve (used only to tell score chasing or budget burn apart from real progress), and a scope hint bounding the audit to a subsystem, time window, or decision.

## The five practices it scans

Every audit covers all five classes, collecting the exact evidence line (quote, step number, or configuration value) that proves each match:

| Practice | What it looks like |
|---|---|
| Symptom patching | A change suppresses a signal (warning, error, failing test, metric) without addressing its cause |
| Infinite retries | A loop, hook, or agent step retries without a bounded attempt count, backoff ceiling, or stop condition |
| Weak verification | A check, gate, or test that can pass while the defect it claims to catch is still present (tautological assertion, mocked-out assertion, missing assertion, green-on-broken) |
| Score chasing | Work optimizes a metric or rubric score while the underlying outcome it proxies degrades or stays unknown |
| Budget burn | Spend, tokens, time, or iterations accumulate without a ceiling or a stopping rule tied to the outcome |

## How the report reads

For every match, the report names the practice class, quotes the evidence line, and states one cheaper alternative that reaches the same goal without the punishing effect. Where no cheaper alternative exists, it says so explicitly instead of inventing one. If no class matches, it reports the artifact clean and states the coverage (the five classes scanned and the artifact scope covered). It emits the report as chat output and never edits, stages, commits, or opens issues.

## Where judgment stays honest

A line that matches only by assuming unstated intent is not classified. It is recorded as unconfirmed with the line quoted, and scanning continues; unconfirmed lines are never promoted to named practices. If the artifact cannot be read or is empty, the skill stops and reports that no scan was possible instead of inferring practices from absence. If scanning is interrupted, it emits the practices already confirmed as evidence-backed and marks the rest not scanned, and never reports clean while classes remain unscanned. The audit is a single pass, not an iterative fix loop, so it never retries and needs no rollback.
