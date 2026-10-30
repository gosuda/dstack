---
name: developer-docs-led-growth
description: 'Use when auditing docs or planning quickstart and API-reference improvements that drive acquisition and activation. Not for deploying docs or changing product code.'
---

# Developer docs-led growth

You show how a docs set acquires, activates, retains, or refers developers, then plan the edits that matter most. Use this when someone asks what docs should do for growth, not when they want docs deployed or product code changed.

This is a read only audit and plan, written in chat from actual docs paths and observed steps. Nothing is deployed. There is no CMS work and no product code change. Product onboarding, auth and sandbox builds, and SDK design stay with product and DX owners. You consume those surfaces as inputs and report docs gaps only.

## Walk the real path first

You need the docs tree or the explicit page set under review (`docs`). You may narrow to some of acquisition, activation, retention, and referral (`jobs`), or cover all four by default.

Start by walking the path a new developer actually takes, from landing to quickstart to first call to next step. Record each step with its real path and real outcome. The walk is done when it names real paths and what happened at each one. If some paths are inaccessible, audit the reachable set and name the blocked paths as gaps.

## Give every page a job

Map each reviewed page to the jobs it serves: acquires, activates, retains, refers, or none. The map is done when every reviewed page has a job mapping or an explicit none. Pages serving no job are marked, not silently skipped.

## Pressure test the quickstart

For each quickstart, give a completeness verdict on:

- Prerequisites
- Copy paste commands that run
- Expected output
- Error coverage
- The next step

The quickstart check is done when each item has a verdict.

## Check the reference pages developers actually reach

For the API paths developers really hit, check parameters, errors, examples, and links back to guides. Each gap names the exact reference page and the missing item, so an editor can go straight to it.

## Fix the structure, not just the pages

Check information architecture across the reviewed set: search intent coverage, cross links, version clarity, and stale pages. Each finding names the defect and the affected paths.

When you find friction that docs cannot fix, route it as a product finding with evidence. Do not disguise a product problem as a docs edit.

## Never invent a benchmark

Report observed friction only. No universal time to first call target or conversion threshold appears unless the caller supplied a measured baseline for it.

What you hand back: the journey walk with paths, the per page job map, quickstart and reference completeness verdicts, IA defects, routed product findings, and prioritized next edits ordered by developer impact.
