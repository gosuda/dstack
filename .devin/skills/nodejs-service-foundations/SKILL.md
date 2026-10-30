---
name: nodejs-service-foundations
description: 'Use when asked to set up or harden Node.js service foundations: env validation, logging, typed errors, type stripping, and shutdown wiring. Not for dedicated shutdown: use nodejs-graceful-shutdown.'
---

# Node.js service foundations

You give a new or rough Node.js service a solid base: config that fails fast, logs that never leak secrets, errors the middleware can actually route, and a startup that runs clean under the compiler. When the job needs a full drain sequence with health flip and dependency teardown, hand that part to nodejs-graceful-shutdown; here you only wire the shutdown spine (signal to abort to exit).

This stays local and reversible. You write only the named local artifacts (env schema, logger, error classes, tsconfig, package scripts) and install the dependencies they declare. Rollback is version control: `git checkout -- <written files>` or deleting the listed untracked files. No remote mutation.

What you need before starting:

- Project root: directory containing or to receive `package.json`. Required.
- Environment variables: each name with its type and whether it is required or optional with a default. Required.
- Secret field names: env keys whose values must be redacted in log output. Required.
- Error catalogue: list of `{ code, message, httpStatus }` tuples for the domain errors. Required.
- Logger dependency: the structured logger in use (for example pino). Required, stated up front, not discovered midstream.

## Validate env before the server binds

Create `src/env.ts`. It reads `process.env` at import time and parses each declared variable against its type (string, number, boolean, URL). A required variable that is missing or malformed throws a descriptive error and the process exits with code 1 before any server binding. Export the frozen validated config object. The service never starts on invalid or missing config.

## Log structured JSON with secrets redacted

Create `src/logger.ts` on the stated logger dependency. Configure the level from env, ISO-8601 timestamps, and a request-id correlation field. Add a redaction serializer that replaces the value of every secret field name with `[REDACTED]` at every log level. Export a singleton instance. If a secret value ever appears unredacted in output, stop: the field-name list or serializer is misconfigured, and you fix it before proceeding.

## Throw errors the middleware can route

Create `src/errors.ts`. It exports a base `ServiceError` with `code: string`, `message: string`, `httpStatus: number`, and `cause?: Error`, plus one named subclass or factory per catalogue entry. Every entry keeps a working `instanceof ServiceError` check so middleware can map codes to HTTP responses, and every code maps to its declared status. A catalogue entry with no subclass or status is a defect: add the missing piece before moving on.

## Wire the shutdown spine

In the service entry point, create an `AbortController`. Listen for `SIGTERM` and `SIGINT`, call `controller.abort()`, pass the signal to in-flight operations, drain active requests, then exit `0` on a clean drain or non-zero on timeout. This is the spine only. The full handler with health flip and dependency teardown is the job of nodejs-graceful-shutdown.

## Confirm startup, failure, types, and redaction

Run these checks and keep every result:

- Start with valid env: the server binds and the startup log is structured JSON with secrets redacted.
- Start with a required variable missing: the process exits code 1 with a descriptive message before binding.
- Run `tsc --noEmit`: zero errors. Fix type errors directly; never suppress with `@ts-ignore` or `any`.
- Instantiate one error subclass: `instanceof ServiceError` is true and its `httpStatus` matches the catalogue.
- Log a record containing a secret field name: the output shows `[REDACTED]`.
- If a stated logger or required package is missing, install it with the project package manager. If installation fails, stop and report it.

## What you hand back

Local named files: `src/env.ts` (validated schema), `src/logger.ts` (structured JSON with redaction), `src/errors.ts` (typed `ServiceError` base and subclasses), `tsconfig.json` (strict type-stripping config), `package.json` (ESM, engines, scripts). All reversible through the stated rollback path, with proof covering startup logs, the invalid-env exit, `tsc`, the instanceof check, the HTTP mapping, and redaction.
