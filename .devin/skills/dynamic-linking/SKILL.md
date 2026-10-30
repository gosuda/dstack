---
name: dynamic-linking
description: 'Use when debugging shared library load failures, setting RPATH or RUNPATH, applying soname versioning, writing dlopen plugins, or intercepting with LD_PRELOAD. Not for static archives.'
---

# Dynamic linking

Linux starts a dynamically linked program through `ld.so`, which finds each needed shared library at startup, or on demand when the program calls `dlopen`. Reach for this skill when a launch dies with `cannot open shared object file` or `symbol lookup error`, when you are versioning a library with a soname, when a binary needs an embedded search path, or when you want to load a plugin or interpose a function with `LD_PRELOAD`. Static archives are out of scope.

Tell me which binary fails or which library you are building, where the library is supposed to live, and whether the install has to be relocatable — that choice decides between `$ORIGIN`, RUNPATH, and system registration. Everything here stays local: the skill writes built `.so` files, symlinks, and source, plus `/etc/ld.so.cache` when `ldconfig` runs, and `ldconfig` needs root. Environment variables and loader flags never leave the session. If you need to undo, revert in version control, delete the symlinks you created, and re-run `ldconfig`.

## Build a library the loader can track

Compile position-independent, link with a soname, and keep the two conventional symlinks. The soname is the name executables record and `ldconfig` maintains; the `.so.1` name is what the loader opens, the bare `.so` is what the linker finds with `-lmylib`.

```bash
gcc -fPIC -c src/mylib.c -o mylib.o
gcc -shared -Wl,-soname,libmylib.so.1 mylib.o -o libmylib.so.1.2.3
ln -s libmylib.so.1.2.3 libmylib.so.1   # loader name
ln -s libmylib.so.1     libmylib.so     # linker name for -lmylib
```

Confirm with `readelf -d libmylib.so.1.2.3`: it should print the intended `SONAME`. Bump the version by what the ABI did, not by habit: a bug fix with no ABI change is a PATCH, added symbols that stay backwards compatible are a MINOR bump that keeps the soname and refreshes the `.so.1` symlink, and a break is a MAJOR bump with a new soname while the old `.so.1` files stay installed for existing binaries.

## Point the binary at the right copy

RPATH is searched before `LD_LIBRARY_PATH`; RUNPATH after it. Prefer RUNPATH for anything you deploy, because then the operator's environment keeps control. `-Wl,--enable-new-dtags` selects RUNPATH and is the modern linker default. `$ORIGIN` expands to the directory holding the binary, which makes an install tree relocatable.

```bash
gcc main.c -L./lib -lmylib \
    -Wl,-rpath,'$ORIGIN/../lib' -Wl,--enable-new-dtags -o myapp
readelf -d myapp | grep -E 'RPATH|RUNPATH'
chrpath -l myapp                 # show
chrpath -r '/new/path' myapp     # rewrite on an existing binary
```

`readelf -d myapp` should show the tag and value you intended. When predicting a failure, walk the order `ld.so` actually uses: `DT_RPATH` when no `DT_RUNPATH` exists, then `LD_LIBRARY_PATH` (ignored for setuid binaries), then `DT_RUNPATH`, then the `/etc/ld.so.cache` built by `ldconfig`, then `/lib` and `/usr/lib`. Put the library at a step your deployment controls, and trace decisions with `LD_DEBUG=libs ./myapp` and `ldd -v ./myapp`, which shows resolved paths plus version requirements.

## Load a plugin while the program runs

Clear `dlerror()` before each call: `dlsym` reports success through a null return from `dlerror`, not from the pointer itself. Link with `-ldl` on glibc before 2.34; glibc 2.34 and later fold `dlfcn` into libc.

```c
#include <dlfcn.h>

typedef int (*plugin_fn_t)(const char *input);

void load_plugin(const char *path) {
    void *handle = dlopen(path, RTLD_NOW | RTLD_LOCAL);
    if (!handle) {
        fprintf(stderr, "dlopen: %s\n", dlerror());
        return;
    }
    dlerror();  // clear any error state before dlsym
    plugin_fn_t fn = (plugin_fn_t)dlsym(handle, "plugin_run");
    const char *err = dlerror();
    if (err) {
        fprintf(stderr, "dlsym: %s\n", err);
        dlclose(handle);
        return;
    }
    fn("hello");
    dlclose(handle);
}
```

You are finished when the plugin loads, its entry point runs, and `dlclose` releases it. If two libraries export the same symbol and calls land in the wrong one, reopen the plugin with `RTLD_LOCAL` or hide the non-public symbols as below.

## Intercept a call without touching the source

A preloaded library is searched first, so its symbols win, and `RTLD_NEXT` reaches the next definition down the chain:

```c
#define _GNU_SOURCE
#include <dlfcn.h>
#include <stdio.h>

void *malloc(size_t size) {
    static void *(*real_malloc)(size_t) = NULL;
    if (!real_malloc)
        real_malloc = (void *(*)(size_t))dlsym(RTLD_NEXT, "malloc");
    void *ptr = real_malloc(size);
    fprintf(stderr, "malloc(%zu) = %p\n", size, ptr);
    return ptr;
}
```

```bash
gcc -shared -fPIC -o myinterpose.so myinterpose.c -ldl
LD_PRELOAD=./myinterpose.so ./myapp
```

Running under `LD_PRELOAD=...` should show the interception while the real call still works. This never applies to setuid binaries: the loader ignores `LD_PRELOAD` and `LD_LIBRARY_PATH` for them by policy, which is not a bug to work around.

## Export only the public API

Build with `-fvisibility=hidden`, mark the public entry points `visibility("default")`, or restrict exports with a version script:

```c
__attribute__((visibility("default"))) int public_api(void) { return 42; }
```

```text
# mylib.map
MYLIB_1.0 {
    global:
        mylib_init;
        mylib_process;
    local:
        *;
};
```

```bash
gcc -shared -fPIC -fvisibility=hidden -Wl,--version-script=mylib.map \
    mylib.c -o libmylib.so
```

`nm -D --defined-only libmylib.so` should list exactly the public API and nothing else. Non-PIC objects fail here with `relocation R_X86_64_32 against .rodata` — recompile that object with `-fPIC`.

## When loading still fails

| Error | Cause | Fix |
|-------|-------|-----|
| `cannot open shared object file` | Library outside the search path | Set RUNPATH, extend `LD_LIBRARY_PATH`, or run `ldconfig` |
| `symbol lookup error: undefined symbol` | Missing library or version mismatch | Check `ldd`, fix link order, or add the missing `-l` |
| `relocation R_X86_64_32 against .rodata` | Non-PIC code in a shared object | Compile that object with `-fPIC` |
| `version 'GLIBC_2.xx' not found` | Built on a newer glibc than the runtime | Build on the older host or link statically |

A few traps survive the table. When `ldd` still shows `not found` despite a correct RUNPATH, the dependency of a dependency needs its own RUNPATH — trace with `LD_DEBUG=libs` and fix the library that records the path, not the top binary. When `chrpath` refuses a longer path, it cannot grow the existing string: rebuild with the right `-Wl,-rpath` or use `patchelf --set-rpath`. Without root there is no `ldconfig`, so ship the RUNPATH inside the binary and skip system-wide registration.

Show the running binary or loaded plugin with its evidence: the `ldd` output, the `SONAME` and RUNPATH lines from `readelf -d`, or the interposition trace. Longer background on search paths, `$ORIGIN`, and version scripts lives in `references/ld-rpath-soname.md`.
