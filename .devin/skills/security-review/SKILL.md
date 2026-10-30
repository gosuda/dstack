---
name: security-review
description: 'Use when changes touch auth, parsing, dependencies, network, or pre-release, or a diff or baseline needs regression review, or the user asks for a security review, vulnerability audit, or OWASP review of a supplied file, diff, or component, covering injection, XSS, auth, or crypto, with high-confidence findings only (mode: confirmed), or an API, configuration schema, cryptographic interface, authentication surface, or library design is audited for misuse resistance or footguns at a caller-named target (mode: edges, inline or delegated specialist). Modes: full, differential, confirmed, edges. Not for adding controls. Not for CodeQL analysis: use codeql-security-analysis.'
---

# Review the change for what an attacker can reach

This skill audits a change for security risk, with the depth set by which question is being asked. Pick the mode that matches the question and stay inside it; the wrong mode gives the wrong report.

| Mode | Question it answers | Default |
|---|---|---|
| full | What is the security posture of this change set | Used unless the request points at a baseline, a named target, or a misuse surface |
| differential | What risk did this PR, commit, diff, or baseline comparison introduce | Applies when a PR, commit, diff, or baseline is supplied for regressions, blast radius, test gaps, or adversarial review of what changed |
| confirmed | Which high confidence vulnerabilities exist in this named file, diff, or component | Applies when the user asks for a security review or vulnerability audit of a named target and expects only data flow confirmed findings in chat |
| edges | Where can a caller misuse this surface | Applies when an API, configuration schema, cryptographic interface, authentication surface, or library design is audited for misuse resistance or footguns; inline by default, isolated delegated analysis only when a caller explicitly assigns the specialist |

Full and differential modes are reversible and local: the write set is one review report file, rollback is deleting that file, and there is no remote mutation. Differential mode always writes the report file, and secret scanning reads without ever mutating credentials. Confirmed and edges modes are read only: no file, version control, credential, paid, published, deployed, or remote mutation, and findings go to chat or back to the delegating caller. No mode edits code.

Three jobs belong elsewhere. Adding security controls during construction is not this skill. Verifying a named allegation as true or false positive belongs to security finding verification. Building or reusing a CodeQL database, or modeling project specific sources and sinks, belongs to codeql security analysis.

## Say which mode, change set, and depth before starting

Name the mode first. Differential needs a baseline to compare; it defaults to the merge base or parent commit. Greenfield code with no baseline, documentation only changes, and formatting only changes use full mode instead. Confirmed needs the review target: the file, diff, or code component under audit, and reporting stays bounded to that target while the entire reachable codebase serves as research scope. Edges needs the surface and the element inside it: the API surface, configuration schema, cryptographic interface, authentication surface, or library design, plus the element under examination. Specialist delegation adds the caller named scope (bounded by what the caller names; the skill refuses to expand it and discovers no additional files or symbols), optional language context inferred from file extensions, and an optional severity floor defaulting to all findings.

Other inputs stay optional. The change set (diff, commit range, or file list) is required for full mode. Depth applies to full and differential only: full depth unless the user explicitly requests quick triage and accepts the residual risk. Confirmed never reduces its data flow checks and edges never reduces its seven edge case or specialist checks. Ecosystem context (language family, framework, dependency manager) is inferred from the repo when absent. A scope hint (auth, crypto, injection, XSS, supply chain) narrows confirmed reviews and selects the walk in full mode; without one, full mode runs the complete STRIDE and OWASP walk.

## Map the change to trust boundaries

For full and differential modes, identify every file in the change set and map each to a trust boundary: external input, internal service, data store, or credential surface. Differential mode extracts the change set from the target with `git diff <base>..<head> --stat`, `git log <base>..<head> --oneline`, `git diff <base>..<head> --name-only`, or `gh pr view <number> --json files,additions,deletions`, then risk scores each changed file.

| Risk | File kinds |
|---|---|
| HIGH | Auth, crypto, external calls, value transfer, validation removal |
| MEDIUM | Business logic, state changes, new public APIs |
| LOW | Comments, tests, UI, logging |

Move on when every file maps to a trust boundary and, in differential mode, every changed file carries a risk score. Prioritize risk and use evidence throughout: focus on auth, crypto, external calls, value transfer, and validation removal, back every finding with evidence, line numbers, and attack scenarios, and classify by risk rather than size since a small diff can carry a critical regression. In full and differential review, familiarity is not coverage, explicit baseline context is built, Git history is never skipped, blast radius is calculated rather than guessed, missing tests elevate severity, and refactors are HIGH until proven LOW.

## Recover the baseline before judging the diff (differential)

Before mutation analysis, capture system wide invariants, trust boundaries and privilege levels, validation patterns, call graphs for critical functions, state flows, and external trust assumptions. Store the record for cross reference, then return to the head commit. Read both versions of each changed file and record BEFORE, AFTER, behavioral CHANGE, and SECURITY implication per diff region.

Blame removed code with `git log -S "removed_code" --all --oneline` and `git blame <baseline> -- file`. Removed code from fix, security, or CVE commits is CRITICAL; recently added then removed is HIGH; code added, removed for security, and re-added is a REGRESSION checked with `git log -S "added_code" --all -p`. Move on when baseline context is stored, removed code is blamed with red flags classified, regressions are checked, and every diff region has its four field record. When there is no Git history, regression and historical context analysis cannot complete: record the limitation, lower confidence, and never fabricate blame output.

## Walk STRIDE (full)

For each component touching a trust boundary, answer all six questions. Differential mode skips this walk; its trust boundary coverage comes from the baseline context and risk scores.

| Threat | Questions to answer |
|---|---|
| Spoofing | Who is the principal, how is identity proven, can the credential be forged, replayed, or stolen, is MFA or mutual auth enforced |
| Tampering | What inputs cross the trust boundary, are they validated against an explicit schema, are messages integrity protected |
| Repudiation | Are security relevant actions logged with actor plus timestamp plus outcome, are logs append only or tamper evident |
| Information disclosure | What is returned in error paths, logs, and telemetry, are PII or secrets ever serialized, are timing side channels addressed |
| Denial of service | Are inputs bounded in size, count, and depth, is parsing resource limited, are external calls rate limited |
| Elevation of privilege | What privilege does the new code execute under, is least privilege honored, can input alter privilege |

## Walk OWASP and the supply chain (full)

Trace authorization policy for broken access control. Grep for weak primitives MD5, SHA1, DES, Math.random, and check unparameterized queries, shell concatenation, and template eval for injection. Cross check STRIDE findings for insecure design. Check TLS, CORS, CSP, cookie flags, and debug toggles for security misconfiguration. Run the ecosystem CVE scanner for vulnerable components. Check token TTL, refresh, session fixation, and MFA for authentication failures. Check lockfile pinning and signature verified artifacts for integrity failures. Check audit log coverage and alerting on authentication failure for logging failures. Check egress allowlist and SSRF guards on URL inputs. Move on when every OWASP category has a pass or fail verdict.

Then run the per ecosystem CVE scanner and the secrets and history scanner from the dep audit tooling matrix in `references/dep-audit-tooling.md`, and record CVE count, secrets found, and SBOM status. When a tool is unavailable, note the missing scanner, proceed manually, and flag it as a gap.

## Separate cover, blast radius, and adversarial depth (differential)

Split production code changes from test changes and search for covering tests per changed function, then apply risk elevation: a new function with no tests moves MEDIUM to HIGH, modified validation with unchanged tests is HIGH, and complex logic over 20 lines with no tests is HIGH.

Count callers per modified function in the language appropriate way and classify the blast.

| Callers | Blast class |
|---|---|
| 1 to 5 | LOW |
| 6 to 20 | MEDIUM |
| 21 to 50 | HIGH |
| 50 plus | CRITICAL |

Combine risk score and blast class into a priority bucket, with deep analysis for high risk high blast changes and standard analysis for the rest. When the scope exceeds the declared depth, analyze the HIGH RISK subset at full depth, surface scan MEDIUM, exclude LOW, and record coverage percentage and confidence rather than claiming full analysis.

Escalate to adversarial analysis regardless of requested depth when removed code comes from security, CVE, or fix commits, access control modifiers are removed, validation is removed without replacement, external calls are added without checks, or a HIGH risk change meets high blast radius.

For HIGH RISK changes, map entry conditions, state reads and writes, external calls, return values, and side effects; trace internal calls recursively and external calls across trust boundaries while checking reentrancy; identify the invariants the change must preserve and run a Five Whys root cause (why changed, why the original existed, why it might break, why this approach, why it could fail in production); and find repeated validation patterns and flag removals that break defense in depth. Then run the five step adversarial method inline or through a subagent: attacker model (who, what access, where they interact), concrete attack vectors (entry point, attack sequence, proof of accessibility verified in code, never assumed), exploitability rating (EASY, MEDIUM, HARD), complete exploit scenario with exact commands, file and line references, and quantified impact (never "could cause issues"), and baseline cross reference (violated invariant, broken trust boundary, bypassed validation, regressed fix). Move on when every HIGH RISK change has the deep context map, the Five Whys, and all five adversarial steps with accessibility verified. Keep findings that reached concrete impact when a delegated adversarial phase does not converge, mark the rest non-converged with the blocker, and never inflate severity.

## Confirm every candidate through data flow (confirmed)

Detect the context from the supplied target before flagging: code type (API routes, frontend or templates, file handling, crypto or secrets, serialization, external requests, business workflows, config or headers or CORS, CI or CD dependencies, error handling, logging) and language or framework from file extensions and imports. For each candidate issue, research the data flow before flagging: where the input actually comes from, whether validation, sanitization, or allowlisting sits upstream, and which framework protections apply.

| Input source | Treatment |
|---|---|
| Server controlled (framework settings such as `django.conf.settings.*`, environment variables, config files, framework constants, hardcoded internal values) | Safe unless user input reaches them; a URL, path, or redirect target from settings or config is not an SSRF, path traversal, or open redirect finding |
| Attacker controlled (request params, body, headers, unsigned cookies, URL path segments, file upload content and names, database content from other users, WebSocket messages) | Traceable to the sink before any finding is reported |

Framework mitigated patterns are safe unless the unsafe variant is present: auto escaped template output (Django `{{ variable }}`, React `{variable}`, Vue `{{ variable }}`) and ORM parameterized queries (`cursor.execute("...%s", (input,))`, `Model.objects.filter(id=input)`) are safe, while `|safe`, `{% autoescape off %}`, `mark_safe(user_input)`, `dangerouslySetInnerHTML={{__html: userInput}}`, `v-html="userInput"`, `.raw()`, `.extra()`, and `RawSQL()` carrying string interpolation or user input are flagged. Always flag unconditionally: `eval` or `exec` on user input, unsafe deserialization (`pickle.loads`, `yaml.load` without `safe_load`, PHP `unserialize`, Java `ObjectInputStream`), `shell=True` or `child_process.exec` with user input, `innerHTML`, `dangerouslySetInnerHTML`, or `v-html` with user input, SQL built by string interpolation or template literals with user input, `os.system` with user input, and hardcoded secrets, API keys, AWS secret keys, or private keys. Never flag test files (unless explicitly reviewing test security), dead or commented code, documentation strings, patterns using constants or server controlled configuration, or code paths unreachable without privileges outside the modeled threat (record the required role as evidence); authorization flaws reachable by an authenticated low privilege user (for example IDOR) stay in scope with the auth precondition recorded. Confirm exploitability per candidate: the framework does not mitigate it and no upstream validation or sanitization library (DOMPurify, bleach, and similar) neutralizes the input. Data flow research is mandatory before flagging; reporting on pattern matching alone is a contract failure.

Classify every candidate HIGH (vulnerable pattern plus attacker controlled input confirmed), MEDIUM (vulnerable pattern with unclear input source; record as Needs verification, never report as a finding), or LOW (theoretical, best practice, or defense in depth; do not report). Move on when code type and language are detected, every candidate has a traced data flow, a classification, and confirmed or refuted exploitability, and only HIGH confidence findings are reported. When no high confidence findings exist, return the cleared report stating no high confidence vulnerabilities were identified rather than fabricating findings to fill it.

## Test every choice against the sharp edges (edges)

Inline mode enumerates every choice point in the target (parameters, return values, configuration keys, defaults, error paths, state transitions) and tests each against all seven edge cases: zero (0, false, equivalent), empty (empty string, empty collection, uninitialized state), null (null, None, nil, undefined, untyped zero value), negative (negative number or unvalidated signed integer), default (implementation defined or unspecified default), type confusion (a value of a different type than expected), and failure (error, exception, or unavailable).

Specialist mode records the caller named targets, binds the scope, and scans it without traversing directories, following imports, or fetching remote content beyond what the caller explicitly names. A directory or glob scope stops the run: ask for an explicit file list rather than auto expanding. Unreadable named targets are recorded as "Unreadable: [filename]" and the run continues with the rest. The four misuse categories are authentication and session management anti-patterns (hardcoded credentials, weak or missing authentication checks, insecure session token generation, missing or broken authorization guards, overly permissive default ACLs), cryptographic API misuse (predictable random sources, weak cipher or hash selection, ECB mode on block ciphers, missing authenticated encryption, hardcoded keys or IVs, incorrect key length, lack of salt for password hashing), configuration anti-patterns (excessive privileges, debug mode in production, disabled security controls, default credentials in config, credential leakage in logs or environment, insecure protocol or port defaults), and interface contract violations (missing null checks on returned objects, unchecked array or buffer bounds, unvalidated external input passed to dangerous sinks, missing error handling on security critical calls). Each concrete, reproducible misuse is classified as input validation, cryptographic misuse, authentication or authorization bypass, resource exhaustion, insecure defaults, state machine violation, or other.

Specialist mode validates exploitability per misuse: reachable from a realistic entry point without requiring an attacker to first introduce additional code or permissions, any pre-existing compensating control that reduces practical impact, and whether it is latent (present but unreachable with the current call graph). Record as Exploitable, Likely Exploitable, Unlikely Exploitable, Not Exploitable, or Latent. Every finding carries category, severity, location, a one sentence reproducible misuse, a one sentence security impact, and a concrete misuse resistant recommendation naming the correct API, configuration, or pattern with the minimum change required, without widening the attack surface. Move on when inline mode has tested every choice point against all seven edge cases, or specialist mode has scanned every misuse category across the named scope. With no security relevant edge cases, return an empty findings report stating no sharp edges were found; specialist mode appends "No misuse patterns detected in the named scope." When the four specialist phases cannot complete for a target, report findings up to the failure point, annotate the incomplete finding with "Phase N incomplete: [reason]", and never present a partial specialist report as complete. When the target is missing, stop without findings and return `error: no-targets` in specialist mode; when referenced source cannot be located, stop and state which target could not be examined.

## Grade honestly, then write the report the mode demands

Assign each finding Critical, High, Medium, Low, Informational, or specialist only Info. Full and differential modes enforce the merge gate: critical and high block merge. Confirmed grades HIGH confidence findings as Critical (direct exploit, severe impact, no auth required: RCE, SQL injection reaching data, auth bypass, hardcoded secrets), High (exploitable with conditions, significant impact: stored XSS, SSRF to metadata, IDOR to sensitive data), Medium (specific conditions required, moderate impact: reflected XSS, CSRF on state changing actions, path traversal), or Low (defense in depth, minimal direct impact: missing headers, verbose errors, weak algorithms in non-critical context). Edges grades misuses as critical (direct privilege escalation or data loss), high (information disclosure or degraded integrity), medium (availability impact or escalation path), or low (defense in depth violation or increased attack surface); specialist may assign Info and assigns Critical only when a single misuse instance is exploitable without prerequisite conditions or additional context. License findings are reported only as agreement gaps against the declared policy (compliance gap, hygiene gap, uninspected); never state a legal determination and never grade a license gap as a vulnerability. Discard evidence free findings: every finding cites specific line numbers and commits, and vague warnings are not findings.

Then compile the report. Full mode returns a structured audit with an executive summary (finding counts by severity), a STRIDE findings table (threat class, component, severity, description, remediation owner), the OWASP walkthrough (pass or fail per category), supply chain scan results (CVE count, secrets found, SBOM status), and the merge gate decision (block when critical or high are present, else pass). Differential mode writes the markdown report file with sections in this order: Executive Summary (severity distribution, overall risk, recommendation, key metrics), What Changed (commit range, per file table with status word PASS for clean, WARN for non-blocking finding, FAIL for blocking critical or high finding), Critical Findings (per HIGH or CRITICAL issue with file and line, blast radius, historical context, attack scenario, fix), Test Coverage Analysis, Blast Radius Analysis, Historical Context, Recommendations (immediate, before production, technical debt), Analysis Methodology (strategy, coverage, limitations, confidence), Appendices. Confirmed mode emits a chat only markdown report titled `## Security Review: [File/Component Name]` with a Summary (count by severity, risk level, confidence), Findings (`[Type: Descriptive Title] (Severity)` with Location, Confidence, Issue, Impact, Evidence, Fix), and Needs Verification (`[Verification Topic: Descriptive Question]` with Location and Question). A cleared confirmed report states "No high-confidence vulnerabilities identified." Edges mode returns a structured findings report with one entry per sharp edge (severity, category, location, misuse, impact, recommendation; specialist mode adds the exploitability determination and a per severity totals line), sorted by severity descending, in the conversation or to the delegating caller with no filesystem writes, no version control operations, and no remote calls.

## Stop rather than stretch the evidence

| Situation | Response |
|---|---|
| Incomplete change set | Report what was audited and skipped; do not widen scope |
| Ambiguous trust boundary | Document the ambiguity and flag for human review; never assume safety |
| Scope creep | Stop at the declared boundary and file separate findings for out of scope concerns |
| Missing baseline or unreadable diff in differential mode | Stop, report the exact target or baseline that could not be resolved, and never invent a baseline |
| Scope exceeding declared depth in differential mode | Analyze HIGH RISK at full depth, surface scan MEDIUM, exclude LOW, and record coverage and confidence |
| Candidate without confirmed attacker control in confirmed mode | Classify MEDIUM, record as Needs verification with the open question, and never promote to HIGH |
| Supplied target unreachable or unreadable in confirmed mode | Report exactly what was inaccessible and stop; never widen scope, guess at unreachable code, or report findings without evidence; remediation stays a recommendation in the report since the read only authority is never breached |
| No target provided in edges mode | Stop without findings and state the target was not specified |
| Missing source code in edges mode | Stop and state which target could not be examined |
| Partial result anywhere | State what was analyzed, what was excluded, and the confidence level; the done predicate holds only for the in scope subset actually analyzed |
