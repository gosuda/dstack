---
name: kernel-internals
description: 'Use when diagnosing scheduler latency, kmalloc vs vmalloc, page cache, meminfo under pressure, or OOM victim choice, or when reading kernel/sched, mm, or fs source.'
---

# Kernel internals

The running kernel explains its own behavior through counters, sysctls, and `/proc` files. Reach for this skill for scheduler latency, allocation failures, VFS and page cache behavior, memory pressure, or the OOM killer choice, and for reading source under `kernel/sched/`, `mm/`, or `fs/`. This skill is read only. Analysis and measurements stay in chat, nothing is written, and no remote machine is mutated.

Tell me the question or symptom: latency, allocation failure, cache behavior, memory pressure, or OOM victim. I can read `/proc`, `/sys`, and `perf` on the running machine when you give access. When no version is stated I assume mainline 7.3 or LTS 6.18.

## Pin the kernel and its scheduler first

Run `uname -r` before reasoning about anything. EEVDF (Earliest Eligible Virtual Deadline First) replaced CFS: it merged as an option in 6.6 and the transition completed in 6.12, so mainline 7.3 and LTS 6.18 run EEVDF. On 6.6 through 6.11, check which fair scheduler is active before applying CFS reasoning. Each CPU carries a runqueue with three classes:

```
Per-CPU runqueue (struct rq)
+-- cfs_rq  fair-class tasks ordered by eligibility and deadline
+-- rt_rq   real-time tasks (FIFO/RR)
+-- dl_rq   SCHED_DEADLINE tasks
```

Record the kernel version and the active fair scheduler before going further.

## Measure scheduling before touching anything

`chrt -p <pid>` reads the scheduling class, `/proc/<pid>/sched` the per task counters, `/sys/kernel/debug/sched/debug` the runqueue state, and `perf sched record` with `perf sched latency` the delay picture. The old CFS sysctls (`kernel.sched_latency_ns`, `kernel.sched_min_granularity_ns`, `kernel.sched_wakeup_granularity_ns`) were removed in 6.12 with EEVDF and exist only on pre 6.12 kernels, so never tune them on a newer one. `vruntime` is virtual runtime, meaning CPU time consumed normalized by weight. Under EEVDF a task with positive lag is eligible and the earliest eligible virtual deadline wins. Name the unfair or slow path from one measurement before changing anything.

## Read fragmentation from the buddy allocator

Physical pages are handed out in power of two orders. Order 0 is one page, 4 KiB on default x86-64 and arm64 configs. `/proc/buddyinfo` shows free blocks per order and zone, `/proc/zoneinfo` the per zone counts. `ZONE_HIGHMEM` exists on 32 bit and selected configs only. On 64 bit x86-64 and arm64 essentially all RAM sits in `ZONE_NORMAL`. Take the fragmentation picture from `buddyinfo`, never from a guess.

## Pick the allocation call by the constraint that binds

| API | Use when |
|---|---|
| `kmalloc(size, GFP_KERNEL)` | Physically contiguous, size bounded by `KMALLOC_MAX_SIZE` (arch dependent) |
| `kzalloc(size, flags)` | Zeroed `kmalloc` |
| `vmalloc(size)` | Virtually contiguous, large, may be physically fragmented |
| `__get_free_pages(gfp, order)` | Direct page granular allocation |

```c
void *buf = kmalloc(4096, GFP_KERNEL);
if (!buf)
    return -ENOMEM;
kfree(buf);
```

The chosen call should match the contiguity and size bound the caller actually needs. On `kmalloc: allocation failed`, the cause is fragmentation or a size over `KMALLOC_MAX_SIZE`, so use `vmalloc`, reduce pressure, and reserve `GFP_ATOMIC` for paths that cannot sleep.

## Separate VFS cache pressure from file leaks

A path lookup walks the dentry cache, the inode carries metadata and ops, and `struct file` holds per open state. `/proc/mounts` lists mounts, `vm.vfs_cache_pressure` sets how eagerly the dentry and inode caches are reclaimed (higher reclaims sooner), and `/proc/<pid>/fd` counts open files. Distinguish cache pressure from file leak pressure before tuning anything. High iowait with low `MemAvailable` is usually page cache thrashing, so add RAM or cut the working set and tune `vfs_cache_pressure` last.

## Judge the page cache together with writeback

`Cached` in meminfo is page cache and tmpfs. `Dirty` pages wait for writeback. `blockdev --getra` reads the readahead window and `--setra` changes it per device. `echo 3 > /proc/sys/vm/drop_caches` after `sync` drops caches for benchmarking only. It is destructive to performance and proves nothing in steady state. Read cache and dirty state together, and treat slow file reads as a readahead question: raise the window and check the backing device.

## Read meminfo fields as a group

| Field | Meaning |
|---|---|
| `MemTotal` | Total usable RAM |
| `MemFree` | Completely unused pages |
| `MemAvailable` | Estimated allocatable memory including reclaimable cache |
| `Cached` | Page cache and tmpfs |
| `Buffers` | Block device metadata cache |
| `SwapTotal` / `SwapFree` | Swap space |
| `Dirty` | Pages pending writeback |
| `AnonPages` | Anonymous heap and stack pages |
| `Slab` | Kernel object cache |
| `SReclaimable` / `SUnreclaim` | Slab split by reclaimability |

```
MemAvailable low + Cached high -> reclaim page cache, pressure is not fatal
AnonPages high + SwapFree low  -> OOM risk
Slab huge                      -> kernel object leak, check /proc/slabinfo
Dirty high                     -> writeback lag, check the I/O scheduler
```

Never diagnose from one field. The pressure verdict should come from two or more fields read together. Suspected SLUB corruption from a use after free in a module goes to `KASAN` with `slub_debug=P`.

## Explain the OOM pick, then move the pick

The killer scores candidates from memory use, child processes, and `oom_score_adj` (-1000 to 1000). Protect a daemon by lowering its adj. Cap a service with a cgroup `memory.max` instead of tuning adj upward for everyone else. Events land in `dmesg` and `journalctl -k`. When the wrong process dies, the cause is usually a big user with a neutral adj, so set `oom_score_adj` or cap with `memory.max`. When real time tasks starve the fair class, audit with `chrt` and use `isolcpus` to split CPUs. State the victim choice and the correction for the next episode.

Trust the kernel over the claim. When a claim contradicts the running kernel, re-read the sysctl or counter and restate the claim with the version attached. When a tunable is missing, the version likely removed it (EEVDF removed the CFS sysctls in 6.12), so do not advise it for newer kernels. When two metrics disagree, measure again under the same load before explaining and never average across episodes.

Hand back three things: the mechanism that explains the observation, the measurements that confirm it with the kernel version attached, and the specific correction to apply.
