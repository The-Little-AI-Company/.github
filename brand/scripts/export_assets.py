from __future__ import annotations

import hashlib
import json
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

import vtracer
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[2]
BRAND = ROOT / "brand"
RASTER_SOURCE = BRAND / "source" / "raster"
VECTOR_SOURCE = BRAND / "source"
POSE_SOURCE = VECTOR_SOURCE / "poses"
FONT_SOURCE = VECTOR_SOURCE / "fonts"
DIST = BRAND / "dist"
PROOFS = BRAND / "proofs"
WORKING = BRAND / ".working" / "vector"

PAPER = "#F3EBDD"
SURFACE = "#FFFDF8"
INK = "#2B2118"
RUST = "#B85C38"
TEAL = "#2D7A78"
SIGNAL = "#205F5D"
MUTED = "#6E6456"
CHARCOAL = "#201A15"

POSES = (
    "welcome",
    "checking",
    "writing",
    "memory",
    "coffee",
    "building",
    "filing",
    "relay",
    "teaching",
)
MARK_SIZES = (16, 20, 32, 40, 64, 128, 200, 256, 512, 1024)


def write_text_lf(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def load_master(name: str) -> Image.Image:
    path = RASTER_SOURCE / f"tlac-owl-{name}-master.png"
    image = Image.open(path).convert("RGBA")
    if image.getbbox() is None:
        raise ValueError(f"{path} has no visible pixels")
    if image.getpixel((0, 0))[3] != 0:
        raise ValueError(f"{path} does not have a transparent corner")
    return image


def trimmed_square(image: Image.Image, padding_ratio: float = 0.1) -> Image.Image:
    bbox = image.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError("image has no visible alpha bounds")
    cropped = image.crop(bbox)
    padding = max(16, round(max(cropped.size) * padding_ratio))
    edge = max(cropped.size) + padding * 2
    canvas = Image.new("RGBA", (edge, edge), (0, 0, 0, 0))
    canvas.alpha_composite(
        cropped,
        ((edge - cropped.width) // 2, (edge - cropped.height) // 2),
    )
    return canvas


def resized(image: Image.Image, size: int) -> Image.Image:
    return image.resize((size, size), Image.Resampling.LANCZOS)


def brand_font(
    size: int,
    *,
    family: str = "inter",
    weight: str = "Regular",
) -> ImageFont.FreeTypeFont:
    if family == "fraunces":
        path = FONT_SOURCE / "fraunces" / "Fraunces.ttf"
    else:
        path = FONT_SOURCE / "inter" / "Inter.ttf"
    result = ImageFont.truetype(str(path), size=size)
    try:
        result.set_variation_by_name(weight)
    except OSError:
        pass
    return result


def outlined_text(
    text: str,
    *,
    family: str,
    weight: int,
    size: float,
    x: float,
    baseline: float,
    fill: str,
    anchor: str = "start",
    letter_spacing: float = 0,
) -> str:
    """Return portable SVG paths for text set in the bundled variable fonts."""
    font_path = FONT_SOURCE / family / (
        "Fraunces.ttf" if family == "fraunces" else "Inter.ttf"
    )
    variable_font = TTFont(font_path)
    font = instantiateVariableFont(
        variable_font,
        {"wght": weight},
        inplace=False,
    )
    glyph_set = font.getGlyphSet()
    cmap = font.getBestCmap()
    if cmap is None:
        raise ValueError(f"{font_path} has no Unicode character map")
    metrics = font["hmtx"].metrics
    scale = size / font["head"].unitsPerEm
    glyph_names: list[str] = []
    for character in text:
        glyph_name = cmap.get(ord(character))
        if glyph_name is None:
            raise ValueError(f"{font_path} has no glyph for {character!r}")
        glyph_names.append(glyph_name)

    width = sum(metrics[name][0] * scale for name in glyph_names)
    width += max(0, len(glyph_names) - 1) * letter_spacing
    cursor = x - width / 2 if anchor == "middle" else x
    paths: list[str] = []
    for index, glyph_name in enumerate(glyph_names):
        pen = SVGPathPen(glyph_set)
        glyph_set[glyph_name].draw(pen)
        commands = pen.getCommands()
        if commands:
            paths.append(
                f'    <path d="{commands}" '
                f'transform="translate({cursor:.4f} {baseline:.4f}) '
                f'scale({scale:.8f} {-scale:.8f})" fill="{fill}"/>'
            )
        cursor += metrics[glyph_name][0] * scale
        if index < len(glyph_names) - 1:
            cursor += letter_spacing
    font.close()
    variable_font.close()
    return "\n".join(paths)


def one_color_raster(mark: Image.Image, color: str) -> Image.Image:
    rgb = tuple(int(color[index : index + 2], 16) for index in (1, 3, 5))
    output: list[tuple[int, int, int, int]] = []
    for red, green, blue, alpha in mark.get_flattened_data():
        luminance = 0.2126 * red + 0.7152 * green + 0.0722 * blue
        visible = alpha if alpha >= 24 and luminance < 205 else 0
        output.append((*rgb, visible))
    result = Image.new("RGBA", mark.size)
    result.putdata(output)
    return result


def silhouette_raster(mark: Image.Image, color: str = INK) -> Image.Image:
    rgb = tuple(int(color[index : index + 2], 16) for index in (1, 3, 5))
    mask = mark.getchannel("A").point(lambda alpha: 255 if alpha >= 24 else 0)
    enclosed = ImageOps.invert(mask)
    ImageDraw.floodfill(enclosed, (0, 0), 0)
    filled = ImageChops.lighter(mask, enclosed)
    result = Image.new("RGBA", mark.size, (*rgb, 0))
    result.putalpha(filled)
    return result


def grayscale_raster(mark: Image.Image) -> Image.Image:
    gray = ImageOps.grayscale(mark.convert("RGB"))
    result = Image.merge("RGBA", (gray, gray, gray, mark.getchannel("A")))
    return result


def trace_svg(
    image: Image.Image,
    output: Path,
    *,
    size: int,
    color_mode: str = "color",
    color_precision: int = 6,
    speckle: int = 8,
    matte: str = PAPER,
) -> str:
    traced = resized(image, size)
    WORKING.mkdir(parents=True, exist_ok=True)
    key = tuple(int(matte[index : index + 2], 16) for index in (1, 3, 5))
    trace_input = Image.new("RGB", traced.size, key)
    opaque = traced.getchannel("A").point(lambda alpha: 255 if alpha >= 24 else 0)
    trace_input.paste(traced.convert("RGB"), (0, 0), opaque)
    input_path = (WORKING / f"{output.stem}-{size}.png").resolve()
    raw_output = (WORKING / f"{output.stem}-{size}.raw.svg").resolve()
    trace_input.save(input_path, optimize=True)
    vtracer.convert_image_to_svg_py(
        str(input_path),
        str(raw_output),
    )
    tree = ET.parse(raw_output)
    root = tree.getroot()
    root.attrib.pop("width", None)
    root.attrib.pop("height", None)
    root.set("viewBox", f"0 0 {size} {size}")
    root.set("role", "img")

    first = list(root)[0]
    fill = first.attrib.get("fill", "")
    if len(fill) != 7 or not fill.startswith("#"):
        raise ValueError(f"{raw_output} has no removable matte path")
    traced_key = tuple(int(fill[index : index + 2], 16) for index in (1, 3, 5))
    if max(abs(left - right) for left, right in zip(key, traced_key)) > 20:
        raise ValueError(f"{raw_output} matte color drifted to {fill}")
    root.remove(first)
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    svg = ET.tostring(root, encoding="unicode", xml_declaration=True)
    output.parent.mkdir(parents=True, exist_ok=True)
    write_text_lf(output, svg)
    return svg


def svg_inner(svg: str) -> str:
    start = svg.index(">", svg.index("<svg")) + 1
    return svg[start : svg.rindex("</svg>")].strip()


def save_vector_sources(mark: Image.Image, mascots: dict[str, Image.Image]) -> dict[str, str]:
    VECTOR_SOURCE.mkdir(parents=True, exist_ok=True)
    POSE_SOURCE.mkdir(parents=True, exist_ok=True)

    sources = {
        "full": trace_svg(
            mark,
            VECTOR_SOURCE / "tlac-owl-mark.svg",
            size=512,
            matte=PAPER,
        ),
        "one_color": trace_svg(
            one_color_raster(mark, INK),
            VECTOR_SOURCE / "tlac-owl-mark-one-color.svg",
            size=512,
            color_precision=8,
            speckle=5,
            matte=SURFACE,
        ),
        "reversed": trace_svg(
            one_color_raster(mark, PAPER),
            VECTOR_SOURCE / "tlac-owl-mark-reversed.svg",
            size=512,
            color_precision=8,
            speckle=5,
            matte=CHARCOAL,
        ),
        "grayscale": trace_svg(
            grayscale_raster(mark),
            VECTOR_SOURCE / "tlac-owl-mark-grayscale.svg",
            size=512,
            color_precision=5,
            matte=PAPER,
        ),
        "silhouette": trace_svg(
            silhouette_raster(mark),
            VECTOR_SOURCE / "tlac-owl-mark-silhouette.svg",
            size=512,
            color_precision=8,
            speckle=5,
            matte=SURFACE,
        ),
    }

    for pose, image in mascots.items():
        trace_svg(
            image,
            POSE_SOURCE / f"tlac-owl-{pose}.svg",
            size=512,
            color_precision=5,
            speckle=12,
            matte=PAPER,
        )
    shutil.copyfile(
        POSE_SOURCE / "tlac-owl-coffee.svg",
        VECTOR_SOURCE / "tlac-owl-mascot-neutral.svg",
    )

    mark_inner = svg_inner(sources["full"])
    horizontal_name = outlined_text(
        "The Little AI Company",
        family="fraunces",
        weight=900,
        size=72,
        x=340,
        baseline=190,
        fill=INK,
    )
    compact_name_top = outlined_text(
        "The Little",
        family="fraunces",
        weight=900,
        size=90,
        x=400,
        baseline=535,
        fill=INK,
        anchor="middle",
    )
    compact_name_bottom = outlined_text(
        "AI Company",
        family="fraunces",
        weight=900,
        size=90,
        x=400,
        baseline=645,
        fill=INK,
        anchor="middle",
    )
    horizontal = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 320" role="img" aria-labelledby="title">
  <title id="title">The Little AI Company</title>
  <g transform="translate(20 20) scale(.546875)">{mark_inner}</g>
  <g aria-hidden="true">
{horizontal_name}
  </g>
</svg>
"""
    compact = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 800" role="img" aria-labelledby="title">
  <title id="title">The Little AI Company</title>
  <g transform="translate(220 30) scale(.703125)">{mark_inner}</g>
  <g aria-hidden="true">
{compact_name_top}
{compact_name_bottom}
  </g>
</svg>
"""
    write_text_lf(VECTOR_SOURCE / "tlac-owl-lockup-horizontal.svg", horizontal)
    write_text_lf(VECTOR_SOURCE / "tlac-owl-lockup-compact.svg", compact)

    favicon = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" role="img" aria-labelledby="title">
  <title id="title">The Little AI Company owl</title>
  <circle cx="512" cy="512" r="512" fill="{PAPER}"/>
  <g transform="translate(72 72) scale(1.71875)">{mark_inner}</g>
</svg>
"""
    (DIST / "favicon").mkdir(parents=True, exist_ok=True)
    write_text_lf(DIST / "favicon" / "favicon.svg", favicon)

    variant_target = DIST / "mark" / "svg"
    variant_target.mkdir(parents=True, exist_ok=True)
    for filename in (
        "tlac-owl-mark.svg",
        "tlac-owl-mark-one-color.svg",
        "tlac-owl-mark-reversed.svg",
        "tlac-owl-mark-grayscale.svg",
        "tlac-owl-mark-silhouette.svg",
    ):
        shutil.copyfile(VECTOR_SOURCE / filename, variant_target / filename)
    return sources


def save_profile_hero(mark_svg: str) -> None:
    target = ROOT / "profile" / "assets"
    target.mkdir(parents=True, exist_ok=True)
    mark_inner = svg_inner(mark_svg)
    label = outlined_text(
        "THE LITTLE AI COMPANY",
        family="inter",
        weight=700,
        size=25,
        x=112,
        baseline=176,
        fill=SIGNAL,
        letter_spacing=2,
    )
    headline_top = outlined_text(
        "Practical AI systems",
        family="fraunces",
        weight=900,
        size=64,
        x=108,
        baseline=285,
        fill=INK,
    )
    headline_bottom = outlined_text(
        "for real work.",
        family="fraunces",
        weight=900,
        size=64,
        x=112,
        baseline=370,
        fill=INK,
    )
    subhead = outlined_text(
        "Useful tools, clear guides, and reliable workflows.",
        family="inter",
        weight=400,
        size=27,
        x=112,
        baseline=448,
        fill=MUTED,
    )
    hero = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 640" role="img" aria-labelledby="title desc">
  <title id="title">The Little AI Company</title>
  <desc id="desc">Practical AI systems for real work.</desc>
  <rect width="1280" height="640" rx="34" fill="{PAPER}"/>
  <rect x="54" y="54" width="1172" height="532" rx="32" fill="{SURFACE}"/>
  <rect x="54" y="54" width="18" height="532" fill="{RUST}"/>
  <g aria-hidden="true">
{label}
{headline_top}
{headline_bottom}
{subhead}
  </g>
  <g transform="translate(820 106) scale(.8203125)">{mark_inner}</g>
</svg>
"""
    write_text_lf(target / "little-ai-company-hero.svg", hero)


def save_raster_marks(
    mark: Image.Image,
    one_color: Image.Image,
    reversed: Image.Image,
    grayscale: Image.Image,
    silhouette: Image.Image,
) -> None:
    mark_target = DIST / "mark"
    avatar_target = DIST / "avatar"
    mark_target.mkdir(parents=True, exist_ok=True)
    avatar_target.mkdir(parents=True, exist_ok=True)
    for size in MARK_SIZES:
        resized(mark, size).save(
            mark_target / f"tlac-owl-mark-{size}.png", optimize=True
        )
        background = Image.new("RGBA", (size, size), PAPER)
        inset = max(1, round(size * 0.09))
        icon = resized(mark, size - inset * 2)
        background.alpha_composite(icon, (inset, inset))
        background.convert("RGB").save(
            avatar_target / f"tlac-avatar-{size}.png", optimize=True
        )

    variants = {
        "one-color": one_color,
        "reversed": reversed,
        "grayscale": grayscale,
        "silhouette": silhouette,
    }
    for name, image in variants.items():
        for size in (32, 64, 128, 256, 512, 1024):
            resized(image, size).save(
                mark_target / f"tlac-owl-mark-{name}-{size}.png",
                optimize=True,
            )


def save_favicons(mark: Image.Image) -> None:
    target = DIST / "favicon"
    target.mkdir(parents=True, exist_ok=True)

    def on_paper(size: int) -> Image.Image:
        image = Image.new("RGBA", (size, size), PAPER)
        inset = max(1, round(size * 0.08))
        image.alpha_composite(resized(mark, size - inset * 2), (inset, inset))
        return image

    for size in (16, 32, 48, 180, 192, 512):
        on_paper(size).save(target / f"favicon-{size}.png", optimize=True)
    on_paper(64).save(
        target / "favicon.ico",
        format="ICO",
        sizes=[(16, 16), (32, 32), (48, 48), (64, 64)],
    )


def save_mascots() -> dict[str, Image.Image]:
    target = DIST / "mascot"
    target.mkdir(parents=True, exist_ok=True)
    masters: dict[str, Image.Image] = {}
    for pose in POSES:
        master = trimmed_square(load_master(pose), padding_ratio=0.075)
        masters[pose] = master
        for size in (320, 640, 1024):
            resized(master, size).save(
                target / f"tlac-owl-{pose}-{size}.webp",
                format="WEBP",
                lossless=True,
                method=6,
            )
    return masters


def save_lockup_rasters(mark: Image.Image) -> tuple[Image.Image, Image.Image]:
    target = DIST / "lockups"
    target.mkdir(parents=True, exist_ok=True)

    horizontal = Image.new("RGBA", (1200, 320), (0, 0, 0, 0))
    horizontal.alpha_composite(resized(mark, 280), (20, 20))
    draw = ImageDraw.Draw(horizontal)
    draw.text(
        (340, 96),
        "The Little AI Company",
        font=brand_font(72, family="fraunces", weight="Black"),
        fill=INK,
    )
    horizontal.save(target / "tlac-lockup-horizontal.png", optimize=True)

    compact = Image.new("RGBA", (800, 800), (0, 0, 0, 0))
    compact.alpha_composite(resized(mark, 360), (220, 30))
    draw = ImageDraw.Draw(compact)
    first = "The Little"
    second = "AI Company"
    display = brand_font(88, family="fraunces", weight="Black")
    for text, y in ((first, 470), (second, 575)):
        box = draw.textbbox((0, 0), text, font=display)
        draw.text(((800 - (box[2] - box[0])) / 2, y), text, font=display, fill=INK)
    compact.save(target / "tlac-lockup-compact.png", optimize=True)
    return horizontal, compact


def save_social(mark: Image.Image, mascot: Image.Image) -> None:
    target = DIST / "social"
    target.mkdir(parents=True, exist_ok=True)

    card = Image.new("RGB", (1280, 640), PAPER)
    draw = ImageDraw.Draw(card)
    draw.rounded_rectangle((54, 54, 1226, 586), radius=32, fill=SURFACE)
    draw.rectangle((54, 54, 72, 586), fill=RUST)
    draw.text(
        (112, 138),
        "THE LITTLE AI COMPANY",
        font=brand_font(25, weight="Bold"),
        fill=SIGNAL,
    )
    draw.text(
        (108, 205),
        "Practical AI systems",
        font=brand_font(64, family="fraunces", weight="Black"),
        fill=INK,
    )
    draw.text(
        (112, 286),
        "for real work.",
        font=brand_font(64, family="fraunces", weight="Black"),
        fill=INK,
    )
    draw.text(
        (112, 402),
        "Useful tools, clear guides, and reliable workflows.",
        font=brand_font(27),
        fill=MUTED,
    )
    icon = resized(mark, 380)
    card.paste(icon, (826, 130), icon)
    card.save(target / "tlac-social-card.png", optimize=True)

    square = Image.new("RGB", (1080, 1080), PAPER)
    draw = ImageDraw.Draw(square)
    draw.rounded_rectangle((72, 72, 1008, 1008), radius=42, fill=SURFACE)
    owl = resized(mascot, 540)
    square.paste(owl, (270, 95), owl)
    display = brand_font(72, family="fraunces", weight="Black")
    for text, y in (("The Little", 670), ("AI Company", 752)):
        box = draw.textbbox((0, 0), text, font=display)
        draw.text(((1080 - (box[2] - box[0])) / 2, y), text, font=display, fill=INK)
    draw.text(
        (300, 875),
        "PRACTICAL AI FOR REAL WORK",
        font=brand_font(24, weight="Bold"),
        fill=SIGNAL,
    )
    square.save(target / "tlac-social-square.png", optimize=True)


def save_proofs(
    mark: Image.Image,
    one_color: Image.Image,
    reversed: Image.Image,
    grayscale: Image.Image,
    silhouette: Image.Image,
    mascots: dict[str, Image.Image],
    lockups: tuple[Image.Image, Image.Image],
) -> None:
    PROOFS.mkdir(parents=True, exist_ok=True)
    heading = brand_font(46, family="fraunces", weight="Black")
    label = brand_font(20, weight="Bold")
    body = brand_font(19)

    mark_sheet = Image.new("RGB", (2200, 1500), PAPER)
    draw = ImageDraw.Draw(mark_sheet)
    draw.text((70, 45), "TLAC owl mark proof", font=heading, fill=INK)
    draw.text(
        (72, 110),
        "Theme, variant, tiny-size, and circular-crop checks",
        font=body,
        fill=MUTED,
    )

    theme_samples = (
        ("Warm cream / full color", PAPER, mark),
        ("White / full color", "#FFFFFF", mark),
        ("Charcoal / reversed", CHARCOAL, reversed),
        ("Transparent / full color", None, mark),
    )
    x = 72
    for name, background, image in theme_samples:
        tile = Image.new("RGB", (470, 390), background or "#D9D1C5")
        if background is None:
            tile_draw = ImageDraw.Draw(tile)
            for row in range(0, 390, 40):
                for column in range(0, 470, 40):
                    if (row // 40 + column // 40) % 2:
                        tile_draw.rectangle(
                            (column, row, column + 39, row + 39),
                            fill="#F4EFE7",
                        )
        icon = resized(image, 320)
        tile.paste(icon, (75, 35), icon)
        mark_sheet.paste(tile, (x, 170))
        draw.text((x, 580), name, font=label, fill=INK)
        x += 520

    variants = (
        ("Full color", mark, SURFACE),
        ("One color", one_color, SURFACE),
        ("Reversed", reversed, CHARCOAL),
        ("Grayscale", grayscale, SURFACE),
        ("Silhouette", silhouette, SURFACE),
    )
    x = 72
    for name, image, background in variants:
        tile = Image.new("RGB", (350, 300), background)
        icon = resized(image, 250)
        tile.paste(icon, (50, 25), icon)
        mark_sheet.paste(tile, (x, 680))
        draw.text((x + 95, 995), name, font=label, fill=INK)
        x += 410

    x = 72
    for size in (16, 20, 32, 40, 64, 128, 200):
        tile = Image.new("RGB", (250, 250), SURFACE)
        icon = resized(mark, size)
        tile.paste(icon, ((250 - size) // 2, (250 - size) // 2), icon)
        circle = ImageDraw.Draw(tile)
        circle.ellipse((24, 24, 226, 226), outline="#B9AD9B", width=2)
        mark_sheet.paste(tile, (x, 1110))
        draw.text((x + 95, 1380), f"{size}px", font=label, fill=INK)
        x += 295
    mark_sheet.save(PROOFS / "tlac-mark-proof-sheet.png", optimize=True)

    pose_sheet = Image.new("RGB", (2000, 1460), PAPER)
    draw = ImageDraw.Draw(pose_sheet)
    draw.text((70, 45), "TLAC owl pose proof", font=heading, fill=INK)
    for index, pose in enumerate(POSES):
        column = index % 5
        row = index // 5
        x = 50 + column * 390
        y = 150 + row * 650
        icon = resized(mascots[pose], 350)
        pose_sheet.paste(icon, (x, y), icon)
        box = draw.textbbox((0, 0), pose, font=label)
        draw.text(
            (x + (350 - (box[2] - box[0])) / 2, y + 385),
            pose,
            font=label,
            fill=INK,
        )
    pose_sheet.save(PROOFS / "tlac-mascot-pose-sheet.png", optimize=True)

    lockup_sheet = Image.new("RGB", (1600, 1200), PAPER)
    draw = ImageDraw.Draw(lockup_sheet)
    draw.text((70, 45), "TLAC lockup proof", font=heading, fill=INK)
    horizontal, compact = lockups
    horizontal_preview = horizontal.copy()
    background = Image.new("RGBA", horizontal_preview.size, SURFACE)
    background.alpha_composite(horizontal_preview)
    lockup_sheet.paste(background.convert("RGB").resize((1440, 384)), (80, 150))
    compact_preview = Image.new("RGBA", compact.size, SURFACE)
    compact_preview.alpha_composite(compact)
    lockup_sheet.paste(compact_preview.convert("RGB").resize((560, 560)), (520, 590))
    lockup_sheet.save(PROOFS / "tlac-lockup-proof-sheet.png", optimize=True)

    combined = Image.new("RGB", (2200, 1500), PAPER)
    combined.paste(mark_sheet.resize((1540, 1050)), (0, 25))
    combined.paste(pose_sheet.resize((650, 475)), (1540, 70))
    combined.paste(lockup_sheet.resize((650, 488)), (1540, 600))
    combined.save(PROOFS / "tlac-brand-proof-sheet.png", optimize=True)


def save_manifest() -> None:
    files = []
    for base in (VECTOR_SOURCE, DIST, PROOFS):
        for path in sorted(base.rglob("*")):
            if not path.is_file() or path.name == "MANIFEST.json":
                continue
            data = path.read_bytes()
            files.append(
                {
                    "path": path.relative_to(BRAND).as_posix(),
                    "bytes": len(data),
                    "sha256": hashlib.sha256(data).hexdigest(),
                }
            )
    write_text_lf(
        BRAND / "MANIFEST.json",
        json.dumps(
            {
                "name": "The Little AI Company owl brand kit",
                "exporter": "brand/scripts/export_assets.py",
                "files": files,
            },
            indent=2,
        )
        + "\n",
    )


def verify_outputs() -> None:
    required_svg = (
        VECTOR_SOURCE / "tlac-owl-mark.svg",
        VECTOR_SOURCE / "tlac-owl-mark-one-color.svg",
        VECTOR_SOURCE / "tlac-owl-mark-reversed.svg",
        VECTOR_SOURCE / "tlac-owl-mark-grayscale.svg",
        VECTOR_SOURCE / "tlac-owl-mark-silhouette.svg",
        VECTOR_SOURCE / "tlac-owl-lockup-horizontal.svg",
        VECTOR_SOURCE / "tlac-owl-lockup-compact.svg",
        VECTOR_SOURCE / "tlac-owl-mascot-neutral.svg",
        DIST / "favicon" / "favicon.svg",
    )
    for path in (*required_svg, *sorted(POSE_SOURCE.glob("*.svg"))):
        text = path.read_text(encoding="utf-8")
        if "<image" in text or "data:" in text:
            raise ValueError(f"{path} contains an embedded payload")
        ET.fromstring(text)
    for path in (
        VECTOR_SOURCE / "tlac-owl-lockup-horizontal.svg",
        VECTOR_SOURCE / "tlac-owl-lockup-compact.svg",
    ):
        text = path.read_text(encoding="utf-8")
        if "The Little AI Company" not in text:
            raise ValueError(f"{path} does not contain the exact company name")
        if "<text " in text:
            raise ValueError(f"{path} contains non-portable live text")
    profile_hero = ROOT / "profile" / "assets" / "little-ai-company-hero.svg"
    profile_text = profile_hero.read_text(encoding="utf-8")
    ET.fromstring(profile_text)
    if "<text " in profile_text:
        raise ValueError(f"{profile_hero} contains non-portable live text")


def main() -> None:
    mark = trimmed_square(load_master("mark"), padding_ratio=0.07)
    one_color = one_color_raster(mark, INK)
    reversed_mark = one_color_raster(mark, PAPER)
    grayscale = grayscale_raster(mark)
    silhouette = silhouette_raster(mark)
    mascots = save_mascots()
    vector_sources = save_vector_sources(mark, mascots)
    save_profile_hero(vector_sources["full"])
    save_raster_marks(
        mark,
        one_color,
        reversed_mark,
        grayscale,
        silhouette,
    )
    save_favicons(mark)
    lockups = save_lockup_rasters(mark)
    save_social(mark, mascots["coffee"])
    save_proofs(
        mark,
        one_color,
        reversed_mark,
        grayscale,
        silhouette,
        mascots,
        lockups,
    )
    verify_outputs()
    save_manifest()
    print(f"Exported and verified TLAC brand assets at {BRAND}")


if __name__ == "__main__":
    main()
