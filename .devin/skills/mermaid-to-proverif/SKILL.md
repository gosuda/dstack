---
name: mermaid-to-proverif
description: 'Use when a crypto Mermaid sequenceDiagram needs a ProVerif model for secrecy, authentication, replay, or forward-secrecy checks. Not for remote, credential, publish, deploy, or irreversible changes.'
disable-model-invocation: true
---

# Mermaid to ProVerif

You turn a cryptographic Mermaid sequence diagram into a ProVerif model that checks what the diagram actually shows, then you run ProVerif and report each result honestly. You never invent cryptographic semantics the diagram does not contain. This skill writes only the named `.pv` model and report files, and rollback is deleting uncommitted files. Not for remote, credential, publish, deploy, or irreversible changes.

## What to take in

* Required: a Mermaid `sequenceDiagram` block or file containing at least two named participants and at least one message between them.
* Optional: the security properties to verify, one or more of `secrecy`, `authentication`, `replay`, `forward_secrecy`. Defaults to all four when not specified.
* Optional: a ProVerif output filename (`.pv`). Defaults to `<diagram-name>.pv`.

## Parse the diagram

Parse the Mermaid `sequenceDiagram` into an abstract syntax tree. Extract every named participant and every directed message (`A->>B: label`). Record message order. Identify cryptographic operation keywords in each label: `encrypt`, `sign`, `hash`, `sharedkey`, `dh`, `pk`, `sk`. A label with no recognized keyword is a plaintext transfer over the channel type indicated by the arrow style (solid for public, dotted for private).

## Declare primitives, channels, and the attacker

Define the Dolev-Yao cryptographic model from the keywords found above. This stage sets the primitive vocabulary the message mapping below translates into, so free form Mermaid labels become valid ProVerif constructs.

Declare types: `key`, `bitstring`, and any protocol specific types the labels reference.

Declare constructors for each cryptographic operation the diagram uses:

| Mermaid keyword | ProVerif constructor |
|---|---|
| `encrypt` | `fun enc(bitstring, key): bitstring` |
| `pk` | `fun pk(key): key` |
| `sk` | `fun sk(key): key` (or `free` for long term keys) |
| `sign` | `fun sign(bitstring, key): bitstring` |
| `hash` | `fun hash(bitstring): bitstring` |
| `sharedkey` | `fun sharedkey(key, key): key` (or a KDF) |
| `dh` | `fun dh(key, key): key` (Diffie Hellman combine) |

Declare destructors for the inverse operations:

| Operation | ProVerif destructor |
|---|---|
| decrypt | `reduc forall m: bitstring, k: key; dec(enc(m, k), k) = m` |
| verify signature | `reduc forall m: bitstring, k: key; getmsg(sign(m, sk(k)), pk(k)) = m` |

A diagram operation with no standard Dolev-Yao primitive stops the run here: report the unsupported construct instead of inventing semantics.

Define channels: a public `channel c` for messages on public networks (the Dolev-Yao attacker controls these), and private channels for messages the diagram annotations mark authenticated or confidential. The attacker is the standard Dolev-Yao attacker: it can intercept, modify, replay, and compose messages on public channels but cannot break cryptographic primitives.

## Map messages to processes and events

Represent each participant as a `let p = ...` process in ProVerif. Map each actor declaration to `new p:name;`.

Convert each message into process actions using the primitives above:

* A plaintext message `A->>B: m` over a public channel becomes `out(c, m)` in A and `in(c, x: bitstring)` in B.
* An encrypted message `A->>B: encrypt(m, k)` becomes `out(c, enc(m, k))` and `in(c, x: bitstring); let m = dec(x, k)`.
* A signed message `A->>B: sign(m, sk_A)` becomes `out(c, sign(m, sk_A))` and `in(c, x: bitstring); let m = getmsg(x, pk(sk_A))`.
* A hashed message becomes `out(c, hash(m))` with no destructor (hash is one way).
* A Diffie Hellman exchange maps to two `out`/`in` pairs for the public values plus a `sharedkey` or `dh` computation on each side.

Emit `event(e_sent(A, m))` before each `out` and `event(e_received(B, m))` after each `in`, preserving the message order from the parse. These events anchor the reachability and authentication queries below.

Write the `.pv` model file. Prefix it with a `(* ADAPTED FROM: Trail of Bits mermaid-to-proverif skill; CC-BY-SA-4.0; https://github.com/trailofbits/skills *)` comment block and a `(* ASSUMPTIONS: <list of assumptions> *)` block derived from the diagram annotations or human supplied constraints.

## Append reachability and security queries

Append one reachability query `query event(e_start) ... event(e_end) ...` for each end to end message sequence before any security query, so reachability is established before security results are trusted.

Then append security queries for the requested properties:

* `secrecy`: `query secret ~m.;` per sensitive message variable `m`.
* `authentication`: `query event(e_received(A,m)) ==> event(e_sent(B,m)).` per message variable `m`.
* `replay`: `query not event(replay_attempted).` per identified vulnerable transition.
* `forward_secrecy`: `query secret ~m. @weak_agree ...` per session key derived variable.

## Execute ProVerif and write the report

Execute `proverif <output>.pv`. Collect the type check result, all `query` results, and any `WARNING` or `RESULT` line.

Validate the output: the type check must succeed; participant sends and receives in ProVerif must correspond to the original diagram participants; each security query must be preceded by a proved reachability query; all assumptions listed in the file header must be acknowledged in the report.

Write the verification report to `<output>_report.txt` containing type check status, participant correspondence confirmation, each reachability result, each security query result, and the assumption list.

## When verification fails

* Type check failure: ProVerif reports a syntax or type error. Report the error verbatim and stop. Trust no query result and produce no partial model.
* Participant mismatch: sender or receiver counts do not match the diagram participants. Report the mismatch and stop; the model is not trustworthy.
* Security query passing without a prior reachability proof: treat the result as indeterminate (`RESULT i: noninterference_interpreted_as_secrecy_not_proved` or equivalent). Never report it as proved.
* Reachability failure: a required event is unreachable. Report which query cannot be evaluated because its precondition is unreachable. Do not claim the property holds.
* Unsupported construct: stop and report it without inventing constructors, destructors, or event semantics.
* Partial output (crash, timeout, unparsable result): report `verification_inconclusive` with the concrete reason. Claim no success.
* Rollback: when the model file was created and verification failed, delete the uncommitted file before reporting.

## What you hand back

* The named `.pv` model file with the converted protocol model, Dolev-Yao primitive declarations, assumption block, reachability queries, and security queries.
* A verification report `<output>_report.txt` with type check status (`SUCCESS` or failure detail), participant correspondence confirmation or mismatch report, each reachability result, each security query result with `RESULT` classification, and the complete assumption list.
