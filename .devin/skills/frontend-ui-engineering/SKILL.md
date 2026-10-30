---
name: frontend-ui-engineering
description: 'Use when asked to build or modify production-quality components, layouts, state, and pages with WCAG 2.1 AA and real content. Not for token-system design.'
---

# Frontend UI engineering

You build or modify user facing interfaces in the local working tree so they look hand crafted, work by keyboard and screen reader, and hold up at every breakpoint. This covers components, layouts, state, and pages. It never covers token system design with slop audit gates, and it never touches remote, credential, publish, deploy, or irreversible changes. Rollback is undoing the local edits.

## Bound the work before writing

List every component and page file you will create or modify, and touch nothing outside that list. Colocate each component with its tests and local types. You need four things before writing:

- The component or page and the local paths that will change.
- The project design system: spacing scale, semantic color tokens, type hierarchy, border radius scale. If it is absent, stop and request it. Never invent values the system does not define.
- The required responsive breakpoints.
- Real content (actual labels, copy, and data shapes) for every rendered surface.

Framework and styling mechanism, state management and data fetching approach, and trusted reference screens from the product team help when they exist, but the four items above are mandatory.

## Let tokens carry every value

Use the system tokens exclusively for spacing, color, type, and radius. Semantic colors such as text-primary, bg-surface, and border-default are the palette. Raw hex values, off scale pixel values, and invented spacing have no place here. When you spot one, replace it with the token or remove the pattern.

| Check | Rule |
|---|---|
| Spacing | Every value comes from the spacing scale |
| Color | Every value traces to a semantic token |
| Type | Every size and weight comes from the hierarchy |
| Radius | Every corner comes from the border radius scale |

## Ground a new look in evidence

When the product needs a distinct visual direction, study two or three relevant trusted screens before choosing a layout. Record what you decided about hierarchy, density, navigation, controls, responsive behavior, and interaction states. Turn those decisions into a short design contract naming the screen job, the primary action, the required states, the responsive rules, and the patterns to reject. Rebuild the useful structure in the product's own components, tokens, content, and visual language. Never copy another product's branding, proprietary text, imagery, or exact layout. When no references exist, document the assumptions and verify the result against the design system.

Reject the AI aesthetic against concrete tells: default purple or indigo palettes, excessive gradients, rounded-2xl on everything, oversized uniform padding, stock card grids, generic hero sections where a content first layout serves, layered shadows the system never specified. Use the project actual palette, flat or subtle gradients matching the system, and the system border radius.

## Keep components small and separated

Keep each component under roughly 200 lines and focused on one concern, splitting larger ones by composition. Separate data fetching from presentation: a container handles loading, error, and empty states while a presentational component receives resolved data and renders it. A component past the line limit or one that mixes fetching with rendering gets split before you continue.

## Pick the narrowest state that fits

| Situation | Use this |
|---|---|
| UI owned by one component | Local component state |
| State shared by two or three siblings | Lifted to the parent |
| Read heavy, write rare values such as theme, auth, locale | Context |
| Shareable filters and pagination | URL state |
| Remote cached data | A server state library |
| Complex app wide client state | A global store, and only then |

Lift state or reach for context before prop drilling past one level, and never drill deeper than three levels.

## Make it keyboard and screen reader ready

Prefer the native element first (button, a, input) so controls are focusable by default, and reach for ARIA only when no native element fits. A non interactive element acting as a control needs role, tabIndex, and Enter and Space key handlers. Icon only controls and inputs with no visible label need aria-label, and inputs pair with label htmlFor. When content changes, move focus to the newly revealed content or its close control, and trap focus inside open modal dialogs. Every interactive element ends keyboard accessible with a visible label or aria-label.

Render meaningful empty, loading, and error states for every data driven surface. Loading uses skeleton placeholders marked aria-busy="true", never a blank screen and never a spinner for content areas. Never use color as the sole indicator of state: pair color with text or icons.

## Lay out mobile first with real content

Build mobile first with the project breakpoint system and expand upward, verifying at 320px, 768px, 1024px, and 1440px, or at the project breakpoints when they differ. Placeholder and lorem ipsum text stays out, since it hides the wrapping, overflow, and length problems that real content reveals.

## Verify before calling it done

| Check | What passes |
|---|---|
| Console | Renders with zero console errors |
| Keyboard | Tab reaches every interactive element in a sensible order |
| Screen reader | Structure and labels are conveyed |
| Responsive | Layout holds at all required breakpoints |
| States | Loading, error, and empty states all render |
| System | Every value traces to a design token |
| Scan | axe-core or browser dev tools accessibility scan reports zero warnings |

An accessibility failure (keyboard trap, missing focus target, contrast below 4.5 to 1 for normal text or 3 to 1 for large text, color as the sole state indicator) gets fixed before proceeding. Warnings are never suppressed and inputs are never special cased. If checks still fail, the work is blocked: report the exact failing check and the file, and do not claim success. Ship only the components that pass; mark any unfinished one blocked with its failing check.
