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

Keep a reviewed snapshot outside this checkout. This file sets commands Git
runs (`core.pager`, `diff.external`, and the `mergiraf` merge driver), so review
the file before enabling it and review each replacement before installing it.

### Locate previous live includes

Before updating an existing installation, inspect both global configuration
files and their includes:

```sh
git config --global --includes --show-origin --get-regexp '^(include|includeif\..*)\.path$'
```

For every include that points inside this checkout, record its source file,
key and exact value. Keep these entries in place until the reviewed snapshot
is installed. Replacing their values in place preserves the order of local
overrides; removing and then appending an include can reverse that order.
Inspect `$XDG_CONFIG_HOME/git/config`, `~/.gitconfig`, and files they include.
The `file:` prefix in the origin output is not part of the filename.

### Stage the reviewed snapshot

Run the following commands from the checkout root. Replace `REVIEWED_COMMIT`
with the commit hash you reviewed. The candidate ends in `.next`, so a failed
copy or an update leaves the installed snapshot intact.

Linux/macOS:

```bash
dstack_commit=REVIEWED_COMMIT
dstack_config="${XDG_CONFIG_HOME:-$HOME/.config}/git/recommended.gitconfig"
mkdir -p "$(dirname "$dstack_config")" &&
  git show "${dstack_commit}:recommended.gitconfig" > "$dstack_config.next"
```

Windows PowerShell, including 5.1:

```powershell
$dstackCommit = 'REVIEWED_COMMIT'
$dstackDirectory = Join-Path $env:USERPROFILE '.config\git'
$dstackConfig = Join-Path $dstackDirectory 'recommended.gitconfig'
$dstackTemporary = Join-Path ([IO.Path]::GetTempPath()) ([guid]::NewGuid().ToString())
New-Item -ItemType Directory -Force -Path $dstackDirectory -ErrorAction Stop | Out-Null
New-Item -ItemType Directory -Path $dstackTemporary -ErrorAction Stop | Out-Null
try {
    $dstackArchive = Join-Path $dstackTemporary 'reviewed.zip'
    git archive --format=zip "--output=$dstackArchive" $dstackCommit -- recommended.gitconfig
    if ($LASTEXITCODE -ne 0) { throw 'Cannot read the reviewed Git configuration.' }
    Expand-Archive -LiteralPath $dstackArchive -DestinationPath $dstackTemporary -ErrorAction Stop
    Copy-Item -LiteralPath (Join-Path $dstackTemporary 'recommended.gitconfig') -Destination "$dstackConfig.next" -ErrorAction Stop
} finally {
    Remove-Item -LiteralPath $dstackTemporary -Recurse -Force
}
```

The ZIP extraction preserves the original bytes. PowerShell's text redirection
is not used, because Windows PowerShell 5.1 would encode the output as UTF-16LE.

### Review and install

On a first installation, read the candidate. On an update, compare the candidate
directly with the installed snapshot so that local edits are visible:

```bash
git --no-pager diff --no-ext-diff --no-textconv --no-index -- "$dstack_config" "$dstack_config.next"
```

In PowerShell, use `$dstackConfig` and `"$dstackConfig.next"` for the two paths.
Git's exit status 1 means the files differ. Save any local overrides before
replacing the snapshot. Put those overrides after the include in your global
configuration, so later snapshot updates preserve them.

After review, install the candidate. Change include entries only after this
operation succeeds.

Linux/macOS:

```bash
mv "$dstack_config.next" "$dstack_config"
```

PowerShell:

```powershell
if ([IO.File]::Exists($dstackConfig)) {
    $dstackBackup = "$dstackConfig.previous-$([guid]::NewGuid())"
    [IO.File]::Replace("$dstackConfig.next", $dstackConfig, $dstackBackup)
} else {
    [IO.File]::Move("$dstackConfig.next", $dstackConfig)
}
```

Windows keeps the replaced snapshot in the reported `$dstackBackup` path.
Keep that backup until the new settings work. If replacement fails, stop and
check the installed file and backup before retrying; do not remove either.
The first-install move refuses to overwrite a file that appears concurrently.

For each existing live include recorded above, replace its exact value in its
original source file. Replace the placeholders with the source filename, full
key, absolute snapshot path and exact old value. This preserves unrelated
includes and the position of settings that already override this include:

```sh
git config --file 'SOURCE_CONFIG' --fixed-value --replace-all 'INCLUDE_KEY' 'SNAPSHOT_PATH' 'LIVE_CHECKOUT_PATH'
```

Use `include.path` for an unconditional include or the full
`includeif....path` key for a conditional include. Keep every argument quoted,
including an old value that starts with `~/`, so the shell does not expand it.
If a value contains an apostrophe, escape it for the shell you use. In a
POSIX shell, write `Dev's config` as `'Dev'"'"'s config'`. In PowerShell,
write it as `'Dev''s config'`. Apply the same escaping to each placeholder.
Replacing a conditional include preserves its condition; a conditional-only
installation remains conditional. Repeat the original
inspection until no live checkout include remains. An installation that
already includes the snapshot needs no registration change.

For a first installation with no existing live or snapshot include, register
the installed path once:

```bash
git config --global --fixed-value --replace-all include.path "$dstack_config" "$dstack_config"
```

In PowerShell, use `$dstackConfig` for both values and check `$LASTEXITCODE`
before continuing. Review the resulting include position and put any local
overrides after it. For example, inspect the effective `core.autocrlf` value
and its origins with `git config --global --includes --show-origin --get-all
core.autocrlf`; the last value takes precedence.

If you install from a release tarball, stage its `gitconfig/recommended.gitconfig`
as the candidate and follow the same review and replacement steps. Never point
an include at the working checkout. Git reads the included file at the position
of its `[include]` entry; later settings in your global configuration override it.

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
