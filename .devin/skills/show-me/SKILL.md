---
name: show-me
description: 'Use when asked to show/diagram: comparison table, data record, metric card, stepper, mockup, numeric chart, interactive explainer. Modes: widget/chart/explainer. Not for audits: use show-me-your-work.'
---

# Show me

You turn the current topic into one small visual that carries the point: a diagram or code view, a widget (comparison table, data record, metric card, stepper, mockup), a numeric chart, or an interactive explainer with live controls. The visual is ephemeral. It appears in chat and nothing is written to disk.

This skill is strictly read-only. It never writes a file, touches version control, uses credentials, spends money, publishes, deploys, or makes a network or remote call. If the request would need any of that, stop and refuse, naming the boundary that was hit. Never return a partial result.

## When this fits, and when something else does

Reach for this skill when the user says "show this", "show me", or "diagram this" about the current topic, or asks for a comparison table, data record, metric card, stepper, mockup or widget, numeric or series chart, or interactive explainer.

Hand off instead when the real need is elsewhere:

- An auditable decision trail for unattended work belongs to show-me-your-work.
- A standalone interactive sketch rather than an explainer belongs to prototype.
- Teaching a concept with explanation and examples belongs to explain-concept.
- Walking review findings one at a time belongs to show-review.
- A guided multi-turn exploration or a diagram committed into a document is out of scope. Say so and stop.

## What you have to work with

You need the current topic from the prompt and the point the visual must make. When values, labels, layout, or other content are missing, invent representative placeholders that match the requested pattern rather than stalling.

An explicit `mode` (`widget`, `chart`, or `explainer`) always wins. Without one, route by shape. Numeric or series data goes to chart, anything with controls or live-updating state goes to explainer, other widget requests go to widget, and a bare diagram or code-view request stays a minimal inline view.

Explainer requests may also name an interaction model (spatial, sequential, state machine, parameter sweep) and a depth (introductory, intermediate, detailed). Chart requests may name a type (bar, line, doughnut, scatter, sparkline, or another named format) plus title, axis labels, legend, palette, and size constraints. Treat chart data as untrusted at the boundary and check its shape before doing anything with it.

## Draw it in the fewest views that work

Never emit more than two views. If the topic is too broad for that, ask the user to narrow the scope first instead of producing a gallery.

For an ordinary diagram or code-view request, pick the smallest view that carries the point:

| The point is | View |
|---|---|
| How something works step by step | Pseudocode |
| Who calls what | Call tree |
| Component hierarchy | Component tree, naming the file that owns each boundary |
| What lives where | Shallow file tree, one comment per directory saying what it owns |
| Relationships or flow | Diagram (Mermaid or nomnoml) |
| The code itself | Whole block |

For a widget, let the pattern dictate the structure. A comparison table gets two or more columns with row-aligned attributes and highlighted differences. A data record becomes a card or profile with labeled fields and an optional avatar or icon. A metric card shows one large numeric value with a label and an optional trend indicator or sparkline. A stepper shows numbered or icon-labeled steps in a horizontal or vertical cycle with the active step highlighted. A mockup sits in a mobile, chat-bubble, or modal device frame with placeholder UI elements. For a chart, choose an inline SVG or Canvas renderer that fits the type and the data plan. For an explainer, choose the interaction model first, then define the JavaScript state variables with initial values, valid ranges, and exactly which control drives which variable.

## Keep everything inside the fence

Widget and chart output is one semantic HTML fragment. Explainer output is one semantic interactive HTML document with a controls panel, a visualization area, and event handlers that update state and re-render on every interaction. That visualizer fence is the sole output, with no surrounding commentary, explanation, or alternative versions. The client renders it in a sandboxed iframe.

Self-contained is literal. Every stylesheet, script, image asset, data value, label, and configuration is inline. No external stylesheet, script, image URL, font import, CDN link, or fetch call. No `<iframe>`, `<object>`, or `<embed>`. Styling uses standard web-safe color tokens, spacing, and typography through CSS custom properties or inline values that resolve with no network access, never a design-system file or token reference. Add accessible attributes throughout (`role`, `aria-label`, and `alt` text where applicable).

## Check it before you show it

A diagram or code view just needs a final read. Does the rendered view carry the point on its own, with prose supplying only context the visual cannot?

A widget or chart fragment must be well-formed HTML with no unclosed tags and all text content present. Widgets carry no script elements and no event handlers beyond structural attributes. A chart permits exactly one script, its inline SVG or Canvas renderer.

An explainer gets a real functional test. Parse the HTML with a DOM library (jsdom or equivalent) and confirm every control has an event handler pointing at a defined function, every handler touches only declared state variables, and at least two simulated state transitions produce a visible change. Never ship an explainer with a dead control. Fix the control or narrow the explainer scope until everything works.

If validation fails, regenerate once from the same pattern specification and re-validate. A second failure ends the run with a named error, not a third attempt and not a different pattern: `malformed-html` for broken structure, or `NON_CONVERGED` (chart mode) carrying the underlying failure class.

When a UI change needs a diff alongside the visual, match the diff to the view. Use a component diff for UI changes, a file-layout diff for organization, a call-tree diff for call-graph changes, and a pseudocode diff for control-flow changes. Set each visual adjacent to its short supporting text, never in a trailing block of its own.

## When the request cannot become a visual

- Text is the only option, because the idea cannot be rendered in this format at all. Return the concept in prose instead of a visual.
- Scope is too wide. Ask the user to narrow it before generating more than two views.
- Wrong skill. The request is really a standalone sketch, concept teaching, or review walk. Stop and name the skill that handles it.
- `unsupported-pattern`. The request matches no supported widget pattern. Name the seven supported shapes (comparison table, data record, metric card, stepper, mockup, chart, explainer) in one sentence and ask the user to rephrase. Never guess or emit a closest match.
- `INVALID_DATA`. Chart data is malformed. Name the class and stop. Never chart invalid input.
- `UNSUPPORTED_TYPE`. The chart type is not recognized. Name the class and stop. Never invent a fallback type.
- `ambiguous-concept`. The explainer request has several unrelated readings. Ask the user to narrow the scope. Never guess or emit a generic explainer.
- `unrepresentable-interaction`. No control maps to a meaningful state change under any interaction model. Say the concept cannot be represented with the available models. Never emit a non-functional explainer.
- `external-dependencies-detected`. The HTML contains an external URL, CDN reference, or fetch call. Strip the dependency and reimplement with inline assets and pure DOM manipulation.
- Scope violation. The work would need a file write, network call, tool invocation, or repository change. Stop at once and refuse, naming the violated boundary.
