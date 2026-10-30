# Sanitizer report interpretation

Use this to read a sanitizer report and map it to a fix. ASan reports carry three parts: the error class, the access stack, and the allocation or free stacks that produced the address. LSan reports carry the error class, the allocation stack, and a leak summary. TSan reports carry the error class and the conflicting access stacks. UBSan instead prints one line per finding with a file, line, column, and check name.

## ASan

### heap-buffer-overflow

```text
ERROR: AddressSanitizer: heap-buffer-overflow on address 0x602000000050
WRITE of size 4 at 0x602000000050 thread T0
    #0 0x401234 in write_past_end main.c:12
    #1 0x401567 in main main.c:40

0x602000000050 is located 0 bytes after a 40-byte region
allocated by thread T0 here:
    #0 0x7f... in malloc
    #1 0x401400 in main main.c:8
```

Frame `#0` of the first stack is the access site at line 12. The allocation is at line 8 for 40 bytes. `0 bytes after` the region end means a classic off-by-one. Fix the loop bound (`i < n`, not `i <= n`). Check the size expression (`n * sizeof(T)`).

### heap-use-after-free

```text
ERROR: AddressSanitizer: heap-use-after-free on address 0x602000000050
READ of size 8 at 0x602000000050 thread T0
    #0 0x401234 in use_ptr main.c:20

freed by thread T0 here:
    #0 0x7f... in free
    #1 0x401300 in cleanup main.c:15
allocated by thread T0 here:
    #0 0x7f... in malloc
    #1 0x401200 in init main.c:5
```

The allocation is at line 5. The free is at line 15. The use is at line 20. The fix is an ownership decision between `cleanup` and `use_ptr`.

### stack-buffer-overflow

```text
ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7fff...
WRITE of size 1 at 0x7fff... thread T0
    #0 0x401234 in foo main.c:8

Address 0x7fff... is located at offset 28 in frame <main.c:5:foo>
This frame has 1 object(s):
    [0, 28) 'buf' (line 6)
```

`buf` holds 28 bytes. The write lands at offset 28, one past the end. Check unbounded copies such as `strcpy`, `sprintf`, and `gets`.

### double-free

```text
ERROR: AddressSanitizer: attempting double-free on 0x602000000050
    #0 0x401234 in bad_free main.c:25

freed here (1st time):
    ...
freed here (2nd time / current):
    #0 0x401234 in bad_free main.c:25
```

Two free paths reach the same pointer. Name one owner for the pointer.

## UBSan

UBSan prints one line per finding in the form `file:line:col: runtime error:`.

```text
src/main.c:15:12: runtime error: signed integer overflow: 2147483647 + 1 cannot be represented in type 'int'
```

Common shapes and fixes:

| Report | Fix |
|---|---|
| signed integer overflow | Widen to `int64_t` or guard the operation |
| member access within null pointer | Check for null before the deref |
| shift exponent 32 too large for 32-bit type | Cast the operand to `uint64_t` or mask the shift |
| load of misaligned address | Use `memcpy` for unaligned data or fix the alignment |

Add `UBSAN_OPTIONS=print_stacktrace=1` to locate the caller when the reported line sits inside a macro.

## TSan

### data race

```text
WARNING: ThreadSanitizer: data race (pid=12345)
Write of size 4 at 0x7f... by thread T2:
    #0 counter_increment counter.c:8
Previous read of size 4 at 0x7f... by thread T1:
    #0 counter_read counter.c:3
Location is global 'g_counter' of size 4
```

Two threads touch the same location without synchronization. At least one access is a write. Fix with a mutex, an atomic, or message passing between the threads.

### lock-order-inversion

```text
WARNING: ThreadSanitizer: lock-order-inversion (potential deadlock)
Mutex M1 acquired here while holding M2:
Mutex M2 acquired here while holding M1:
```

Two paths acquire the same mutexes in opposite order. Fix with one global lock order. Every path acquires M1 before M2.

## LSan

```text
==12345==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 40 byte(s) in 1 object(s) allocated from:
    #0 0x7f... in malloc
    #1 0x401234 in create_thing main.c:10
    #2 0x401567 in main main.c:35

SUMMARY: AddressSanitizer: 40 byte(s) leaked in 1 allocation(s).
```

`create_thing` allocates and nobody frees the object. Trace the owner of the object. A leak reachable at exit can be intentional. Suppress it in a file with a named owner. Never hide it by disabling `detect_leaks`.
