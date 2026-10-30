---
name: compile-3d-workflow
description: 'Use when the user asks for direction and a compilable 3D workflow from an interview. Not for remote, credential, publish, deploy, or irreversible changes.'
---

# Compile 3D workflow

You turn an interview about direction into a workflow file a machine can check: a task DAG (topology), concept groups over those tasks (ontology), and control cycles (feedback loops). You interview, you author, you validate, you write the file. Nothing remote, no credentials, no publish, no deploy, nothing irreversible.

This stays local and reversible: you write only the named local artifact file, and rollback is deleting that file. No remote state is touched.

What you need before starting:

- A direction interview with the user, supplying all four of these, recorded verbatim and never inferred: the problem being solved, what success looks like, binding constraints, and what is explicitly out of scope.
- The output file path for the workflow artifact. Required.

## Author the artifact from the interview answers

Build the three dimensions from what the user said. The file is YAML with this structure:

```yaml
problem: <string>
success_criteria: <string>
constraints: [<string>, ...]
out_of_scope: [<string>, ...]
topology:
  nodes:
    - id: <string>
      task: <string>
      depends_on: [<node_id>, ...]
ontology:
  groups:
    - name: <string>
      members: [<node_id>, ...]
feedback_loops:
  - name: <string>
    sensor: <string>
    comparator: <string>
    actuator: <string>
```

Topology is a DAG of tasks. Each node carries an id, a task description, and a `depends_on` list naming the node ids it waits on. No cycles, no node depending on itself, and every `depends_on` entry must reference an existing node id. Ontology groups are named concept clusters over the work: every group is non-empty and every member must exist in the topology. Feedback loops are cybernetic control cycles: each loop names its sensor (what is measured), comparator (what is expected), and actuator (what action re-routes), all as non-empty strings.

## Validate every structural check before writing

Check each rule, and stop with the specific defect named if any check fails:

- Every node has a unique id and a non-empty task.
- Every `depends_on` entry references an existing node id.
- No cycle exists in the dependency graph (a topological sort succeeds).
- Every ontology group is non-empty and every member references an existing node id.
- Every feedback loop names a non-empty sensor, comparator, and actuator.

Only a file passing every check counts as a compiled workflow. A partially written file is not one: delete it and report the rollback.

Write the validated artifact to the output path as YAML, then state the rollback path (delete the local artifact file) and that no remote state was touched.

## When the workflow cannot compile

- Interview incomplete: the user cannot supply the problem, success criteria, constraints, or scope. Stop and report which inputs are missing. Do not infer or fabricate direction.
- Schema validation failure: a node without an id or task, a `depends_on` entry pointing at a non-existent node, a cycle in the graph, an empty ontology group or a member pointing nowhere, or a feedback loop missing its sensor, comparator, or actuator. Report the specific defect and stop. Do not present a partial artifact as complete.

## What you hand back

A validated local YAML artifact at the output path, containing the DAG topology, ontology groups, and feedback loops, with every structural check passing.
