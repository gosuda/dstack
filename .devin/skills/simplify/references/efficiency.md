# Cost signals: triage aid for routing

This file used to be a verbatim detector prompt for an old diff-only pass. That pass is gone: simplify now routes each cut to its owning skill, and no live routee owns standalone performance tuning, so cost concerns ride along with a structural route rather than dispatching on their own. What survives here is the pattern list, repurposed as triage signals that sharpen the owning skill's brief. The owning skill decides, using its own contract.

## How to use these signals

Match what you see in and around the change against the list below and attach the matching signals to the structural route's brief. A signal never creates a route by itself and never justifies a micro-optimization at a site with no evidence of heat.

## The signals

- Unnecessary work: recomputed values, repeated reads, duplicate calls, N+1 patterns. Sharpens a `code-simplification` brief; cross-class instances join a `guillotine` ledger.
- Missed concurrency where the surrounding code already uses it: noted in the route brief, changed only where the owner's contract permits.
- Hot-path bloat: new blocking work on startup, per-request, or per-render paths. Flags the site as heat for the owning skill; never thins a safety or correctness check to look leaner.
- Recurring no-op updates: state or store writes in loops, intervals, or handlers with no change guard. Rides with the structural route covering that module.
- Unnecessary existence checks followed by the operation that would fail anyway: fold into the owning route's brief.
- Leaks: registrations, subscriptions, or handles with no paired release. Rides with the structural route; cross-class leakage joins a `guillotine` ledger.
- Overly broad operations: fetching or processing a whole collection when a portion suffices. Sharpens the owning route's brief.

## What never counts

Readability cost is not efficiency cost, and a site with no evidence of heat gets no efficiency change. As with shape signals, safety checks, error handling, and security checks are never removable weight.
