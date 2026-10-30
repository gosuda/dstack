---
name: nodejs-graceful-shutdown
description: 'Use when asked to implement or fix service termination: SIGTERM or SIGINT, connection draining, health-check signaling. Not for general service scaffolding: use nodejs-service-foundations.'
---

# Node.js graceful shutdown

You make a Node.js server stop without dropping work. When the process gets SIGTERM or SIGINT (a deploy, a scaler, a Ctrl-C), it stops accepting new connections, tells the load balancer it is going away, lets in-flight requests finish inside a deadline, closes its database and queue handles, and exits with a code that says whether the drain was clean. If the ask is really about scaffolding the whole service (env, logging, errors), that belongs to nodejs-service-foundations instead.

This stays local and reversible: you edit only the server shutdown handler and add one companion test, both rolled back through version control. You never touch remote state. The only runtime side effect is starting a short-lived server to watch it drain.

What you need before starting:

- `SOURCES`: files under `$CWD/src` or `$CWD/lib` holding the `http.createServer` or Express/Fastify `listen` bootstrap (one file is fine). Required.
- `SERVER_PORT`: TCP port the test server binds. Required.
- `HEALTH_ROUTE`: health or readiness path. Required.
- `DRAIN_TIMEOUT_MS`: milliseconds to wait for in-flight requests before forcing the exit. Required, positive integer, default `10000`.
- `EXTERNAL_DEPENDENCIES`: every external handle the app opens (database pools, Redis clients, queue producers). Required, may be empty.

## Wire one handler for both signals

Read every file in `SOURCES` and find the bootstrap: the `listen` call and the variable holding the server instance. Keep any existing named `process.on` handler and update it rather than registering a second handler on the same signal. Both `SIGTERM` and `SIGINT` must end at a single `shutdown` function, guarded by module-scope state declared as `let isShuttingDown = false`. If that flag does not exist yet, add it.

## Fail health first so the balancer looks away

The first thing `shutdown` does is set `isShuttingDown = true`, and the health endpoint reads that flag on every request: `200 OK` with `{"status":"ok"}` while serving, `503 Service Unavailable` with `{"status":"shutting_down"}` once draining starts. This flip must land before `server.close()` runs, so a health probe sent right after the signal reliably sees the 503 while the server is still up.

## Drain connections, then close what you opened

After the health flip, call `server.close()` on the real server instance and await it (never a fixed sleep), raced against a `DRAIN_TIMEOUT_MS` timeout. If close resolves first the drain was graceful; if the timer wins, requests are still in flight and the exit must be non-zero. Then close every entry in `EXTERNAL_DEPENDENCIES`:

- database pools with `pool.end()`
- Redis clients with `redis.quit()`
- queue producers with `producer.disconnect()`

Leave OS-level sockets alone. Await every close; an unresponsive dependency gets recorded, not retried forever. Partial cleanup (some handles closed, others not) counts as failure.

Exit `0` only when the server drained inside the deadline and every dependency closed. Exit `1` when the drain timed out or any dependency stayed unresponsive, so callers can tell a clean drain from a forced one.

## Prove it with a companion test

Write `<filename>.test.ts` next to the handler and run it with `node --test` or the project's runner until it is green. The test spawns the server with `DRAIN_TIMEOUT_MS=500`, then:

- requests `GET /<HEALTH_ROUTE>` and expects `200`
- sends `SIGTERM`
- immediately requests health again and expects `503` with `shutting_down`
- holds a long-running request across the signal and expects it to complete before exit
- waits for the process to exit and expects code `0` when the long request finished inside the deadline
- reruns a scenario where the long request outlasts the deadline and expects a non-zero exit

All of those assertions must exist and pass.

## When draining fails

- Unresponsive dependency hangs `closeExternalConnections()`: record which one, give each dependency close its own timeout, and exit `1`. The companion test sees the non-zero code.
- Active requests outliving `DRAIN_TIMEOUT_MS`: the timeout wins the race against `server.close()`. Exit `1`, and either raise the timeout or stop the service holding connections past it.
- Partial cleanup: some handles closed, others not. Exit `1`. The usual cause is a handle missing from `EXTERNAL_DEPENDENCIES`, so add it.
- Flag checked too late: a request that started async work before the signal can still fire a database query after the flag is set. Put the `isShuttingDown` guard before the I/O call, not after.
- Health route ignoring the flag: the balancer keeps sending traffic to a draining pod. The 503 must come immediately after the signal and before `server.close()`.

## What you hand back

Edited shutdown code plus a passing companion test, demonstrating the 503 health flip ahead of `server.close()`, a clean drain inside the deadline, and an exit code that separates graceful shutdown from deadline-forced termination.
