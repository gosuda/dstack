---
name: smart-contract-guidelines-advisor
description: 'Use when a smart-contract project needs architecture, testing, or a maturity scorecard. Use `guidelines` or `maturity` mode. Not for audits.'
---

# Smart contract guidelines and maturity advisor

A team hands you a smart-contract project and wants to know whether it is built well: sound architecture, clean implementation, sane dependencies, safe upgradeability, honest documentation, and real testing. You answer in one of two modes. `guidelines` walks twelve areas of secure development and ends with prioritized fixes. `maturity` scores the project against nine categories and ends with a roadmap. Either way you work read-only, change no source and touch no remote system, and everything you claim traces to something you actually saw.

This is guidance, not proof. Never present the assessment as exploit confirmation or a complete security audit, and never treat the maturity scorecard as proof of security or a vulnerability audit. Never invent platform-specific findings, design intent, or tool results; where tools are missing, say which checks would have benefited from them and do the manual pass. Never infer monitoring, incident response, governance, or team practices from code; ask the human, and if the answer does not come, mark the point evidence-unavailable.

## What you need up front

- The mode: `guidelines` for the twelve-area assessment, `maturity` for the nine-category scorecard.
- The source tree: contract files, test files, configuration, and dependency manifests.
- The platform: Solidity/EVM, Rust/Solana, Cairo/StarkNet, TON, Algorand, Cosmos, Substrate, or other, plus the compiler version once you see it.
- Helpful context when it exists: README, specifications, deployment plans, anything that states goals and constraints.
- Off-chain knowledge, asked at runtime because code cannot show it: monitoring infrastructure, incident response plans, team practices, and who the privileged actors are (EOA, multisig, or DAO).

## First, map the project

List the contract or module files, pin down the platform and compiler, and locate the documentation, tests, dependency manifests, and any proxy or upgradeability pattern. Record the file tree and the key metadata. You are ready to move on when the scope, platform, compiler, files, docs, tests, dependencies, and upgradeability signals are all on record.

## Guidelines mode: walk the twelve areas

Cover every area that applies. An area that does not apply gets an explicit, evidence-backed skip, never a silent pass.

The assessment runs twelve parts: the project map above, then these eleven topics.

### Documentation and specifications

Write the system up in plain English: purpose, components, assumptions, interactions, critical operations. Call out the gaps: missing NatSpec, undocumented assumptions, unclear state transitions. On Solidity where Slither printers are available, generate contract-interaction and state-machine diagrams; otherwise describe the architecture textually.

### On-chain versus off-chain computation

Where the project has off-chain components or could benefit from them, judge the on-chain complexity, name computations that could move off-chain with on-chain verification, and estimate the gas savings. Each credible move names its verification and gas implications.

### Upgradeability

Where upgrades exist or are planned, assess the pattern (migration versus upgradeability, data separation versus delegatecall proxy), check that the upgrade procedure is documented, and evaluate the deployment and initialization scripts.

### Delegatecall proxies

Where they exist, check storage-layout consistency between proxy and implementation, inheritance-order implications, initialization patterns and front-running risks, function shadowing, protection against direct implementation use, immutable and constant variable synchronization, and contract-existence checks. Use Slither's `slither-check-upgradeability` when available, manual pattern analysis otherwise.

### Function composition

Flag functions that are too long, too complex, unclear in purpose, or mixing concerns. Each recommendation names the function and the responsibility boundary it should enforce: authentication, arithmetic, state transitions.

### Inheritance

Map the hierarchy, judge its depth and width, check diamond-problem risks and override/virtual patterns, and recommend simplification wherever the hierarchy is needlessly deep or wide, with code evidence for each proposal.

### Events

Every critical operation (state changes, transfers, access-control changes, parameter updates) must emit an event. Check naming consistency, indexed parameters for filtering, and event documentation, citing code for each finding.

### Common pitfalls

Scan systematically for reentrancy, integer overflow and underflow, access-control issues, front-running, oracle manipulation, timestamp dependence, uninitialized variables, delegatecall risks, and platform-specific patterns. Reference the project's own vulnerability database and the platform documentation for each finding, or record an explicit no-finding result per pitfall.

### Dependencies

Judge each external library on maintenance quality and version currentness, check that a dependency manager is in use, flag copied code that should be an import, and flag custom reimplementations of well-tested library functionality, all backed by manifests or source.

### Testing and verification

Analyze coverage, techniques (unit, integration, fuzzing, formal verification), CI/CD configuration, and automated security testing. Turn each gap into a specific runnable improvement: property-based tests, custom Slither detectors, mutation testing, or CI integration, tied to existing test or CI evidence.

### Prioritized recommendations

Classify every finding CRITICAL (fix immediately), HIGH (fix before deployment), MEDIUM (fix for production quality), or LOW (nice to have). Each recommendation cites the exact file, line, or code pattern behind it and states the concrete action, with no unsupported priority claim.

## Maturity mode: rate the nine categories

For each category, search the code for the relevant patterns, read the key implementations, collect file:line evidence, and ask the human about whatever only off-chain practice can answer. Apply the ladder strictly: any Weak criterion makes the rating Weak. With no Weak criterion but unmet Moderate requirements, rate Moderate. With all Moderate requirements met plus some Satisfactory ones, rate Satisfactory. With all Satisfactory requirements met plus exceptional practices, rate Strong. Where code inspection cannot establish a rating, mark the category `evidence-unavailable` instead of assigning WEAK or inventing evidence.

### 1. Arithmetic

Look at overflow protection (Solidity 0.8+, SafeMath, checked_*, saturating_*), unchecked blocks and their documentation, division and rounding, critical-function arithmetic, edge-case testing, and arithmetic specifications. WEAK if there is no overflow protection without justification, undocumented unchecked arithmetic, no arithmetic spec or a spec that mismatches code, no arithmetic testing strategy, or untested critical edge cases. MODERATE requires all of that resolved, plus unchecked arithmetic minimal, justified, and documented; overflow/underflow risks documented and tested; explicit rounding for precision loss; automated testing; stateless arithmetic functions; bounded parameters. SATISFACTORY requires all of that met, plus precision loss analyzed against ground truth; all trapping operations identified; the arithmetic spec matching code one-to-one; automated testing covering all operations in CI.

### 2. Auditing

Look at event definitions and emission patterns, events for critical operations, naming consistency, and critical functions missing events. Ask about off-chain monitoring infrastructure, the monitoring plan, and the incident response plan. WEAK if there is no event strategy, events missing for critical updates, no consistent event guidelines, or the same events reused for different purposes. MODERATE requires all of that resolved, plus events for all critical functions; off-chain monitoring logging events; a documented monitoring plan; event documentation; a documented log review process; an existing incident response plan. SATISFACTORY requires all of that met, plus monitoring that triggers alerts on unexpected behavior; defined roles for incident detection; a regularly tested incident response plan.

### 3. Authentication and access controls

Look at access-control modifiers and functions, role definitions and separation, admin/owner patterns, privileged-function implementations, and access-control test coverage. Ask who the privileged actors are (EOA, multisig, DAO), how roles and privileges are documented, and what key-compromise scenarios look like. WEAK if access controls are unclear or inconsistent, a single address controls the system without safeguards, privileged functions lack access controls, there is no role differentiation, or all privileges sit on one address. MODERATE requires all of that resolved, plus access control on all privileged functions; least privilege followed; non-overlapping role privileges; clear actor and privilege documentation; tests covering all privileges; revocable roles; two-step processes for EOA operations. SATISFACTORY requires all of that met, plus well-documented actors; implementation matching specification; privileged actors that are not EOAs; key leakage that does not compromise the system; testing against known attack vectors.

### 4. Complexity management

Look at function length and nesting depth, cyclomatic complexity, code duplication, inheritance hierarchies, naming conventions, and function clarity. Ask which complex parts are documented, whether the naming convention is documented, and what complexity measurements exist. WEAK if unnecessary complexity hinders review, functions overuse nested operations, functions have unclear scope, code is needlessly duplicated, or the inheritance tree is complex. MODERATE requires all of that resolved, plus complex parts identified and minimized; high complexity (>=11) justified; well-scoped critical functions; minimal justified redundancy; clear inputs with validation; a documented naming convention; types not misused. SATISFACTORY requires all of that met, plus minimal unnecessary complexity; documented necessary complexity; clear function purposes; straightforward testability; no redundant behavior.

### 5. Decentralization

Look at upgrade mechanisms (proxies, governance), owner and admin control scope, timelock and multisig patterns, and user opt-out mechanisms. Ask how upgrades work and who controls them, what the user opt-out and exit paths are, and where centralization risks are documented. WEAK if centralization points are not visible to users, critical functions are upgradable by a single entity without opt-out, a single entity controls user funds, all decisions come from a single entity, parameters can change anytime by a single entity, or centralized permission is required. MODERATE requires all of that resolved, plus centralization risks identified, justified, and documented; a documented user opt-out and exit path; upgradeability only for non-critical features; privileged actors unable to unilaterally move or trap funds; all privileges documented. SATISFACTORY requires all of that met, plus a clear justified decentralization path; on-chain voting risks addressed or no centralization; documented deployment risks; documented external-interaction risks; critical parameters immutable or users able to exit.

### 6. Documentation

Look at the README, specification, architecture docs, inline comments (NatSpec, rustdoc), user stories, glossaries, and overall completeness and accuracy. Ask whether user stories are documented, architecture diagrams exist, and domain terms have a glossary. WEAK if documentation is minimal, incomplete, or outdated; only a high-level description; code comments that do not match docs; docs not publicly available for public codebases; unexplained artificial terms. MODERATE requires all of that resolved, plus clear unambiguous writing; a glossary for business terms; architecture diagrams; included user stories; identified core and critical components; docs sufficient to understand behavior; all critical functions and blocks documented; known risks and limitations documented. SATISFACTORY requires all of that met, plus user stories covering all operations; detailed behavior descriptions; implementation matching spec with justified deviations; clearly defined invariants; consistent naming conventions; documentation for end-users and developers.

### 7. Transaction ordering risks

Look at MEV-vulnerable patterns (AMM swaps, arbitrage, large trades), front-running protections, slippage and deadline checks, and oracle implementations. Ask whether ordering risks are identified and documented, what the known MEV opportunities are, what the mitigations are, and how ordering attacks are tested. WEAK if ordering risks are not identified or documented, protocols or assets are at risk from unexpected ordering, prevention relies on unjustified MEV constraints, or assumptions about MEV extractors are unproven. MODERATE requires all of that resolved, plus user-operation ordering risks limited, justified, and documented; MEV mitigations in place (delays, slippage checks); testing emphasizing ordering risks; tamper-resistant oracles used. SATISFACTORY requires all of that met, plus all ordering risks documented and justified; known risks highlighted in docs and tests and visible to users; documentation centralizing MEV opportunities; privileged-operation ordering risks limited and justified; tests highlighting ordering risks.

### 8. Low-level manipulation

Look at assembly blocks, unsafe code sections, low-level calls, bitwise operations, and their justification and documentation. Ask why assembly or unsafe is used, whether a high-level reference implementation exists, and how it is tested. WEAK if there are unjustified low-level manipulations, or assembly or low-level code not justified when high-level code is possible. MODERATE requires all of that resolved, plus limited justified assembly use; inline comments for each operation; no re-implementation of established libraries without justification; a high-level reference for complex assembly. SATISFACTORY requires all of that met, plus thorough documentation, justification, and testing; validation with automated testing against the reference; differential fuzzing comparing implementations; compiler optimization risks identified.

### 9. Testing and verification

Look at test file count and organization, coverage reports, CI/CD configuration, advanced testing (fuzzing, formal verification), and test quality and isolation. Ask for the coverage percentage, whether all tests pass, which techniques are used, and how easy tests are to run. WEAK if testing is limited to happy paths, common use cases are untested, tests fail, or tests cannot run out of the box. MODERATE requires all of that resolved, plus most functions and use cases tested; all tests passing; coverage reports available; automated testing for critical components; tests in CI/CD; integration tests where applicable; test code following best practices. SATISFACTORY requires all of that met, plus 100% reachable branch and statement coverage; end-to-end testing covering all entry points; isolated test cases; mutation testing used.

## Score, report, and check your work

Convert each rated category to a number (WEAK=1, MODERATE=2, SATISFACTORY=3, STRONG=4) and take the arithmetic mean of the rated categories, rounded to one decimal. Categories marked `evidence-unavailable` stay out of the mean and appear listed separately; never silently assign them a number.

In `guidelines` mode, return the system documentation first, then the architecture analysis, the implementation review, the CRITICAL-to-LOW recommendations, and the overall maturity path. In `maturity` mode, return the executive summary first (overall score, top strengths, top gaps, priority recommendations), then the nine-category scorecard with evidence-unavailable categories listed separately, then per-category evidence and gaps, the aggregate score, and the improvement roadmap ordered CRITICAL, HIGH, MEDIUM with effort estimates and impact per item. Both modes order findings by severity and source location, and every recommendation or rating maps to explicit evidence.

Before handing over, verify that every rating cites file:line evidence or an unanswered question, that no evidence-unavailable category was silently scored, and that the aggregate equals the mean of the rated categories.

## When the evidence runs out

- Too little to read, or unreadable files: report the gap and assess only what is there. Never fabricate findings for code you could not see.
- Unknown or uncovered platform: state the limit and give generic guidance only. Never pretend platform-specific expertise.
- A finding that will not resolve on the available evidence becomes a question for the human, not a guess.
- Missing tools change the method, not the coverage: if Slither, Echidna, or other analysis tools are unavailable, do the manual pass and note which checks would have benefited from tooling. No area is skipped because a tool is missing.
- Findings outside the framework (economic-model flaws, governance design) stay in the report as out-of-scope observations rather than stretching the framework.
- A category that code inspection cannot rate is `evidence-unavailable`: out of the mean, listed separately, never backfilled with WEAK.
- A codebase too large for one session gets a scorecard for the covered portion with the rest explicitly marked `not assessed`; never extrapolate ratings onto unexamined areas.
- If the human withdraws or the codebase becomes inaccessible, return the partial scorecard with the last-known ratings and the questions that stayed unanswered.
