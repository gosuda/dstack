---
name: fastopt
description: 'Use when optimizing suspected hot paths without waiting for benchmarks. Not for estimated hot and cold analysis: use fastopt-extreme. Not for measured-floor campaigns: use optimize-extremely.'
---

# Fastopt

Your job is to turn each suspicion into a labeled hypothesis plus a benchmark design that could confirm or refute it, and to stop there. This skill is read-only: no file, VCS, credential, paid, published, deployed, or remote change. You emit hypotheses and benchmark designs as chat output, and you make no speed claim. Broader read-only hot-and-cold analysis belongs to `fastopt-extreme`, and a full measured campaign belongs to `optimize-extremely`; naming a peer never runs it. A path that stays blocked is reported as blocked with its reason, never reshaped into success.

## Name the paths and the workload

You need, per suspected path, the file, function, or call site the user names plus the workload or input shape that makes it potentially hot. Prior measurements, profiling traces, or environment constraints are welcome when offered; absent measurements mean unmeasured, never evidence of slowness. If the hot path is ambiguous, ask the user to name the path and workload and stop rather than guess.

## Read each path before theorizing

Read the source and surrounding call graph read-only, and record the inputs, allocations, loops, and branches that plausibly dominate cost. Every named path gets read and its cost-plausible elements recorded before any hypothesis is written.

## Label every cost a hypothesis, never a finding

Each observation carries its assumed workload, its assumed dominant operation, and its assumed magnitude rank, with no speed claim attached. Anything unmeasured is marked unmeasured; do not infer slowness from absence of data.

## Design the benchmark that would settle it

Every hypothesis gets a benchmark design naming all seven elements: metric, baseline, variant, workload generator, warm-up, repetition count, and noise controls. Keep the implied change scoped to the named path; do not propose edits outside it or assume a fix is correct. If a hypothesis cannot be tested without mutating code, state the minimal mutation that would unblock measurement and the reason it blocks, then stop before performing it.

## What you hand back

A chat report with, per suspected hot path, one labeled hypothesis (workload, dominant operation, magnitude rank, no speed claim) and one benchmark design (metric, baseline, variant, workload generator, warm-up, repetitions, noise controls). Blocked paths are reported as blocked with the reason. No mutation, no speed claim.
