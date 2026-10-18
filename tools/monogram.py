#!/usr/bin/env python3
# /// script
# dependencies = ["fonttools>=4.40"]
# ///
"""Turn any letter into a monogram favicon (or square logo tile).

The glyph is converted into a self-contained SVG path, so the output references
no font and renders identically everywhere. Tile size, corner radius, colours,
and how much of the tile the letter's outline fills are all arguments.

Usage:
    uv run tools/monogram.py a -o public/favicon.svg
    uv run tools/monogram.py B --font source-code-pro -o favicon.svg
    uv run tools/monogram.py a --font google-sans --weight 500 -o favicon.svg
    uv run tools/monogram.py x --font-url https://example.com/Font.ttf -o x.svg

Built-in fonts are fetched once from Google's open repository (all OFL, cached
in ~/.cache/monogram-fonts). Any other .ttf/.otf works via --font-url.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
import urllib.parse
import urllib.request
from pathlib import Path

from fontTools.misc.transform import Transform
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

FONTS = {
    "google-sans-code": "https://raw.githubusercontent.com/google/fonts/main/ofl/googlesanscode/GoogleSansCode[wght].ttf",
    "source-code-pro": "https://raw.githubusercontent.com/google/fonts/main/ofl/sourcecodepro/SourceCodePro[wght].ttf",
    "google-sans": "https://raw.githubusercontent.com/google/fonts/main/ofl/googlesans/GoogleSans[GRAD,opsz,wght].ttf",
}

CACHE_DIR = Path.home() / ".cache" / "monogram-fonts"


def fetch_font(url: str, cache_dir: Path) -> Path:
    """Download a font once into the cache and return the local path."""
    cache_dir.mkdir(parents=True, exist_ok=True)
    name = urllib.parse.quote(url.rsplit("/", 1)[-1], safe="")
    path = cache_dir / f"{hashlib.sha1(url.encode()).hexdigest()[:12]}-{name}"
    if not path.exists():
        print(f"fetching {url}", file=sys.stderr)
        request = urllib.request.Request(url, headers={"User-Agent": "monogram.py"})
        with urllib.request.urlopen(request, timeout=60) as response:  # noqa: S310
            path.write_bytes(response.read())
    return path


def load_font(path: Path, weight: float) -> TTFont:
    """Open a font, instantiating its wght axis when it has one."""
    font = TTFont(path)
    axes = {axis.axisTag: axis for axis in font["fvar"].axes} if "fvar" in font else {}
    if "wght" not in axes:
        print(f"note: {path.name} has no wght axis, using it as-is", file=sys.stderr)
        return font
    axis = axes["wght"]
    if not axis.minValue <= weight <= axis.maxValue:
        sys.exit(f"error: weight {weight:g} is outside {axis.minValue:g}-{axis.maxValue:g} for {path.name}")
    return instantiateVariableFont(font, {"wght": weight}, updateFontNames=False)


def glyph_of(font: TTFont, letter: str):
    cmap = font.getBestCmap()
    if ord(letter) not in cmap:
        sys.exit(f"error: no glyph for {letter!r} in this font")
    name = cmap[ord(letter)]
    return font.getGlyphSet(), name


def glyph_bounds(glyph_set, name: str) -> tuple[float, float, float, float]:
    pen = BoundsPen(glyph_set)
    glyph_set[name].draw(pen)
    if pen.bounds is None:
        sys.exit(f"error: glyph {name!r} has no outline (a space, for instance)")
    return pen.bounds


def monogram_path(glyph_set, name: str, size: int, fill: float) -> str:
    """Outline of the glyph, flipped to SVG coordinates and centred on the tile."""
    x0, y0, x1, y1 = glyph_bounds(glyph_set, name)
    width, height = x1 - x0, y1 - y0
    scale = fill * size / max(width, height)
    # Centre the outline itself, not the advance width, so the glyph sits optically.
    sx = (size - width * scale) / 2 - x0 * scale
    sy = (size - height * scale) / 2 + y1 * scale
    pen = SVGPathPen(glyph_set)
    glyph_set[name].draw(TransformPen(pen, Transform(scale, 0, 0, -scale, sx, sy)))
    return pen.getCommands()


def markup(size: int, radius: float, background: str, foreground: str, data: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}">\n'
        f'  <rect width="{size}" height="{size}" rx="{radius}" fill="{background}"/>\n'
        f'  <path d="{data}" fill="{foreground}"/>\n'
        f"</svg>\n"
    )


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0], formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("letter", help="the single letter to draw")
    parser.add_argument("-o", "--output", default="favicon.svg", help="output path, or - for stdout")
    parser.add_argument("--font", choices=sorted(FONTS), default="google-sans-code", help="built-in font (default: google-sans-code)")
    parser.add_argument("--font-url", help="URL of a .ttf/.otf to use instead of a built-in font")
    parser.add_argument("--weight", type=float, default=700, help="wght value for variable fonts (default: 700)")
    parser.add_argument("--fill", type=float, default=0.7, help="fraction of the tile the outline fills (default: 0.7)")
    parser.add_argument("--size", type=int, default=64, help="viewBox size in px (default: 64)")
    parser.add_argument("--radius", type=float, default=8, help="corner radius in px (default: 8)")
    parser.add_argument("--bg", "--background", default="#121212", help="tile colour")
    parser.add_argument("--fg", "--foreground", default="#f5f5f5", help="letter colour")
    parser.add_argument("--cache-dir", type=Path, default=CACHE_DIR, help="where to cache downloaded fonts")
    args = parser.parse_args(argv)

    if len(args.letter) != 1:
        sys.exit("error: give exactly one letter")

    url = args.font_url or FONTS[args.font]
    font_path = fetch_font(url, args.cache_dir)
    font = load_font(font_path, args.weight)
    glyph_set, name = glyph_of(font, args.letter)
    data = monogram_path(glyph_set, name, args.size, args.fill)
    svg = markup(args.size, args.radius, args.bg, args.fg, data)

    if args.output == "-":
        sys.stdout.write(svg)
    else:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(svg)
        print(f"wrote {output} ({len(svg)} bytes, glyph {name!r} of {font_path.name} at wght {args.weight:g})")


if __name__ == "__main__":
    main()
