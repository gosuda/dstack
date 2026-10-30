---
name: workflow-from-chats
description: 'Use when a user asks to mine recent chats for workflow preferences. Don''t use for tasks that require source or remote-system changes.'
disable-model-invocation: true
---

# Learning workflow preferences from recent chats

You write nothing and change no source or remote system. No file, VCS, credential, paid, published, deployed, or remote mutation. Your whole result is a report returned in chat.

## Confirming what to read

Start with the chat history source and the scope around it. You need one required input:

- Chat history, or a path it can be read from.

These narrow the scope and are optional:

- Time window.
- Topic filter.
- Named agent or session identifier.

If no readable chat source exists, report the failure with a specific error and do not proceed.

## Reading sessions and extracting signals

Enumerate the chat sessions inside the window, bounded by whatever filter was supplied. From each session, pull out recurring intent patterns, explicit preference statements, tool use frequencies, and rejected suggestions. If no extractable signals turn up, return a report saying zero preferences were found. Never fabricate patterns.

## Sorting signals into a profile

Classify every extracted signal into one of these workflow categories:

- Automation.
- Prompting.
- Tooling.
- Routing.
- Escalation.

Then synthesize a preference profile from the classified signals. Flag low confidence signals and exclude uncorroborated single instance claims. If synthesis only goes partway, return the partial result with explicit gaps listed. Never fill gaps by invention.

## Proposing artifacts where evidence is strong

For high confidence preferences, propose named workflow artifacts. Each proposal names its trigger, inputs, steps, and done criterion. If no proposal holds up, return the profile without proposed artifacts rather than inventing any.

## What you hand back

A structured report in this order:

1. Extracted preference signals with source citations.
2. Synthesized preference profile with confidence ratings.
3. Proposed workflow artifacts with trigger, inputs, steps, and done criterion.
