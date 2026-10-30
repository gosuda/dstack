---
name: developer-community
description: 'Use when designing developer community operations including platform choice, moderation, and health metrics. Not for creating servers, inviting members, or automated outreach.'
---

# Developer community

Design a developer community that volunteers can run: the right platform, a clear channel map, a walkable path from first visit to first contribution, and moderation the team can sustain. The result is an operating brief in chat. No servers are created, nobody is invited, and no community state changes.

Platform notes here may compare Discord, Slack, GitHub Discussions, and Discourse (they are options, not separate skills). Running the community, moderating members, or contacting anyone stays human; this skill designs the brief.

## What you need before starting

- `purpose` (required): what the community exists to do for developers.
- `scale` (optional): current size and moderation capacity. When omitted, plan for a small volunteer-run group.
- `constraints` (optional): platform limits, brand rules, or staffing the user names.

## Designing the operating brief

Work through these in order:

1. Decide the platform from purpose and capacity, comparing the candidates on threading, search, discoverability, and moderation cost. Name the reasons for the choice and the reasons each rejected option lost.
2. Draw the channel map: a purpose per channel, what belongs where, and the archive policy. Each channel gets a misplacement rule so content lands in the right place.
3. Write the onboarding path from first visit to first contribution, with the exact links and docs a newcomer needs. It must be walkable from the stated entry point.
4. Set the code of conduct, the moderation matrix pairing each violation class with its response, and the escalation path from moderator to maintainer to legal where relevant. Every violation class ends at an escalation endpoint.
5. Define health metrics from behavior the team can already observe (response times already measurable, repeat contributors, resolved-question rate). Each metric names its existing measurement source, and none may need a new credential.

Throughout, purge automation: bots, scheduled prompts, and outreach sequences may appear only as explicitly human-approved future options, never as embedded steps. No server creation, invites, bot setup, member pinging, or automated outreach belongs in the brief.

## When the plan outruns its keepers

- Capacity too small for the ambition: cut scope to what the stated moderators can run, and name the cut.
- Platform decision blocked on unknown policy: mark it unknown with the policy question stated. Do not guess.

## What you hand back

A community operating brief: platform decision with reasons, channel map, onboarding path, code of conduct, moderation matrix, escalation path, health metrics, and staffing assumptions, with no creation, invitation, or automation step included.
