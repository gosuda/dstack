# Section templates

Every README follows the fixed order from the skill: title block, Install, Quick start, core sections, Development, License. The archetype decides only the core sections. Adapt them to what the project actually does, and fill each one from project files rather than guesses.

## Fixed frame

1. Title block: name, tagline, optional badge row, opening paragraph, facts list, 4 to 10 line example with output
2. Install
3. Quick start
4. Core sections: Features, Usage, then the archetype sections below
5. Development: setup, test, build, and a Contributing subsection
6. License

## Core sections by archetype

Features and Usage open the core sections for every archetype. The table lists what each archetype adds to Usage and what follows it.

| Archetype | Detected from | Core sections after Features |
|-----------|---------------|---------------|
| Library or package | `package.json` with `main` or `exports`, `Cargo.toml` with `[lib]`, `Package.swift` library product, `pyproject.toml` | Usage (API examples), Configuration, API reference or a link to it |
| CLI tool | `bin` entry, `Cargo.toml` with `[[bin]]`, `go.mod` with a `main` package, executable product | Usage (real commands with flags), Commands and options, Configuration |
| Web application or service | Server entry point, `Dockerfile`, framework config | Usage (routes or endpoints), Configuration (environment variables), Deployment notes |
| Desktop app | `*.xcodeproj`, app bundle target, Electron or Tauri config | Usage (main workflows, screenshots), Requirements, Configuration |

A CLI Usage section shows real commands and their flags, not library import snippets. A web app keeps local setup, test, and build commands in Development so they stay out of the reader's first-run path.

Omit an archetype section when the project has no such surface. Install, Quick start, Features, Usage, Contributing, and License are never omitted.
