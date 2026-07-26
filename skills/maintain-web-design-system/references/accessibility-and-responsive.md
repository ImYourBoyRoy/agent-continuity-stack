# Accessibility and responsive review

## Structure and interaction

- Use semantic elements before adding ARIA.
- Keep headings and landmarks meaningful.
- Ensure every interactive control has an accessible name.
- Preserve logical focus order and visible focus.
- Make all required actions keyboard-operable.
- Associate errors and help text with their controls.

## Responsive behavior

- Test text expansion, zoom, narrow widths, landscape, and wide layouts.
- Avoid horizontal scrolling except for intentionally two-dimensional content.
- Preserve readable line lengths and content order.
- Ensure fixed and sticky elements do not obscure focused content.
- Confirm pointer targets and gestures have accessible alternatives.

## Motion and media

- Respect reduced-motion preferences.
- Avoid essential information conveyed only by animation.
- Provide captions, transcripts, or descriptions where the product requires
  them.

Automated tools catch only a subset. Combine them with keyboard, screen-size,
and representative manual inspection.

