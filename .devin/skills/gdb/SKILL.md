---
name: gdb
description: 'Use when running GDB: breakpoints, watchpoints, segfault or hang debugging, reverse debugging, remote gdbserver, core dumps, pretty-printers, Python scripting, or multi-threaded debugging.'
---

# GDB

GDB stops a C or C++ program where it misbehaves and shows the state at that point. Reach for it for breakpoints, watchpoints, stepping, crash or hang diagnosis, reverse debugging, remote debugging with gdbserver, core files, or Python scripting. This skill is read only. It emits analysis and commands for you to run on the target, writes nothing, and mutates no remote machine.

Tell me the binary (built with `-g`; `-Og` or `-O0` gives the most debuggable code) and the symptom: crash, hang, wrong value, or a question about program state. Add the core file, PID, or remote target when the workflow is post mortem, attach, or gdbserver.

## Build so the debugger can see

```bash
gcc -g -Og -o prog main.c
```

For release builds use `-g -O2` and keep an unstripped copy. To ship stripped binaries while keeping debuggability, split the symbols and link them back:

```bash
objcopy --only-keep-debug prog prog.debug
strip prog
objcopy --add-gnu-debuglink=prog.debug prog
```

The binary should carry debug info before any session starts.

## Open the session

```bash
gdb ./prog                            # load a binary
gdb ./prog core                       # binary plus core dump
gdb -p 12345                          # attach to a running process
gdb --args ./prog arg1 arg2           # pass arguments
gdb -batch -ex 'run' -ex 'bt' ./prog  # non-interactive, for CI
```

Continue once GDB holds a live inferior or a loaded core.

## Stop where it matters

| Command | Shortcut | Effect |
|---|---|---|
| `run [args]` | `r` | Start the program |
| `continue` | `c` | Resume after a stop |
| `next` | `n` | Step over, source line |
| `step` | `s` | Step into, source line |
| `nexti` | `ni` | Step over, one instruction |
| `stepi` | `si` | Step into, one instruction |
| `finish` | | Run to the end of the function |
| `until N` | | Run to line N |
| `return [val]` | | Force a return from the function |
| `quit` | `q` | Exit |

Set the stop condition next:

```gdb
break main                          # function
break file.c:42                     # line
break *0x400abc                     # address
break foo if x > 10                 # conditional
tbreak foo                          # fires once
rbreak ^mylib_.*                    # regex over function names
catch throw                         # C++ exception
catch syscall mmap                  # syscall

watch x                             # break when x is written
watch *(int*)0x601060               # watch an address
rwatch x                            # break on read
awatch x                            # break on read or write

info breakpoints
delete 3 / disable 3 / enable 3
ignore 3 100                        # skip the next 100 hits
commands 3 ... end                  # run commands on each hit
```

Execution should stop at the condition that matters before you move on.

## Read the state at the stop

```gdb
print x / print/x x                 # value, hex
print *ptr                          # dereference
print arr[0]@10                     # ten elements from arr[0]
display x                           # print on every stop
info locals / info args
info registers rip rsp rbp
x/10wx 0x7fff0000                   # examine memory: count/format/unit
x/s 0x400abc                        # as string
x/i $rip                            # current instruction
backtrace / bt full
frame 2 / up / down
```

Read the variable, register, or memory region in question before concluding anything.

## Untangle threads

```gdb
info threads
thread 3
thread apply all bt full
set scheduler-locking on            # only the current thread runs while stepping
```

Know each thread state before naming a cause. Deadlock cycles and race reports belong to `concurrency-debugging`, which this skill hands off to once single thread state is read.

## Walk backward when forward misses

```gdb
(gdb) record                        # software record, slow but universal
(gdb) run
(gdb) reverse-continue              # back to the last event
(gdb) reverse-next / reverse-step / reverse-finish
(gdb) record btrace                 # hardware branch trace (Intel PT or BTS)
(gdb) record instruction-history    # replay recorded instructions
```

Use reverse debugging when the bug is easier to catch going backward. Stop when the execution history reaches the state before the bug.

## Drive a remote or embedded target

On the target:

```bash
gdbserver :1234 ./prog              # on the target
gdbserver :1234 --attach 5678       # attach variant
```

On the host:

```gdb
(gdb) target remote 192.168.1.10:1234
```

For cross compiled targets use the matching GDB, for example `aarch64-linux-gnu-gdb`. The host GDB should control the target process before you debug further.

## Make defaults stick

Put session defaults in `~/.gdbinit` once:

```gdb
set history save on
set history size 1000
set print pretty on
set print array on
set print array-indexes on
set pagination off
set confirm off
```

The full command cheatsheet lives in `references/cheatsheet.md`. Pretty printers and the Python API live in `references/scripting.md`.

## When GDB fights back

| Symptom | Cause | Fix |
|---|---|---|
| `No symbol table` | Built without `-g` | Rebuild with `-g` |
| `??` frames in the backtrace | Missing debug info or stack corruption | Install the debug package; suspect a stack smash |
| `Cannot access memory at address` | Null or freed pointer | Check the pointer; run under ASan |
| `SIGABRT` in the backtrace | `abort()` or a failed assertion | Walk up frames to the check |
| GDB hangs on `run` | Program waits on stdin | `run < /dev/null` |
| Breakpoint lands wrong | Optimizer moved the code | Rebuild with `-Og`, or step with `nexti` |

Hand back the bug localized to a frame, variable, register, or instruction, with the commands that produced the evidence. When a blocker stops the session (no symbols, no core, unreachable target), name it with its fix instead.
