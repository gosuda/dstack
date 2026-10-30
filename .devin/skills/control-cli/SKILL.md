---
name: control-cli
description: 'Use when asked to reproduce, profile, or verify CLI/TUI behavior. Produces a deterministic transcript or profile proof with session cleanup. Not for CLI design advice.'
---

# Reproducing CLI behavior with a transcript to prove it

This skill drives a CLI or TUI inside a temporary terminal session, captures what actually rendered, and leaves a transcript or profile artifact behind. Live PTY sessions get terminated and their runtime scratch gets removed before returning.

Only temporary artifacts change: transcript or profile files under a system temp directory, plus PTY session scratch that is cleaned up. No remote mutation. No source or VCS mutation. No credential or paid mutation. Never modify source, initialize a repository, repair an installation, enable paid calls, or alter the user session store.

## What you need before you start

- The CLI or TUI binary or command to exercise (required).
- The exact reproduction steps, profile target, or verification scenario (required).
- Optionally: expected output, timeout, and environment variables.

## Driving the session

Create a fresh session directory under the system temp path for the captured artifact and the PTY or tmux runtime scratch. Record that directory so cleanup can find it.

Spawn the target under a PTY, or a tmux session attached to a PTY, so interactive behavior stays observable. Send one input at a time and capture the full terminal render before sending the next.

For a reproduction, drive the supplied steps in order and append the terminal state after each action to the transcript artifact. For a profile run, run the target under the chosen profiler and write timing or allocation output into the profile artifact. For a verification, exercise the scenario, compare observed output against the expected output when supplied, and record the pass or fail classification in the transcript artifact.
Terminate the PTY process, or detach and kill the tmux session. Remove the PTY or tmux runtime scratch (pipes and sockets). The captured transcript or profile artifact file remains as the retained proof.

## Running clean

Use temporary credential-free HOME, configuration, data, and session roots when the application supports them. Record the executable, arguments, environment relevant to the scenario, terminal geometry, and launch identity. If concurrent rebuilding could replace the executable, launch a permission-preserving snapshot under the existing temporary-artifact authority.

Declare the terminal capability profile. Answer only the queries appropriate to that profile and record the replies. Copied capability tables can invalidate a legacy-terminal test. Wait for the painted input surface, send one contract-correct input, drain output, and capture the settled rendered state before the next action.

Keep raw bytes and rendered frames with input and byte-offset attribution. Byte claims rest on raw-stream assertions. Paint claims rest on terminal-emulated rows and cursor state. Redraw fragmentation can defeat a phrase search without proving absent paint. A distinctive token may locate a frame without replacing the scenario's complete rendered predicate.

For synthetic approval fixtures, touch only the currently visible permitted question and answer row. Real user consent cannot be inferred, and production approval policy stays enabled. Idle predicates derive from state-bearing output and get tested against a known busy frame. Resize claims require exercising resize after startup.

For a normal-exit claim, invoke the application exit action and observe and reap its child status before cleanup termination. Cleanup terminates only still-live processes owned by this session. Failed captures are retained, and runtime scratch goes away without deleting unrelated processes or user data.

Animation evidence needs a deterministic input script or transcript plus the actual terminal geometry. Representative rendered frames get inspected, including a post-paint frame, before claiming the animation shows the intended behavior. Blank startup frames and nondeterminism are recorded honestly. Recordings stay local. Commits, orphan asset branches, uploads, and hosted URLs need a separate publication owner and grant.

## When the proof falls short

- PTY spawn failure or binary not found. Record the error in the transcript, invent no output, and return blocked with the spawn error.
- Timeout. Terminate the PTY process, append the partial transcript up to the timeout, and return blocked with the timeout boundary.
- Non-deterministic output. Run a second capture, record the observed variance, mark the proof non-deterministic, and return blocked rather than asserting a false pass.
- Any failure ends with the PTY or tmux process terminated and its runtime scratch removed. With no artifact captured, delete the whole temp session directory. Errors are never swallowed, and the pass is never claimed complete when the proof is missing or inconclusive.

The returned artifact holds captured terminal evidence with a final classification: reproduced, profiled, verified-pass, verified-fail, blocked, or non-deterministic. The live PTY session is terminated and its runtime scratch removed before return.
