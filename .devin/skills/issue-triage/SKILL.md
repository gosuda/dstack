---
name: issue-triage
description: 'Use when a human invokes triage on a new configured Slack issue report. Not for triaging reports from other channels or posting more than one verdict.'
disable-model-invocation: true
---

# Triage a Slack issue report

A human points you at one fresh report in a configured Slack channel and you decide what it deserves: acknowledge, defer, escalate, close, or track it. You speak exactly once in the thread and file at most one tracker issue. Anything outside that channel, or any second verdict on the same report, is out of scope.

## What you need before touching anything

You need the report URL (`slack_report_url`) first. From it you derive the channel (`slack_channel_id`) and the message timestamp (`slack_thread_ts`). Never accept those derived values from anyone else's summary.

You need a Slack bot token (`slack_token`) scoped to reply in that thread. You need a tracker token (`tracker_token`) plus its instance URL (`tracker_base_url`) only if the verdict ends up calling for a tracker issue. Before any credential use, any data-at-rest change, any paid action, or any publishing or remote write, say plainly what target you will touch and what will change as a consequence.

## Work the report in order

1. Confirm a human asked for this triage, then fetch the message behind `slack_report_url`. When the call is not human originated, stop with no post and no issue. If the channel or thread does not resolve, stop with no post, no issue, and say the report could not be found.
2. Read the message content and pick exactly one verdict, with the report evidence that earns it. A verdict without its evidence citation is not a verdict. Never invent evidence the report does not contain.

| Verdict | When it fits | Evidence to cite |
|---|---|---|
| `ack` | Valid report needing no action, restates a known and already tracked condition with nothing new | Existing tracker reference or known status evidence |
| `defer` | Valid but consciously postponed, actionable yet lower priority than current work | Prioritization reason |
| `escalate` | Urgent or outside this tracker scope (security incident, data loss, service outage, or a problem needing a human beyond this workflow) | Urgency signal or scope boundary |
| `close` | Invalid, already resolved, or not actionable (duplicates a resolved issue, describes expected behavior, or lacks reproducible information) | Resolution, expected behavior reference, or missing information gap |
| `track` | Actionable work that must persist, a reproducible problem not yet tracked | Reproduction evidence |
3. Check for duplicates when you can. If `tracker_token` and `tracker_base_url` are present, query the tracker for existing issues referencing this Slack report and record the outcome. Without those credentials, skip the query and record it as skipped. A skip is never proof of absence. When the verdict is `track` and a duplicate exists, drop the creation plan and carry the existing issue URL forward.
4. Post exactly one thread reply with the verdict and its evidence citation, and capture its timestamp. If the post fails, stop right there and file nothing. A verdict that never landed authorizes no tracker write.
5. Only when the verdict is `track` and no duplicate exists, create exactly one tracker issue linked to the Slack report. If creation fails after a successful post, leave the posted reply alone. It stands as authoritative and is never edited or deleted to cover the miss.
6. Confirm the end state: the one reply exists, and where you queried the tracker there is at most one issue per report.

## What to hand back

Return one JSON object with `verdict` (one of `ack`|`defer`|`escalate`|`close`|`track`), `evidence_citation`, `slack_reply_ts`, `tracker_issue_url` (the created or existing duplicate URL when the verdict is `track`, otherwise null), and `is_duplicate`.

Map failures to these outcomes: a non-human call or an unfetchable report stops with an error and no side effects; a duplicate skips creation and still posts; a failed Slack post stops before any tracker write and reports the partial result; a failed tracker write keeps the Slack post and reports the partial result. No failure path claims the triage is complete.
