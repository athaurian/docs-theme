# docs-theme

Shared theme and tooling for my documentation sites.

## Screenshots

Screenshots switch between light and dark with the rest of the page, including
when they open in the lightbox. A single screenshot sits in a
`figure.screenshot`, while a pair sits in an `.image-pair`.

If an image has a light and a dark version, its path ends with `#only-light` or
`#only-dark`. The theme shows the matching version. The site config enables
`auto_themed` so each mode keeps its own lightbox gallery:

```toml
[project.markdown_extensions]
zensical.extensions.glightbox.auto_themed = true
```

## Theme switch

Switching between light and dark uses a diagonal wipe from the top-right corner
to the bottom-left. If the browser does not support it, or reduced motion is
enabled, the colors change immediately.
