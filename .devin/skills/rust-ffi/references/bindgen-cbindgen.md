# bindgen and cbindgen configuration reference

Use bindgen when Rust must call C: it reads a C header and generates matching Rust declarations. Use cbindgen for the opposite direction: it reads Rust items and writes a C or C++ header. Build the C side with the `cc` crate and locate installed system libraries with `pkg-config`, all driven from `build.rs`.

## bindgen options

### Builder configuration

Narrow generation with allowlists so only your library's symbols land in the bindings; `allowlist_item` matches every kind at once. Hide internals with blocklists. Control how C enums surface with `bitfield_enum`, `newtype_enum`, `constified_enum_module`, or `rustified_enum`, and which standard traits structs derive. Mark incomplete C types opaque so bindgen never lays out their fields. Emit lint allowances with a raw line. For dynamic loading instead of a static link, set `dynamic_library_name`.

```rust
bindgen::Builder::default()
    .header("wrapper.h")
    .clang_arg("-I/usr/local/include")
    .clang_arg("-DFEATURE=1")
    .clang_arg("--target=aarch64-linux-gnu")
    .allowlist_function("mylib_.*")
    .allowlist_type("MyLib.*|MyErr.*")
    .allowlist_var("MYLIB_[A-Z_]+")
    .allowlist_item("mylib_.*")
    .blocklist_function("mylib_internal_.*")
    .blocklist_type("__.*")
    .derive_debug(true)
    .derive_copy(true)
    .derive_default(true)
    .derive_hash(true)
    .derive_eq(true)
    .derive_ord(true)
    .bitfield_enum("MyFlags")
    .newtype_enum("MyError")
    .constified_enum_module("MyStatus")
    .opaque_type("FILE")
    .no_partialeq("MyStruct")
    .raw_line("#[allow(non_upper_case_globals, non_camel_case_types, non_snake_case)]")
    .rustified_enum("MyEnum")
    .generate()
```

### Command-line bindgen

Install the CLI, then generate bindings directly. Pass allowlists as flags and forward include paths to Clang after `--`.

```bash
cargo install bindgen-cli

bindgen wrapper.h \
    --allowlist-function 'mylib_.*' \
    --allowlist-type 'MyLib.*' \
    -- -I/usr/local/include \
    > src/bindings.rs
```

### bindgen.toml (configuration file)

```toml
# bindgen.toml
allowlist_function = ["mylib_.*"]
allowlist_type = ["MyLib.*"]
derive_debug = true
derive_default = true
```

## cbindgen options

### cbindgen.toml

`export.include` names the only items that appear in the header; `export.exclude` removes internals. Rename items, prefix every function declaration, emit feature guards, set enum variant casing, add struct trait derivations, and pick the doc-comment style.

```toml
language = "C"   # or "C++"
documentation = true
documentation_style = "c"       # or "doxy"

[export]
include = ["MyLib", "MyError"]  # Only export these
exclude = ["InternalState"]

[export.rename]
"MyLib" = "mylib_t"             # Rename in generated header

[fn]
prefix = "MYLIB_API"            # Add prefix to all function declarations

[defines]
# Generate #define guards
"feature_a" = "MYLIB_FEATURE_A"

[enum]
rename_variants = "ScreamingSnakeCase"

[struct]
derive_eq = true
derive_hash = true
```

### Language options

Each `with_language` call sets the output language and replaces any earlier one, so a builder chaining `C` then `Cxx` emits only the C++ header: keep exactly one call per generated header. The example below emits a **C** header that stays includable from C++ sources: the guard prevents double inclusion, and `with_cpp_compat(true)` makes cbindgen emit the `#ifdef __cplusplus` / `extern "C"` wrapper itself.

```rust
cbindgen::Builder::new()
    .with_crate(&crate_dir)
    .with_language(cbindgen::Language::C)
    .with_cpp_compat(true)
    .with_include_guard("MYLIB_H")
    .generate()
```

To emit a C++ header instead, make the same single call with `cbindgen::Language::Cxx`, add `.with_namespace("mylib")` (namespaces apply to C++ output only), and drop `.with_cpp_compat(true)`: cbindgen wraps declarations in `extern "C"` itself in C++ mode. In both cases set the header guard with `with_include_guard`.

## cc crate for building C code

List sources, headers, defines, and flags in `build.rs`. Enable position-independent code for shared linking. The `compile` call builds the static library and emits the link directive for it.

```toml
[build-dependencies]
cc = "1.0"
```

```rust
// build.rs
fn main() {
    cc::Build::new()
        .files(["src/a.c", "src/b.c"])
        .include("include/")
        .define("FEATURE_X", "1")
        .flag("-std=c11")
        .flag_if_supported("-Wno-unused-parameter")
        .pic(true)
        .static_flag(true)
        .warnings(true)
        .extra_warnings(true)
        .compile("myhelper");
}
```

`compile("myhelper")` builds `libmyhelper.a` and emits `cargo:rustc-link-lib=static=myhelper`.

## pkg-config integration

Probe the installed library for its version and use its reported include paths for bindgen. Fall back to manual link directives when probing fails.

```toml
[build-dependencies]
pkg-config = "0.3"
```

```rust
// build.rs
fn main() {
    match pkg_config::Config::new()
        .atleast_version("2.0")
        .statik(false)
        .probe("mylib")
    {
        Ok(lib) => {
            for path in &lib.include_paths {
                println!("cargo:include={}", path.display());
            }
        }
        Err(e) => {
            eprintln!("pkg-config failed: {e}");
            println!("cargo:rustc-link-lib=mylib");
            println!("cargo:rustc-link-search=/usr/local/lib");
        }
    }
}
```

## Common FFI safety patterns

Reject a null return at the boundary by building the wrapper only when the pointer is non-null.

```rust
pub fn new() -> Option<Self> {
    let ptr = unsafe { ffi::create() };
    if ptr.is_null() {
        None
    } else {
        Some(Self { ptr })
    }
}
```

Tie a borrowed handle to the lifetime of its owner with `PhantomData` so the wrapper cannot outlive the C object.

```rust
pub struct BorrowedHandle<'a> {
    ptr: *mut ffi::handle_t,
    _marker: std::marker::PhantomData<&'a ()>,
}
```

Mark the wrapper `Send` only after verifying the C library is thread-safe, and `Sync` only when it uses internal locking. An incorrect impl is a data race the compiler can no longer catch.

```rust
unsafe impl Send for MyLib {}
unsafe impl Sync for MyLib {}
```
