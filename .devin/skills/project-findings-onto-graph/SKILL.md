---
name: project-findings-onto-graph
description: 'Use when graph-backed security analysis is needed: project SARIF or reviewer findings onto a program graph; build or query a multi-language graph; summarize Trailmark structure; map smart-contract entry points; compare two refs or snapshots; or hunt confirmed vulnerability variants with pattern or graph seeding. Select findings, build-program-graph, trailmark-structural, entry-point-analyzer, graph-evolution, or variant-hunt mode and supply its required inputs. Not for initial vulnerability discovery: use security-review. Not for verifying one named allegation: use security-finding-verification. Not for security-finding triage: use triage-security-finding. Not for unrelated remote, credential, publish, deploy, or irreversible work.'
---

# Project findings and graph backed security analysis

External findings, source structure, entry points, structural changes, and confirmed root causes meet on one evidence surface here. The default `findings` mode projects SARIF or other supported exports onto an existing graph. The other modes build or query that graph, summarize a Trailmark snapshot, map smart contract entry points, compare two snapshots, or hunt variants of a confirmed root cause. Imported severity stays authoritative, and graph reachability never proves data flow.

Reads cover the supplied source, graph, refs, snapshots, and finding exports. Depending on mode the skill writes graph exports, annotations, declared links, structural or variant reports, or temporary snapshot worktrees. `entry-point-analyzer` is read only and emits chat output only. Temporary worktrees go away before completion. No remote mutation occurs. Roll back by deleting named artifacts, removing annotations by source tag, and removing temporary snapshot worktrees.

## What to take in

* `mode` (optional, default `findings`): one of `findings`, `build-program-graph`, `trailmark-structural`, `entry-point-analyzer`, `graph-evolution`, `variant-hunt`.
* `findings`: a program graph already built for the target repository plus at least one graph importable finding export. SARIF 2.1.0 is the standard format; reviewer annotations and other tool exports count when an importer or file and line anchors exist. Optional preanalysis evidence and extra source exports may ride along.
* `build-program-graph`: a target source directory, an optional explicit language list, an existing declared links file for cross boundary edges, and an optional external binary analysis graph export when supported. The installed graph analyzer is required.
* `trailmark-structural`: a target directory plus `summary` or `full` mode (default `full`). Trailmark must already be available; summary returns languages, entry points, and dependencies, while full returns the version gated structural payload.
* `entry-point-analyzer`: a smart contract codebase, an optional directory filter, and an optional project name. Supported inputs are Solidity, Vyper, Solana/Rust, Move Sui, Move Aptos, TON, and CosmWasm. The human invoked `entry-points` command may supply the directory path.
* `graph-evolution`: `before_ref` and `after_ref`, each a git ref or an existing directory path; an optional language (`auto`, one language, or a comma separated list); and installed Trailmark. Refs create temporary worktrees, directory inputs get used directly.
* `variant-hunt`: a confirmed root cause statement, the original bug location or vulnerable snippet, and the reachable project codebase. Optional inputs select ripgrep, Semgrep, or CodeQL; `pattern-search` or `graph-seeding`; a graph seed node; ranking weights; and an exclusion scope.

## Boundaries that hold in every mode

`findings` never builds a missing graph as part of augmentation. Switch to `build-program-graph` first. Never install or upgrade the graph analyzer, and never install Trailmark into the project; only `trailmark-structural` may use an ephemeral `uv run --with trailmark` probe, and that probe must not modify the project. Call graph reachability and taint subgraph membership never count as attacker controlled data flow or vulnerability proof. Imported findings keep their source severity and status; this skill never promotes them. Matching heuristics never widen to force unmatched findings or variant candidates into the graph. Uncertain smart contract access never classifies as confident; ambiguous restrictions remain `Restricted (Review Required)`. No evolution report comes from one healthy snapshot, a malformed ref, or a language mismatched empty graph. `entry-point-analyzer` performs no file, VCS, credential, paid, published, deployed, or remote mutation.

## Select and validate the mode

Use `findings` when no mode is named. Validate every required path, ref, export, root cause statement, or graph seed at its trust boundary before running a mode. Reject an unknown mode or a missing required input with its exact name; never widen scope by guessing.

## Findings mode: project exports onto an existing graph

Load the graph through the graph tool API. When loading fails, return `blocked: no-graph` and direct the invoker to `build-program-graph`; never build the graph in this mode.

Reuse preanalysis when present; otherwise run blast radius, entry point, privilege boundary, and taint passes on the loaded graph. When preanalysis cannot be made available, continue only with that absence recorded and omit cross reference claims.

Locate every supplied finding export and record its path and format. Probe optional importers on the loaded graph object before using them. Skip any input whose importer is unavailable and name the requirement; never invent a CLI flag or API.

Project each input with its native importer. With no importer available, resolve each file and line finding to the graph node whose span contains the normalized location and record that the match was manual. Record matched findings, unmatched findings, and created subgraphs per source.

Report matched and unmatched counts per source. Investigate path alignment or scope when unmatched counts run high, but do not widen the heuristic. Enumerate annotated nodes and subgraphs; severity subgraphs use `sarif:error`, `sarif:warning`, and `sarif:note`, while source subgraphs retain tags such as `sarif:<tool>`, `weaudit:<author>`, or `binary:<artifact>`.

Overlap severity subgraphs with `tainted`, `high_blast_radius`, and `privilege_boundary` sets. Attach the result as prioritization context without reclassifying the imported finding.

Emit an augmentation report ordered by source path and format: matched and unmatched counts, subgraphs, cross reference highlights, skipped inputs, and reasons.

## Build program graph mode: build and query the full graph

Verify the installed graph analyzer sits on PATH and imports from scripts. Record its version. When unavailable, report the installation gap and stop without installing or manually replacing the analysis.

Ask the installed build which languages it supports and detect which languages exist under the target. Treat documentation as non authoritative; the installed build answers. Stop when nothing parses.

Build the full graph for the selected languages, using auto detection unless the invoker supplied an explicit list. Never sample the tree. When supplied and supported, incorporate an external binary analysis graph export as an augmentation and record its provenance; otherwise report that augmentation is unavailable.

Run all preanalysis passes before dependent queries: blast radius estimation with downstream and upstream annotations and `high_blast_radius`; entry point enumeration with `entrypoints`, `entrypoint_reachable`, `untrusted_external`, `semi_trusted_external`, and `trusted_internal`; privilege boundary detection with `privilege_boundary`; and taint propagation from untrusted and semi trusted entry points into `tainted`, with trusted entry points generating none.

Execute requested queries with the version safe vocabulary: direct callers and callees; paths between functions or from entry points to targets; transitive ancestor and descendant slices; `complexity_hotspots(threshold=N)`; `attack_surface()` (passing newer `attributes` objects through unchanged); summary and JSON export; named subgraphs; structured annotations (`ASSUMPTION`, `PRECONDITION`, `POSTCONDITION`, `INVARIANT`) with a source convention of `llm`, `docstring`, `manual`, or `preanalysis`.

Probe method or attribute presence before every version specific feature. On older builds use the documented baseline or compute from the export, such as selecting edges whose endpoints both sit in a named subgraph.

Declare parser invisible FFI, RPC, IPC, or contract edges in the analysis root links file when needed. Use TOML `[[link]]` blocks with `source`, `target`, `kind`, `confidence`, and optional `description` or `target_external = true`. Reject ambiguous endpoints, unknown internal endpoints, invalid enums, and malformed TOML. Record `configured_by` on declared edges and treat `proxy.external:<symbol>` nodes as system boundaries, not source functions.

Record the model the installed build emits: node kinds (`function`, `method`, `class`, `module`, `struct`, `interface`, `trait`, `enum`, `namespace`, `contract`, `library`, `template`, newer `proxy`, `schema`, `table`, `view`, `procedure`); origins (`source`, `proxy`, `binary`, `synthetic`); edge kinds and confidence; per unit parameters, return and exception types, cyclomatic complexity, and branch metadata. Describe the installed build rather than documentation.

Bound every security claim. Paths are call graph reachability; `tainted` means reachable from an untrusted entry point, not interprocedural data flow. Verify data flow by hand, account for `uncertain` dynamic dispatch edges, and never treat proxy or binary nodes as source functions.

Write the requested JSON export with summary, nodes, edges, and subgraphs. Record emitted proxy nodes, external endpoints, and origins.

## Trailmark structural mode: summarize one target

Confirm the supplied target exists as a readable directory. Check the `trailmark` command or Python module, with `uv run trailmark analyze --help` as an acceptable probe fallback. Record a version when available. An ephemeral `uv run --with trailmark` retry may only test the import and must not install into the project. When all checks fail, report `trailmark is not installed` and return.

Detect languages through `trailmark.parse.detect_languages`, falling back to `trailmark.query.api.detect_languages` for pre 0.3 builds. On an empty result, report `Trailmark found no supported languages under target` and return.

For `summary`, run only `trailmark analyze --language auto --summary <target>` (or its `uv run` fallback), and verify the detected languages, `Entrypoints:`, and `Dependencies:` are present. For `full`, construct `QueryEngine.from_directory(target, language="auto")`, run `preanalysis()`, and assemble version gated `languages`, `summary`, `preanalysis`, `attack_surface`, `hotspots`, `proxy_nodes`, and every named subgraph with counts and sample IDs. Probe `subgraph_edges`, `type_references`, and other newer methods with `hasattr()`; preserve `attack_surface` attributes and explicit empty sections.

Verify and return the complete summary or full payload, including the version when captured, or the exact missing field or import gap.

## Entry point analyzer mode: map state changing entry points

Resolve the codebase or `entry-points` command directory to an absolute readable path. Detect languages from extensions and manifests: Solidity; Vyper; Solana/Rust with `solana-program` or an equivalent program entrypoint; Move Sui with `Move.toml` Sui or edition metadata; Move Aptos with `Move.toml` Aptos metadata; TON (`.fc`, `.func`, `.tact`); CosmWasm with `cosmwasm-std`. On no supported language, report the unsupported codebase and stop.

Apply the optional directory filter and locate every contract or module file in scope. Never sample the tree. Record generated, inherited, vendored, and unreadable paths separately.

Use source inspection as the authoritative foundation. A locally available Solidity analyzer may serve as supplementary evidence, but it is never required, never installed, and never authoritative for access classification. When the analyzer is absent or fails, continue with manual source analysis and record the fallback. Invent no replacement command.

Retain every externally callable, state changing function and exclude only forms that are read only or not externally reachable in the target language:

* Solidity: exclude `view` and `pure`; include state changing `external` and `public` functions, `receive`, `fallback`, and state changing callbacks.
* Vyper: exclude `@view` and `@pure`; include state changing `@external` functions and the state changing default handler.
* Solana/Rust: include the native program entrypoint, instruction handlers, and Anchor program functions that can mutate accounts; exclude helpers and handlers whose accounts are not mutable.
* Move Aptos: include `public entry fun`, `entry fun`, and `public fun` when the body changes state or accesses mutable resources. Exclude private, `public(package)`, and `public(friend)` functions as independent transaction entry points.
* Move Sui: include `public entry fun`, `entry fun`, and transaction reachable `public fun` when they mutate an owned or shared object. Exclude private `fun` and `public(package) fun`.
* TON: include state changing `recv_internal`, `recv_external`, tick tock handlers, Tact `receive`, `external`, and `bounced` handlers; exclude getters and read only receivers.
* CosmWasm: include `instantiate`, `execute`, `migrate`, `reply`, `sudo`, IBC, and other state changing callback entry points; exclude `query`.

Never decide Move entry point status from the presence or absence of `entry` alone. Judge state effects and transaction reachability per the target Move dialect.

Classify each retained function as exactly one of `Public (Unrestricted)`, `Role-Restricted`, `Restricted (Review Required)`, or `Contract-Only (Internal Integration Point)`. Trace actual restrictions: owner, admin, governance, guardian, operator, minter, pauser, keeper, relayer checks, role predicates, capability objects, ownership constraints, signer checks, sender equality, inherited modifiers and decorators. Read every modifier, helper, parent definition, handler, and constraint that establishes the restriction. Names are search hints, not proof.

Apply these adversarial checks before preparing the report: an unguarded callback is Public regardless of name; a configured caller address whose identity is not established remains Restricted (Review Required), not Contract Only; Aptos public non entry functions that mutate state stay included; Sui public non entry transaction reachable mutating functions stay included; read only Solidity, Vyper, Move, TON, and CosmWasm forms stay excluded from the recurring inventory; CosmWasm `execute` message variants classify at their handlers, not only at the dispatcher; constructors, initializers, upgrade functions, and proxy dispatchers list separately when they are not recurring entry points; a signer argument alone is not an administrator role; `msg.sender != tx.origin` is a call path condition, not authentication; an inherited, generated, or unresolved restriction remains a warning or Review Required classification.

Record for every entry point: signature or message variant; file and line; state changing operation; access class; exact restriction evidence; inherited or delegated restriction implementation; callback or integration role; expected caller and how that identity is established; unresolved assumptions.

Emit the markdown report with project and optional project name; timestamp; scope and directory filter; detected languages; state changing only focus; summary counts for Public, Role Restricted, Restricted (Review Required), Contract Only, deployment only, and recurring total; per category entry point tables; read only exclusions; per file accounting; Analysis Warnings. The report must contain an explicit recurring state changing entry point count and an explicit Analysis Warnings section, even when empty. Entry point mode is inventory only: it reports no vulnerabilities, assigns no exploitability or severity, generates no exploits, recommends no fixes, and never invokes `security-review` automatically.

## Graph evolution mode: compare structure across two refs or snapshots

Confirm both refs resolve or both directories exist. Run `trailmark --help`; when absent, report the installation gap and stop.

For git refs, create temporary `mktemp -d` worktrees with `git worktree add`; for directory inputs, use them directly. Confirm both snapshots are non empty.

Build a Trailmark graph and run preanalysis for each snapshot, export both JSON graphs, and verify nonzero, plausible node counts.

Run `trailmark diff --json --language {language}` with the same explicit language used to build the graphs. Never accept the default `python`. Distinguish a healthy empty diff from a language missed near empty graph using the summaries.

Compute membership changes for `tainted`, `high_blast_radius`, `privilege_boundary`, and related subgraphs from the exports, using `graph_diff.py` when available or direct set differences otherwise.

Classify every change in priority order: new tainted paths; privilege boundary changes; attack surface growth, especially `untrusted_external`; high blast radius additions; cyclomatic complexity increases greater than 3 on tainted or entry point reachable nodes; structural additions; structural removals checked for replacement rather than silent deletion.

Assign severity to every finding, including removals: CRITICAL for a new tainted path to a sensitive function or removed auth boundary; HIGH for a new high blast radius entry point or large tainted node complexity increase; MEDIUM for new trust boundary edges or moderate complexity increase; LOW for additions without entry point reachability; INFO for dead code removal or complexity reduction.

For refs, capture `git diff {before_ref}..{after_ref}` and attach source context to findings naming nodes or edges. For directory inputs, state that source level VCS context is unavailable.

Write `GRAPH_EVOLUTION_{project}_{before_ref}_{after_ref}.md` with summary metrics, critical changes and recommendations, attack surface, complexity, taint, blast radius, privilege boundaries, added and removed nodes and edges, methodology, preanalysis, refs, and honest limitations.

Remove temporary worktrees after writing the report and record their removal.

## Variant hunt mode: search variants of a confirmed root cause

Require a confirmed root cause statement plus either the original location or a vulnerable snippet. Validate the supplied location in the codebase; otherwise preserve and validate the snippet before proceeding. With neither present, return `blocked: root cause and original location or snippet required`. This mode never serves initial vulnerability discovery (route that to `security-review`) nor verification of one allegation (route that to `security-finding-verification`).

State the root cause precisely. For taint like defects: `[data or state] reaches [dangerous operation or decision] without [required protection] under [enabling context].` For logic, ordering, or concurrency defects without a taint flow: `[invariant] must hold across [operation], but [ordering or state transition] allows it to fail.` A check/use separation such as TOCTOU counts as a changing checked state, a check/use gap, or a missing atomicity guarantee. Never reduce it to generic untrusted input reaches a sink language.

Enumerate grounded expansion axes: dangerous operation; dangerous data or state; missing protection; enabling context; semantically related identifiers; sibling APIs and callbacks; alternate entry points; copied implementations; alternate manifestations of the same invariant failure; null, empty, zero, negative, maximum, repeated, and nested values; success, error, cancellation, teardown, and cleanup paths. Search for evidence that each proposed identifier or axis exists in the codebase. Never invent a family from names alone.

Calibrate with an exact pattern that matches only the known bug. Use the strongest available local mechanism: repository native structural search, Semgrep, CodeQL, or simpler textual search when the stronger tool is unavailable. Never install a tool or fabricate a command. The exact pattern must match the original location or supplied snippet. A zero hit calibration returns `blocked: pattern does not match known bug`, which never counts as evidence that no variants exist. Record the tool actually used and any precision loss from fallback.

Generalize one element at a time. For each axis: change exactly one name, literal, structural relation, source/sink, or graph expansion parameter; search the complete declared source scope; record all matches; read every new match; record confirmed variants, safe matches, unreadable matches, and noise; stop that axis when more than half its matches are noise. Never jump from the seed straight to a maximally broad semantic pattern. A pattern change past the noise threshold gets rejected or narrowed, not hidden.

In graph seeding mode, load an existing graph and resolve the seed. With no graph artifact, return `blocked: missing-graph-artifact` and direct the invoker to `build-program-graph`. Malformed or missing nodes return `blocked: invalid node object` or `blocked: node-not-found`. Compute at most three hops, exclude the seed, confirmed vulnerabilities, out of scope nodes, and nodes without textual or symbol content. Bound the candidate set to 50 and rank by at least three of degree centrality, clustering coefficient, path length, and structural similarity. Record weights, truncation, and the fact that every result is only a review target.

Triage every pattern or graph candidate. Read the surrounding function, relevant callers and callees, types, guards, sanitizers, validation, ownership, and entry point reachability. Assign exactly one status: `confirmed-variant` (same root cause present); `safe-look-alike` (shape resembles the seed but an actual guard, sanitizer, type constraint, or different sink prevents the defect); `unreachable-unprotected` (protection absent but current reachability not established; retain at lower confidence and state what would make it reachable); `unreadable` (required source or callee evidence unreadable); `out-of-scope` (match outside declared scope). A candidate is not safe merely for having no callers, and not confirmed merely for resembling the seed. Record severity and confidence separately. For every ruled out candidate record why it was safe. For every confirmed candidate quote the code and identify the violated invariant or source to sink path.

Write the variant report with root cause; original location; analyzed scope and coverage; methodology table; exact and generalized patterns; confirmed findings with quoted code; grouped safe look alikes; unreachable, unreadable, and out of scope candidates; graph seed, hop bound, ranking dimensions, weights, and truncation when graph seeding applied; a CI ready regression rule recommendation from the strongest pattern. End the report with an explicit conclusion: `variants found: N` or `no confirmed variants found in the analyzed scope`. A per candidate not a variant list without an overall conclusion is incomplete. A negative conclusion names the analyzed scope and any unreadable remainder. State that graph reachability is not data flow proof. Variant hunt is read, search, and report work only: it edits no source, tests, CI, or graph data to make a candidate pass, and its CI ready rule is a recommendation only.

## Failures and how each mode recovers

* Findings: missing graph returns `blocked: no-graph`; missing preanalysis produces an explicitly unprioritized report; an absent importer skips only the affected input; malformed inputs report their path and continue; high unmatched counts trigger path root review without heuristic widening; interruption returns collected sources and their completion states; rollback deletes the augmented export or removes source tagged annotations.
* Build program graph: a missing tool, import error, language detection failure, or unrun preanalysis stops the affected analysis and reports the gap; version gated methods fall back to the baseline or export computation; rollback deletes exports and declared links, while in memory annotations vanish with the engine.
* Trailmark structural: invalid target, missing Trailmark, no supported languages, import failure, missing summary field, or failed feature probe gets reported without fabricated sections; empty pass outputs are valid and returned explicitly; partial output is labeled partial.
* Entry point analyzer: an unsupported codebase returns no invented entry points; unparsable files remain in Analysis Warnings; analyzer failures fall back to manual analysis; ambiguous access remains Restricted (Review Required); no source or repository mutation is attempted.
* Graph evolution: Trailmark absence, failed diff, a single failed snapshot, skipped preanalysis, or a language mismatched empty diff stops report generation. Healthy nonzero summaries plus empty arrays mean structural stability. When cleanup is interrupted, remove temporary worktrees before retrying and report the incomplete state.
* Variant hunt: missing root cause, missing location or snippet, zero exact matches, excessive false positives, missing graph artifacts, missing or malformed seed nodes, zero candidates, unsupported initial discovery requests, one finding verification requests, and write failures return their named blocked result. With more than 200 candidates before triage, triage the first 200 and document the remainder. Past the graph seeded 50 candidate bound, truncate by the documented ranking and record the truncation. Delete partial reports after a failed write.
* Rollback in every mode: remove each named local artifact and temporary worktree the mode created. No remote state ever changes.

## What you hand back

* `findings`: an augmentation report ordered by source path and format, with matched and unmatched counts, annotated nodes, created subgraphs, tainted, high blast radius, and privilege boundary overlaps, skipped inputs, and source severity preserved.
* `build-program-graph`: an evidence report ordered by installed version and parser coverage, languages, graph summary, preanalysis, requested queries, model metadata, exports, and limitations; it states that reachability is not data flow proof.
* `trailmark-structural`: the requested Trailmark summary with language, `Entrypoints:`, `Dependencies:`, and version, or the full JSON payload ordered as languages, summary, preanalysis, attack surface, hotspots, proxy nodes, subgraphs, and optional type reference samples.
* `entry-point-analyzer`: the scoped markdown entry point report with summary and per category tables, file accounting, restriction evidence, callbacks, and warnings.
* `graph-evolution`: `GRAPH_EVOLUTION_{project}_{before_ref}_{after_ref}.md` with metrics, all structural and security relevant changes, severity, source context, and cleanup methodology.
* `variant-hunt`: a local variant report with root cause, original location, analyzed scope and coverage, methodology table, exact and generalized patterns, confirmed findings with quoted code, grouped safe look alikes, unreachable, unreadable, and out of scope candidates, graph seeding details when selected, an explicit `variants found: N` or `no confirmed variants found in the analyzed scope` conclusion naming scope and unreadable remainder, and a CI ready regression rule recommendation; states that reachability is not data flow proof.
