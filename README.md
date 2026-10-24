# docs-theme

This is the theme and tooling I use for my documentation sites.

## Screenshots

Screenshots follow the page's light or dark mode, including in the lightbox. A
single screenshot sits in a `figure.screenshot`, and a pair sits in an
`.image-pair`.

Screenshot corners are rounded by default. Add `no-radius` to the figure or
pair when the image has rounded corners of its own, such as a tight window crop
or a card with transparent corners.

If an image has a light and a dark version, end its path with `#only-light` or
`#only-dark`. The theme shows the matching version. The site config turns on
`auto_themed` so each mode keeps its own lightbox gallery:

```toml
[project.markdown_extensions]
zensical.extensions.glightbox.auto_themed = true
```

## Social banner

Set `og_image` under `[project.extra]` to a 1200x630 image path relative to the
site URL. Without it, link previews are text only.

## oEmbed

Set `oembed` under `[project.extra]` to a JSON file path relative to the site
URL. Discord reads `provider_name` and `provider_url` from the file to link the
site name in a preview.

## Favicons

Each site keeps its monogram at `docs/favicon.svg`. Run `make favicons` from
this checkout to regenerate the ICO and PNG icons for every site. The target
needs `rsvg-convert` and ImageMagick.

## Theme switch

The theme switch uses a diagonal wipe from the top-right corner to the
bottom-left. If the browser does not support it, or reduced motion is on, the
colors change immediately. Scrolling pauses during the wipe and the sticky
header stays put.
