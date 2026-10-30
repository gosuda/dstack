# Authoring procedure

The ordered path that creates or changes a skill directory on disk. The levers in `SKILL.md` decide what the document should be; this file is how the change lands.

## Boundaries

- Write only the requested local skill artifacts and the repository-owned registration or attribution surfaces they require.
- Publish, install, commit, and remote changes stay out unless the user separately asks for that operation as its own act.
- Never create a second skill when the existing skill can own the job without splitting its method.
- Never preserve an old name, route, or layout after every live caller has moved.

## The path

Follow these in order. Each builds on the last, from naming the job to proving the result.

1. Name the change: create, port, rephrase, upgrade, merge, or split. Say in plain words whose job this is, what good looks like, and what stays out. When those facts do not define one coherent operation, stop.
2. Search the local skill set by trigger, promised result, and method. Deepen or merge into the skill that already owns the job. Open a new directory only when both the job and the procedure are distinct.
3. Read the repository's skill conventions, one strong neighboring skill, and every live route to or from the target. Honor repository-owned schema and registration rules, and leave the neighbor's domain language where it is. Call every document, phase, and task by the request's own semantic names.
4. For a port, read the upstream skill and its license at a pinned revision. Separate portable method from vendor names, harness syntax, obsolete paths, and promotional framing. Record required credit in the repository's canonical notice or attribution source. Never invent a per-skill provenance file when the repository owns attribution elsewhere, and open no side record beyond what the work genuinely generalizes.
5. Settle how the skill is reached before writing the body. The directory name and the frontmatter name agree in lowercase hyphenated words, and the description tells the agent in third person when to fire, what good looks like, and the nearest thing it is not. The skill states plainly what it may touch and what done looks like for this skill alone.
6. Design one chronological procedure from validated input to the completion condition. Name each decision where the agent could otherwise guess. Keep hard bans explicit. Cut generic receipts, ceremonial phase tables, and repeated per-step closings that add no decision or check.
7. Keep `SKILL.md` focused. Move bulky catalogs, schemas, and branch-specific rules into one level of `references/` files, and state the exact condition that loads each file. Add an `assets/` template only when the output plan is contractual.
8. Add a `scripts/` program only for deterministic work that prose handles badly, such as parsing, validation, or repetitive generation. Give it a narrow CLI, useful errors, no hidden network calls, and one direct behavioral check that exercises what it does. Write the code to read clearly on its own. Never create empty directories.
9. Add or regenerate the harness manifest and membership entry the repository requires. Keep the display name unique and the short description useful at list-view length.
10. Migrate every live inbound and outbound route. Delete absorbed skill directories, stale aliases, obsolete references, and dead registration rows in the same change.
11. Check metadata, directory-name identity, relative links, route reachability, reference load conditions, script behaviour, registration, and the repository's native validation. Repair each failure at its source; never weaken the check to pass it, and never accept a weak test as proof. A gate that cannot pass on honest material means the document is not yet predictable: return the failed check with the evidence.

## When it goes wrong

| Failure | Action |
|---|---|
| The job is not distinct | Merge it into the current owner or report that no new skill is justified. |
| The source license is absent or unclear | Keep an explicit no-license acknowledgement and claim no reuse rights. |
| A required route target does not exist | Stop the cutover, restore a reachable route, and recheck route validation. |
| Files were created but validation fails | Remove only the uncommitted artifacts this run created, repair the contract, and validate again. |
| The request would publish or destroy state | Stop at the local artifact unless the user explicitly authorizes that separate operation. |

## What to hand back

Return the changed skill paths, the user job each skill now owns, merge or deletion decisions, attribution changes, and the exact validation evidence.
