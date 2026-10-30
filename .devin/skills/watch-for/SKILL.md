---
name: watch-for
description: 'Use when monitoring a file, log, endpoint, or artifact for drift or errors, or polling a target until a predicate holds. Modes: watch (default), until. Not for source or remote-system changes.'
---

# Watch for

You sit on a changing surface and say what changed. In the default `watch` mode you sample a file, URL, log, or artifact on an interval, judge each sample against your anomaly criteria, and finish with a summary when the stop condition arrives. In `until` mode you poll a target until a falsifiable completion predicate holds, then report the terminal verdict. Either way you only read, you never mutate anything remote, and you never pretend a predicate holds when it does not.

What you need before starting:

- Mode, required: `watch` (the default) or `until`.
- Surface address for `watch`, or target for `until`, required: the file, URL, log, or artifact to observe or poll.
- Anomaly criteria, required for `watch`: the condition, pattern, threshold, or structural rule that marks a sample anomalous.
- Completion predicate, required for `until`: a falsifiable condition checked against the current observed state on each poll.
- Sampling or poll interval, required: seconds between reads, a cron expression, or an event-driven trigger name.
- Stop condition, required for `watch`: a predicate that ends the watch on its own, or an explicit tick count after which it stops.
- Deadline or maximum poll count, required for `until`: the watch stops at whichever comes first.

## Binding the surface and taking a baseline

Record the mode, the address, the interval, and the mode-specific control (anomaly criteria for `watch`, completion predicate plus deadline and max polls for `until`). Refuse anything outside that declared scope. Then read the surface once and record the baseline snapshot.

## Judging each tick in watch mode

Wait the interval and sample the surface. If the sample will not read, emit an error judgment naming the surface and the reason, then wait for the next interval rather than widening scope or inventing data. A sample that arrives but cannot be trusted is marked stale-data, and the tick still counts.

Compare each good sample against the baseline with the anomaly criteria. Classify it as normal, anomalous, error, or stale, and emit a judgment carrying the address, the timestamp, what changed or why the read failed, and the severity when anomalous. Then move the baseline forward to the current sample.

When the stop condition is met, end with a final summary: total ticks, anomaly count, error count, and final surface state. If someone asks you to look beyond the bounded surface, refuse, report the refusal, and keep watching the declared surface. If the stop condition proves unreachable, say so and keep going until stopped by hand.

## Polling to a verdict in until mode

On each poll, check the completion predicate against the current observed state. When it holds, stop and report `predicate-holds` with the final state.

Stop and report `blocked`, with the read failure and the last known state, when the target is unreadable or has disappeared (never restart or recreate it) or when the predicate itself is unparseable or ambiguous (never infer a replacement). Stop and report `non-converged`, with the last observed state and the poll count, when the deadline or maximum poll count arrives. Also stop with `non-converged` when the target oscillates, meaning the same two or more distinct states repeat in a cycle of 3 consecutive polls without the predicate holding; include the oscillation pattern and count. Otherwise poll again.

## What you hand back

- In `watch` mode: a stream of per-tick judgments (surface address, timestamp, classification as normal, anomalous, error, or stale, what changed or why the read failed, severity when anomalous), plus the final summary on stop.
- In `until` mode: one terminal classification. `predicate-holds` carries the final observed state. `non-converged` carries the last observed state, the poll count, and the failure class that stopped it. `blocked` carries the failure reason and the last known state.
