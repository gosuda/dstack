---
name: concurrency-debugging
description: 'Use when reading TSan race reports, debugging deadlocks with GDB thread inspection, analyzing Helgrind lock-order violations, or reviewing std::atomic and happens-before usage.'
---

# Concurrency debugging

This skill names the fault behind a ThreadSanitizer or Helgrind report, a hung process, or suspect cross-thread code: the race is the pair of conflicting accesses on one address with no synchronization between them, and a deadlock is the cycle of threads and mutexes. Bring the symptom (the TSan or Helgrind report, the hung or deadlocked process, or the code under review), the code paths named in the report, and, for sanitizer or Valgrind runs, a project that rebuilds with the needed flags.

Everything here is read-only. The skill emits analysis, diagnostic commands, and the verification run in chat; the operator runs commands against the target, no file is written, and nothing touches a remote resource. The work is done when the race or deadlock is named by its conflicting accesses or lock cycle, the fix is stated, and the verification run is described: clean TSan or Helgrind output, or the resolved GDB thread state.

## Catch the race with ThreadSanitizer

TSan ships inside GCC and Clang and needs no separate install. An uninstrumented binary produces no report, so rebuild first:

```bash
gcc -fsanitize=thread -g -O1 -o prog main.c    # clang takes the same flags
./prog
TSAN_OPTIONS="halt_on_error=1:second_deadlock_stack=1" ./prog
```

`halt_on_error` stops at the first report; `second_deadlock_stack` adds the other lock stack to deadlock reports. The step ends with a report in hand or a clean run.

## Read the report as an access pair

A report names the access type and address, the stack of the thread that performed it, the stack of the conflicting earlier access, and where each thread was created:

```text
WARNING: ThreadSanitizer: data race (pid=12345)
  Write of size 4 at 0x7f1234 by thread T2:
    #0 increment /src/counter.c:8:5
  Previous read of size 4 at 0x7f1234 by thread T1:
    #0 read_counter /src/counter.c:3:14
  Thread T2 created at:
    #0 pthread_create ...
    #1 main /src/counter.c:28:3
SUMMARY: ThreadSanitizer: data race /src/counter.c:8:5 in increment
```

Name the two conflicting accesses, their threads, and the shared address. Then fix by pattern:

| Race pattern | Fix |
|---|---|
| Unsynchronized read or write on shared state | Add a mutex or make the variable `std::atomic` |
| Double-checked locking without atomics | `std::once_flag` with `std::call_once` |
| Compound update on a shared integer | `fetch_add` or `compare_exchange_strong` |
| Container mutated during iteration | Hold the lock for the whole critical section |
| `shared_ptr` control block | Already atomic; the pointed-to object still needs its own synchronization |

Every reported access pair gets a named fix. A report that is benign by design, such as a statistical counter, still gets silenced explicitly: make it a `memory_order_relaxed` atomic so the intent is on record.

## Expose lock-order violations with Helgrind

Helgrind runs on Valgrind and reports acquisition orders that can deadlock:

```bash
valgrind --tool=helgrind --log-file=helgrind.log ./prog
```

A lock-order report names two observed orders over the same mutex pair: thread T1 takes M1 then M2, thread T2 takes M2 then M1. The fix is one global order: take M1 before M2 at every site. Helgrind reports on custom spinlocks or lock-free code are expected noise; annotate or filter them rather than chasing them as bugs.

## Find the deadlock cycle in GDB

A process that will not reproduce under the debugger still shows its cycle: attach to the stopped process and read `info threads` with a per-thread backtrace.

```bash
gdb -p $(pgrep prog)
```

```gdb
(gdb) info threads        # threads parked in __lll_lock_wait wait on a mutex
(gdb) thread 2
(gdb) bt                  # which lock this thread waits on
(gdb) p ((pthread_mutex_t*)0x601090)->__data.__owner   # glibc: TID of the owner
```

`__data.__owner` is a glibc implementation detail; on another libc it is absent, so identify the mutex owner from the backtraces instead. To dump every thread at once:

```python
python
import gdb
for t in gdb.selected_inferior().threads():
    t.switch()
    print(f"Thread {t.num}: {gdb.execute('bt 3', to_string=True)}")
end
```

Name the cycle of threads and mutexes.

## Fix std::atomic misuse

A check followed by a store is two operations, not one; publication across threads needs release on the producer side and acquire on the consumer side:

```cpp
// TOCTOU: the check and the store are not one operation
if (counter == 0) counter = 1;
// Fix: one atomic compare-exchange
int expected = 0;
counter.compare_exchange_strong(expected, 1);

// Publication needs release/acquire, not relaxed
data = 42;
ready.store(true, std::memory_order_release);   // producer
if (ready.load(std::memory_order_acquire)) {    // consumer
    use(data);                                 // sees data == 42
}
```

Every shared access ends up atomic or mutex-guarded, and every publication uses release/acquire.

## Justify each cross-thread read with a happens-before edge

The edges are: sequenced-before orders statements inside one thread; `store(release)` synchronizes-with `load(acquire)` on the same atomic; thread creation synchronizes-with the new thread's first action; a thread's last action synchronizes-before `join`; `unlock(M)` synchronizes-with the next `lock(M)`. A cross-thread read with no edge behind it is a race. Give each cross-thread read its named edge or flag it.

## Carry the same reasoning into Rust

Ownership rejects data races at compile time: shared mutable state goes behind `Arc<Mutex<T>>` or atomics, and `Send`/`Sync` gate what crosses a thread boundary. TSan works on nightly:

```bash
RUSTFLAGS="-Zsanitizer=thread" cargo +nightly test
```

Shared state sits behind `Arc<Mutex<T>>` or atomics, or the nightly TSan run is clean.

Hand back a verdict naming the race or deadlock by its conflicting accesses or lock cycle, the fix per pattern, and the verification run.
