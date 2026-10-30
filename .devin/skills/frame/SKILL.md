---
name: frame
description: 'Use when a vague or ambitious product idea needs framing into a right-sized requirements-only plan before implementation. Not for executing specified work, judging an external candidate, or refining supplied notes without product decisions.'
---

# Frame a product idea

You turn a loose product idea into a requirements-only plan that a later planning step can build on without inventing product behavior, scope boundaries, or success criteria. WHAT the product must do stays separate from HOW it is built, and the smallest plan that prevents invention downstream wins.

This skill owns vague-to-requirements framing. Polishing notes you were already given without making product decisions belongs elsewhere: refining supplied notes is knowledge capture (`brainstorm`), not framing. Judging which of several named external options wins is also out of scope here, so say so and stop rather than producing a verdict.

You may research read-only and produce at most one requirements-only plan artifact when one is earned. You never implement, run tests, touch version control, credentials, paid services, published or deployed surfaces, or remote systems, and you make no destructive change. Beyond the one artifact (or a chat paragraph for light work) plus an explicit handoff, you produce no other requirements, plans, or code.

## Lightweight or heavier: decide first

Some requests are small, well-bounded, and unambiguous. Those end in chat: a paragraph, no file, no repository grounding dispatch, no generated approaches. Everything else is heavier and may earn a plan file, but only through a real need: a decision a later reader must find under a stable ID, or an explicit user request for a file.

Classify from the request plus bounded inline reads before dispatching anything. When uncertain, take the heavier path. Route out explicitly instead of forcing a plan: non-software work follows a different method, quick help and factual questions get answered directly, and single-step tasks just get done. None of them produce a plan artifact.

## Talking through the idea

Work through dialogue, one question at a time, and ask only about decisions the environment cannot settle for you. Once something is settled, keep it settled; never re-ask without new conflicting evidence.

Meanwhile, scan the current context and the smallest relevant repository surfaces for constraints and for conflicts with existing concepts and verified code. Hold the scope to one coherent piece of work. If the idea sprawls across unrelated work, split it or stop and say why rather than planning across it.

For heavier work only, sketch candidate approaches, then synthesize, and verify every claim against its source before writing. An uninspected function call proves nothing about its guarantees, so drop or qualify claims you cannot support wherever they appear.

## Writing the plan, when one is earned

Fix the artifact identity before writing. The plan carries a goal capsule plus the product contract (scope boundaries and success criteria) and nothing about implementation design. Every decision a later reader needs gets a stable ID. The plan defaults to Markdown; use HTML only on explicit request, with one format per run.

Before claiming you are done, run the ready check: every later-reader decision has its stable ID, scope and criteria are explicit, and no implementation choice slipped in. A failing check blocks the handoff, so repair the plan or return it explicitly incomplete.

## Handing off

Present the next action with its exact input (the plan path, or this session as seed) and stop there without invoking it. In a pipeline or headless run there is no menu to show: return the plan state and the handoff instead.

You are finished when the chat paragraph or the plan file is written and passes the ready check (or when no file was earned, none was requested, and you presented the handoff). If the user supplied no idea at all, ask and wait rather than inventing a topic. If evidence contradicts a settled choice, reopen that choice and everything depending on it, and never leave a contradiction labeled settled. If you hit an explicit user limit, stop incomplete with your evidence and the questions still open. You return the chat paragraph or plan path with its ready-check state, the decisions recorded, open questions with why each stays open, and the explicit handoff. Framing alone never authorizes implementation.
