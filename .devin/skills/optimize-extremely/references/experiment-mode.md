# Optimize-extremely experiment extension: metric-driven broad search

An optional extension to the `optimize-extremely` hot-path campaign. Use when the target has
a measurable metric but the search space is broad: parameter tuning, threshold finding,
configuration search, or preprocessing search, rather than a single hot-path transform.

The campaign five-lens fan-out, benchmark, gate, and commit loop remains the default.
This extension applies only when the conditions below are met.

## When to use this extension

- The optimization target has a measurable metric (latency, accuracy, cost, throughput) but
  no single obvious hot-path transform addresses it.
- The search space is combinatorial: configuration parameters, threshold
  values, feature toggles, or preprocessing pipelines.
- Hard metrics alone may be gameable: a judge rubric can catch degenerate solutions that
  optimize the metric without improving the real objective.
- Never for single hot-path transforms. That is the main campaign loop's job.
- Never a silent conversion of a runtime request into prompt optimization or arbitrary
  repository tuning. The request must explicitly name the measurable search target.

## Benchmark loop discipline

1. Define the measurement harness before generating hypotheses. The harness is the
   contract: it specifies what is measured, how, and with what parameters. No harness, no
   experiments.
2. Run baseline measurement with the variance check. Standard deviation must sit below 20
   percent of median, matching the campaign condition. Fix noise before proceeding (pin CPU,
   isolate process, widen sample count).
3. Each experiment: apply variant, measure, record result immediately to disk.
4. Verify writes. Read back every critical write. Disk is the source of truth, not
   context or memory.
5. Crash-recovery markers. In worktrees, mark each experiment's state so an interrupted
   run can resume without re-running completed work.
6. Strategy digest after each batch. Compress learnings into a short summary after every
   batch of experiments: what worked, what failed, what to try next. This keeps context
   bounded across long runs.

## Experiment-log schema

Run state lives at `.outline/optimize/<target>/experiment-log.yaml`.

Persistence model: `experiments` is append-only. Each experiment record is written
the moment it completes and never rewritten. A later evaluation (kept, reverted,
degenerate, error, timeout) is appended as a transition record keyed to the same
experiment iteration; the original `measured` record stays intact. The `best` value is
reconstructed from appended events on recovery, and the `hypothesis_backlog` below is
mutable checkpoint state: rewritten after each batch evaluation once the batch
results are verified on disk. On crash recovery, replay `experiments` to reconstruct
`best`. The `hypothesis_backlog` cannot be replayed from experiment records (unexecuted
entries are not recorded); recover it from the latest checkpoint, and when the checkpoint
is missing, regenerate it explicitly from the current code state and experiment history.

```yaml
spec: <string>           # optimization spec name
run_id: <string>         # unique run identifier
started_at: <timestamp>  # ISO 8601
baseline:
  timestamp: <timestamp>
  metrics:
    <name>: <value>      # gate and diagnostic metrics
experiments:             # ordered list, append-only during iteration
  - iteration: <int>
    batch: <int>
    hypothesis: <string>
    category: <string>
    outcome: <enum>      # measured, then a later appended transition: kept | reverted | degenerate | error | timeout
    metrics: <object>
    learnings: <string>
    commit: <string>     # SHA if kept
best:
  iteration: <int>
  metrics: <object>
hypothesis_backlog:      # remaining hypotheses
  - description: <string>
    category: <string>
    priority: <enum>     # high | medium | low
```

### Outcome state transitions

- `measured`: raw metrics persisted, awaiting batch evaluation. Never rewritten.
- `kept`: a later appended transition records an improved primary metric with gates passed.
- `reverted`: a later appended transition records no improvement.
- `degenerate`: a later appended transition records a gate failure (metric gamed, output degenerate).
- `error` / `timeout`: a later appended transition records measurement failure.

## Stopping rules

Evaluate before each new experiment. Stop on the first that trips:

- Target reached. Primary metric meets the defined target.
- Explicit user limit reached. Wall time, attempt count, spend, or marginal-gain floor the
  user set is met. There are no default iteration, wall-time, plateau, or marginal-gain
  caps in this extension. Reaching an explicit limit with work outstanding is incomplete,
  never success.
- Empty backlog. No hypotheses remain and no new ones can be generated from current evidence.

## Judge rubric (for qualitative metrics)

Use when the metric can be gamed or human judgment matters: clustering quality, search
relevance, summarization quality, prompt quality. A paid or remote judge is outside local
authority. Never invoke one merely because this reference describes a judge rubric; use only
an authorized local judge or no judge.

### Three-tier approach

1. Degenerate gates (hard, cheap, fast). Catch obviously broken solutions. Run first.
   When gates fail, skip the expensive judge step. Examples: output length bounds, format
   compliance, non-empty checks, deduplication rate thresholds.
2. Local judge (the actual optimization target). Sample outputs, score against a
   rubric, aggregate. This is what the loop optimizes. Use a 1-5 scale with concrete
   per-level descriptions. Include supplementary diagnostic fields. Make the rubric
   specific enough for inter-judge consistency.
3. Diagnostics (logged, not gated). Distribution stats, counts, timing, useful for
   understanding why a judge score changed, not for accept or reject decisions.

### Rubric design

- 1-5 scale with concrete per-level descriptions (not vague "good" or "bad").
- Supplementary diagnostic fields: what specifically was scored, what drove the rating.
- Specific enough that two independent judge runs on the same output converge.

### Sampling strategy

- Stratified by output characteristics (length, complexity, domain).
- Include edge cases and singletons when coverage matters.
- Sample size: minimum 5 per stratum for stable estimates; scale up for high-variance
  domains.

## Hypothesis generation

1. Analyze current code and configuration to identify improvement opportunities.
2. Generate 10-30 initial hypotheses. Each has: description, category, priority.
3. Categories (adapt to domain): signal-extraction, algorithm, preprocessing,
   parameter-tuning, architecture, data-handling.
4. Dependency pre-approval: collect all new dependencies upfront and present for bulk
   approval before iterating. Do not pause mid-loop for dependency approval.
5. After each batch, update the hypothesis backlog based on learnings. Prune dead ends,
   promote promising directions, add newly discovered opportunities.
