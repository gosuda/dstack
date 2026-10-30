---
name: wizard
description: 'Use when a human must perform steps only they can, such as provisioning infrastructure, entering credentials or CI secrets, walking an unfamiliar third-party dashboard, or running a one-off migration or cutover. Not for steps the agent can perform itself.'
---

# Wizard

You write a script a stranger can follow, for the steps only a human can do. When infrastructure must be provisioned, credentials or CI secrets entered, an unfamiliar third-party dashboard walked, or a one-off migration or cutover run, the human drives the browser and types the secrets. You never run the wizard end to end, never enter credentials, and never perform the manual steps yourself.

Your only write is the wizard script itself at the named target path, which is reversible local work (deleting the file rolls it back). Verification is static only.

What you need before starting:

- Procedure description, required: what the wizard must accomplish.
- Target path, optional: where to write the script, defaulting to `scripts/setup-<topic>.sh`.
- Repository context, read and never asked for cold: `.env`, `.env.example`, `.env.*`, `README`, `docker-compose*`, framework configuration, and `.github/workflows/*`.

## Scoping the procedure from the repo

Read the repository context first. Treat every `secrets.*` and `vars.*` reference in a workflow as a value the wizard must produce. For a migration, read the current state, the target state, and every irreversible action between them. Show the ordered stage list with the values each stage produces and confirm it with the user. This step is done when every stage is named in order and every captured value has a known source, a destination (`.env`, a CI secret, both, or nowhere for a pure-action stage), and a secret or public classification. If the scope is still unconfirmed, stop before authoring, re-present the stage list, and wait (`scope-unconfirmed`).

## Mapping the human journey

Write instructions per stage that a stranger can follow: which URL to open, what to click, where the value appears, and which variable it fills. Where the current UI or the exact command is unknown, say so and check the official docs or ask the user. Never invent steps that may not exist. This step is done when every stage traces to concrete followable instructions. If anything is still unknown, stop and report what is unknown and how to resolve it (`unknown-step`).

## Authoring the script from the template

Fail before any write when a file already exists at the target path; report the existing path and never overwrite it (`path-collision`). Copy `scripts/wizard-template.sh` to the target path and replace only the example stage with one `stage` per step in dependency order. Set `TOTAL_STAGES` and `TOTAL_MINUTES` to honest values and keep each stage to one focused task. Use the library helpers only by the contract in `references/library-helpers.md`: open the URL before asking for its value, `ask_secret` for secrets, `write_env` for every persisted value, `set_secret` only for values CI needs, and `confirm` before any irreversible action. Never hand-edit the library above the stages marker. This step is done when the script holds one stage per step with honest totals and every helper used by contract. If any value has no capture or no destination, stop and report it rather than handing off (`value-untraced`). If any `set_secret` name does not exactly match its `secrets.*` workflow reference, stop and reconcile before handoff (`secret-mismatch`).

## Verifying without running, then handing off

Run `bash -n <script>`, run `shellcheck <script>` when available, and run `chmod +x <script>`, then fix any `bash -n` or `shellcheck` error before handoff (`syntax-failed`). Never execute the wizard, since it opens browsers and blocks on human input. Trace statically instead: every value from scoping is captured and lands where scoping declared, and every `set_secret` name exactly matches a `secrets.*` workflow reference. When the `gh` CLI is not ready for a secret, record that in `SKIPPED` so the script warns at runtime and the human sets the secret by hand (`gh-unready`). Tell the user how to run the script. Commit it only when the user wants a repeatable setup path that lives in the repo and is linked from the README; otherwise treat it as ephemeral and delete it when the job is done.

A partially authored script is never handed off. While it is still uncommitted, rollback is deleting the script file.

## What you hand back

A self-contained executable bash wizard at the target path with honest totals and every scoped value captured and routed to its declared destination, plus the run instruction and the ephemeral or repeatable disposition.
