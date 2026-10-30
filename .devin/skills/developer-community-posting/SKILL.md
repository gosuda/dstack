---
name: developer-community-posting
description: 'Use when preparing a Hacker News or Reddit post package with eligibility, disclosure, and do-not-post conditions. Not for posting, replying, voting, or account activity.'
disable-model-invocation: true
---

# Developer community posting

Prepare a Hacker News or Reddit post so a human can post it well, or decide not to post at all. This skill only prepares; the human posts, replies, and votes. Nothing here ever posts, replies, votes, asks for upvotes, creates accounts, runs alternate accounts or rings, astroturfs, or circumvents moderators.

Hacker News and Reddit are separate internal profiles with different rules. Never flatten them into one set of advice.

## What you need before starting

- `venue` (required): `hacker-news` or `reddit:<subreddit>`.
- `material` (required): the technical substance (launch, Show-style demo, question, or technical writeup), with sources.
- `standing` (optional): the poster account history the user discloses, such as age and prior participation. It informs eligibility risk only; automation is never used to improve it.

Drafts never leave chat without explicit target and content consent, and consent to draft is never consent to post.

## Checking eligibility first

Run the eligibility and risk check against current venue rules, citing URLs and observation dates: account standing, venue fit, prior-post history, duplicate or merge-bait risk, and moderator-edit expectations. End with either proceed-with-risk or do-not-post, stated plainly. If the venue rules cannot be verified, mark them unknown and stop. Never proceed on lore, timing myths, karma ladders, or algorithm claims. Where do-not-post conditions hold (duplicate, rule mismatch, standing risk, astroturf pressure), stop with the reasons; never reframe the package to evade rules.

## Drafting to the venue profile

Both venues share a baseline: human voice, technical specifics, affiliation disclosure, no duplicate posts, and the creator available to answer as a human task. On top of that, follow only the selected profile:

- Hacker News: no upvote asks, no voting rings, no multiple-account voting, no astroturf. The title states the technical substance, and the first comment adds substance the linked page lacks.
- Reddit: the subreddit rules are read and cited, comment-first history is honored, disclosure goes in the post or flair as the rules require, no vote manipulation, no alternate accounts. Cross-posts are tailored per community with separate risk notes.

Draft the title, body, and first-comment substance (what to add beyond the link, not a verbatim script to paste blindly), each matching the venue shape and length norms, with reasons.

## Response guidance and disclosure

Write guidance covering which questions the human answers and which to decline, plus how to handle corrections, hostile threads, and moderator edits. Then write the disclosure line the human uses, placed where the venue requires affiliation to appear.

## What you hand back

A preparation package: the eligibility verdict with cited rules, title, body, first-comment guidance, response guidance, the disclosure line, do-not-post conditions, and a human-action checklist naming who posts, from which standing account, with the human deciding when, plus the explicit reminder that no agent action posts.
