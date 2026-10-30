---
name: explore
description: 'Use when asked to explore the codebase to map structure, symbols, and dependencies. Not for a single file under 50 LOC: read it directly.'
---

# Explore the codebase

You build a map of unfamiliar code and hand it back as a structured report in chat. You read only; you change no files, commits, state, credentials, or remote targets. You may dispatch Explore subagents for multi-file work. For a single file under 50 lines of code, skip this skill and read the file directly.

You start with the task text (the orientation question or concern), read-only access to the local checkout, and optionally specific files, directories, or concerns that bound the scope.

## Declare the scope first

Parse the task, identify the files, directories, and concerns in scope, and state the scope explicitly before any dispatch or read.

## Answer small questions compactly

When the task is a single bounded question, use compact question and answer mode and skip the 8-section report. This mode switch runs before any dispatch or synthesis. In this mode, emit an answer with per-claim code, docs, or inference labels plus file and line or URL citations, state contradictory sources explicitly, and list gaps and caveats. State why the 8-section form does not apply. The dispatch, synthesis, and output section rules below do not apply in this mode.

The one exception that also permits direct reads: external API or library docs needed to answer the bounded question may be fetched with web search and URL reads. Cite the source and distinguish documented behavior from observed behavior. Independent external research stays with research. No persistent artifact is required here.

## Send scouts for anything wider

For multi-file or uncertain tasks, dispatch Explore subagents instead of reading directly, and dispatch first: do not grep or glob a multi-file task before dispatching. Use 1 subagent for a single-concern known scope, 3 for multiple concerns or unknown scope, and 5 for a cross-module or architectural survey. Direct reads without dispatch are allowed only for a single file under 50 lines.

Keep discovery token-efficient: file discovery with `fd -e <ext> --max-results 50`, symbol search with `ast-grep run -p 'PATTERN' -l <lang> -C 1` or `git --no-pager grep -n -C 2 'pattern'`, content preview with `bat -P -p -n -r START:END file` or read with offset and limit, directory structure with `eza --tree --level=2`.

Never re-enter a router or orchestrator skill from inside this leaf skill.

## Write the orientation report

Emit all 8 sections in order: task understanding, architecture context, pattern context, tooling context, dependency map, critical files summary, constraints and considerations, and recommended next steps. Omit a section only when it genuinely does not apply, and state why.

When the scope exceeds 50 files, use a codebase-packing tool only as an internal analysis aid. Never give packed output to the user; search it for targeted extraction instead. If no packing tool is available, narrow the scope, state the narrowing, and proceed with the reduced scope.

Stay inside read-only tooling: `eza`, `fd`, `ast-grep` (find-only), `git grep`, `rg`, `bat`, `tokei`, `Read`, `codebase_search`, and any available codebase-analysis or codebase-packing MCP tooling, plus web search and URL reads solely for the compact-mode case above. Never invoke `Edit`, `Write`, `mcp__edit__edit_file`, `git commit`, or any state-mutating bash command. If a mutating tool call is attempted, stop immediately, perform no mutation, and report the attempt. No rollback is needed because no mutation occurs.

When source is empty or missing, state per affected section that it does not apply and explain why rather than fabricating content. When dispatch fails, return a partial result with the sections that could be filled, and never claim the run is done while required sections are missing. A blocked or non-converged result is a terminal classification stating which sections could not be filled and the concrete reason.
