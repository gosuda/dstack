# Project setup and testing

Set up a project structure before using YAML rules to lint or scan a codebase.

## Scaffolding

Use the CLI to create a new project:

```bash
ast-grep new project
```

This creates the standard directory structure:

```
project-root/
├── sgconfig.yml         # Root configuration
├── rules/               # Rule definitions (.yml)
├── rule-tests/          # Test cases (.yml)
└── utils/               # Reusable utility rules
```

## Configuration (`sgconfig.yml`)

The `sgconfig.yml` file defines where ast-grep looks for rules and tests.

```yaml
# List of directories containing rule files
ruleDirs:
  - rules

# List of directories containing utility rules
utilDirs:
  - utils

# Configuration for tests
testConfigs:
  - testDir: rule-tests
```

## Testing rules

Test rules to confirm they match what you expect and produce neither false positives (noisy matches) nor false negatives (missing matches).

### Test file structure

Test files (e.g., `rule-tests/my-rule-test.yml`) map test cases to a rule ID.

```yaml
id: my-rule-id # Must match the 'id' in your rule YAML
valid:
  - "const x = 1;" # Code that should NOT trigger the rule
  - "var y = 2;"
invalid:
  - "const x = eval('1');" # Code that SHOULD trigger the rule
  - "eval(foo);"
```

### Running tests

```bash
# Run all tests
ast-grep test

# Update snapshots for human review of diagnostic or fix changes
ast-grep test -U

# Interactive mode
ast-grep test -i
```

### Snapshots and verification

When you run tests with `-U`, ast-grep creates or updates a `__snapshots__` directory storing diagnostic messages and fix replacements for invalid cases. Treat snapshots as human review aids to inspect diffs during development, never as an automated acceptance oracle or proof of correctness. Saved output wording pins broken or unintended behavior.

Automated acceptance relies on independent invariants:
- Valid cases serve as input fixtures proving that conforming constructs, edge cases, and non-target code do not trigger the rule.
- Invalid cases serve as input fixtures that exercise target patterns, syntax boundaries, and adversarial variants to prove the rule triggers where intended.
- Fix transformations must be verified against independent invariants, ensuring the rewritten code produces valid syntax and the expected target AST structure rather than relying on brittle snapshot string matching as an oracle.
