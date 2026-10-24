# docs-theme

Shared theme and tooling for my documentation sites.

## Screenshots

Screenshots switch between light and dark with the rest of the page, including
when they open in the lightbox. A single screenshot sits in a
`figure.screenshot`, while a pair sits in an `.image-pair`.

Screenshot corners are rounded by default. Add `no-radius` to the figure or
pair when the image already has rounded corners of its own (a tight window
crop, a card with transparent corners), so the rounding cannot clip them.

If an image has a light and a dark version, its path ends with `#only-light` or
`#only-dark`. The theme shows the matching version. The site config enables
`auto_themed` so each mode keeps its own lightbox gallery:

```toml
[project.markdown_extensions]
zensical.extensions.glightbox.auto_themed = true
```

## Favicons

Each site keeps its monogram at `docs/favicon.svg`. Run `make favicons` from the
theme checkout to regenerate `favicon.ico`, `favicon-32x32.png`, and
`apple-touch-icon.png` for every site. The target needs `rsvg-convert` and
ImageMagick.

## Theme switch

Switching between light and dark uses a diagonal wipe from the top-right corner
to the bottom-left. If the browser does not support it, or reduced motion is
enabled, the colors change immediately. Scrolling is paused for the short wipe
so the old and new views stay aligned, and the sticky header is pinned in its
viewport position while the wipe runs.
