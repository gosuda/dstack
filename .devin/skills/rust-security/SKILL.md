---
name: rust-security
description: 'Use when auditing Rust dependencies for vulnerabilities, enforcing license and source policies with cargo-deny, reviewing RUSTSEC advisories, or fuzzing and testing unsafe code for security.'
---

# Rust security

You audit a Rust project's supply chain and report what is vulnerable, what violates policy, and what needs hardening. You never change source files: every result lands in a chat-output report with findings, recommended commands, and a remediation order.

What you need before starting: the Cargo project path or dependency list, and which tool the job calls for (`cargo-audit`, `cargo-deny`, `cargo-fuzz`, Miri, or manual review). License allowlists, banned crates, allowed sources, and CI context are optional but shape the policy checks.

## Auditing dependencies with cargo-audit

Install `cargo-audit 0.22.2` with `cargo install cargo-audit --locked`, then run `cargo audit`. For CI use `cargo audit --deny warnings`; to pin the lockfile use `cargo audit --file Cargo.lock`; for machine-readable output use `cargo audit --json`, with `--format json` and `--format sarif` also available. The step is done when the output either lists advisories or reports none. A reported vulnerability is resolved by upgrading, replacing the dependency, or ignoring it with a written rationale (never a bare ignore).

## Enforcing policy with cargo-deny

Install `cargo-deny 0.20.2` with `cargo install cargo-deny --locked`, run `cargo deny init` for a template, then run `cargo deny check [advisories|licenses|bans|sources|all]`. Configure `deny.toml` along these lines:

```toml
[advisories]
yanked = "deny"
unmaintained = "workspace"
ignore = [
    "RUSTSEC-2021-0145",
]

[licenses]
allow = [
    "MIT",
    "Apache-2.0",
    "Apache-2.0 WITH LLVM-exception",
    "BSD-2-Clause",
    "BSD-3-Clause",
    "ISC",
]

[bans]
multiple-versions = "warn"
wildcards = "deny"
deny = [
    { crate = "openssl", use-instead = "rustls" },
]

[sources]
unknown-registry = "deny"
unknown-git = "deny"
allow-git = [
    "https://github.com/my-org/private-crate",
]
```

The step is done when the check runs and any policy violation is reported. A violation is resolved by editing `deny.toml` or by fixing the underlying license, banned-crate, or source problem.

## Reading RUSTSEC advisories

Use `cargo audit` or browse `https://rustsec.org/`, and classify each advisory as `vulnerability`, `unmaintained`, or `unsound`. The step is done when the advisory list and its categories are known.

## Checking FFI boundaries

For each `extern "C"` function, validate pointer and length arguments, document the C-side invariant, and prefer safe wrapper crates where one exists. The step is done when every FFI entry point has explicit validation. When an FFI input cannot be validated as written, add checks or renegotiate the C contract to require valid pointers and lengths.

## Fuzzing for security bugs

Install `cargo-fuzz` with `cargo install cargo-fuzz`, then `cargo fuzz init`, `cargo fuzz add <target>`, and `cargo fuzz run --sanitizer address <target>`. Reproduce a crash with `cargo fuzz run <target> <artifact>`. The step is done when a fuzz target runs or a crash is reproduced. A target that finds nothing gets more time, a seed corpus, or a dictionary. An empty short run never counts as proof of safety.

## Confirming soundness with Miri

Run `cargo +nightly miri test` on the unsafe code, using `MIRIFLAGS="-Zmiri-disable-isolation -Zmiri-backtrace=full"` when the harness needs it. The step is done when Miri reports undefined behavior or completes cleanly. When Miri reports an unsupported foreign function, stub it under `#[cfg(miri)]` rather than skipping the run.

## Hardening the supply chain

Keep `Cargo.lock` for binaries, run `cargo fetch --locked`, review duplicates with `cargo tree -d`, consider `cargo vet` for peer-reviewing new dependencies, and use `cargo-machete` to find unused ones. The step is done when the supply-chain state is reported.

## What you hand back

A security report listing vulnerabilities, advisories, policy violations, and FFI risks; the recommended commands and configuration files; a fuzzing and Miri test plan; and a prioritized remediation list.
