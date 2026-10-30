# GDB command cheatsheet

Use these commands to run, stop, and inspect a program under the debugger. Source: the GDB manual at sourceware.org/gdb/documentation/.

## Startup

Load the binary first. Attach to a running process with `-p`, pass arguments with `--args`, or script a non-interactive run with `-batch` and `-ex`.

```gdb
gdb prog                         # load binary
gdb prog core                    # load with core
gdb -p PID                       # attach to process
gdb --args prog a b c            # pass arguments
gdb -batch -ex 'run' -ex 'bt'    # non-interactive
set args a b c                   # set args after load
```

## Execution control

Step with `next` to stay at the current level and `step` to descend into calls. Append `i` to move one machine instruction instead of one source line.

```gdb
run / r [args]                   # start
continue / c                     # resume
next / n                         # step over, source line
step / s                         # step into, source line
nexti / ni                       # step over, one instruction
stepi / si                       # step into, one instruction
finish                           # run to end of function
until N                          # run to line N in the current file
until file.c:N                   # run to a specific line
advance foo                      # run to the next call of foo
return [expr]                    # force a return value
signal SIGUSR1                   # deliver a signal
kill                             # kill the program
```

## Breakpoints and watchpoints

Break on code with `break`. Stop on data with `watch`: `watch` fires on writes, `rwatch` on reads, `awatch` on either. List and manage every stop point with `info`, `delete`, `disable`, and `enable`.

```gdb
break main                       # function
break file.c:42                  # line
break *0x400abc                  # address
break foo if x > 0               # conditional
tbreak foo                       # temporary, fires once
rbreak regex                     # all matching functions
catch throw                      # C++ exception thrown
catch syscall mmap               # syscall breakpoint

watch var                        # write watchpoint
rwatch var                       # read watchpoint
awatch var                       # read/write watchpoint
watch *(int*)addr                # memory watchpoint

info breakpoints                 # list
delete N                         # remove
disable N / enable N             # toggle
ignore N count                   # skip N hits
commands N                       # run commands on each hit
```

## Inspection

Print values with `print` and a format suffix. Show whole arrays with `arr[0]@N`. Track an expression across stops with `display`. Read types with `ptype` and `whatis`, and dump scopes with `info locals`, `info args`, and `info variables`.

```gdb
print expr / p expr              # print an expression
print/x expr                     # hex
print/t expr                     # binary
print/f expr                     # float
print/c expr                     # char
print/d expr                     # signed decimal
print/u expr                     # unsigned decimal
print/a expr                     # as address

print arr[0]@N                   # N elements starting at arr[0]
print *ptr                       # dereference
print *((int*)ptr)               # cast and dereference

display expr                     # print on every stop
undisplay N                      # remove an auto-display
info display                     # list them

ptype var                        # full type
whatis var                       # brief type
info locals                      # all locals
info args                        # function arguments
info variables                   # all globals
```

## Stack

`bt full` adds locals to every frame. Move with `up` and `down`, or jump straight to a frame with `frame N`.

```gdb
backtrace / bt                   # call stack
bt N                             # top N frames
bt full                          # frames plus locals
bt -N                            # bottom N frames
frame N / f N                    # select frame N
up / down                        # move in the stack
info frame                       # frame details
```

## Memory

The `x/Nuf` form takes a count, a unit size, and a display format. Units: `b` byte, `h` halfword (2), `w` word (4), `g` giant (8). Formats: `x` hex, `d` dec, `u` uint, `o` octal, `t` binary, `f` float, `s` string, `i` insn.

```gdb
x/Nuf addr                       # examine memory
#   N = count
#   u = unit: b byte, h halfword (2), w word (4), g giant (8)
#   f = format: x hex, d dec, u uint, o octal, t binary, f float, s string, i insn

x/10wx 0x7fff0000                # 10 words in hex
x/4gx $rsp                       # 4 giants at the stack top
x/20i $rip                       # 20 instructions from RIP
x/s 0x400abc                     # string
x/b &var                         # single byte

set {int}0xaddr = 42             # write memory
set variable x = 42              # set a variable
```

## Threads

List threads with `info threads` and switch with `thread N`. Run a command on several threads at once with `thread apply`. Lock the scheduler while you step a single thread.

```gdb
info threads                     # list
thread N                         # switch
thread apply all bt              # backtrace all
thread apply all bt full
thread apply 1 2 print x         # specific threads
set scheduler-locking on/off     # lock other threads during a step
```

## Reverse debugging

Record execution first, then step backward. `record btrace` uses hardware branch tracing where the CPU supports it. Flip `exec-direction` to make plain `n` and `s` run backward.

```gdb
record                           # start software record
record btrace                    # start hardware branch trace
record stop                      # stop recording
reverse-continue / rc            # back to the last event
reverse-next / rn                # reverse step over
reverse-step / rs                # reverse step into
reverse-finish                   # reverse out of the function
set exec-direction reverse       # make n/s go backward
set exec-direction forward       # restore
record instruction-history       # recorded instructions, btrace
record function-call-history     # recorded calls, btrace
```

## Display formats

Pair these with `print` for values and `x` for memory. `p/x var` shows a value in hex. `x/s ptr` reads a C string.

| Format | Code | Example |
|---|---|---|
| Hex | `/x` | `p/x var` |
| Decimal | `/d` | `p/d var` |
| Binary | `/t` | `p/t var` |
| Float | `/f` | `p/f var` |
| Char | `/c` | `p/c var` |
| String | `/s` | `x/s ptr` |
| Instruction | `/i` | `x/5i $pc` |
