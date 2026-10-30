---
name: watch-for-structured
description: 'Use when the user wants to classify a surface state and page an on-call API when triggered. Not for read-only anomaly watching without paging: use watch-for.'
disable-model-invocation: true
---

# Single-snapshot alert

You look once, classify what you see, and page a human when the rules say so. The user names a surface to observe, the severity rules to judge it by, and where each severity level should route. You read the current state a single time, put it into exactly one severity bucket, and when the on-call policy for that level demands a page, you send it through the alerting API and report back with severity, routing, and what the page did.

Looking is read-only. Paging is remote, since it sends through the alerting API to real routing destinations, so it only ever happens on explicit human invocation, and you preview the target and the consequence before any page goes out or any credential is used.

You need five things before starting, all required: the watch surface state (a reachable, named resource, endpoint, log stream, or metric), the severity rules (each level naming the threshold or pattern that triggers it), the routing table (each severity level mapped to its channel, team, person, or endpoint destinations), the on-call policy (escalation chain, acknowledgement timeout, and paging method per level), and the paging API endpoint (the remote alerting or on-call base URL).

## Reading once and deciding whether to page

Work the steps in order. You take one snapshot, never a running watch. For continuous observation without paging, use watch-for instead.

1. Read the current state of the watch surface. You are done with this step when the state is read or the surface is reported unreachable.
2. Compare what you observed against the severity rules and classify it into exactly one severity level. You are done when the observation sits in one level or the classification is reported as ambiguous.
3. Look up the routing targets for that level. If the routing table has no entry for it, stop here and report the classification with a missing-route flag. You are done when targets are identified or missing-route is reported.
4. When the on-call policy requires paging at this level, confirm the paging API endpoint is reachable, build the page carrying severity, surface identity, observation summary, and routing targets, send it, and record the confirmation or the failure. You are done when the page is sent with its outcome recorded, or when this severity needs no page.
5. Assemble the structured report: watch surface, observed state, classified severity, routing targets, on-call disposition, and timestamps. You are done when the report is returned.

## When the snapshot will not cooperate

A surface that cannot be reached means reporting its identity and the error, with no page sent and severity left unclassified. An observation that fits no single level, or fits several, is reported with every candidate level flagged and no page sent, since a human resolves the ambiguity. A classified severity with no routing entry is reported with the missing-route flag and no page sent. A paging API that cannot be reached is reported with classification and routing intact and disposition set to page-failed, while one that rejects the payload is reported with the API error and disposition set to page-rejected. Neither paging failure retries automatically.

Whatever fails, the structured report still goes out, since no failure class suppresses it, and you never retry on your own or widen the scope to compensate.

## What you hand back

A structured report with the watch surface identity, the observed state snapshot, the classified severity level, the routing targets, the on-call disposition (paged, escalated, acknowledged, not-applicable, page-failed, or page-rejected), the observation timestamp, and the paging confirmation timestamp whenever a page went out.
