<div align="center">
<img src="monogram.svg" alt="docs-theme monogram" width="128">

# docs-theme

</div>

Hi. This is the shared code and config for my documentation sites.

## Syncing and verification

Consumer repositories vendor these assets rather than pulling them at build time. From this repository:

```bash
make sync      # copy theme overrides and assets into sibling repositories
make check     # verify templates, styles, and scripts
make favicons  # regenerate favicon assets via tools/monogram.py
```

## Screenshots and themed images

Wrap screenshots in `<figure class="screenshot">` (or `<div class="image-pair">` for side-by-side comparisons).

- **Border radius:** Screenshots get rounded corners and a subtle border by default. Add the `no-radius` class when capturing full-bleed unrounded surfaces such as status bars.
- **Light and dark variants:** Append `#only-light` or `#only-dark` to image URLs to swap screenshots with the active theme, or set `auto_themed = true` in the site configuration when light/dark pairs follow the standard naming convention.

## Typography and UI workarounds

- **Fonts:** Uses **Geist** for UI, **Merriweather** for headings and body prose, and **Geist Mono** for code blocks.
- **Search modal (`javascripts/search-fix.js`):** Zensical `0.1.0` renders its search UI inside an open Shadow DOM root that inherits negative heading letter-spacing inconsistently. `search-fix.js` attaches to the shadow root to normalize input and result spacing.
- **Theme switch transitions:** Temporarily suppresses CSS transitions during light/dark mode toggles so components repaint together instead of fading at different speeds.

## OpenGraph cards and `tools/monogram.py`

`tools/monogram.py` renders repository monograms, favicons, and OpenGraph social cards (`og_image` / `oembed`), caching rendered fonts and intermediate assets under `~/.cache/monogram-fonts/`.

When updating an OpenGraph card, increment the query string on `og_image` so crawlers invalidate cached previews.

## License

MIT
