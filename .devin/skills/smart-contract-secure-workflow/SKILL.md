---
name: smart-contract-secure-workflow
description: 'Use when a smart-contract team invokes this before check-in or deployment. Not for audit prep. Not for guidelines: use smart-contract-guidelines-advisor.'
---

# Smart contract secure workflow

A team is about to check in or deploy and wants the same safety pass run the same way every time. You walk their contract source through five stages (properties, tests, manual review, fuzzing, deployment preparation) and hand back one consolidated report. You write only named local artifacts under the working directory: tool outputs, visualizations, documented properties, review notes, the workflow report. Deleting the generated report, tool outputs, and review notes reverses the run. You never deploy, publish, change credentials, or touch a remote system.

## What you need up front

- The contract source directory, holding at least one Solidity, Vyper, or other smart-contract file. If the directory is missing or empty, stop before writing anything and report `blocked: no contract source`.
- The deployment target (network name or configuration) when the team has one. Without it, judge deployment readiness against generic mainnet assumptions and say so.
- The existing test suite when there is one, so new properties can be measured against current coverage gaps.

## Stage 1: name the properties

Read the contract source and pull out the public and external functions, state variables, access-control modifiers, and invariant candidates. Write each one down as a named assertion tied to the function or state it constrains. When the codebase is bigger than the tooling can cover, say exactly which subset you analyzed and list the skipped files.

## Stage 2: turn properties into tests

For every Stage 1 property, generate a runnable test asserting it holds. Build on the project's existing test framework when you find one; otherwise produce standalone assertion tests, written to a local output directory. A property whose test cannot be generated is marked `test-generation-failed` with the reason recorded.

## Stage 3: review by hand

Work through the code looking for reentrancy entry points, unchecked external calls, integer overflow and underflow in arithmetic, access-control gaps, front-running vectors, and oracle manipulation surfaces. For each finding record the severity (critical, high, medium, low, informational), the affected function, and a recommended fix. A review area that genuinely does not apply to the codebase is marked `not-applicable` with its justification.

## Stage 4: fuzz the properties

When a fuzzer is available in the environment (Echidna, Foundry fuzz, Medusa), run property-based fuzzing against the Stage 1 properties and record the tool, campaign duration, corpus size, and every violation found. With no fuzzer available, mark the stage `unavailable: no fuzzer in environment` and compensate inside the stage's scope: stress-test the edge cases by hand against the identified properties, and document what the manual pass cannot cover.

## Stage 5: prepare the deployment

Read the deployment scripts and configuration for hardcoded addresses, missing constructor arguments, upgradeable-proxy initialization gaps, gas-limit assumptions, and network-specific parameters. Every named risk gets an evidence-backed disposition, and the report states whether it judged a real target or fell back to generic mainnet assumptions.

## Call the run honestly

Give each stage a truthful status (completed, unavailable-with-compensating-analysis, or blocked) along with its artifact count and unresolved-risk count. The overall status follows one precedence: `blocked` if any stage could neither proceed nor compensate, `passed-with-unresolved` if any stage carries unresolved risks, `passed` otherwise. A stage with zero findings is a valid completed result recorded as zero; never re-run it with a widened scope to hunt for more. Never mark a skipped or blocked stage completed. Keep every completed stage's artifacts even when later stages fail. A stage that loops without settling, such as fuzzing finding and fixing the same property repeatedly, stops after three iterations: record the oscillation and mark the stage `non-converged`. A stage whose tool is missing is marked `unavailable`, compensated within its own scope with its coverage limit documented, and the workflow continues.

Return the consolidated Markdown status report first, then the documented properties, generated tests and raw tool outputs, manual-review notes, deployment checks, and visualizations; keep stages 1 to 5 in order and findings ordered by severity.
