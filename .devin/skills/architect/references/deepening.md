# Deepening a cluster of shallow modules

How to fold a group of shallow modules into one deep module without breaking what depends on it. Reads with the shared words from `../SKILL.md`: module, interface, seam, adapter.

## Sort dependencies first

How the deepened module gets tested depends on what it depends on. Classify each dependency before choosing:

### Plain computation

Pure computation and in-memory state, no I/O. Usually deepenable when the modules share one owner and one change reason: merge the modules and test through the new interface directly. No adapter needed. Keep separate when owners or change reasons differ.

### Local stand-in available

Dependencies with local test stand-ins (in-memory filesystems, PGLite for Postgres, Testcontainers, OCaml `Eio_mock`). Deepenable when the stand-in exists. The deepened module is tested with the stand-in running in the suite. The seam stays internal; no port at the module's external interface.

### Owned service across a network

Services the team controls across a network bound (microservices, internal APIs). Define a port (interface) at the seam. The deep module holds the logic; the transport arrives as an injected adapter. Tests use an in-memory adapter. Production uses the HTTP, gRPC, or queue adapter.

### Third-party service

Services the team does not control (Stripe, Twilio, GitHub, Auth0). The deepened module takes the external dependency as an injected port; tests use a test adapter, an in-memory or recording fake asserting observable outcomes through the interface, not an echo of calls.

## Seam discipline

One adapter means a hypothetical seam. Do not introduce a port unless at least two adapters are justified, typically production plus test. A single-adapter seam is just indirection.

Private implementation seams are not test entry points. Tests observe public behavior through the module's interface. Use existing public dependency injection ports or the actual environment boundary to supply test adapters. Keep internal seams private. Do not widen the API or add passthrough wrappers solely for tests. Preserve genuine production and test adapters with independent outcome oracles.

## Testing: replace, do not layer

Old tests on the shallow modules become waste once tests at the deepened module's interface exist: delete them. Write new tests at the deepened module's interface; the interface is the test surface. Assert on observable outcomes through the interface, never internal state. Tests must survive internal refactors since they describe behavior, not implementation. When a test has to change because the implementation changed, it is testing past the interface.
