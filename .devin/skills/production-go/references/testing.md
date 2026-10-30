# Testing Patterns in Go

Go's `testing` package + `go test` covers ~95% of real needs without a framework. The leverage is in the *deltas*: subtests that `t.Parallel` correctly, `t.Cleanup`/`t.Setenv`/`t.Chdir` semantics (and which can't run in parallel), `B.Loop` over `b.N`, `testing/synctest` for time-dependent code, and the coverage flags most people never reach for. Reach for testify when assertions get verbose; never reach for a *framework*.

The testing philosophy centers on state invariants (correctness is proven through state invariants, preconditions, and postconditions $\{P\} C \{Q\}$, never incidental execution traces) and ruthless empirical validation (test real systems end-to-end and use deterministic simulation over fragile mock echoes; tests must be resilient to internal refactoring while strictly asserting system behavior).

> Source horizon: verified against Go **1.26.x** (stable) plus the **1.27** final release notes (GA 2026-08-19; stable patch 1.27.3 pinned in SKILL.md) for the `[1.27]` claims; an earlier pass (2026-06) used the RC notes. Version tags `[1.N]` mark the release a claim applies to. Written from primary sources (pkg.go.dev, release notes, Go blog).

## TL;DR: the modern deltas (read first)

- `for b.Loop()` [1.24] is the new benchmark loop. The condition must be written *exactly* `b.Loop()`; the compiler keeps loop-body args/results alive (a `runtime.KeepAlive` transform on statements *syntactically inside the braces*), so dead-code elimination can't hollow out your benchmark. It auto-resets the timer on first call and stops it on the last. **Never mix it with a `b.N` loop.**
- `testing/synctest` graduated [1.25] → stable [1.26]. `synctest.Test(t, func(*testing.T))` runs a "bubble" with a fake clock; `synctest.Wait()` blocks until every *other* goroutine in the bubble is durably blocked. The trap: **mutexes, I/O, and syscalls are NOT durably blocking**: a test that does a loopback `net.Dial` or grabs a global mutex never goes idle. Use `net.Pipe`.
- `t.Setenv` is [1.17], `t.Cleanup` [1.14], `t.TempDir` [1.15]; only `t.Chdir`/`t.Context` are [1.24]. **`t.Setenv` and `t.Chdir` panic in a test that has called `t.Parallel` (or has a parallel ancestor)**; they mutate process-global state.
- The [1.22] loop-variable change makes the old `tt := tt` copy redundant in `for _, tt := range tests`; but it is **not** a substitute for `t.Parallel` correctness, and it changed nothing for index-style `for i := 0; i < n; i++` loops (`go vet`'s `copylock` [1.24] now flags lock copies there).
- Integration coverage [1.20]: `go build -cover` instruments a *binary*; set `GOCOVERDIR`, run it, then `go tool covdata`. Coverage is no longer test-only.
- `go test` caches results keyed on inputs; a passing test that touches the network/clock can be served from cache and mask a regression. `-count=1` is the documented cache-buster.

## Table of Contents
1. [Table-Driven Tests](#table-driven)
2. [Subtests and Parallel Execution](#subtests)
3. [Deterministic Concurrency Testing](#synctest)
4. [Test Helpers](#helpers)
5. [Cleanup, TempDir, Setenv, Chdir](#fixtures)
6. [TestMain and global setup](#testmain)
7. [Mocking with Interfaces](#mocking)
8. [HTTP Handler Testing](#http-testing)
9. [Database Testing](#db-testing)
10. [Benchmarks](#benchmarks)
11. [Fuzz Testing](#fuzzing)
12. [Golden Files](#golden-files)
13. [Example Tests](#examples)
14. [Coverage](#coverage)
15. [Test Artifacts](#artifacts)
16. [Integration Tests](#integration)
17. [stdlib vs testify](#libraries)
18. [Version map](#versions)
19. [What models get wrong](#stale)

---

## Table-Driven Tests {#table-driven}

The canonical Go test shape. The value is *one assertion path, many cases*; a failure names the case, and `-run Name/case` reruns one.

```go
var (
    ErrEmptyInput = errors.New("empty duration")
    ErrOverflow   = errors.New("duration overflow")
)

func TestParseDuration(t *testing.T) {
    tests := map[string]struct {
        in      string
        want    time.Duration
        wantErr error // explicit error invariant, not a loose boolean
    }{
        "seconds":  {in: "5s", want: 5 * time.Second},
        "empty":    {in: "", wantErr: ErrEmptyInput},
        "negative": {in: "-1h", want: -time.Hour},
        "overflow": {in: "9999999999h", wantErr: ErrOverflow},
    }
    for name, tt := range tests {
        t.Run(name, func(t *testing.T) {
            got, err := ParseDuration(tt.in)
            if tt.wantErr != nil {
                if !errors.Is(err, tt.wantErr) {
                    t.Fatalf("got err %v, want %v", err, tt.wantErr)
                }
                return
            }
            if err != nil {
                t.Fatalf("unexpected err: %v", err)
            }
            if got != tt.want {
                t.Errorf("got %v, want %v", got, tt.want)
            }
        })
    }
}
```

Map keys become the subtest names, so no name field is needed. Use `Fatal` to stop a subtest when a precondition fails, such as an unexpected error. Use `Error` to keep checking the remaining fields after a value mismatch.

Expert points:
- A `map` table gives randomized iteration order (surfaces order-dependence for free) but non-deterministic *output* order; use a slice when you need stable ordering or duplicate names.
- **Assert error invariants, not boolean flags or strings**: A bare `wantErr: true` boolean is weak because any unintended error or recovered panic satisfies it. Conversely, matching `err.Error()` substrings is brittle: it pins incidental English phrasing, breaks across refactorings, and proves nothing about programmatic error handling. Always check error identity with `errors.Is` (for sentinels) or error structure with `errors.As` (for typed errors).
- `t.Fatal`/`Fatalf` calls `runtime.Goexit`; it must run on the **test goroutine**, so calling it from inside a spawned goroutine doesn't fail the test (it just kills that goroutine); send the error back over a channel or use `t.Error` from there.
- Always include zero values, empty, nil, boundaries, and the error branch; a table with no `wantErr` case usually has an untested error path.

---

## Subtests and Parallel Execution {#subtests}

```go
func TestUserService(t *testing.T) {
    svc := setupTestService(t)

    t.Run("group", func(t *testing.T) {
        for name, tt := range cases {
            t.Run(name, func(t *testing.T) {
                t.Parallel()
                got := svc.Do(tt.in)
                if got != tt.want { t.Errorf("got %v want %v", got, tt.want) }
            })
        }
    })
}
```

Do shared setup in the parent before the parallel children start. Children must only read that shared state, never write it. `t.Parallel` pauses the subtest here; it resumes after the enclosing `Run` returns.

`t.Parallel` mechanics (the part models get wrong): calling it *pauses* the subtest until its parent test function returns, then all paused siblings run concurrently. Consequences:
- A parent's code after its `t.Run` block runs **before** the parallel children; so deferred/inline teardown in the parent tears down resources the children still need. Put teardown in `t.Cleanup`, which is **deferred until after parallel subtests finish**.
- [1.22] killed the classic loop-capture bug: each iteration of `for _, tt := range tests` now gets a fresh `tt`, so the old `tt := tt` shadow before `t.Parallel()` is dead weight (`go vet`/`gopls` flag it as redundant). This is the loop-variable scoping change, not a change to `t.Parallel`. It does **not** apply to C-style `for i := 0; i < n; i++`; there `i` is still shared, and a parallel subtest closing over `i` still races.
- `t.Setenv`/`t.Chdir` **panic** if the test is parallel; they're process-global. Conversely, a non-parallel test that calls `t.Setenv` makes the whole subtree effectively serial for that var.

```bash
go test -run 'TestUserService/group/create' ./...   # / selects subtest path; arg is a regexp per segment
go test -race -count=1 -shuffle=on ./...             # -shuffle [1.17] randomizes test+benchmark order
go test -parallel=4 ./...                            # cap concurrent t.Parallel subtests (default GOMAXPROCS)
```

---

## Deterministic Concurrency Testing {#synctest}

`testing/synctest` makes time-dependent and goroutine-coordination tests **fast and deterministic** with no clock-injection interface and no `time.Sleep`-for-sync. Experimental in [1.24] (`synctest.Run`, behind `GOEXPERIMENT=synctest`); **stable [1.25]** as `synctest.Test(t, func(*testing.T))`; carried into [1.26].

```go
import (
    "sync/atomic"
    "testing"
    "testing/synctest"
    "time"
)

func TestDebounce(t *testing.T) {
    synctest.Test(t, func(t *testing.T) {
        var count atomic.Int32
        debounced := Debounce(func() { count.Add(1) }, 100*time.Millisecond)
        debounced()

        time.Sleep(99 * time.Millisecond)
        synctest.Wait()
        if count.Load() != 0 { t.Fatal("fired too early") }

        time.Sleep(time.Millisecond)
        synctest.Wait()
        if count.Load() != 1 { t.Fatal("expected exactly one call") }
    })
}
```

The sleeps run on a fake clock, so they complete in almost no wall time. Each `Wait` blocks until every other goroutine in the bubble is durably blocked, then the test asserts the settled state.

Model ("durably blocked"): the bubble has its own fake clock (starts midnight UTC 2000-01-01). When *every* goroutine in it is durably blocked, an outstanding `Wait()` returns; else the clock jumps to the next timer; else it's deadlocked and `Test` panics. **Durably blocking** (complete list): send/recv on a nil channel; send/recv on a channel *created inside the bubble*; a `select` where every case durably blocks; `time.Sleep`; `sync.Cond.Wait`; `sync.WaitGroup.Wait`.

NOT durably blocking (the failure modes):
- `sync.Mutex`/`RWMutex` lock: a goroutine waiting for a mutex held outside the bubble could be unblocked from outside, so it doesn't count. A test that contends on a global mutex (e.g. via `reflect`) may never go idle.
- I/O and syscalls: a loopback `net.Dial`/`net.Listen` read can be unblocked by the kernel; the runtime can't tell "waiting for data" from "data en route." **Use `net.Pipe` (in-memory `net.Conn`)** to test client/server code in a bubble.

Rules inside the bubble: `T.Run`, `T.Parallel`, `T.Deadline` must **not** be called; `T.Cleanup` runs in-bubble just before `Test` returns; `T.Context()`'s `Done` is bubble-scoped. **Operating on a bubbled channel/timer/ticker from outside panics.** A package-level `var wg sync.WaitGroup` can't associate with a bubble (its `Wait` won't durably block); use `var wg = new(sync.WaitGroup)`. The **race detector understands `Wait`**: a missing `Wait()` between a bubble write and read is a reported race under `-race`. `Test` waits for all bubble goroutines to exit, so a leaked background goroutine deadlocks the test.

See also [concurrency.md](concurrency.md) for synctest applied to channel/worker patterns and [testing-advanced.md](testing-advanced.md#synctest-patterns) for deeper recipes.

---

## Test Helpers {#helpers}

```go
func assertEqual[T comparable](t *testing.T, got, want T) {
    t.Helper()
    if got != want {
        t.Errorf("got %v, want %v", got, want)
    }
}
```

Call `t.Helper` as the first line, so failures report at the caller's line instead of inside the helper.

Expert points: `t.Helper()` re-attributes only the immediate frame; a helper calling another helper needs it in *both*. Idiomatically a helper takes `*testing.T` and calls `t.Fatal`/`t.Error` itself rather than returning an error to check; a helper returning a value should `t.Helper()` then `t.Fatalf` on failure so the value is always usable. `t.TempDir()`/`t.Cleanup()` registered in a helper are owned by the *test*, not the helper.

---

## Cleanup, TempDir, Setenv, Chdir {#fixtures}

The `testing.TB` fixture methods, with their real version tags and the parallel-safety rules that trip people up:

```go
func setupTestDB(t *testing.T) *sql.DB {
    t.Helper()
    db, err := sql.Open("pgx", dsn)
    if err != nil { t.Fatal(err) }
    t.Cleanup(func() { db.Close() })
    return db
}
```

| Method | Tag | Behavior / trap |
|---|---|---|
| `t.Cleanup(f)` | **[1.14]** | LIFO stack; runs after the test and any parallel subtests. Survives `t.Fatal`/`Goexit` (unlike a bare `defer` in a helper that already returned). On `T`, `B`, `F`. |
| `t.TempDir()` | **[1.15]** | Per-test dir auto-removed via Cleanup; unique per test/subtest. Use it instead of `os.MkdirTemp`+manual cleanup. |
| `t.Setenv(k,v)` | **[1.17]** | Sets env via `os.Setenv`, restores on cleanup. **Panics if the test is parallel or has a parallel ancestor.** Calling it implicitly serializes the subtree. |
| `t.Chdir(dir)` | **[1.24]** | `os.Chdir` + restore on cleanup (also sets `PWD` on Unix). **Cannot be used in parallel tests**: process-wide cwd. Prefer absolute paths / `os.Root` [1.24] over changing cwd at all. |
| `t.Context()` | **[1.24]** | Returns a `context.Context` **canceled just before** Cleanup functions run; propagate it into the code under test so it observes test teardown. |

`t.Output() io.Writer` and `t.Attr(key, value)` are **[1.25]**; `t.ArtifactDir()` is **[1.26]** (see [Artifacts](#artifacts)).

---

## TestMain and global setup {#testmain}

```go
func TestMain(m *testing.M) {
    flag.Parse()
    pool := startSharedResource()
    code := m.Run()
    pool.Close()
    os.Exit(code)
}
```

Flags are not parsed yet when `TestMain` starts, so call `flag.Parse` yourself when you read flags here. `m.Run` returns the exit code; `os.Exit` skips deferred cleanup, so close resources before exiting. Since [1.15] `TestMain` may also return instead of calling `os.Exit`, and the exit code is then `m.Run`'s.

Expert points: `TestMain` is a *package-level* hook (one per test binary) for setup too expensive per-test (shared container, connection pool) or that must run on the main goroutine. Don't use it for ordinary setup; per-test `t.Cleanup` is parallel-safe and scoped. There's no `*testing.T`, so `t.Skip`/per-test helpers don't apply.

---

## Mocking with Interfaces {#mocking}

Define the interface **at the consumer**, keep it small, and prefer an in-memory stateful fake over a passive mock for anything under ~3 methods.

A test that tells a mock to return a canned value and asserts that the service returned that exact value is a **mock-return echo**. It proves only that Go function calls forward pointers; it proves zero invariants about domain rules, state transitions, or error handling. Model stateful behavior instead and verify postconditions and fault handling:

```go
type UserRepo interface {
    FindUser(ctx context.Context, id string) (*User, error)
    SaveUser(ctx context.Context, u *User) error
}

// In-memory fake: stores real state to verify state transitions and invariants.
type memUserRepo struct {
    users map[string]*User
    saves int
}

func (m *memUserRepo) FindUser(_ context.Context, id string) (*User, error) {
    u, ok := m.users[id]
    if !ok {
        return nil, ErrNotFound
    }
    cp := *u // return copy so caller cannot mutate internal store without SaveUser
    return &cp, nil
}

func (m *memUserRepo) SaveUser(_ context.Context, u *User) error {
    m.saves++
    cp := *u
    m.users[u.ID] = &cp
    return nil
}

func TestUserService_PromoteUser(t *testing.T) {
    repo := &memUserRepo{
        users: map[string]*User{
            "u1": {ID: "u1", Role: RoleStandard, Status: StatusActive},
        },
    }
    svc := NewUserService(repo)

    // 1. Verify state transition postcondition:
    err := svc.PromoteUser(t.Context(), "u1", RoleAdmin)
    if err != nil {
        t.Fatalf("promote user: %v", err)
    }

    updated, err := repo.FindUser(t.Context(), "u1")
    if err != nil {
        t.Fatalf("fetch updated user: %v", err)
    }
    if updated.Role != RoleAdmin {
        t.Errorf("role = %v, want %v", updated.Role, RoleAdmin)
    }
    if repo.saves != 1 {
        t.Errorf("saves count = %d, want 1", repo.saves)
    }

    // 2. Verify fault resilience: missing user returns domain error, leaves state unchanged
    err = svc.PromoteUser(t.Context(), "unknown", RoleAdmin)
    if !errors.Is(err, ErrUserNotFound) {
        t.Errorf("got err %v, want %v", err, ErrUserNotFound)
    }
}
```

When to generate: for large interfaces or strict protocol sequences, `go.uber.org/mock` (`mockgen`; the maintained successor to the archived `golang/mock`) or `matryer/moq` (generates func-field fakes). Drive generation with a `//go:generate` directive or a `tool` directive [1.24] in `go.mod`. **Don't mock what you don't own** (DB drivers, `http.Client`); fake at the seam you control (a repo interface, an `httptest.Server`). Over-mocking yields tests that pass while the integration is broken. Mocking/fakes depth: [testing-advanced.md](testing-advanced.md#mocking-strategy).

---

## HTTP Handler Testing {#http-testing}

Two levels. Handler level calls the handler directly: no socket, synchronous, fast. Always assert status code, header invariants (e.g. `Content-Type`), and decode response bodies into structured domain types.

```go
func TestUsersHandler(t *testing.T) {
    req := httptest.NewRequestWithContext(t.Context(), "GET", "/api/v1/users/123", nil)
    rec := httptest.NewRecorder()
    handler.ServeHTTP(rec, req)

    res := rec.Result()
    defer res.Body.Close()

    if res.StatusCode != http.StatusOK {
        t.Fatalf("status = %d, want %d", res.StatusCode, http.StatusOK)
    }
    if ct := res.Header.Get("Content-Type"); ct != "application/json" {
        t.Errorf("Content-Type = %q, want application/json", ct)
    }

    var user UserResponse
    if err := json.NewDecoder(res.Body).Decode(&user); err != nil {
        t.Fatalf("decode response body: %v", err)
    }
    if user.ID != "123" || user.Name == "" {
        t.Errorf("unexpected decoded user: %+v", user)
    }
}

func TestUsersHandler_NotFound(t *testing.T) {
    req := httptest.NewRequestWithContext(t.Context(), "GET", "/api/v1/users/unknown", nil)
    rec := httptest.NewRecorder()
    handler.ServeHTTP(rec, req)

    res := rec.Result()
    defer res.Body.Close()

    if res.StatusCode != http.StatusNotFound {
        t.Fatalf("status = %d, want 404", res.StatusCode)
    }
    var prob ProblemDetails
    if err := json.NewDecoder(res.Body).Decode(&prob); err != nil {
        t.Fatalf("decode problem payload: %v", err)
    }
    if prob.Code != "user_not_found" {
        t.Errorf("error code = %q, want user_not_found", prob.Code)
    }
}
```

Stack level runs a real loopback server, which also exercises middleware, routing, and TLS.

```go
func TestHealth(t *testing.T) {
    srv := httptest.NewServer(router)
    t.Cleanup(srv.Close)

    res, err := srv.Client().Get(srv.URL + "/healthz")
    if err != nil {
        t.Fatalf("health request failed: %v", err)
    }
    defer res.Body.Close()

    if res.StatusCode != http.StatusOK {
        t.Fatalf("status = %d, want %d", res.StatusCode, http.StatusOK)
    }
    var body struct{ Status string }
    if err := json.NewDecoder(res.Body).Decode(&body); err != nil {
        t.Fatalf("decode health body: %v", err)
    }
    if body.Status != "ok" {
        t.Errorf("status payload = %q, want ok", body.Status)
    }
}
```

Expert points: `httptest.NewRequestWithContext` is [1.23]. `NewRecorder` skips the server machinery (no write deadlines, `Flusher` timing, or `Server` middleware); use `NewServer`/`NewTLSServer` for those, and with TLS always dial via `srv.Client()` (it trusts the server cert). `ResponseRecorder.Code` defaults to 200 even if the handler never calls `WriteHeader`; assert on `Result().StatusCode`. Always decode the response body: asserting only `StatusCode == 200` lets empty bodies, corrupt payloads, and serialization bugs slip through. Unit-test a client by pointing its `Transport` at an `httptest.Server`, not by mocking `http.Client`. Inside `synctest`, loopback needs `net.Pipe`. Config: [http-and-apis.md](http-and-apis.md).

---

## Database Testing {#db-testing}

Prefer a **real engine** (testcontainers-go, or a CI service container) over an in-memory SQL emulator; dialect drift (SQLite vs Postgres) silently passes tests that break in prod. Isolate parallel tests with a per-test schema or a rolled-back transaction, never a shared mutable table; register teardown via `t.Cleanup(func(){ container.Terminate(ctx) })`. `sqlmock` is brittle (asserts exact query strings); reserve it for *error-handling* paths you can't easily provoke against a live DB. Driver/migration patterns: [database.md](database.md). Full integration scaffolding: [Integration Tests](#integration).

---

## Benchmarks {#benchmarks}

```go
func BenchmarkMarshal(b *testing.B) {
    data := makeData()
    b.ReportAllocs()
    for b.Loop() {
        sink, _ = json.Marshal(data)
    }
}
```

Setup stays before the loop, so the timer excludes it. The condition must read exactly `b.Loop()` [1.24]. Assigning the result to a package-level sink was needed before [1.24]; with `b.Loop` the compiler keeps loop-body results alive, so it is redundant but harmless.

`for b.Loop()` vs `for i := 0; i < b.N; i++` [1.24]:

| Aspect | `for b.Loop()` | `for i := 0; i < b.N; i++` |
|---|---|---|
| Timer | Resets on first `Loop()`, stops on last; setup/cleanup outside the loop is free | Manual `b.ResetTimer()`/`b.StopTimer()` |
| Dead-code elimination | Loop-body args/results kept alive (KeepAlive on statements *inside the braces*) | Compiler may delete an unused result → fake "0.3 ns/op" |
| Function executions | Function body runs **once** per `-count`; iterations adjusted internally | Whole function re-run multiple times as `b.N` grows |
| `b.N` | Holds **total iterations** *after* the loop (use for derived metrics) | The iteration count you loop to |

Traps: the loop condition must be written literally `b.Loop()` (the compiler pattern-matches the syntax); a wrapper like `for cond := b.Loop(); cond; cond = b.Loop()` defeats the KeepAlive transform. **Never mix `b.Loop()` and `b.N`** in one benchmark. `b.RunParallel(func(pb *testing.PB){ for pb.Next() {...} })` is still the API for parallel benchmarks (`b.Loop` is single-goroutine). Statistical rigor (multiple runs, `benchstat`) and profiling belong in [performance.md](performance.md#benchmarking); don't eyeball a single run.

```bash
go test -bench=. -benchmem -count=10 ./...   # -count=10 for variance; pipe to benchstat
go test -bench=BenchmarkMarshal -cpuprofile=cpu.out ./...
```

---

## Fuzz Testing {#fuzzing}

Native fuzzing landed **[1.18]** (`*testing.F`, `f.Add`, `f.Fuzz`). Seed the corpus, then assert an *invariant*; not a hardcoded output.

```go
func FuzzRoundTrip(f *testing.F) {
    f.Add("https://example.com/p?q=1")
    f.Add("")
    f.Fuzz(func(t *testing.T, in string) {
        u, err := Parse(in)
        if err != nil { return }
        if got := Parse(mustString(u)); got != u {
            t.Errorf("round-trip: %v != %v", got, u)
        }
    })
}
```

Seeds also persist under `testdata/fuzz/`. Rejecting invalid input is not a failure. The asserted property is round-trip identity: parsing formatted output returns the same value.

```bash
go test -run='^$' -fuzz=FuzzRoundTrip -fuzztime=30s ./pkg
```

`-run '^$'` skips the unit tests while fuzzing, so only the fuzz target runs.

Expert points: fuzz arguments are limited to the supported types (`[]byte`, `string`, the numeric types, `bool`, `rune`); no structs/slices; pack structured inputs into `[]byte` and decode inside `f.Fuzz`. Without `-fuzz`, a `Fuzz` target runs only its **seed corpus** as a normal unit test (so seeds are regression tests). A crasher is written to `testdata/fuzz/<FuzzName>/` and **must be committed**: it then reproduces deterministically in CI without re-fuzzing. `-fuzz` runs **one target at a time**, so fuzzing isn't a CI default; gate it on a nightly/dedicated job. Property-based testing depth: [testing-advanced.md](testing-advanced.md#property-based).

## Golden Files {#golden-files}

`testdata/` as *input* is fine. A committed expected-output file as the *pass oracle* is not: `-update` overwrites the proof, so the test detects byte drift, not a user-visible fault, and fails on formatting refactors. Assert meaning instead, and keep saved output as an inspection/debugging aid only.

```go
func TestRender(t *testing.T) {
    pages := loadPages(t, "testdata/pages")
    for name, in := range pages {
        t.Run(name, func(t *testing.T) {
            out := render(in)

            // 1. Proof: Output parses under target format rules.
            doc, err := parse(out)
            if err != nil {
                t.Fatalf("rendered output does not parse: %v", err)
            }
            // 2. Proof: Output satisfies structural schema invariants.
            if err := checkSchema(doc); err != nil {
                t.Fatalf("rendered output violates schema: %v", err)
            }
            // 3. Proof: Semantic meaning matches input invariants.
            if !sameMeaning(doc, in) {
                t.Errorf("meaning changed for input %s", name)
                // Inspection artifact: diff against last-known sample is logged for diagnostics,
                // or written to t.ArtifactDir() on failure, but never gates pass/fail.
                t.Logf("diagnostic diff vs baseline sample:\n%s",
                    cmp.Diff(knownGoodSamples[name], out))
            }
        })
    }
}
```

Three checks, in order: the output parses, it satisfies the schema, and it means the same as the input (round-trip identity, canonical equivalence insensitive to formatting). A diff against a committed sample may appear in the failure log or be saved to `t.ArtifactDir()` to speed up human inspection; it must never decide pass or fail. Normalize nondeterminism (timestamps, random IDs, map order) before comparing, or every run creates a false diff.

Expert points: `testdata/` is special; `go build`/`go test` ignore it, and the working directory during a test is the **package directory**, so `testdata/...` resolves without tricks. It works well for large input corpora (templates, serialized trees) where inline literals would be unreadable. `t.Name()` includes the subtest path with `/`; sanitize it for filesystem-unsafe characters if your subtest names contain them.

---

## Example Tests {#examples}

Examples are compiled, run, **and** checked against their `// Output:` comment. Treat that check as documentation quality, not behavior proof: it pins exact stdout, so a formatting-only change fails it while proving nothing about the values a caller actually receives. Keep the example for godoc, and pair it with a real test that asserts a semantic predicate on the parsed result.

```go
func ExampleParse() {
    u, _ := Parse("https://go.dev")
    fmt.Println(u.Host)
    // Output: go.dev
}

func TestParseFields(t *testing.T) {
    u, err := Parse("https://go.dev/path?q=1")
    if err != nil {
        t.Fatalf("parse: %v", err)
    }
    if u.Scheme != "https" || u.Host != "go.dev" || u.Path != "/path" {
        t.Errorf("decoded fields wrong: %+v", u)
    }
}
```

The `// Output:` comment keeps the godoc honest about what the example prints. The `TestParseFields` assertions prove what the code returns. One may change without the other: reworded printing breaks only the example, a misparsed field breaks only the test.

Expert points: the name must be `Example`, `ExampleF`, `ExampleT`, or `ExampleT_M` (in a `_test.go` file) to attach to godoc. An example with **no `// Output:`** comment is *compiled but not run* (verifies only that it builds). `// Unordered output:` matches lines in any order. Name a method example `ExampleType_Method` so it attaches to that method's godoc.

---

## Coverage {#coverage}

```bash
go test -cover ./...
go test -coverprofile=cov.out -covermode=atomic ./...
go tool cover -func=cov.out
go tool cover -html=cov.out
go test -coverpkg=./... -coverprofile=cov.out ./...
```

`-cover` prints a summary percentage per package. `cover -func` prints a per-function table; `cover -html` opens annotated source in a browser.

**`-covermode`:** `set` (default; did-it-run booleans), `count` (hit counts), `atomic` (count, race-safe). **Use `atomic` whenever `-race` is on**; `count` mode's non-atomic counters are themselves data races. `-coverpkg` widens *instrumentation* to packages beyond the one under test (e.g. measure how much of `./internal/...` your handler tests exercise); without it you only see the test's own package.

Integration coverage of binaries [1.20]; coverage is no longer test-only:

```bash
go build -cover -o app.exe ./cmd/app
GOCOVERDIR=$(mktemp -d) ./app.exe ...
go tool covdata percent  -i="$GOCOVERDIR"
go tool covdata textfmt  -i="$GOCOVERDIR" -o=cov.txt
go tool covdata merge    -i=dir1,dir2 -o=merged
```

The build instruments the binary (by default, the main module's packages). Each run writes counter files into `GOCOVERDIR`. `textfmt` feeds `go tool cover -func/-html`; `merge` combines many runs.

`go build -cover -coverpkg=...` extends binary instrumentation to dependencies. This lets end-to-end / CLI / server-under-load tests contribute to a coverage number, merged with unit-test profiles via `covdata merge`.

---

## Test Artifacts {#artifacts}

**[1.26]** `t.ArtifactDir()` (on `T`, `B`, `F`) returns a per-test directory for output files (screenshots, debug dumps, captured payloads). With `go test -artifacts`, it lives under the test output dir and **persists**: without the flag it's a temp dir removed after the test. Repeated calls in the same (sub)test return the same path.

```go
if err := os.WriteFile(filepath.Join(t.ArtifactDir(), "response.json"), body, 0o644); err != nil {
    t.Fatal(err)
}
```

Pair with `t.Attr(key, value)` [1.25] to emit CI-readable test metadata, and `t.Output() io.Writer` [1.25] to stream large diagnostic output through the test log without `t.Log`'s per-call source annotation. For scratch space that should *not* survive, keep using `t.TempDir()`. `t.ArtifactDir()` cleanly separates diagnostic dumps and captured payloads from programmatic test oracles.

---

## Integration Tests {#integration}

```go
//go:build integration

package myapp_test
```

The tag excludes the file from the default `go test`; run it with `-tags=integration`.

```bash
go test -short ./...
go test -tags=integration -count=1 ./...
```

`-short` is the fast path: integration tests self-skip on `testing.Short()`. `-count=1` disables result caching so cached results cannot hide infrastructure changes.

Two gating mechanisms, used together: a **build tag** (`//go:build integration`) keeps slow tests out of the default compile entirely; **`testing.Short()`** lets a test skip itself under `-short` even when compiled in. Build tags are coarse (whole file); `Short()` is per-test.

Test organization:
- `package foo` in `*_test.go` → **white-box** (can touch unexported identifiers).
- `package foo_test` in the same dir → **black-box** (only the public API; the documented default for most packages). You can have *both* files in one directory.
- `testdata/` → fixtures, ignored by the toolchain; cwd during tests is the package dir.
- `TestMain` → one-time package-level setup ([above](#testmain)).

---

## stdlib vs testify {#libraries}

| Tool | Status [2026] | Use when |
|---|---|---|
| stdlib `testing` + `go test` | **Default** | Always the baseline; covers ~95% |
| `google/go-cmp` (`cmp.Diff`) | **De-facto standard** for deep equality | Comparing structs/maps/slices with readable diffs; honors `cmpopts`, `Equal` methods. Don't use `reflect.DeepEqual` in tests. |
| `stretchr/testify` (`assert`/`require`) | Very common, maintained | Cutting assertion boilerplate. `require.*` stops the test (like `Fatal`); `assert.*` continues (like `Error`). Avoid `testify/suite`; fights `t.Parallel` and Go test idioms. |
| `go.uber.org/mock` (`mockgen`) | Maintained successor to archived `golang/mock` | Generated mocks with call-order/expectation assertions on large interfaces |
| `matryer/moq` | Maintained | Lightweight func-field mock generation |
| `testcontainers/testcontainers-go` | Maintained | Ephemeral real dependencies (DB, broker) for integration tests |
| `quicktest`, `is`, Ginkgo/Gomega | Niche / BDD | Rarely needed; Ginkgo's DSL diverges from idiomatic Go testing |

Rule of thumb: stdlib for control flow and `t.Run`; `go-cmp` for equality; `testify/require` to trim repetitive `if err != nil` chains. A *framework* (Ginkgo) is almost never the right call in Go.

---

## Version map {#versions}

| Ver | Testing-relevant additions |
|---|---|
| **[1.14]** | `t.Cleanup` |
| **[1.15]** | `t.TempDir`; `TestMain` may return instead of calling `os.Exit` |
| **[1.17]** | `t.Setenv`; `go test -shuffle` |
| **[1.18]** | Native fuzzing (`*testing.F`, `f.Add`, `f.Fuzz`); generics (typed test helpers) |
| **[1.20]** | `go build -cover` + `go tool covdata` (integration coverage of binaries) |
| **[1.21]** | `testing.Testing()` (am I running under `go test`?) |
| **[1.22]** | Loop-variable per-iteration scoping (kills `tt := tt`); enhanced `ServeMux` routing eases handler tests |
| **[1.23]** | `httptest.NewRequestWithContext`; timers GC'd unreferenced (old `time.After` leak advice stale) |
| **[1.24]** | `for b.Loop()`; `t.Chdir`/`t.Context`; `testing/synctest` (experimental, `GOEXPERIMENT=synctest`); `tool` directives in go.mod; `tests` vet analyzer; `copylock` flags 3-clause-loop lock copies |
| **[1.25]** | `testing/synctest` **stable** (`synctest.Test`/`Wait`); `t.Output`, `t.Attr` |
| **[1.26]** | `t.ArtifactDir` + `go test -artifacts`; synctest carried forward |
| **[1.27]** | `testing/synctest.Sleep` (combines `time.Sleep` and `synctest.Wait` in one call); `httptest.NewTestServer` (in-memory fake network suitable for use with `testing/synctest`); `go test` runs the `stdversion` vet check by default; `go test -json` `Action:output` lines gain `OutputType` (`error`, `error-continue`, `frame`). GA 2026-08-19; additions verified against the final release notes. |

---

## What models get wrong {#stale}

1. Claiming `t.Setenv`/`t.Cleanup`/`t.TempDir` are all "[1.24]"; only `t.Chdir`/`t.Context` are; `Cleanup` [1.14], `TempDir` [1.15], `Setenv` [1.17].
2. Calling `t.Setenv` or `t.Chdir` in a test that also calls `t.Parallel`; it **panics** (process-global state).
3. Still writing `tt := tt` before `t.Parallel()` in a `range` loop; redundant since [1.22]; but assuming [1.22] also fixed C-style `for i := 0; i < n; i++` (it didn't).
4. Treating `b.Loop()` as cosmetic over `b.N`; it changes timer handling, prevents DCE, and runs the body once per `-count`. And **mixing** `b.Loop()` with a `b.N` loop.
5. Writing the `b.Loop()` condition indirectly (assigning it to a variable); defeats the compiler's KeepAlive transform.
6. Using `synctest` with loopback `net.Dial` or a global mutex and wondering why it hangs; those aren't durably blocking; use `net.Pipe`.
7. Calling `t.Run`/`t.Parallel` *inside* a `synctest` bubble; forbidden.
8. Forgetting `synctest.Wait()` between a bubble write and read; `-race` reports it as a data race.
9. Calling `t.Fatal` from a spawned goroutine; it only `Goexit`s that goroutine, not failing the test; send the error back to the test goroutine.
10. Tearing down shared resources via parent `defer`/inline code with parallel subtests; runs before the children; use `t.Cleanup`.
11. `reflect.DeepEqual` for test equality instead of `cmp.Diff` (no diff, surprising NaN/unexported behavior).
12. Running `-race` with `-covermode=count`; the counters race; use `atomic`.
13. Relying on cached `go test` results for tests that touch the clock/network; use `-count=1`.
14. Asserting on `ResponseRecorder.Code` (defaults to 200) instead of `Result().StatusCode`.
15. A fuzz target with no `// Output`-style invariant, or not committing the `testdata/fuzz/` crasher (so CI can't reproduce it).
16. Reaching for `testify/suite` or Ginkgo when `t.Run` + table tests + `go-cmp` suffice.
17. Mocking `http.Client`/DB drivers (don't own them) instead of faking at an owned seam (`httptest.Server`, repo interface).
18. Treating mock-return echoes, golden file byte diffs, or `err.Error()` string matches as correctness proof. A test must verify independent invariants, system state transitions, and typed error classifications (`errors.Is`/`errors.As`), keeping diffs and dumped payloads strictly as inspection/debug artifacts.

---

## See Also {#see-also}

- [testing-advanced.md](testing-advanced.md); fuzzing depth, property-based testing, mocking strategies, test architecture, load/chaos
- [concurrency.md](concurrency.md); `synctest` for channel/worker patterns, goroutine lifecycle
- [debugging-and-diagnostics.md](debugging-and-diagnostics.md); race detector internals, `dlv`
- [performance.md](performance.md#benchmarking); benchmark statistics, `benchstat`, profiling
- [http-and-apis.md](http-and-apis.md); server/client config behind `httptest`

## Sources {#sources}

- pkg.go.dev/testing (go1.26), pkg.go.dev/testing/synctest (go1.26.4), pkg.go.dev/net/http/httptest
- go.dev/doc/go1.{14,15,17,18,20,22,23,24,25,26} release notes
- go.dev/blog/synctest (Damien Neil, 2025-02; durably-blocked rules, `net.Pipe`); go.dev/blog/integration-test-coverage (Than McIntosh, 2023-03; `go build -cover`/`covdata`)
- go.dev/blog/fuzz-beta; go.dev/security/fuzz; github.com/google/go-cmp; github.com/stretchr/testify; go.uber.org/mock; testcontainers-go
