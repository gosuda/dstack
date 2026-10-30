---
name: riffrec-feedback-analysis
description: 'Use when a Riffrec capture or other screen, voice, or notes artifact needs interpretation into bug or requirements evidence. Not for generic recordings without product feedback, and not for capturing durable learning.'
---

# Turning a capture into evidence

You take a Riffrec bundle (the synchronized screen, voice, and event capture from the Riffrec tool) or a related screen, voice, or notes artifact and turn it into evidence the product process can use. Raw capture and interpreted evidence are separate artifacts with an explicit boundary, and every artifact you produce keeps what its consumer needs and nothing more.

You read the supplied capture and write only explicitly requested evidence artifacts. Raw recordings, audio chunks, zip contents, session dumps, and extracted screenshots stay local-only by default and are never committed without explicit privacy-cleared authorization. You perform no publication, remote, credential, paid, or destructive action.

A route is finished only when its complete result or an actionable blocker is returned. Partial interpretation is never claimed as complete evidence.

## What you start with

| Input | Required |
|---|---|
| The input artifact or the setup question | Yes |
| The desired route (setup, quick bug report, or extensive analysis) when length and event content do not decide it | Ask when ambiguous |

Route from the input itself. Setup means no recording exists yet and there are install, capture, or share questions. Quick means a short capture (about a minute or less), a single specific issue, or an explicit quick or transcribe request. Extensive means longer, multi-issue, requirements-bearing, or workflow-walkthrough material, or an explicit requirements request. Generic recordings without product feedback are out of scope: return the boundary rather than analyzing them as product evidence.

## Choosing the route first

Route before doing anything heavy, and load only that route. When the input is ambiguous, inspect recording length and event count before choosing; when still unclear, ask which route applies. Never default to extensive. With no input and no setup question, ask for the artifact or question and analyze nothing.

## Setup route

Report the current supported capture and share path from presently readable project or vendor guidance. Invent no install commands, flags, or endpoints. When guidance is unavailable or stale, return that as the blocker with what would unblock it. The route closes with the path.

## Quick route

Interpret the single issue into one evidence-backed bug report with reproduction, observed behavior, expected behavior, and cited capture moments. Create no durable artifact unless requested. The route closes with the report. If the analyzer cannot do the work, stop with `blocked` naming the exact missing capability and its recovery.

## Extensive route

Build the complete evidence set:

- Problem analyses for each issue found.
- Requirements kickoff material.
- A source manifest with repo-relative screenshot paths and no absolute local paths.

Keep text artifacts committable only when needed for traceability and free of sensitive data; privacy-sensitive raw material stays local-only, and cleared text is committed only on explicit authorization. Unless the user asked for extraction only, hand the evidence to product framing as the next owner without executing it here. The route closes with the evidence set plus the framing handoff, or with extraction-only delivery. Analyzer or input failure ends as a blocker with recovery, never a partial success claim.

## What you return

The route taken, the setup path or bug report or evidence set with manifest paths, the framing handoff when one applies, and any blocker with recovery. Raw stays local; evidence carries repo-relative references later agents can open.
