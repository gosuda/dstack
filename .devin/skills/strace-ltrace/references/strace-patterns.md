# strace and ltrace recipes

Use this when a filtered trace points at a syscall class and you need the exact command for that case. Every flag here was checked against strace 6.19 and ltrace 0.7.91 or read from their man pages.

## Line format

Each traced call prints its arguments and its return value. Failed calls add the errno name and message.

```text
syscall(arg1, arg2, ...) = return_value [-ERRNO (message) on failed calls]
```

```text
openat(AT_FDCWD, "/etc/passwd", O_RDONLY) = 3
read(3, "root:x:0:0:root:/root:/bin/bash\n"..., 4096) = 1234
mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f1234567000
clone(child_stack=NULL, flags=CLONE_VM|CLONE_FS|...) = 12346
openat(AT_FDCWD, "/missing", O_RDONLY) = -1 ENOENT (No such file or directory)
+++ exited with 0 +++
```

`-y` adds the path behind each descriptor, as in `read(3</etc/passwd>, ...)`. `-f` follows forks and prefixes each line with its PID, as in `[pid 12346]`.

## Binary will not start

Run one of these commands. `-Z` prints only syscalls that returned with an error code (verified as `--failed-only` in `strace --help`). `ENOEXEC` means the binary targets another architecture or has a bad interpreter line. `ENOENT` on a `.so` path means a missing shared library.

```bash
strace -f -e trace=execve ./myapp
strace -Z -e trace=openat ./myapp
```

For the loader's own search, `dynamic-linking` covers `LD_DEBUG` and RPATH. `elf-inspection` reads the binary's declared dependencies.

## File not found

The first command shows every failing path operation. The second lists every path the program tried, in order. The order of attempts shows the search path the program walks. The first `ENOENT` in the expected directory usually marks the misconfiguration.

```bash
strace -f -Z -e trace=%file ./myapp
strace -e trace=openat ./myapp 2>&1 | grep -o '"[^"]*"'
```

## Network

The first command shows every connection attempt with its address. The second covers sockets, binds, sends, and receives. The third isolates the DNS path through resolver files and port 53.

```bash
strace -f -s 256 -e trace=connect ./myapp
strace -f -e trace=%network -s 256 ./myapp
strace -f -e trace=openat,connect,sendto,recvfrom ./myapp 2>&1 | grep -E 'resolv|:53'
```

`ECONNREFUSED` on `connect` means nothing listens at that address. `EADDRINUSE` on `bind` means the port is held. `EINPROGRESS` on a non-blocking `connect` is normal. The result arrives in a later `poll` or `getsockopt`.

## Permissions and policy

The first command shows `EACCES` and `EPERM` with the operation that hit them. The second isolates credential and capability calls. The third shows the last calls before a `SIGSYS` from seccomp or a `SIGKILL`.

```bash
strace -f -Z -e trace=%file,%creds ./myapp
strace -f -e trace=%creds ./myapp
strace -f ./myapp 2>&1 | tail -20
```

## Memory

The first command shows refused allocations. The second shows mapping and limit calls.

```bash
strace -e trace=%memory ./myapp 2>&1 | grep -E 'ENOMEM'
strace -e trace=mmap,getrlimit,setrlimit,prlimit64 ./myapp
```

## Summary profile

```text
% time     seconds  usecs/call     calls    errors syscall
------ ----------- ----------- --------- --------- ----------------
 62.34    0.012456         124       100        12 read
 18.91    0.003782          37       102           write
 11.23    0.002246        1123         2           futex
```

`% time` shows where kernel time goes. `usecs/call` marks blocking calls. `errors` marks retries. `strace -c -f` includes children. `-w` switches the table to wall-clock time per call instead of system time.

## ltrace filters

The filter grammar is `{[+-][symbol_pattern][@library_pattern]}`. Join symbols with `+`. Prefix with `-` to exclude.

```bash
ltrace -e malloc+calloc+realloc+free ./myapp
ltrace -e 'str*' ./myapp
ltrace -e 'fopen+fclose+fread+fwrite' ./myapp
ltrace -e 'printf+fprintf+sprintf+snprintf' -s 256 ./myapp
ltrace -e 'pthread_*' ./myapp
ltrace -e 'dlopen+dlsym+dlclose' ./myapp
ltrace -e 'malloc+free-@libc.so*' ./myapp
ltrace -l 'libssl.so*' ./myapp
```

`'str*'` globs over string functions. The `malloc+free-@libc.so*` form traces `malloc` and `free` from anywhere except libc itself. `-l 'libssl.so*'` traces every call into one library.

## From strace to the code location

`-k` prints a stack for each traced syscall. That stack is often enough to find the caller.

```bash
strace -k -Z -e trace=openat ./myapp
```

When you need a breakpoint, catch the syscall in `gdb` directly.

```text
(gdb) catch syscall openat
(gdb) run
(gdb) bt
```

## Containers

`ptrace` is not in the default container capability set. For Docker, add `SYS_PTRACE` to the run. For Kubernetes, add `SYS_PTRACE` under `securityContext.capabilities.add`. Confirm tracing works with a trivial command inside the container before tracing the real workload.

```bash
docker run --cap-add=SYS_PTRACE image strace ./myapp
strace -o /dev/null true
```
