# Retention Contracts: Admission, Ownership, and Retained Memory

A cap on serialized work or on an admission budget says nothing about how much decoded heap stays alive. State retention bounds in terms of owning handles and the lifetimes they cover, never in terms of budgets alone.

## A budget is not a retention bound

Trace every owning handle and say exactly which owner and which lifetime the bound covers. Anything the bound does not name, it does not limit.

## One entry or a real policy

When consecutive-identity reuse meets the requirement, a single cache entry keyed by the complete identity can bound cache-owned retention. Otherwise define a genuine multi-entry retention policy instead of stretching the single entry to cover cases it cannot.

## Release before replacing, when the contract says so

On a cache miss, release the old cache-owned value before allocating its replacement wherever the contract requires that ordering. Keep the order even when swapping it looks harmless.

## Keep charges and verified values intact

Preserve admission charges unless changing them is explicitly in scope. Cache only verified values, and account for revisits that arrive after an eviction.

## Prove ownership with witnesses

Prove exact-identity reuse, old-value release, and scope teardown with ownership witnesses such as weak references. Each claim needs a witness that breaks if the ownership story changes.

## State the other limits separately

Limits on caller-held values, transient allocations, outputs, and concurrent requests belong in their own statements. Do not let them hide inside the cache-owned bound.

## Mutations must fail behaviorally

A mutation proof must compile and then fail at the intended behavioral assertion. A mutation that merely fails to compile proves nothing about behavior.
