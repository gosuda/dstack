# MISSION.md format

`MISSION.md` lives at the workspace root. It holds the _reason_ the user is learning this topic. Every teaching decision traces back to it: what to teach next, which resources to surface, which exercises to design.

## The shape of a mission

```md
# Mission: {Topic}

## Why
{1-3 sentences. The concrete real-world goal the user is chasing. What changes in their life or work when they have this skill? Avoid abstract framings like "to understand X". Push for the underlying outcome.}

## Success looks like
- {A specific, observable thing the user will be able to do}
- {Another specific thing}
- {…}

## Constraints
- {Time, budget, prior commitments, learning preferences, anything that bounds the approach}

## Out of scope
- {Adjacent topics the user explicitly does not want to chase right now. This protects the zone of proximal development.}
```

## Keeping the mission honest

- Keep one mission per workspace. Two unrelated goals mean two workspaces.
- Stay concrete. "Run a half marathon by October" beats "get fitter." "Ship a Rust CLI to my team" beats "learn Rust."
- Push back on vagueness. When the user cannot articulate why they are learning this, interview them before writing anything. A bad mission steers worse than no mission.
- Revise when reality shifts. Goals move. When the user's goal moves, update this file. Never leave a stale mission steering future sessions.
- Keep it short. When `MISSION.md` runs past a screen, it has stopped being a compass and started being a plan.
