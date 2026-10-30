---
name: control-ui
description: 'Use when asked to verify or reproduce browser or Electron UI behavior with before-and-after evidence and no leftover processes. Not for remote, credential, publish, deploy, or irreversible changes.'
---

# Control UI

You prove what the UI actually does, with pictures. When someone asks whether a browser or Electron surface behaves as expected, you capture it before and after the behavior, compare the two, and leave no running process behind. The run is done when both evidence sets sit in one named directory and nothing you launched is still alive.

This skill never touches remote URLs, never uses credentials the human did not hand you, and never publishes, deploys, or mutates anything beyond its evidence directory. Everything it writes is reversible local output: rollback is deleting the evidence directory and killing any spawned process.

What you need before starting: a UI target, which is required and must be a local app command, a local URL, or an Electron entry supplied by the human. Optional extras are a viewport size, an authentication state file, and an evidence directory name, which defaults to a timestamped folder under the working directory. If the target is remote or needs credentials the human did not provide, refuse it rather than working around it.

## Capture before, act, capture after

Create or reuse the named evidence directory under the working directory first, so every artifact has somewhere to land.

Then launch the app or browser, navigate to the target, and record the before state into the evidence directory as `before.*`: the viewport, a screenshot, the console log, and the relevant DOM state.

Next perform the behavior under test, a click, input, or navigation, or follow the reported reproduction steps exactly. Write down each step you take as you take it.

Then record the after state the same way, as `after.*`: screenshot, console log, and DOM state. Compare the two sets against the expected behavior and record one classification: pass, fail, or mismatch, citing the evidence file names that differ.

Finally terminate every app or browser process you spawned and confirm none remain.

## When the run breaks

The app or browser does not start: record the launch error, leave no process behind, and return blocked naming the error.

The after state matches the before state: keep both evidence sets, return the mismatch classification, and do not invent a difference that is not there.

A spawned process outlives the capture: kill it by PID, and if it cannot be killed return blocked naming the PID.

Capture fails halfway: keep the before evidence, discard the incomplete after artifacts, and return blocked naming the failed capture step.

## What you hand back

A before/after evidence directory with screenshots, console logs, and DOM state, plus a one-line classification (pass, fail, mismatch, or blocked) citing the evidence file names.
