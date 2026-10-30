# DStack

> Vibes are too shallow. Specs are too complex. Let there be the outline.

**Beyond specs. Beyond vibes.** A versioned outline becomes the contract for every agentic act.

[![GitHub Stars](https://img.shields.io/github/stars/gosuda/dalcom-skills?style=flat-square)](https://github.com/gosuda/dalcom-skills/stargazers)
[![License](https://img.shields.io/badge/license-MIT-c8803c?style=flat-square)](LICENSE)
[![Last commit](https://img.shields.io/github/last-commit/gosuda/dalcom-skills?style=flat-square)](https://github.com/gosuda/dalcom-skills/commits/main)
[![Site](https://img.shields.io/badge/site-outlinedriven.github.io-c8803c?style=flat-square)](https://outlinedriven.github.io)

---

## Contents

- [What is DStack](#what-is-dstack)
- [Implementation](#implementation)
- [Install](#install)
- [Comparison](#comparison)
- [Status](#status-2026-09)
- [Contributing](#contributing)
- [License](#license)

---

## What is DStack

DStack (formerly Outline-Driven Development) is a coding methodology for LLM code agents. It occupies the space between two failure modes: vibes (too shallow, non-reproducible) and specs (too rigid, too expensive to maintain). We balance it with the sweeter taste(dalcom).

The outline is harness-agnostic. One implementation carries it to every agent, and the methodology
itself lives here as prompt files that any agent can consume. See [PHILOSOPHY.md](PHILOSOPHY.md)
for the full design rationale and traceability model.

---

## Implementation

[dalcom-skills](https://github.com/gosuda/dalcom-skills) is the single source: 304
skills in 22 plugins at release 2.1.8, authored once and discovered by Claude Code, Codex, Cursor, and any Agent
Plugins client from the same tree. There is no separate per-agent repository to install or track.

---

## Install

### Claude Code

```
/plugin marketplace add gosuda/dalcom-skills
/plugin install dstack-core@dstack
```

### Codex

```
codex plugin marketplace add gosuda/dalcom-skills
codex plugin add dstack-core@dstack
```

### Cursor

Add the `gosuda/dalcom-skills` marketplace in Cursor, then:

```
/plugin install dstack-core
```

Cursor reads the Agent Plugins manifest at each plugin root.

### Devin

Devin has no marketplace step. It reads project skills from `.devin/skills/<skill>/SKILL.md`, and
this repository carries every skill there as a flat, generated mirror of the plugin tree.
`.devin/skills/index.json` records the plugin each skill came from and the release it mirrors. See
[.devin/skills/README.md](.devin/skills/README.md).

### Pick your plugins

`dstack-core` is the base installed above. The other 21 plugins are optional, so add the domains you
work in and skip the rest. Every one installs the same way, for example
`/plugin install dstack-planning@dstack`. Three common additions:

| Working on | Add |
|---|---|
| Everyday code changes | `dstack-code`, `dstack-run` |
| Planning and task breakdown | `dstack-planning` |
| Knowledge and context retention | `dstack-knowledge` |

The full domain-to-plugin table, with the skill count per plugin, is in the
[dalcom-skills README](https://github.com/gosuda/dalcom-skills#choose-your-plugins).

### CLI tools

See [INSTALL.md](INSTALL.md) for CLI tool prerequisites and detailed setup.

---

## Comparison

| Aspect | Vibe coding | Spec-driven (Spec Kit) | BMad | **DStack (Outline-Driven)** |
|---|---|---|---|---|
| Source of truth | LLM intuition | Spec doc | Behavioral specs | **Versioned outline (hash-anchored)** |
| Iteration unit | "Try again" | Spec -> re-prompt | BDD scenarios | **Outline node x diff** |
| Validation | Eyeball | Spec compliance | Acceptance tests | **Diagram-first invariants + AST** |
| Tooling | Plain chat | GitHub Spec Kit | BMad CLI | **One plugin tree for Claude Code, Codex, and Cursor** |
| Reuse unit | Conversation | Spec template | Story | **Skill / agent / outline** |
| LLM creativity | Unbounded | Bounded by spec | Bounded by story | **Bounded by outline; preserved within envelope** |
| Best for | Throwaway scripts | Greenfield features | User-facing flows | **Long-lived methodologies + agentic work** |

---

## Status (2026-09)

dalcom-skills at release 2.1.8 is the single implementation, shipping 304 skills across 22 plugins for
Claude Code, Codex, Cursor, and any Agent Plugins client. The three prompt files were stripped of
persona doctrine in early September 2026, so the methodology carries no agent identity of its own.
Releases ship from the implementation repository, not from here.

---

## Contributing

Open an issue to discuss ideas or report bugs. PRs improving the methodology, prompts, or tooling documentation are welcome.

Do not edit `.devin/skills/` here. Every file under it is written by `scripts/sync-outline-skills.mjs`
in [dalcom-skills](https://github.com/gosuda/dalcom-skills), which also deletes any
file the plugin tree no longer carries. Change the skill under `plugins/<plugin>/skills/<slug>/` in
that repository and run `just sync-outline` there. The script writes to the sibling checkout
`../dstack` by default; `node scripts/sync-outline-skills.mjs --target <path>`
points it elsewhere, and `--check` reports drift without writing.

---

## License

MIT: see [LICENSE](LICENSE).
