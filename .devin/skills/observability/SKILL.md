---
name: observability
description: 'Use when adding telemetry, composing an observability surface, reviewing alerts, shipping a production feature, or diagnosing a production issue. Not for live failures, profiling, or launch runbooks.'
---

# Observability

When a production feature ships, or an opaque production issue needs diagnosis, the system needs the smallest telemetry surface that still lets on-call answer what broke and why. This skill builds that surface: structured logs, RED/USE metrics, traces, symptom-based alerts, and a dashboard where every panel maps to a failure mode. It covers adding telemetry, composing the surface, reviewing alerting rules, shipping a production feature, or diagnosing an opaque production issue. It does not cover live failures, profiling, or launch runbooks.

You work reversibly and locally here. Write only instrumentation code and local telemetry configuration in the working tree. Rolling back means discarding the edits. Never mutate anything remote.

## What you need before you start

Name the target source files or endpoints to instrument and their runtime (language and framework). Useful extras when they exist: the current logging, metrics, or tracing libraries; a pinned metrics or tracing backend; SLOs or historical latency and error data to justify thresholds; the alert delivery channel and the runbook location. When no backend is pinned, write against the vendor-neutral OpenTelemetry APIs so the exporter can be configured later.

## Confirm the target

Read the named target code and confirm its runtime and the surface you will write to. If you cannot identify the target, stop without writing anything.

## Ask what on-call needs to know

Write down 2 to 4 questions the on-call engineer will ask about this feature. Examples: what fraction of attempts succeed on the first try, why a permanent failure happens, whether the provider is slower than usual. Every signal you add below must answer one of these questions and map to a decision an operator will act on. Reject any signal that does not. If no question can be named, stop and report that the feature needs defined questions before instrumentation. This gate exists to prevent logging everything and learning nothing.

## Map each question to one kind of signal

For each question, pick the signal that answers it: how often or how fast in aggregate calls for a metric; where time goes across services calls for a trace; what happened in one specific case calls for a log. Cover every request-driven endpoint and external dependency with RED (rate, errors, duration). Cover queues, pools, and hosts with USE (utilization, saturation, errors).

## Add structured logging

Write every line as a JSON object with a stable event name and machine-readable fields such as IDs, provider, error code, and attempt count. Never interpolate values into prose strings. Use levels the same way everywhere: `error` for broken invariants that need investigation, `warn` for degraded but handled behavior, `info` for significant business events, and `debug` off in production by default.

## Trace each request across the system

Generate or accept a request ID at the system boundary (the `x-request-id` header when present, else a UUID). Attach it to every log line, span, and outbound call, and echo it on the response. Without it, a single request cannot be reconstructed from interleaved logs.

## Keep secrets out of the telemetry

Never log secrets, tokens, passwords, or unredacted PII. Allowlist the fields you log, and never log whole request bodies.

## Add metrics with bounded labels

Add a latency histogram per endpoint and dependency (for example `http_request_duration_seconds`, with buckets spanning roughly 0.05s to 5s and labels `method`, route template, and `status_class` holding `2xx`/`3xx`/`4xx`/`5xx` classes, never the raw status code). Read p50/p95/p99, never averages. Take labels only from small fixed sets such as route template, status class, and provider name. Never use user IDs, emails, request IDs, full URLs, or error message text as labels.

## Add tracing with the minimum spans that work

Enable OpenTelemetry auto-instrumentation for HTTP, gRPC, and database clients, initialized before application code, with the service name set. Add manual spans only around meaningful internal units of work, carrying the attributes on-call will filter by. Keep the span count at the minimum that reconstructs the critical request path. Propagate context across every async boundary (HTTP headers, queue message metadata), or the trace dies at the gap. Use tail sampling to retain all error traces and a low rate of success traces. When tail sampling is unavailable, use head sampling at a low rate and record that dropped error traces cannot be recovered.

## Define alerts on symptoms, not causes

Alert on what users feel: sustained error rate over a small percentage, p99 latency over seconds, queue age over minutes. Never alert on causes like CPU, pod restarts, or disk usage. Each alert must be actionable (if the response is to ignore it, delete it), link a runbook stating its meaning, first query, and escalation path, carry a threshold and duration justified by the SLO or historical data, and use exactly two severities: `page` for user-facing issues that need action now, and `ticket` for degradation that needs action this week. When no SLO or historical data justifies a threshold, do not guess a number. Record the alert with its query and mark its threshold unjustified; that alert does not meet the completion standard below.

## Build the dashboard around failure modes

Build the dashboard from the failure modes your signals and traces revealed. Every panel must map to a failure mode or one of the on-call questions. Leave out charts no one will read.

## Keep only the surface the team will maintain

Remove any instrumentation, label, span, or panel that duplicates another or that no owner will keep current. A surface no one maintains is not durable, so reuse an existing signal instead of adding a duplicate.

## Verify the surface emits locally

Run the system or a representative test and confirm the surface compiles, loads, and emits: structured logs appear as JSON with the correlation ID intact (no `[object Object]`); metric series appear with the expected labels and sane values; one request traces end to end with no broken spans. If the system cannot run locally, say so plainly and mark local emission unverified. When a check fails (unstructured log output, missing or mislabeled metric series, broken spans), treat it as an instrumentation bug, fix the instrumentation, and re-run the failed checks. Never claim completion with a failing or unexecuted check. All changes are working-tree edits, so rollback is discarding or reverting them.

## What you hand back

The modified target source files carrying structured logs, metrics, tracing setup, alert definitions, and dashboard panels grouped by failure mode; the written on-call questions; the alert list with runbook links; and a local verification report marking each check pass or fail. Keep the parts that pass and list every check result in the report. Never swallow errors or claim completion when it does not hold. Close with one of two readings: done when all local checks pass, or blocked naming the failing, unjustified, or unverifiable item. When the system cannot run locally, the edits stand but completion is not reached: blocked with telemetry unverified.
