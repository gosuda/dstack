---
name: viral-opportunity-scout
description: 'Use when asked to find distribution opportunities for a template, tool, or artifact. Not for content creation, campaign management, or paid placement.'
disable-model-invocation: true
---

# Viral opportunity scout

You find where a template, tool, or artifact could be distributed through niche or high-impact channels, and you report back in chat. Content creation, campaign management, posting, submission, and paid placement execution are out of scope.

This skill is read-only. No file, VCS, credential, paid, published, deployed, submitted, posted, or remote mutation happens. Research uses public official documentation and web search only, never social-post scraping. Nothing external changes, so the only deliverable is the report. You are finished when the report ranks every validated channel with its fit, entry barrier, submission rationale, cited reach or explicit unknown, and the user decision each channel needs.

## What you need

The artifact is required, as a text description or verbatim content. Without it, stop and report the failure. Do not produce a partial report. Two optional inputs narrow the work: a comma-separated `target_audience` that narrows channel mapping, and `channels` that restricts scouting to `community`, `platform`, `editorial`, `aggregator`, `offline`, or `social`. When `channels` is omitted, scout all families.

## Naming what you are scouting

Classify the artifact first. If the user supplied a type, use it. Otherwise infer it: executable code, CLI, or API is a tool; fill-in fields or placeholders make a template; short copy-pasteable code is a snippet; packaged code with imports and a public API is a library; prose or structured documentation is an article; slide format is a deck; audio or video content is video; tabular or structured data is a dataset; an agent workflow, harness, or scaffold is an agent harness; none of the above is unknown. Move on once the type is determined.

## Checking channels

Query known directories and aggregator platforms per in-scope family, and verify each platform is live and public through official docs or current search results. Social-platform research uses official public policy or metadata pages or user-supplied evidence, never scraped feeds. Move on once every in-scope family is queried and each candidate is confirmed live or skipped with a reason.

Then keep only active communities. Confirm recent activity (posts or submissions within the last 90 days) and public submission access (no invite-only or closed communities). Skip failures with named reasons. Move on once every candidate is validated or skipped with a named reason. If no viable channel survives, return a non-converged result with the artifact classification and a statement that no matching channel was validated. That outcome does not satisfy the finished condition above.

## Scoring honestly

Score each validated channel on reach, fit, and entry barrier. Reach is 1 to 5 with a cited current authorized source for the band, or `unknown` when no such source exists. Fit is 1 to 5 with the evidence behind it. Priority is reach times fit only when reach is cited; otherwise rank by fit and mark priority provisional. Entry barrier is low, medium, or high with the entry policy cited. Write a one-sentence submission rationale per channel. Never infer or fabricate an unvalidated opportunity, and flag any family where validation was skipped. Move on once every validated channel carries reach (cited or unknown), evidence-backed fit, barrier with policy, and rationale.

## The report you hand over

Compile a ranked report with an artifact summary and channel opportunities grouped by family, each carrying reach (cited or unknown), evidence-backed fit, priority, entry barrier with policy citation, and submission rationale. Present recommendations first, then secondary opportunities, then skipped families with reasons. Keep proven fit, entry policy, estimated reach, unresolved evidence, and the user decision in separate places so the report distinguishes what is proven, what is unknown, and what the user must decide.
