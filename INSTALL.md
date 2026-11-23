# Prerequisites and Install Details

## Required CLI Tools

`ast-grep` | `ripgrep` | `fd` | `eza` | `lsd` | `tokei` | `bat` | `just` | `git-branchless` | `difftastic` | `procs` | `fend` | `hck` | `hyperfine` | and others

### Install Cargo (if not installed)

<https://rustup.rs/>

### Linux/macOS

```bash
export RUSTFLAGS="-C target-cpu=native -C opt-level=3 -C strip=symbols -C panic=abort"

cargo install --locked cargo-binstall
cargo install ast-grep ripgrep fd-find eza lsd
cargo binstall -y bat tokei git-delta just raff-cli difftastic git-branchless zoxide procs bfs fselect tealdeer srgn nomino shellharden grex mergiraf jaq jql hck huniq lemmeknow hyperfine rargs eva fend rip2 sccache
```

### Windows (PowerShell)

```powershell
$env:RUSTFLAGS="-C target-cpu=native -C opt-level=3 -C strip=symbols -C panic=abort -C link-arg=/LTCG -C link-arg=/OPT:REF"

cargo install --locked --force cargo-binstall
cargo install ast-grep ripgrep fd-find eza lsd
cargo binstall -y bat tokei git-delta just raff-cli difftastic git-branchless zoxide procs bfs fselect tealdeer srgn nomino shellharden grex mergiraf jaq jql hck huniq lemmeknow hyperfine rargs eva fend rip2 sccache
```

## Recommended Git Config

[recommended.gitconfig](recommended.gitconfig) is an opinionated global Git configuration: `delta` as
the pager, `difft` as the external diff, histogram diff with `zdiff3` conflict markers, branches and
tags sorted by date and version, `fsckObjects` on fetch, transfer, and receive, `rerere`, and a
`mergiraf` merge driver. Comments in the file are in Korean.

Copy the file into your own config once, then review each update by hand.
A later pull must never change the way git behaves on your machine without
your review. This file sets commands git runs (`core.pager`, `diff.external`,
and the `mergiraf` merge driver), so an unreviewed change could redirect
those commands to something else.
From the checkout root, copy the commit you reviewed:

```bash
git show <commit>:recommended.gitconfig > ~/.config/git/recommended.gitconfig
git config --global include.path ~/.config/git/recommended.gitconfig
```

Before you move to a newer commit, read the diff first:

```bash
git diff <old-commit> <new-commit> -- recommended.gitconfig
```

Copy the new file over only after you have read the diff. If you install
from a release tarball, use its `gitconfig/recommended.gitconfig` copy and
review it the same way. Do not point `include.path` at a file inside this
checkout.

Git reads the included file at the position of the `[include]` entry, so any key you set later in
your own global config overrides the copied file's value.

Requirements:

- Git 2.44 or newer. `fetch.all` is read from 2.44; older Git ignores the key and `git fetch` stays
  single-remote.
- `delta`, `difft`, and `mergiraf` on `PATH`. All three ship in the `cargo binstall` line above
  (`git-delta`, `difftastic`, `mergiraf`). `git diff` calls `difft` on every run, so install it
  before enabling the include.

Pitfalls:

- The `mergiraf` driver is registered but inactive until a gitattributes file selects it. Add
  `* merge=mergiraf` to `~/.config/git/attributes` (global) or to a repository `.gitattributes`.
  The [mergiraf usage guide](https://mergiraf.org/usage.html) recommends `merge.conflictStyle = diff3`
  once the driver is active; this file sets `zdiff3`, which mergiraf's guide says can confuse its base
  reconstruction. If you enable the driver, set `merge.conflictStyle = diff3` after the include.
- `core.autocrlf = input` is the Linux/macOS value. Set `true` on Windows, as the inline comment says.
- `push.autoSetupRemote = true` pushes a new branch to the default remote. With several remotes,
  unset it per repository with `git config push.autoSetupRemote false`.

## Recommended MCP Extensions

### Crucial (automatically installed)

repomix | sequentialthinking-tools | actor-critic-thinking | shannon-thinking

### Additional (manually install if needed)

Time, Context7, Tavily, Exa, Github-grep, Deepwiki, Ref-tools
