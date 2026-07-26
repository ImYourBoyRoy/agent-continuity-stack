---
name: maintain-web-design-system
description: Create or extend a web design system, tokens, theming, component styling, responsive behavior, and accessibility. Use for substantial UI-system work, not isolated cosmetic fixes or asset conversion.
---

# Maintain Web Design System

Extend the existing visual authority without creating a competing style layer.

If Portable Web Toolkit management is established by repository instructions,
`Web_Toolkit/`, toolkit scripts, or a toolkit site profile, use its Brand Guide
and validation tools as the specialist implementation authority. Do not create
a parallel token, stylesheet, or brand-validation system.

## Find the visual authority

Inspect:

- design or brand guidance
- token files and theme configuration
- global stylesheet entry points
- component primitives and canonical examples
- typography and icon systems
- accessibility requirements
- visual-regression infrastructure

Resolve conflicts explicitly. Follow the repository's established Tailwind,
CSS Modules, scoped CSS, CSS-in-JS, or stylesheet architecture before proposing
a new system.

## Design coherently

- Reuse semantic tokens for color, typography, spacing, radii, shadows,
  breakpoints, motion, and elevation.
- Prefer intent-based names over page-specific literals.
- Preserve component states: default, hover, focus, active, disabled, loading,
  error, and selected.
- Keep structure, behavior, and presentation responsibilities understandable.
- Avoid global overrides that silently alter unrelated screens.
- Treat file length as a review signal, not an automatic split rule.
- Document a new token or component contract only when future consumers need it.

Read `references/accessibility-and-responsive.md` for material component and
layout changes.

## Accessibility and resilience

Treat applicable accessibility as correctness:

- semantic structure and landmarks
- keyboard access and visible focus
- labels, descriptions, and error association
- contrast and non-color indicators
- reduced-motion behavior
- zoom, reflow, and text expansion
- touch target and responsive interaction behavior

Default to WCAG AA for a public product when no stricter project policy exists,
but do not claim compliance from automated checks alone.

## Validate

Use the approved build and test path. Select relevant stylesheet, type,
accessibility, responsive, browser, and visual-regression checks. Inspect both
narrow and wide layouts and representative interaction states.

Report the authority followed, tokens and components affected, accessibility
decisions, checks, visual surfaces not inspected, and any migration risk.
