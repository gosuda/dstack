---
name: decoded-memo-retention
description: 'Use when a query-scoped decoded-block cache is bounded only by serialized work bytes, or when fallback paths retain many decoded blocks. Not for total-process memory promises: this skill never claims a process-wide bound.'
---

# Decoded memo retention

Some query-scoped decoded-block cache is bounded only by serialized work bytes or request count while retaining decoded heap across many block identities, and memory amplification from repeated fallback paths needs review. Your job is to give that memo a real retention contract: at most one decoded block retained through the memo itself, proven by measurement and regression tests. You never claim a process-wide bound.

You work locally and reversibly: the named memo, its ownership and eviction contract, one explicitly bounded local measurement instrument, and authorized regression coverage. A production cache-policy change stays human-gated. No remote changes, credentials, deployment, paid services, or automatic commit. Single-bottleneck speed work belongs to `optimize`, and a full measured-floor campaign belongs to `optimize-extremely`; naming a peer never runs it.

## Map the risk before changing anything

Trace the full-block fallback path, the cache ownership, and the lifetime of returned handles. Establish the representative workload: candidate identities whose full identity does and does not match the request, including consecutive-identity reuse. Find out whether untrusted queries can visit many distinct block identities. A serialized-byte work budget does not establish a decoded-heap retention bound: a query can retain many decoded blocks, and concurrent requests multiply that retained state. You are ready to continue when the fallback path, ownership, handle lifetime, and reachable identity set are all stated.

## Keep admission charges separate from retention

Keep existing read-count and byte charges unless the task explicitly changes them. Do not relabel serialized bytes as heap bytes. The retention contract is stated on its own, next to the admission charges, never merged into them.

## Choose the retention shape

When consecutive-identity reuse meets the requirement, prefer a single entry keyed by the complete `(height, hash)` identity over a map of every block visited. When retaining multiple identities is genuinely required, define a real decoded-memory policy instead. Never ship the map as a bound: if consecutive reuse does not meet the requirement and no decoded-memory policy is authorized, stop blocked.

## Measure owned retention before touching the bound

The metric is decoded bytes owned through the memo under the representative workload. State the tool, the input identities, the conditions, and the repeat count; record before bytes with observed variance. Never substitute process RSS: allocator behavior, fragmentation, and other owners can hold RSS steady while owned retention falls. Keep this ownership measurement separate from fetch-count evidence. If the measurement cannot clear its variance band, stop blocked until the noise clears.

## Release before replacing

- On a cache hit, reuse the shared handle without another fetch or decode.
- On an identity miss, release the previous cached block before fetching and decoding the replacement.
- Cache only successfully verified blocks. Verification gates caching: a block that failed verification must never be served, and a stale or unverified block found in the memo is reverted immediately.
- Revisiting an evicted identity reads and charges it again.

## Re-measure, then keep or revert

Repeat the measurement under the same workload, method, conditions, and repeat count. Record after bytes with variance and the before-and-after difference. Revert neutral results, regressions, and any win obtained by dropping required freshness or verification. If the bound adds no retention benefit or costs correctness or performance, report the non-win honestly with before-and-after evidence, and never reframe it as an RSS win.

## Remember what the slot does not bound

Inspect callers for handles retained across iterations. A single cache slot bounds cache-owned retention only, not arbitrary caller-held handles, output allocations, transient decode memory, or total process heap. Enumerate caller-held retention and exclude it from the cache-owned bound.

## Prove ownership and query behavior with regressions

- Ownership: retain a block only through the memo, keep a weak reference, miss on another identity, and assert the weak reference can no longer upgrade before inserting the replacement. Cover exact-identity hits and release when the query budget drops. If the weak reference still upgrades after an identity miss, the previous block is retained outside the memo: restore release-before-replace and re-prove.
- Query behavior: exercise several candidate heights whose full script identity does not match the request, verifying correct empty results and distinct-identity body reads. Preserve the existing same-block reuse and cross-query isolation tests.

## Mutate to prove the tests are load-bearing

Two mutations, each restored surgically with a source-hash comparison against the verified pre-mutation content (never a whole-file restore from HEAD over uncommitted worker changes):

1. Restore the actual old map representation and methods while keeping the new tests. The retention assertion must fail; a compile failure does not count as proof.
2. Remove identity matching. The distinct-height test must fail.

If either mutation passes, the tests do not prove retention: repair them before claiming the bound.

## Keep the cold path spare

Refuse added layers, flags, caches on caches, or indirection bought for cold-path microseconds. The bound stays a single slot plus its explicit eviction and invalidation terms.

## Write it down beside the owning contract

Document precisely beside the owning contract clause: the memo retains at most one decoded block. Do not write that every identity is decoded once during the query, or that the process cannot run out of memory. Place the retention requirement with the exact eviction, reuse, fallback, ownership measurement, and mutation test names. Keep benchmark and total-memory claims separate from fetch-count and ownership evidence. Return a ledger per attempt: candidates, evidence paths, before and after owned bytes with tool and variance, behavior result, and verdict.

## Stop conditions

- The retention pool cannot be established from inspected source, the measurement stays noisy, or multiple identities are required with no authorized policy. Result: blocked. Do not invent candidates or ship the map as a bound.
- The change needs production rollout, credentials, remote mutation, or paid services. Result: document the requirement and stop without widening authority.

## What you hand back

The bounded memo with its single-identity retention contract, release-before-replace eviction, before-and-after retained decoded ownership with tool and variance, green ownership and query regressions, both mutation results with restored source hashes, and the exact test names beside the owning clause. On failure, the precise blocked, reverted, or non-win state with measurements and the exact blocker. Never a total-process memory bound.
