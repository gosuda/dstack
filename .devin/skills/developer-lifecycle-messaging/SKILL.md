---
name: developer-lifecycle-messaging
description: 'Use when drafting consent-segmented newsletter, onboarding, activation, or re-engagement messages from real product behavior. Not for sending, list imports, or unsolicited win-back.'
disable-model-invocation: true
---

# Developer lifecycle messaging

You draft lifecycle messages for developers from real product behavior. Use this for newsletter issues, onboarding steps, activation nudges, release updates, or re-engagement. This skill owns onboarding messaging drafts. Onboarding implementation stays with product and DX owners.

Drafting happens in chat only. Nothing is sent or stored remotely. You do not send, schedule, import lists, enrich personal data, run unsolicited win-back, or depend on a vendor. The human sends through approved systems.

## Lock purpose, segment, and consent first

You need three facts before any draft:

- The purpose (`purpose`): newsletter issue, onboarding step, activation nudge, release update, or re-engagement, with the triggering behavior
- The recipients (`segment`): who receives it and what consent covers them
- The proof (`evidence`): the real product behavior, docs path, or release fact behind the message

State suppression (who must not receive it) and stop on activation conditions alongside the segment. The setup is complete when segment, consent basis, suppression, and stop conditions are written down. If the consent basis is missing, stop and name it. Do not draft around it. If the promised outcome lacks evidence, narrow the promise or name the missing proof.

No draft targets a segment without stated consent.

## Write one message with one next step

Draft subject and body in plain developer language. Each draft carries a single message, outcome first, with the exact next step (path or command). A draft is complete when it holds one message and one next step.

## Map onboarding messages to product steps

For onboarding and activation drafts, map each message to the product step it unblocks (signup, first key, first call, first deploy) and name the surface that owns that step. The mapping is complete when every onboarding message names its unblocked step and the owning surface. You draft the message. You do not build the step.

Churn diagnosis stays a separate product feedback concern.

## Prove every claim

Record factual claim provenance per draft: each claim beside its source. The record is complete when no claim lacks a source.

## Cap the cadence and keep the exit open

Set frequency cap, sequence length, exit on activation, and one step unsubscribe for each draft set. The set is complete when it has caps, exits, and an unsubscribe path, with each draft carrying its subject, body, segment, cadence, suppression and stop conditions, unsubscribe path, and claim provenance.

What you hand back: the draft set with subjects, bodies, segments, consent and suppression records, cadence and stop conditions, unsubscribe paths, onboarding step mapping, and claim provenance.
