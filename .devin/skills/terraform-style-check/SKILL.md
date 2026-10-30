---
name: terraform-style-check
description: 'Use when writing, reviewing, or generating Terraform HCL that must pass fmt and validate. Not for module authoring, state operations, `terraform apply`, or remote state.'
disable-model-invocation: true
---

# Terraform style check

Terraform configurations drift toward misplaced blocks, loose names, unpinned versions, and open security defaults. This skill brings a root module or a set of `.tf` files back to file organization, naming, version pinning, and security best practices, and proves it with `terraform fmt` and `terraform validate`. Reach for it when writing, reviewing, or generating Terraform HCL. It does not cover module authoring, state operations, `terraform apply`, or remote state.

You work reversibly and locally: write only the named local HCL files, with rollback through version control. Never mutate anything remote.

## Limits that hold for the whole run

- Never run `terraform apply`, `terraform plan`, or any state-mutating command.
- Never touch files outside the declared target set, except that the file-organization step below may create or modify conventionally named destination files (`main.tf`, `<resource_type>.tf`, `variables.tf`, `outputs.tf`, `versions.tf`) when moving blocks into them.
- Never suppress, comment out, or work around a validation diagnostic. The HCL is not valid until the diagnostic resolves.
- Never install the Terraform CLI if it is missing.

## What you need before you start

- The target directory or files: the Terraform root module or specific `.tf` files to check. The target must exist on disk.
- The Terraform CLI: `terraform` must be available on PATH.
- Style overrides (optional): project-specific naming prefixes or security exceptions. When absent, the defaults below apply.

## Working through the module

1. Define the target scope. Enumerate the `.tf` files under the target directory and record the file set. Do not read or modify files outside this set.
2. Fix file organization. Each resource type lives in its conventionally named file: `main.tf` for provider and terraform blocks, `<resource_type>.tf` for resources, `variables.tf` for variable declarations, `outputs.tf` for outputs, `versions.tf` for required_providers and required_version. Move misplaced blocks into their conventional file, creating it when it does not exist yet.
3. Fix naming. Use snake_case for all resource, variable, output, and local names. Give each resource a descriptive suffix matching its type (`aws_instance.web_server`, not `aws_instance.this`). Give each variable a descriptive noun (`vpc_cidr_block`, not `cidr`).
4. Pin versions. Every provider in `required_providers` needs an exact version constraint (`= X.Y.Z` or `~> X.Y.Z` with the minor pinned). Every registry `module` source needs a `version` constraint and every Git `module` source pins `?ref=`; record local-path modules as manual-review since they accept no version constraint. Fill missing provider pins from the currently resolved version in `.terraform.lock.hcl` when available; for modules use the registry version or `?ref=`, or flag for manual review. Flagging a missing pin for manual review is a non-blocking partial success: the step counts as done for that provider or module, and the flag goes into the compliance report.
5. Apply security defaults. S3 buckets need `server_side_encryption_configuration`, public access blocks (`block_public_acls`, `block_public_policy`, `restrict_public_buckets`, `ignore_public_acls`, all `true`), and `versioning` enabled. Security groups default to deny-all ingress. RDS instances need `storage_encrypted = true` and `publicly_accessible = false`. EC2 instances need `metadata_options.http_tokens = "required"`. Apply the defaults where missing, unless the file carries an explicit `# tfsec:ignore` or `# checkov:skip` annotation for that resource.
6. Run `terraform fmt -recursive -diff` on the target scope. When the input is a specific file list rather than a directory, run `terraform fmt -diff` on each file individually instead of `-recursive`. Capture stdout and stderr. This step passes when `terraform fmt` exits zero.
7. Run `terraform validate` on the target directory. When the input is a specific file list rather than a directory, skip `terraform validate` (it needs a full module directory) and note the skip in the compliance report. Capture stdout and stderr. This step passes when `terraform validate` exits zero, or when the skip is recorded for single-file input.
8. Re-enumerate the target `.tf` file set. Confirm no file outside the original set was created or modified, except conventionally named destination files from step 2. List any new conventionally named files explicitly.
9. Report the final state. List each file touched, each check category (organization, naming, version pinning, security) with pass or fail, and the terraform fmt and validate exit codes.

## When something goes wrong

- Syntax or validation error: report the exact terraform validate diagnostic. Do not suppress, comment out, or work around the error. The HCL is not valid until the diagnostic resolves.
- Scope expansion: stop immediately. Report which files were created or modified outside the original target set and the conventionally named destination files step 2 allows. Revert the out-of-scope changes with `git checkout` or manual deletion.
- Missing terraform CLI: report that `terraform` is not available on PATH and stop. Do not attempt installation. The check cannot proceed.
- Partial result (steps 1 through 5 pass, step 6 or 7 fails): intermediate HCL changes stay on disk. The failure report names the step that failed and the files already modified. The user decides whether to keep or revert.

## What you hand back

The formatted and validated HCL files in place, plus a compliance report listing files touched, per-category pass or fail (organization, naming, version pinning, security), and the terraform fmt and validate exit codes. On failure the report adds the specific diagnostic, the failed step, and the set of files modified before the failure.
