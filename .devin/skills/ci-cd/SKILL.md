---
name: ci-cd
description: 'Use when setting up or modifying CI/CD pipelines, quality gates, test runners, or deployment pipeline configuration through workflow files. Not for triggering a deployment.'
---

# Author pipelines and deployment configuration that stay local

Someone needs a pipeline created or changed: quality gates, test runners, a deployment strategy, all expressed as workflow and deployment configuration files in the repository. Your job is to write exactly those files with gates in a fixed blocking order, secrets referenced but never stored, a deployment stage that can roll back, and local validation proving the files parse and the gates run. Nothing here deploys, publishes, configures credentials remotely, or mutates any remote system. Edited files are version controlled, so rollback is restoring them from VCS to the pre edit state.

## Confirm the provider and the file set before writing

First bound the scope: the work is authoring or modifying CI workflow and deployment configuration files in the repository. No deployments, no published artifacts, no branch protection changes, no secrets placed in a remote manager, no remote mutation. Enumerate the exact files this skill creates or edits, show the set to the user before mutation, and write only those files.

Then identify the CI provider and the target ecosystem from existing configuration (`.github/workflows/` versus `.gitlab-ci.yml`) or from the verified repository remote URL. Never assume; when the provider is ambiguous, stop and ask rather than defaulting to GitHub. For GitLab bind host and project separately: the host comes from the remote URL or `GITLAB_HOST` (GitLab.com, Dedicated, or self managed) and the project is the full `GROUP[/SUBGROUP]/PROJECT` path; for forks bind source and target projects separately.

Gather the rest of the inputs before authoring: the quality gates the project requires (defaulting to the fixed gate order below), the ecosystem commands realizing each gate, the deployment target with its rollback strategy whenever a deployment stage is in scope, any required deployment secrets, environment names, or build commands (supplied by the user; this skill never invents credentials), and the existing pipeline to modify when this is a change rather than a creation. Missing ecosystem commands stop the run; ask the user and never invent commands. An unsupported CI provider stops the run; report it and never guess a provider specific schema.

## Lay the gates in their fixed blocking order

Every PR or MR and every push to main passes the same sequence: lint, type check, unit tests, build, integration tests, E2E (optional at construction; when included, blocking), security audit, bundle size. The order is fixed across ecosystems; only the commands change. Representative commands: Node with `pnpm exec biome check .`, `pnpm exec tsc --noEmit`, `pnpm exec vitest run`, `pnpm run build`; Python with `uv run ruff check .`, `uv run ruff format --check .`, `uv run pyright`, `uv run pytest`, `uvx pip-audit`; Rust with `cargo clippy`, `cargo test`, `cargo build`, `cargo audit`. On GitLab the same order becomes `stages:` in `.gitlab-ci.yml` (one stage per gate, same sequence) with merge request pipelines scoped by `rules: - if: $CI_PIPELINE_SOURCE == 'merge_request_event'` (https://docs.gitlab.com/ci/pipelines/merge_request_pipelines/). Add no stages the user did not request.

Every gate blocks. No gate may be skipped. When lint fails, fix lint; when a test fails, fix the code. Never disable the rule or skip the test, and never re run a flaky test instead of fixing the flakiness.

## Reference secrets, never store them

Secrets enter the workflow file only as references to environment variables the provider supplies. Never store a secret in code or in workflow configuration. The user places secrets in the provider secret store out of band; this skill writes only the variable references. When a secret leaks into a config or code file, remove the secret from the file, rotate it, and re reference it as an env var before proceeding.

## Author the deployment stage with its way back

Configure the deployment pipeline stages (build, test, deploy) from the user supplied platform, environment, and commands, and include a defined rollback step. Add no stages the user did not request. Do not mark deployment configuration done while the rollback mechanism is missing.

## Validate locally and interpret filters with the provider grammar

Run the project local check set (lint, build, test) against the pipeline definition, and run the platform local validation for the workflow file when one exists: `actionlint` for GitHub Actions, `glab ci lint [--dry-run] [--ref <branch>] [--include-jobs]` for GitLab (see https://docs.gitlab.com/cli/ci/lint/). No `glab mr` command carries a general dry run (the dry run surface is CI only), so preview MR effects by local computation or JSON reads, never by submitting. Never trigger a deployment.

Interpret trigger filters with the CI provider documented grammar, not a generic glob or regex engine. Before changing a filter, state the intended included and excluded events and verify representative boundary cases against that grammar; a numeric version triple is not a complete SemVer grammar. On GitLab this is the `rules:if` grammar (`$CI_PIPELINE_SOURCE == 'merge_request_event'`, branch patterns per https://docs.gitlab.com/ci/jobs/job_rules/). For action, tool, image, runner, and toolchain pins, record the primary source and resolved commit or artifact identity. Resolve annotated tags to their commit and verify asset digests through the applicable release source. Treat runner and runtime updates as possible compatibility floor changes; never claim a floor violation without target evidence. Distinguish YAML parsing, workflow validation, embedded shell analysis, and actual job execution; report which occurred and never imply shell checking merely because a workflow linter ran.

## Route an existing failure to its owner instead of rerunning it

When a CI run already failed, hand the failure back to the agent owning the change: copy the failing job name, the error text, and the repo state at failure, so the root cause gets fixed rather than re run. Skip this step when setting up a pipeline that never ran.

For a GitLab MR read the head pipeline with `glab ci get --merge-request <iid> -F json` (explicit host from the remote URL or `GITLAB_HOST`, project via `-R GROUP/PROJECT`; forks need source and target projects bound separately; note `-p` on this command selects a pipeline ID, it is not a page flag), enumerate every page on list reads (`glab ci list -P/--per-page` with `-p`, or `glab api --paginate` for REST reads), and pull logs with `glab ci trace <job>`; the bundled helper `python3 "<path-to-skill>/scripts/inspect_mr_checks.py" --host HOST --project GROUP/PROJECT --mr IID --json` is the scripted equivalent. Match the pipeline `sha` against the MR head SHA: a missing, skipped, or unrelated successful pipeline is not proof. When the MR head moved during review, prior pipeline and approval evidence is invalid; re read the MR head SHA and its pipeline before reporting gates green.

## When to stop instead

Stop with a report naming exactly what is missing and what was tried, leaving edited files in place for the user to correct (or reverting them to prior state on request): unsupported provider; missing ecosystem commands; a gate failure you fix in code or configuration rather than by disabling the gate, skipping the test, or rerunning flake; a leaked secret, rotated before continuing; a missing rollback; a validation failure naming the file and line, never marking the pipeline verified while it fails. Keep all completed gate configuration on a partial result, but never commit a pipeline missing a blocking gate, a secret boundary, or a rollback. Platform side merge gates (required approvals, unresolved discussions, draft state, project merge policy) are enforced by the forge, not authored here; never treat CI green as merge approval and never bypass those gates from pipeline configuration.

Before handing back, verify every element: all gates present in order, the pipeline running on every PR or MR and push to main, secrets referenced via env vars, deployment carrying a rollback mechanism, and local schema validation passing.

## What you hand back

The written `.github/workflows/*.yml` or `.gitlab-ci.yml` (per the detected provider) plus deployment configuration files implementing the fixed gate order, blocking gates, secret references via environment variables, a deployment rollback mechanism with local schema validation, plus a report listing files written and per check pass or fail status. No deployment triggered.
