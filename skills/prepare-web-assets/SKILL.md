---
name: prepare-web-assets
description: Prepare and integrate production web images, icons, logos, favicons, and social assets with correct formats, derivatives, accessibility, provenance, and performance. Generate artwork only when explicitly requested.
---

# Prepare Web Assets

Produce traceable, appropriately licensed, accessible assets without replacing
official source material.

When Portable Web Toolkit manages the project, use its `brand-doctor` and
`image-pipeline` where applicable. Do not create a competing asset manifest,
derivative pipeline, or brand-validation command.

## Establish source authority

1. Locate official masters, brand guidance, licenses, attribution requirements,
   and existing asset manifests.
2. Preserve originals separately from generated derivatives.
3. Do not redraw trademarks, alter supplied official logos, or replace approved
   assets without authorization.
4. Record provenance for externally sourced material.
5. If source quality is insufficient, report the limitation before inventing a
   replacement.

## Select formats

- Use SVG for suitable logos, icons, diagrams, and scalable illustrations.
- Sanitize externally sourced SVG and remove scripts or unsafe references.
- Use AVIF or WebP for photographic assets when project and browser support
  justify it; provide the required fallback.
- Keep PNG where transparency, lossless detail, or platform tooling requires it.
- Avoid recompressing already degraded sources.
- Generate only sizes the interface or metadata actually consumes.

Use `references/asset-matrix.md` for common web destinations.

## Integrate correctly

- Use stable, collision-resistant filenames consistent with project conventions.
- Include width and height or aspect ratio to reduce layout shift.
- Provide `srcset` and `sizes` based on real layout behavior.
- Use meaningful alternative text for informative imagery.
- Use empty alternative text or presentation semantics for decoration.
- Do not put essential text only inside an image.
- Keep social-card, favicon, app-icon, and inline-image concerns distinct.
- Avoid embedding secrets, private metadata, or unintended EXIF location data.

## Generation boundary

Use an image-generation tool only when the user explicitly requests new visual
content or editing. Treat generated output as a candidate requiring human review
for brand, factual, licensing, and accessibility suitability.

## Validate

Check file integrity, dimensions, transparency, color behavior, file weight,
references, responsive selection, browser rendering, alternative text, and
licensing records. Use lossless or reversible operations on masters.

Report source assets, derivatives, transformation commands, quality tradeoffs,
integration changes, checks, and unresolved rights or brand questions.
