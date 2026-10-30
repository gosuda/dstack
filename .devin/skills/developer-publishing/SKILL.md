---
name: developer-publishing
description: 'Use when adapting a finished technical draft for Dev.to or Hashnode with correct canonical and metadata handling. Not for account creation, publication, or scheduling.'
disable-model-invocation: true
---

# Developer publishing

You adapt a finished technical draft for Dev.to or Hashnode so the human can publish it. Use this when someone supplies the draft and names `dev-to`, `hashnode`, or both (`targets`) as adaptation targets.

This is an adaptation pack in chat only. Nothing is published. Dev.to and Hashnode are separate internal profiles with their own rules, and you treat them that way. You do not create accounts, publish, schedule, manipulate followers, or change the canonical URL. The human publishes. You prepare the pack they apply.

## Fix canonical ownership first

You need the finished technical draft with its canonical home URL (`draft`). You may also receive existing tags, series, or custom domain facts (`metadata`).

State the canonical URL and require it recorded on every syndicated copy. Never change canonical as part of adaptation. The pack is blocked until canonical is stated and every target pack references it. If the canonical home is missing, stop and ask. Do not syndicate an orphan.

## Apply each venue profile from current docs

For Dev.to, fill frontmatter fields, tag selection within venue limits, series placement, and cover and description rules per current venue docs. For Hashnode, fill article settings, tags, series, and custom domain behavior per current venue docs. Each venue section is complete when every field is filled or marked venue default with the doc cited. Where venue docs are unavailable for a setting, mark it venue default unknown with the open question. Do not guess.

## State differences and verify parity

Say what is trimmed, expanded, or reformatted per venue and why. Confirm factual parity across versions: titles, descriptions, tags, and code match the draft, or the difference is named. The pack is complete when every difference names its reason and no silent drift remains, with canonical ownership stated, per platform metadata in agreement, and series placement and content differences explicit.

What you hand back: one adaptation pack per target with the canonical statement, metadata fields with cited venue docs, series placement, content differences with reasons, and the parity verification note.
