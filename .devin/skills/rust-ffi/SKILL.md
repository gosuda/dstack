---
name: rust-ffi
description: 'Use when calling C libraries from Rust, generating bindings with bindgen, exporting Rust functions to C with cbindgen, writing safe wrappers over unsafe FFI, or linking system libraries.'
---

# Rust FFI

Rust calls C through `unsafe extern` blocks and exports to C through `extern "C"` functions. The unsafe surface stays at the boundary; everything behind it is a safe API.

Scope stays local and reversible. This skill writes only the target crate's `Cargo.toml`, `build.rs`, wrapper header, source files, and the generated C header inside the project, with version control as the rollback. bindgen output lands in `OUT_DIR`; cbindgen output lands at the named header path. The work is done when `cargo build` succeeds, the boundary is declared or generated, and every unsafe call sits behind a safe wrapper or an exported `extern "C"` function.

What you need before starting:

- The C library (required). Headers, library name, and whether it is system installed, vendored, or built from source.
- The direction (required). C to Rust, Rust to C, or both.
- The crate layout (optional). Single crate or a `-sys` crate plus a safe wrapper crate; inferred from the workspace when omitted.
- The edition (optional). Edition 2024 is assumed, so extern blocks are `unsafe extern` and `no_mangle` is written `#[unsafe(no_mangle)]`.

## Declaring a small surface by hand

For a handful of calls, declare them directly and skip generation:

```rust
use std::ffi::{c_char, c_int, c_void, CString};

unsafe extern "C" {
    fn my_lib_init(config: *const c_char) -> c_int;
    fn my_lib_process(handle: *mut c_void, data: *const u8, len: usize) -> c_int;
    fn my_lib_cleanup(handle: *mut c_void);
}
```

Move on when the strategy is named.

## Generating bindings with bindgen

When the header surface is real, add `bindgen = "0.73"` under `build-dependencies` and restrict output with allowlists so system headers do not leak in:

```rust
// build.rs
fn main() {
    println!("cargo:rerun-if-changed=wrapper.h");
    println!("cargo:rustc-link-lib=mylib");
    println!("cargo:rustc-link-search=/usr/local/lib");

    let bindings = bindgen::Builder::default()
        .header("wrapper.h")
        .clang_arg("-I/usr/local/include")
        .allowlist_function("mylib_.*")
        .allowlist_type("MyLib.*")
        .allowlist_var("MYLIB_.*")
        .derive_debug(true)
        .derive_default(true)
        .blocklist_type("__va_list_tag")
        .generate()
        .expect("bindgen failed");

    let out = std::path::PathBuf::from(std::env::var("OUT_DIR").unwrap());
    bindings.write_to_file(out.join("bindings.rs")).unwrap();
}
```

```rust
// src/lib.rs
#![allow(non_upper_case_globals)]
#![allow(non_camel_case_types)]
#![allow(non_snake_case)]

include!(concat!(env!("OUT_DIR"), "/bindings.rs"));
```

This step lands when `build.rs` writes `bindings.rs` into `OUT_DIR` and `lib.rs` includes it. When bindgen cannot parse the header, shrink `wrapper.h` to the needed includes and pass include paths and defines through `clang_arg`. When the library is missing at link time, add `cargo:rustc-link-search`, probe with pkg-config, or build the vendored source with `cc`.

## Structuring the sys crate

A `-sys` crate owns the link and the raw bindings; the safe crate depends on it. The `links` manifest key tells Cargo which native library the crate links:

```text
mylib-sys/
  Cargo.toml      # links = "mylib"
  build.rs        # probes pkg-config, falls back to a vendored cc build
  wrapper.h
  src/lib.rs      # includes the generated bindings
mylib/
  Cargo.toml      # depends on mylib-sys
  src/lib.rs      # safe API
```

```rust
// mylib-sys/build.rs
fn main() {
    if let Ok(lib) = pkg_config::probe_library("mylib") {
        for path in lib.include_paths {
            println!("cargo:include={}", path.display());
        }
        return;
    }
    cc::Build::new()
        .file("vendor/mylib/src/mylib.c")
        .include("vendor/mylib/include")
        .compile("mylib");
    println!("cargo:rerun-if-changed=vendor/mylib/src/mylib.c");
}
```

## Wrapping every unsafe call

Check for null handles, map C error codes to `Result`, free resources in `Drop`, and add `Send` or `Sync` only after verifying the C library threading contract:

```rust
pub struct MyLib {
    handle: *mut ffi::mylib_t,
}

impl MyLib {
    pub fn new(config: &str) -> Result<Self, Error> {
        let c = CString::new(config).map_err(|_| Error::InvalidConfig)?;
        let handle = unsafe { ffi::mylib_create(c.as_ptr()) };
        if handle.is_null() {
            return Err(Error::InitFailed);
        }
        Ok(Self { handle })
    }
}

impl Drop for MyLib {
    fn drop(&mut self) {
        unsafe { ffi::mylib_destroy(self.handle) };
    }
}
```

No safe public function should reach `unsafe` without a validity check. Map a null-returning C constructor to `Result` or `Option` and never store a null handle. Keep the default of neither `Send` nor `Sync` while the C locking contract stays unverified. Never let a panic cross the boundary: return an error code or use `catch_unwind`, since unwinding out of an `extern "C"` function aborts. Use `extern "C-unwind"` only when the C side is built to propagate.

## Exporting Rust to C with cbindgen

Exported functions are `extern "C"` with `#[unsafe(no_mangle)]`; ownership crosses the boundary through `Box::into_raw` and `Box::from_raw`:

```rust
#[unsafe(no_mangle)]
pub extern "C" fn mylib_destroy(ptr: *mut MyLib) {
    if !ptr.is_null() {
        unsafe { drop(Box::from_raw(ptr)) };
    }
}
```

```rust
// build.rs
fn main() {
    let crate_dir = std::env::var("CARGO_MANIFEST_DIR").unwrap();
    cbindgen::Builder::new()
        .with_crate(crate_dir)
        .with_language(cbindgen::Language::C)
        .generate()
        .expect("cbindgen failed")
        .write_to_file("include/mylib.h");
}
```

This step lands when the generated header exists at the configured path.

## Linking and proving the boundary

Emit link directives from `build.rs` (`cargo:rustc-link-lib=static=name`, `dylib=name`, or `framework=name` on macOS, plus `cargo:rustc-link-search=` for nonstandard paths). `cargo build` should link without unresolved `-l` errors. Then build the crate, confirm the generated bindings or header exist, and exercise one call across the boundary. The call should return the expected result. When the boundary stays unproven, files already written remain and the report names the failed step with its command output, with version control as the rollback. Full builder options, `cbindgen.toml` keys, `cc`, pkg-config, and safety patterns live in `references/bindgen-cbindgen.md`.

## What you hand back

A crate that builds with a verified call across the FFI boundary, plus a report listing files written, the safe API surface, and the link directives emitted.
