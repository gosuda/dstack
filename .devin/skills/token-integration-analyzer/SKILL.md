---
name: token-integration-analyzer
description: 'Use when a token implementation or integration needs standards, privilege, nonstandard-behavior, and defensive-integration analysis. Not for source or remote-system changes.'
disable-model-invocation: true
---

# Token integration analyzer

A team ships a token or builds on someone else's, and wants to know where the bodies are buried: does it follow the standard, who holds power over it, which nonstandard behaviors it exhibits, and what an integrating protocol must do to survive them. You read the code, work every applicable category in `references/assessment-categories.md`, optionally check the live chain, and hand back a structured security report ending in prioritized remediation. Each recommendation ties one unsafe assumption to one concrete defensive change. You change nothing: no file writes, no credential use, no remote mutation, so there is nothing to roll back.

## What you hand it

- A codebase or contract source the session can read.
- The context: token implementation, token integration, or both.
- The token type: ERC20, ERC721, or both.
- Optionally, the deployed contract address together with an RPC endpoint URL. The address is required for on-chain scarcity and holder analysis, and the endpoint is required whenever the address is supplied.

## Honesty limits

- Never fabricate on-chain facts when the address or RPC endpoint is absent.
- Never invent evidence or call external tools outside this procedure.
- Never label a behavior confirmed when static code alone cannot establish it; label it unverified.

## How the analysis runs

### Name the context

Classify the work as implementation, integration, or both. Identify the platform (Ethereum, another EVM chain, or non-EVM) and confirm which token types are under analysis.

### Run the Solidity tooling

On Solidity with Slither available, run `slither-check-erc` for ERC20 or ERC721 conformity, `slither --print human-summary` for complexity and upgrade analysis, and `slither --print contract-summary` for the function inventory, capturing all output verbatim. Without Slither, verify every ERC conformity criterion by hand and document each manual check so the gap is visible.

### Work every applicable category

Evaluate each checklist item in `references/assessment-categories.md` against the codebase and produce a compliance finding of pass, warning, or fail with file and line references. The categories cover general considerations (audit history, team transparency, security contact), contract composition (complexity, arithmetic guards, non-token functions, single entry point), owner privileges (upgradeability, minting caps, pausability, blacklisting, accountability), ERC20 conformity and extension risks, the 24 weird ERC20 patterns, token integration safety (SafeERC20 transfer patterns, balance verification, allowlists, wrappers, reentrancy guards), and the ERC721 conformity and risk checklists.

### Read the chain when you can

When address and RPC endpoint are both supplied, retrieve the name, symbol, decimals, totalSupply, owner or admin address, and pause status, then map holder distribution and concentration. When either is missing, omit the on-chain scarcity and holder analysis and note the exclusion in the report.

### Write the remediation report

Order the report as executive summary (overall risk level with critical and high counts), per-category findings (pass, warning, or fail with evidence), the weird-token-pattern table (each applicable pattern with presence, risk level, evidence, and mitigation), the on-chain analysis (when an address was supplied), the integration-safety assessment (when a protocol integration was analyzed), and the prioritized recommendations grouped CRITICAL (fix before deployment), HIGH (fix soon), MEDIUM (improve), LOW (best practice). Every recommendation ties one unsafe assumption to one concrete defensive change.

## When something gives

- `no-token-code`: the codebase holds no token-related source. Say so and stop.
- `slither-unavailable`: Slither is not installed or not on PATH. Continue with manual ERC conformity verification and document each manual check.
- `on-chain-unavailable`: no contract address or no RPC endpoint. Omit the on-chain scarcity and holder analysis and note the exclusion.
- `behavior-undetermined`: the behavior cannot be inferred from static code alone. Label the assumption unverified rather than fabricating a finding.
- `scope-widening`: the next step would reach past token safety. Stop at the boundary instead of inventing evidence or calling outside tools.

Return findings for every category that succeeded; mark each blocked category unevaluated with its failure class and reason.
