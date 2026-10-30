# Running broad metric searches without losing the plot

An optional extension to the primary hot-path optimization loop. Use when the target has
a measurable metric but the search space is broad (parameter tuning, prompt optimization,
threshold finding, configuration search) rather than a single hot-path transform.

The primary optimize loop (five-lens fan-out, benchmark, gate, commit) remains the default.
Experiment mode applies only when the conditions below are met.

## When this mode earns its keep

- The optimization target has a measurable metric (latency, accuracy, cost, throughput) but
  no single obvious hot-path transform addresses it.
- The search space is combinatorial: configuration parameters, prompt variants, threshold
  values, feature toggles, preprocessing pipelines.
- Hard metrics alone may be gameable: LLM-as-judge can catch degenerate solutions that
  optimize the metric without improving the real objective.
- NOT for single hot-path transforms. That is the main optimize loop's job.

Start serial (no parallel experiments), cap iterations at 10-15, and use the smallest sample
sizes that still pass the variance check. Scale up only after the loop proves productive.

## Holding the loop to a measured baseline

1. **Set the harness before dreaming up hypotheses.** The harness is the
   contract: it says what is measured, how, and with what parameters. No harness, no
   experiments.
2. **Pin the baseline and check its variance.** Stddev must be under 20% of the median. Fix
   noise before proceeding (pin CPU, isolate the process, widen the sample count).
3. **Each experiment:** apply the variant, measure, and record the result to disk immediately.
4. **Read back every critical write.** Disk is the source of truth, not
   context or memory.
5. **Leave crash-recovery markers.** In worktrees, mark each experiment's state so an interrupted
   run can resume without re-running completed work.
6. **Write a short strategy digest after each batch.** Sum up what worked, what failed, and what
   to try next. This keeps context bounded across long runs.

## What lives in the experiment log

Run state lives at `.outline/optimize/<target>/experiment-log.yaml`.

The `experiments` list is append-only: each experiment record is written
the moment it completes and never rewritten. The `best` and `hypothesis_backlog` fields
are mutable checkpoint state: rewritten after each batch evaluation, once the batch
results are verified on disk. On crash recovery, replay `experiments` to reconstruct
`best`. The `hypothesis_backlog` cannot be replayed from experiment records (unexecuted
entries are not recorded); recover it from the latest checkpoint; if the checkpoint is
missing, regenerate from scratch using the current code state and experiment history.

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
    outcome: <enum>      # measured | kept | reverted | degenerate | error | timeout
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

### What each outcome means

- `measured`: raw metrics persisted, awaiting batch evaluation
- `kept`: improved primary metric, gates passed
- `reverted`: did not improve
- `degenerate`: gate failed (metric gamed, output degenerate)
- `error` / `timeout`: measurement failure

## Knowing when to stop

Evaluate before each new experiment. Stop on the first that trips:

- Target reached. Primary metric meets the defined target.
- Max iterations. Total experiments >= configured cap.
- Max wall-hours. Wall-clock since `started_at` exceeds the cap.
- Plateau. No improvement for N consecutive experiments (N configurable, default 5).
- Judge budget exhausted. Cumulative judge spend >= cap (when using judge mode).
- Empty backlog. No hypotheses remain and no new ones can be generated.

## Judging quality a raw number cannot catch

Use when the metric can be gamed or human judgment matters: clustering quality, search
relevance, summarization quality, prompt quality.

### Three passes, cheapest first

1. **Degenerate gates** (hard, cheap, fast). Catch obviously broken solutions. Run first.
   If gates fail, skip the expensive judge step. Examples: output length bounds, format
   compliance, non-empty checks, deduplication rate thresholds.
2. **LLM-as-judge** (the actual optimization target). Sample outputs, score against a
   rubric, aggregate. This is what the loop optimizes. Use a 1-5 scale with concrete
   per-level descriptions. Include supplementary diagnostic fields. Make the rubric
   specific enough for inter-judge consistency.
3. **Diagnostics** (logged, not gated). Distribution stats, counts, timing, useful for
   understanding why a judge score changed, not for accept/reject decisions.

### Writing a rubric two judges can share

- 1-5 scale with concrete per-level descriptions (not vague "good/bad").
- Supplementary diagnostic fields: what specifically was scored, what drove the rating.
- Specific enough that two independent judge runs on the same output converge.

### Sampling without fooling yourself

- Stratified by output characteristics (length, complexity, domain).
- Include edge cases and singletons when coverage matters.
- Sample size: minimum 5 per stratum for stable estimates; scale up for high-variance
  domains.

## Keeping the hypothesis pipeline fed

1. Analyze current code and configuration to identify improvement opportunities.
2. Generate 10-30 initial hypotheses. Each has: description, category, priority.
3. Categories (adapt to domain): signal-extraction, algorithm, preprocessing,
   parameter-tuning, architecture, data-handling.
4. Dependency pre-approval: collect all new dependencies upfront and present for bulk
   approval before iterating. Do not pause mid-loop for dependency approval.
5. After each batch, update the hypothesis backlog based on learnings. Prune dead ends,
   promote promising directions, add newly discovered opportunities.
