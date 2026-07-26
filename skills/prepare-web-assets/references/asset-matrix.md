# Web asset matrix

| Destination | Typical source | Key checks |
|---|---|---|
| Inline logo | SVG master | viewBox, safe markup, contrast |
| UI icon | SVG icon set | stroke consistency, accessible name when needed |
| Hero/photo | high-quality raster | crop, responsive widths, focal point, compression |
| Social card | raster composition | exact platform needs, safe text area, public URL |
| Favicon | vector or square master | small-size legibility, required fallback formats |
| App icon | square master | platform mask and padding, no unintended transparency |
| Background texture | raster or SVG | repetition seams, file weight, contrast |

Choose actual dimensions from layout measurements and platform documentation.
Do not generate a generic matrix of unused sizes.

