---
name: capstone
description: 'Use when the learner is ready to apply cleared concepts in a real project. Not for exercises or quizzes.'
disable-model-invocation: true
---

# Setting a real project for cleared concepts

You give a learner who has finished the lessons something real to build. You size one project around what they can already do, write it up as a brief, hand it over, and judge the finished work against that brief when they return. You never teach new material here and you never touch any progress record.

You write one file only: `capstone-<slug>.md` at the workspace root, with `<slug>` derived from the project name. Deleting that file rolls back the run. There is no remote mutation.

## Collecting what the learner can already do

Read `PROGRESS.md` at the workspace root and collect the cleared concepts. A concept counts as cleared only when its independent rung passed with no hints. If `PROGRESS.md` does not exist, ask once what the learner can already do without help, treat the answer as the cleared set, and do not ask again. If there are no cleared concepts and no usable answer, stop and report that a capstone cannot be sized. Write nothing and invent no syllabus.

You also need the domain or goal the project serves. Take it from the invocation argument when the argument carries it, otherwise ask once.

## Keeping the project a capstone, not a tutorial

Bound the project before writing anything:

- It may use only cleared concepts plus at most one unfamiliar concept. With two or more unfamiliar concepts it is a tutorial, so stop, report the cutoff, and propose a smaller project or classify the request as an exercise. Never write a tutorial brief.
- The deliverable must be something runnable, readable, or usable. Anything smaller is an exercise, so say so and stop rather than write a brief.

Then order the milestones so each one leaves something that works.

## Writing the brief and handing it over

Write `capstone-<slug>.md` following `references/BRIEF-FORMAT.md`. It carries the concepts exercised (the cleared set plus the one unfamiliar concept, if any), the ordered milestones, and the done test. The done test must state a result another person can check. "Understand X" is not a done test.

After the brief is written, stop and hand the learner the brief file path and the done test. The learner leaves to do the project and no further work happens in this session. If scoping or bounding failed after the brief was written, delete the brief rather than leave one that violates the bounds.

## Judging the work on return

The review stage begins only when the learner returns in a later turn or session with finished work. Judge it against the brief's done test and concept list item by item, one verdict per concept and per milestone. Never substitute an overall impression for items. If the work cannot be run, read, or used, report the done test as failed per item without softening the verdict. If review stops partway, keep the per item verdicts already reached and report exactly those, never a whole work verdict without per item evidence.

Name every concept the work does not demonstrate as not cleared and hand that list to the learner as practice items. Write no progress lines. Ownership of any progress record stays outside this skill.
