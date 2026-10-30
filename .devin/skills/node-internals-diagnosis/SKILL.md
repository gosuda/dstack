---
name: node-internals-diagnosis
description: 'Use when Node.js segfaults, addon crashes, leaks, event-loop anomalies, thread-pool saturation, V8 deoptimizations, or binding.gyp failures need diagnosis. Not for code edits or service restarts.'
disable-model-invocation: true
---

# Node internals diagnosis

Crashes and stalls in Node.js rarely explain themselves. This skill traces a native segfault, addon crash, memory leak, event-loop anomaly, thread-pool saturation, deoptimization storm, or binding.gyp failure to one root cause backed by tool evidence. The run ends with a diagnosis report naming that cause, or with a blocked report naming the blocker.

Nothing here edits code or restarts services. The skill runs diagnostic binaries and writes only the diagnosis report plus its diagnostic artifacts; rollback deletes those artifacts. No file, version-control, credential, paid, published, deployed, or remote mutation occurs.
What you need before diagnosing: the symptom class, which is required, and the Node.js version and platform (OS, arch), also required.

Optional evidence sharpens the work: crash signal (such as SIGSEGV or SIGABRT) and process ID, a core dump or minidump path, a heap snapshot (`--heap-snapshot-signal` or `v8.writeHeapSnapshot()` output), a `--trace-deopt` log, libuv trace output (`LIBUV_TRACE` level 1-4), a gdb or lldb backtrace, and the crashing native addon or module name and version.

## Classify, then collect the evidence for that class

Match the symptom to one class first: segfault or addon crash, native memory leak, heap (V8) leak, event-loop anomaly, thread-pool saturation, V8 deoptimization, or binding.gyp failure. A symptom outside all seven stops the run with `blocked: unsupported-failure-class`.

Gather the minimum evidence for the matched class:

- Segfault or addon crash: run the process under gdb with a catchpoint on the signal, or attach to the core dump. Capture `thread apply all bt full`. Note the crashing instruction address and shared object name.
- Native memory leak: run AddressSanitizer or Valgrind on the process and capture the leak report. Cross-reference the addon active at the earliest leak frame.
- Heap leak (V8): take a heap snapshot with `--heap-snapshot-signal=SIGUSR2` or `v8.writeHeapSnapshot()`. Diff two snapshots and find which objects retain the most paths.
- Event-loop anomaly: reproduce with `LIBUV_TRACE=4` enabled. Identify handles alive past their expected lifetime and check libuv refs on them.
- Thread-pool saturation: probe with `UV_THREADPOOL_SIZE`, capturing queue depth and average wait time. Correlate with the async operations outstanding.
- V8 deoptimization: parse the `--trace-deopt` output. For each deopt site, reconstruct the hidden class and property access order. A site firing repeatedly points at a polymorphic inline cache gone megamorphic.
- binding.gyp failure: inspect `include_dirs`, `libraries`, and `cflags_c` in the generated `build/config.gypi`. Confirm the target Node.js `abi_{NODE_MODULE_VERSION}` matches the runtime and that platform detection (win, darwin, linux) is correct.

## Follow the decision tree to a root cause

Each class has its own checks. A segfault trace gets HandleScope-lifetime and libuv-lifetime review: was a C++ object used after destruction, or a handle closed too early? Backtraces into a native addon point at its lifetime violations; backtraces into V8 internals point at improper `Persistent` handle management. A native-leak report leads to the allocating frame: an addon freeing nothing, or a `Persistent` handle pinning a native buffer past collection. Cross-reference the addon's cleanup path. A heap-snapshot delta exposes the retaining path: a closure holding an unexpected reference, an unremoved event listener, a cache growing without eviction, a `setInterval` callback holding objects. Name the path and the code creating it. An event-loop anomaly comes down to the handle type keeping the loop alive (timer, socket, pipe, signal, `uv_poll_t`): never closed, closed with a retained reference, or re-registered on every callback iteration. Look for missing `uv_close()` calls and for unref'd handles that should have stayed ref'd. Thread-pool saturation means workload beyond `UV_THREADPOOL_SIZE` (default 4), one slow operation blocking the pool, or work on the pool that belonged on the event loop. Name the blocking operation and the pool-size mismatch. A deopt site means property insertion order varying across calls, a constructor returning a different layout than first built, or a polymorphic cache turned megamorphic. Name the site, the hidden-class transition, and the layout-diverging code. A binding.gyp failure means a missing header path, an ABI version mismatching the runtime, or broken platform detection. Name the configuration error.

Write the diagnosis report with the root cause named as one of: C++ object lifetime violation, megamorphic IC, hidden-class layout mismatch, thread-pool starvation, libuv handle leak, native allocation leak, V8 retaining-path leak, event-loop handle leak, ABI mismatch, or other. Attach the supporting evidence: backtrace, leak report, snapshot delta, trace output, or queue metrics. Confirm the report states failure class, root cause, supporting evidence, and any missing evidence. A contradictory or ambiguous picture stops the run with `blocked: ambiguous-root-cause` rather than a guess.

## When diagnosis stops instead

The diagnostic binary errors or produces nothing: capture stderr and return `blocked: missing-evidence` with the message. Never fabricate a root cause.

The symptom fits no decision tree: return `blocked: unsupported-failure-class`.

Tool output contradicts itself, for instance a reported leak with a flat snapshot: return `blocked: ambiguous-root-cause` listing both findings. Resolve the contradiction before naming anything.

Partial evidence still has value: return the partial classification with the evidence on hand and name explicitly what is missing.

## What you hand back

One diagnosis report: failure class, root cause, supporting evidence, and missing evidence, or `blocked` with the named blocker and detail.
