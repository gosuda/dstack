# Rust unsafe patterns reference

Use `unsafe` only to encapsulate an invariant the compiler cannot check, and expose a safe interface whose callers need no contract. Two different notes carry the argument: `# Safety` on an unsafe function states the caller's obligations, while `SAFETY:` beside an unsafe block justifies why that block upholds its callee's contract. The `undocumented_unsafe_blocks` Clippy lint requires the block-level note.

## The unsafe contract

`# Safety` on an unsafe function states the caller's obligations; `SAFETY:` beside an unsafe block justifies why that block is sound. Write both, in those places.

```rust
/// # Safety
/// - `ptr` must be non-null
/// - `ptr` must be aligned to `align_of::<T>()`
/// - `ptr` must point to `len` initialized values of type `T`
/// - The memory must remain valid and not be mutated for the lifetime of the returned slice
unsafe fn raw_slice<'a, T>(ptr: *const T, len: usize) -> &'a [T] {
    // SAFETY: upheld by the caller under the contract above.
    unsafe { std::slice::from_raw_parts(ptr, len) }
}
```

## Raw pointer patterns

### NonNull: non-null raw pointer wrapper

`NonNull` encodes non-nullness in the type, so the null check happens once at construction. Dereferencing and reclaiming ownership stay unsafe because only the programmer knows the pointer is still valid and uniquely owned.

```rust
use std::ptr::NonNull;

struct Node<T> {
    data: T,
    next: Option<NonNull<Node<T>>>,
}

let boxed = Box::new(42u32);
let nn: NonNull<u32> = NonNull::new(Box::into_raw(boxed)).unwrap();

let val = unsafe { nn.as_ref() };

let boxed_again = unsafe { Box::from_raw(nn.as_ptr()) };
```

### Pointer arithmetic

`wrapping_add` never causes undefined behavior by itself, but dereferencing its result still requires bounds. `add` requires its result to stay in bounds even when nothing is dereferenced. Measure spans with `offset_from` between pointers into the same allocation.

```rust
let arr = [1u32, 2, 3, 4, 5];
let ptr = arr.as_ptr();

let p3 = ptr.wrapping_add(2);
let third = unsafe { *ptr.add(2) };

let end = unsafe { ptr.add(arr.len()) };
let count = unsafe { end.offset_from(ptr) };
```

### Read and write without creating references

Raw access copies, overwrites, or destroys a value without binding a reference, so no aliasing lifetime is created. `read` copies the value out, `write` replaces it without dropping the old one, `copy` tolerates overlap while `copy_nonoverlapping` requires disjoint ranges, and `drop_in_place` runs the destructor without freeing the memory.

```rust
let val: u32 = unsafe { std::ptr::read(ptr) };

unsafe { std::ptr::write(mut_ptr, new_val) };

unsafe { std::ptr::copy_nonoverlapping(src, dst, count) };
unsafe { std::ptr::copy(src, dst, count) };

unsafe { std::ptr::drop_in_place(ptr) };
```

### Invariant-based safety

Allocator boundary: `alloc`, `alloc_zeroed`, and `dealloc` require a non-zero-size
`Layout`; passing a zero-size layout is undefined behavior per
`GlobalAlloc::alloc` and `GlobalAlloc::alloc_zeroed`. A zero-length buffer therefore
never reaches the allocator: construction stores no pointer, access returns `&[]`
without `from_raw_parts`, and `Drop` skips `dealloc`. No extra byte is allocated to
hide the zero case, and no sentinel address is assumed from the allocator.
Validate once at construction, then rely on the stored invariant at every use. Here
the constructor rejects bad layouts and null returns, so the accessor's slice is
sound without rechecking. The buffer owns its memory and frees it in `Drop` with
the same layout, so no successful construction leaks.

```rust
use std::alloc::Layout;
use std::ptr::NonNull;

pub struct AlignedBuffer {
    ptr: Option<NonNull<u8>>,
    layout: Layout,
}

impl AlignedBuffer {
    pub fn new(len: usize, align: usize) -> Option<Self> {
        let layout = Layout::from_size_align(len, align).ok()?;
        if len == 0 {
            return Some(Self { ptr: None, layout });
        }
        // SAFETY: layout is valid by construction and size is non-zero.
        let ptr = unsafe { std::alloc::alloc_zeroed(layout) };
        let ptr = NonNull::new(ptr)?;
        Some(Self { ptr: Some(ptr), layout })
    }

    pub fn as_slice(&self) -> &[u8] {
        match self.ptr {
            // SAFETY: ptr came from alloc_zeroed with this len and alignment.
            Some(ptr) => unsafe { std::slice::from_raw_parts(ptr.as_ptr(), self.layout.size()) },
            None => &[],
        }
    }
}
impl Drop for AlignedBuffer {
    fn drop(&mut self) {
        if let Some(ptr) = self.ptr {
            // SAFETY: ptr came from alloc_zeroed with this layout, freed once.
            unsafe { std::alloc::dealloc(ptr.as_ptr(), self.layout) };
        }
    }
}

```

### Pin and self-referential structs

Pinning plus `PhantomPinned` opts out of `Unpin`, so the boxed value can never move and a pointer into its own field stays valid. Build the pointer with `addr_of!` to avoid creating an intermediate shared reference whose tag would conflict with the later mutation.

```rust
use std::pin::Pin;
use std::marker::PhantomPinned;
use std::ptr::addr_of;

struct SelfRef {
    data: String,
    data_ref: *const String,
    _pin: PhantomPinned,
}

impl SelfRef {
    fn new(s: String) -> Pin<Box<Self>> {
        let mut boxed = Box::pin(SelfRef {
            data: s,
            data_ref: std::ptr::null(),
            _pin: PhantomPinned,
        });
        // SAFETY: addr_of! keeps the &mut tag and pin keeps the box unmoved.
        unsafe {
            let this = boxed.as_mut().get_unchecked_mut();
            this.data_ref = addr_of!(this.data);
        }
        boxed
    }
}
```

## Transmute safety table

| From | To | Safe? | Alternative |
|---|---|---|---|
| `u32` | `f32` | yes (same size) | `f32::from_bits(u)` |
| `[u8; 4]` | `u32` | yes | `u32::from_ne_bytes(arr)` |
| `&T` | `*const T` | yes | `ptr as *const T` |
| `*mut T` | `*const T` | yes | `ptr as *const T` |
| `&'a T` | `&'b T` (longer) | no | Restructure lifetimes |
| `Box<T>` | `*mut T` | yes | `Box::into_raw(b)` |
| `u8` | `bool` | no, unless 0/1 | Match on value |
| `u8` | `MyEnum` | no, unless valid tag | `MyEnum::try_from(u)` |
| `i32` | `u32` | yes | `i as u32` |
| `Vec<T>` | `Vec<U>` | no | Manual conversion |

Prefer the named conversion in the last column wherever one exists; it states the intent and stays valid when representations change.

## Miri testing for unsafe

Run the unsafe tests under Miri to catch provenance and aliasing faults the normal test harness cannot see. A Miri error is a soundness fault even when every assertion passes. Use strict provenance for aliasing-sensitive code and isolate a single test while debugging.

```bash
cargo +nightly miri test

MIRIFLAGS="-Zmiri-strict-provenance" cargo +nightly miri test

cargo +nightly miri test test_my_unsafe_fn
```

Prove the aliasing invariant, not saved values. The first test states that the returned view covers exactly the backing allocation: same length, same base address. The second probes the zero-length edge the slice contract allows: a dangling but aligned pointer with length zero is a valid empty slice through `from_raw_parts`. That edge never extends to the allocator: passing a zero-size `Layout` to `alloc`, `alloc_zeroed`, or `dealloc` is undefined behavior. Never rely on a field-only oracle that checks struct fields without observing allocation operations. Instead, verify empty-buffer behavior via a self-contained allocator-observation, fault-injection, and Miri procedure: place an explicit zero-size guard before forwarding any request to the allocator, enforce matching `Layout` (identical size and alignment) between allocation and deallocation, and ensure the negative control trips (via an instrumented test allocator or panic hook) before any allocator undefined behavior can occur. The third test proves writes through the raw pointer reach the safe owner. Invalid inputs (null with nonzero length, length past the allocation) are caller obligations from the `# Safety` section above; never execute them to observe behavior, since Miri reports undefined behavior rather than a test failure. Run these under Miri; a Miri error is a soundness fault even when every assertion passes. No Miri outcome is claimed here.

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn raw_slice_covers_exactly_the_backing_allocation() {
        let data = vec![1u32, 2, 3, 4, 5];
        // SAFETY: data is alive and holds five initialized values.
        let slice = unsafe { raw_slice(data.as_ptr(), data.len()) };
        assert_eq!(slice.len(), data.len());
        assert!(std::ptr::eq(slice.as_ptr(), data.as_ptr()));
    }

    #[test]
    fn raw_slice_accepts_zero_length_dangling_pointer() {
        let ptr = std::ptr::NonNull::<u32>::dangling().as_ptr() as *const u32;
        // SAFETY: dangling pointer is aligned with zero length, no access occurs.
        let slice = unsafe { raw_slice(ptr, 0) };
        assert!(slice.is_empty());
    }

    #[test]
    fn write_through_pointer_reaches_backing_store() {
        let mut data = vec![0u32; 4];
        // SAFETY: index one is inside the four-element allocation.
        unsafe { std::ptr::write(data.as_mut_ptr().add(1), 7) };
        assert_eq!(data[1], 7);
    }
}
```

## Clippy for unsafe

Enable the unsafe-focused lints during development, and deny undocumented unsafe blocks in shipped code so every new block must state its contract. That deny lint requires a `// SAFETY:` note on each `unsafe` block; keep that minimum note and no further inline explanation. Existing gates stay as they are: nothing here weakens them or adds new lint requirements.

```bash
cargo clippy -- -W clippy::undocumented-unsafe-blocks \
               -W clippy::multiple-unsafe-ops-per-block \
               -W clippy::transmute-undefined-repr \
               -W clippy::ptr-as-ptr
```

```rust
#![deny(clippy::undocumented_unsafe_blocks)]
```

## Stacked borrows rules

1. Each borrow creates a new tag on the borrow stack.
2. `&mut T` access pops all borrows above it from the stack and invalidates them.
3. `&T` access is valid as long as the shared reference is on the stack.
4. Raw pointer access is valid only if its tag is still on the stack at the time of access.

The shared borrow below pushes a new tag that pops the raw pointer's `&mut` tag, so the final dereference through the raw pointer is the violation.

```rust
let mut x = 5u32;
let raw = &mut x as *mut u32;
let shared = &x;
let _ = unsafe { *raw };
```
