# Badges

A badge earns its place only when project files prove the value behind it: a CI workflow file, a published registry package, a license file, or a coverage integration. Prefer a plain sentence when it says the same thing. Place the row directly under the project name and tagline.

## Rules

- Replace every angle-bracket variable with a value derived from project files.
- Omit any badge whose value cannot be proven.
- Every kept badge must render dynamically: HTTP 200 from a read-only GET, and not the shields "invalid" card.
- Use `style=flat-square` or `style=flat`.
- Use the default color or a semantic one (green for passing, red for failing).
- Keep the row on one line; wrap to a second only when more than five badges are proven.

## Providers

| Provider | URL pattern | Shows |
|----------|-------------|-------|
| shields.io | `https://img.shields.io/...` | Static and dynamic values |
| GitHub Actions | `https://github.com/<owner>/<repo>/actions/workflows/<workflow>.yml/badge.svg` | CI build status |
| npm | `https://img.shields.io/npm/v/<package>` | Published version |
| PyPI | `https://img.shields.io/pypi/v/<package>` | Published version |
| crates.io | `https://img.shields.io/crates/v/<crate>` | Published version |

## Patterns

CI build status, proven by a workflow file:

```markdown
![CI](https://github.com/<owner>/<repo>/actions/workflows/ci.yml/badge.svg)
```

Version, proven by a published package:

```markdown
![npm version](https://img.shields.io/npm/v/<package>)
```

License, proven by a license file:

```markdown
![license](https://img.shields.io/github/license/<owner>/<repo>)
```

Coverage, proven by a coverage integration:

```markdown
![coverage](https://img.shields.io/codecov/c/github/<owner>/<repo>)
```

Downloads, proven by a published package:

```markdown
![downloads](https://img.shields.io/npm/dm/<package>)
```
