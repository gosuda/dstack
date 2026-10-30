---
name: automatic-freeform-graphs-design
description: 'Use when a user wants a looser conceptual graph for exploratory work. Not for remote, credential, publish, deploy, or irreversible changes.'
---

# Automatic freeform graphs design

Some work needs a map, not a plan. This builds a loose conceptual graph of a topic: ideas and questions as nodes, relationships as labeled edges, with unknowns left visible instead of forced into an order. The artifact is one plain-text file a human can read and revise without tooling. It changes nothing else on disk, and deleting or overwriting that one file reverts everything.

## Start from the topic in front of you

You need an exploratory topic or problem statement (a question, a half-formed idea, a domain, a bundle of concerns) and any existing notes or fragments the graph should absorb. An output path is optional; without one, write into the working directory.

Read the topic and notes first and name what kind of exploration this is: open-ended question, design-space survey, concept mapping, or unknown-territory scouting. If the topic is too vague to yield nodes, ask the human for one concrete anchor (a question, a constraint, a stakeholder concern) and proceed from there. Never fabricate concepts to fill the graph.

## Grow nodes, not sequences

Pull out concepts, questions, unknowns, and hypotheses as candidate nodes. Resist turning them into a dependency order. This is exploration, not execution planning, so a node earns its place by being genuinely in the territory, not by fitting a chain.

## Connect loosely and allow cycles

Map relationships as labeled edges using exploration-suited types: influences, tensions, supports, contradicts, depends-on-maybe, raises-question-of, unknown-link. Cycles, bidirectional edges, and self-references are all welcome where the territory calls for them. If the graph collapses into a linear chain or a strict DAG, the work has drifted toward planning. Restart from this step and deliberately use non-dependency relationship types (tensions, unknowns, contradictions) to break the chain.

## Mark what you do not know

Give every node and edge a confidence marker: certain, suspected, or unknown. Mark open questions explicitly so the graph surfaces ignorance instead of hiding it. A graph that looks fully certain about half-formed territory is lying.

## Name the themes and the bridges

Find clusters of tightly connected nodes and label them as provisional themes. Find the edges spanning clusters and flag them as bridges: high-value exploration targets, the places where one pocket of the map talks to another.

If the graph grows too dense to read, collapse low-confidence peripheral nodes into a summary node and keep the high-value bridges visible, preserving the full node list in an appendix section.

## Write it down so a human can revise it

Produce the artifact in plain text or markdown with five sections in this order:

1. Node list with confidence markers
2. Labeled edge list, cycles permitted
3. Provisional cluster summary
4. High-value bridge targets
5. Open questions

Then read it back against the original topic. It should surface the key unknowns without imposing a false dependency order. Where a region is sparse or missing, add nodes and edges rather than leaving gaps. If you stop before this review, deliver the graph as-is with an explicit note naming the review you did not complete. Never claim the graph is finished when it is not.
