---
name: ast-grep
description: 'Use when asked to run AST-based structural search, lint, or rewrite of code when regex is too fragile. Not for remote, credential, publish, deploy, or irreversible changes.'
---

# Structural search and rewrite with ast-grep

Use this when the task is about code shape (a call, function, class, or import that looks a certain way) rather than about text. ast-grep matches syntax trees, not bytes: if you catch yourself reaching for `|`, `.*`, `\w`, or `[...]`, the task is lexical and you want grep instead. If you need types, references, or callers resolved semantically, you want the language server or compiler instead. Only structural work belongs here.

Everything here is local and reversible. Searching reads nothing but the tree; rewriting touches only version-controlled source files, and only through the helper's dry-run-then-apply flow, so `git` is always your rollback. Nothing here mutates remotes, credentials, or published artifacts.

## What you need up front

A pattern, always single-quoted in the shell so `$VAR` reaches ast-grep unexpanded. A language (`--lang`) or a target path whose extension detects it (stdin patterns always need `--lang`). For a rewrite, a rewrite template plus one or more target paths (current directory when omitted). Optional extras: repeatable include/exclude globs (`!` excludes), context lines, JSON output.

Pattern syntax in brief: `$VAR` matches any single node, `$$$ARGS` matches zero or more nodes, `$_` matches any node without capturing. A pattern is code, not regex.

One more naming rule, because it bites: invoke `ast-grep`, never `sg` (`sg` collides with the `setgroups` binary on many systems).

## Validate, then search

Never search with an unvalidated pattern. Run:

```sh
python3 scripts/ast_grep_helper.py validate '<pattern>' --lang <L>
```

Exit 0 means ast-grep parses it cleanly and you may proceed. Exit 2 means malformed, and the helper prints the parsed pattern tree with the ERROR node marked, so fix the pattern and re-validate. If the ast-grep binary is absent, validation degrades: it checks only for regex smell, warns, and `replace` will exit 2 without running, so install ast-grep before going further.

If a search unexpectedly matches nothing, work this ladder in order: re-validate the pattern; check the dialect (`tsx` is not `ts`, and the wrong one silently matches nothing); run `ast-grep run -p '<pattern>' -l <L> --debug-query=pattern` and look for `ERROR`; inspect the target's real tree with `--debug-query=ast` on a snippet you know should match; reproduce in the online playground. Touch no files until a correct match is confirmed.

## Rewrite in two passes, never one

A rewrite is a dry run first, eyes on the diff, and only then an apply:

```sh
python3 scripts/ast_grep_helper.py replace '<pattern>' '<rewrite>' --lang <L> <paths>
python3 scripts/ast_grep_helper.py replace '<pattern>' '<rewrite>' --lang <L> <paths> --apply
```

Read the dry-run diff and the `N matches across M files` count. If the blast radius is wrong (too wide, too narrow, the wrong shape), stop. Tighten meta-variables, add `--lang`, add context, and re-run the dry run. Never `--apply` a diff you have not approved. The helper writes through a separate `--update-all` pass; keep it that way, because combining `--json` and `--update-all` makes `--json` silently win and the write is dropped with no error.

Before a structural migration, inventory the distinct syntactic roles carrying the changed contract: declarations, construction expressions, destructuring patterns, reconstruction paths, accessors. A pattern matching one role does not cover the others, so review an example from every affected role and record how each migrates. Match counts never prove semantic completeness.

If the apply pass fails partway, whatever ast-grep wrote stays written: never report done. Revert the version-controlled targets and re-run the full dry-run/apply sequence.

## For larger rule sets

Complex tasks graduate to YAML rule files (`sgconfig.yml`, `ast-grep new project`) with `rule`, `fix`, `inside`, `any`, and `matches` fields; drive those with `ast-grep scan` / `run` / `test` directly rather than the helper.

## What each command reports

`validate` exits 0 for a clean pattern, 2 for a malformed one (with the pattern debug tree), plus advisory regex-smell hints on stderr. A dry-run `replace` prints a compact unified diff and an `N matches across M files` summary and modifies nothing. `replace --apply` updates the version-controlled files via `--update-all` and prints a confirmation line. A direct `ast-grep` search reports matched code locations.
