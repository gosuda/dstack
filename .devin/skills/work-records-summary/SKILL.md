---
name: work-records-summary
description: 'Use when the user asks to discover, group, and summarize work records across multiple systems for a given period or project. Not for organizing projects into child documents or local-only summaries.'
disable-model-invocation: true
---

# Summarizing work across systems

You gather work records from several source systems for one period or project, group them, draft the summary for human review, and only then publish one summary document through the target system API. The human asks for the run explicitly and reviews the draft before anything is published. You produce no local file.

The run is finished when a published summary document holds every grouped cross-source record with no truncation, and you hand back its URL. A partially written or truncated publish is a failure, never a pass.

## What you start with

| Input | Required |
|---|---|
| Date range for the records | Yes |
| Source system credentials and API keys, for each configured source | Yes, missing or refused credentials stop the run before any partial action |
| Grouping approach (by project, by team, by area, or another explicit scheme) | Yes |
| Target document parent ID for the summary | Yes |
| Target system API credentials with create permissions on that parent | Yes |
| Repositories or sources to include or exclude | Optional, when the human specifies |

## Confirming the scope

Present the date range, the configured sources, and the proposed grouping approach, and get explicit confirmation before proceeding. If the human revokes confirmation at any point before the write, stop immediately; no rollback is needed while nothing is written.

## Gathering records

Query each configured source for records in the date range, extracting title, URL, date, and project or area metadata. If a source API fails, stop gathering for that source and report what was gathered and which source failed; do not proceed to publish with partial data. If credentials are missing, stop before any network call and name the absent or unconfirmed credential. If the gather yields zero records, stop, report zero, and fabricate nothing.

## Grouping and drafting

Assign every record to a group under the agreed approach, using titles, descriptions, and metadata. Generate the draft summary with one section per group, writing all records with no truncation or abbreviation. Then present the draft to the human for correction and wait for explicit confirmation or adjustments.

## Publishing and handing back the link

Using the confirmed target parent ID and credentials, create the summary document with one section per group. Each group section holds a group name header, a summary line counting records per source, and subsections listing every record as a link with its date. Give the sections the requested period as the document title. Confirm creation and return the document URL. If the publish lands partial or truncated, treat it as failure and report the last successfully written group without claiming completion.
