from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
GENERATED = Path.home() / ".codex" / "generated_images" / "019e24b1-a145-7041-8e28-6e52eaca78d9"
SITE_PUBLIC = ROOT / "publish_staging" / "medioevo-duat-public-release" / "public"

FONT_SANS = Path("C:/Windows/Fonts/bahnschrift.ttf")
FONT_SANS_BOLD = Path("C:/Windows/Fonts/arialbd.ttf")
FONT_SERIF_BOLD = Path("C:/Windows/Fonts/georgiab.ttf")
FONT_SERIF = Path("C:/Windows/Fonts/georgia.ttf")


@dataclass(frozen=True)
class ProductAsset:
    slug: str
    title: str
    subtitle: str
    kicker: str
    footer: str
    source_file: str
    product_dir: Path
    text_mode: str
    title_font: Path
    subtitle_font: Path
    centering_cover: tuple[float, float]
    centering_square: tuple[float, float]
    centering_social: tuple[float, float]
    accent: tuple[int, int, int]


PRODUCTS = [
    ProductAsset(
        slug="medioevo-despertar-preview",
        title="MEDIOEVO",
        subtitle="DESPERTAR",
        kicker="PUBLIC PREVIEW",
        footer="L.R. Gonzalez",
        source_file="ig_07e4d1f3a2cdd56a016a057f766ce081919e09396792e714e7.png",
        product_dir=ROOT / "PRODUCTOS_MEDIOEVO" / "01_LIBROS_Y_BUNDLES" / "despertar-preview-gumroad_20260513_232758",
        text_mode="light",
        title_font=FONT_SERIF_BOLD,
        subtitle_font=FONT_SERIF_BOLD,
        centering_cover=(0.5, 0.5),
        centering_square=(0.5, 0.62),
        centering_social=(0.58, 0.58),
        accent=(234, 185, 92),
    ),
    ProductAsset(
        slug="duat-templates",
        title="DUAT",
        subtitle="TEMPLATES",
        kicker="SYNTHETIC LAB PACK",
        footer="MEDIOEVO Tools",
        source_file="ig_07e4d1f3a2cdd56a016a057fce4c5c8191bb6d3b7267baa9cf.png",
        product_dir=ROOT / "packages" / "paid" / "duat-templates",
        text_mode="dark",
        title_font=FONT_SANS_BOLD,
        subtitle_font=FONT_SANS_BOLD,
        centering_cover=(0.5, 0.58),
        centering_square=(0.5, 0.62),
        centering_social=(0.5, 0.62),
        accent=(42, 101, 126),
    ),
    ProductAsset(
        slug="medioevo-agent-ops-pack",
        title="AGENT OPS",
        subtitle="PACK",
        kicker="ACTIONGATE / HANDOFF / RELEASE",
        footer="MEDIOEVO Tools",
        source_file="ig_07e4d1f3a2cdd56a016a058029096c819187ade4309bdd0a24.png",
        product_dir=ROOT / "packages" / "paid" / "medioevo-agent-ops-pack",
        text_mode="light",
        title_font=FONT_SANS_BOLD,
        subtitle_font=FONT_SANS_BOLD,
        centering_cover=(0.5, 0.56),
        centering_square=(0.5, 0.62),
        centering_social=(0.55, 0.56),
        accent=(87, 222, 205),
    ),
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fit_source(path: Path, size: tuple[int, int], centering: tuple[float, float]) -> Image.Image:
    with Image.open(path) as source:
        return ImageOpsFit(source.convert("RGB"), size, centering)


def ImageOpsFit(image: Image.Image, size: tuple[int, int], centering: tuple[float, float]) -> Image.Image:
    src_w, src_h = image.size
    dst_w, dst_h = size
    scale = max(dst_w / src_w, dst_h / src_h)
    next_size = (int(src_w * scale + 0.5), int(src_h * scale + 0.5))
    resized = image.resize(next_size, Image.Resampling.LANCZOS)
    max_x = max(0, resized.width - dst_w)
    max_y = max(0, resized.height - dst_h)
    left = int(max_x * centering[0])
    top = int(max_y * centering[1])
    return resized.crop((left, top, left + dst_w, top + dst_h))


def gradient(size: tuple[int, int], top: tuple[int, int, int, int], bottom: tuple[int, int, int, int]) -> Image.Image:
    width, height = size
    overlay = Image.new("RGBA", size)
    draw = ImageDraw.Draw(overlay)
    for y in range(height):
        ratio = y / max(1, height - 1)
        color = tuple(int(top[i] * (1 - ratio) + bottom[i] * ratio) for i in range(4))
        draw.line([(0, y), (width, y)], fill=color)
    return overlay


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size)


def fit_font(text: str, path: Path, max_width: int, size: int, minimum: int = 36) -> ImageFont.FreeTypeFont:
    probe = Image.new("RGB", (10, 10))
    draw = ImageDraw.Draw(probe)
    current = size
    while current >= minimum:
        fnt = font(path, current)
        bbox = draw.textbbox((0, 0), text, font=fnt)
        if bbox[2] - bbox[0] <= max_width:
            return fnt
        current -= 4
    return font(path, minimum)


def draw_centered(draw: ImageDraw.ImageDraw, text: str, y: int, fnt: ImageFont.FreeTypeFont, fill: tuple[int, int, int], width: int, stroke: int = 0) -> int:
    bbox = draw.textbbox((0, 0), text, font=fnt, stroke_width=stroke)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (width - text_width) // 2
    draw.text((x, y), text, font=fnt, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
    return y + text_height


def draw_left(draw: ImageDraw.ImageDraw, text: str, xy: tuple[int, int], fnt: ImageFont.FreeTypeFont, fill: tuple[int, int, int], stroke: int = 0) -> int:
    draw.text(xy, text, font=fnt, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
    bbox = draw.textbbox(xy, text, font=fnt, stroke_width=stroke)
    return bbox[3]


def palette(product: ProductAsset) -> dict[str, tuple[int, int, int]]:
    if product.text_mode == "dark":
        return {
            "main": (18, 31, 39),
            "sub": (39, 76, 92),
            "muted": (62, 82, 91),
            "rule": product.accent,
        }
    return {
        "main": (247, 249, 242),
        "sub": (255, 219, 142),
        "muted": (208, 229, 229),
        "rule": product.accent,
    }


def apply_cover_treatment(image: Image.Image, product: ProductAsset) -> Image.Image:
    base = image.convert("RGBA")
    if product.text_mode == "dark":
        base = Image.alpha_composite(base, gradient(base.size, (255, 255, 255, 208), (255, 255, 255, 0)))
        base = Image.alpha_composite(base, gradient(base.size, (255, 255, 255, 0), (255, 255, 255, 70)))
    else:
        base = Image.alpha_composite(base, gradient(base.size, (0, 0, 0, 190), (0, 0, 0, 0)))
        base = Image.alpha_composite(base, gradient(base.size, (0, 0, 0, 0), (0, 0, 0, 150)))
    return base


def render_cover(product: ProductAsset, source: Path, output: Path) -> None:
    image = apply_cover_treatment(fit_source(source, (1600, 2400), product.centering_cover), product)
    draw = ImageDraw.Draw(image)
    colors = palette(product)
    stroke = 2 if product.text_mode == "light" else 0
    draw.rectangle((132, 148, 1468, 154), fill=colors["rule"])
    kicker_font = fit_font(product.kicker, FONT_SANS_BOLD, 1320, 58, 34)
    title_font = fit_font(product.title, product.title_font, 1320, 172, 72)
    subtitle_font = fit_font(product.subtitle, product.subtitle_font, 1320, 230, 86)
    y = 188
    y = draw_centered(draw, product.kicker, y, kicker_font, colors["muted"], 1600, stroke=stroke) + 40
    y = draw_centered(draw, product.title, y, title_font, colors["main"], 1600, stroke=stroke) + 18
    draw_centered(draw, product.subtitle, y, subtitle_font, colors["sub"], 1600, stroke=stroke)
    footer_font = fit_font(product.footer, FONT_SANS, 1280, 56, 30)
    draw_centered(draw, product.footer, 2256, footer_font, colors["muted"], 1600, stroke=stroke)
    output.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(output, "PNG", optimize=True)


def render_square(product: ProductAsset, source: Path, output: Path) -> None:
    image = apply_cover_treatment(fit_source(source, (1600, 1600), product.centering_square), product)
    draw = ImageDraw.Draw(image)
    colors = palette(product)
    stroke = 2 if product.text_mode == "light" else 0
    draw.rectangle((110, 108, 1490, 114), fill=colors["rule"])
    kicker_font = fit_font(product.kicker, FONT_SANS_BOLD, 1320, 54, 30)
    title_font = fit_font(product.title, product.title_font, 1180, 128, 54)
    subtitle_font = fit_font(product.subtitle, product.subtitle_font, 1180, 150, 58)
    y = 144
    y = draw_centered(draw, product.kicker, y, kicker_font, colors["muted"], 1600, stroke=stroke) + 34
    y = draw_centered(draw, product.title, y, title_font, colors["main"], 1600, stroke=stroke) + 10
    draw_centered(draw, product.subtitle, y, subtitle_font, colors["sub"], 1600, stroke=stroke)
    output.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(output, "PNG", optimize=True)


def render_social(product: ProductAsset, source: Path, output: Path) -> None:
    image = fit_source(source, (1200, 630), product.centering_social).convert("RGBA")
    if product.text_mode == "dark":
        overlay = Image.new("RGBA", image.size, (255, 255, 255, 150))
        image = Image.alpha_composite(image, overlay)
        image = Image.alpha_composite(image, gradient(image.size, (255, 255, 255, 88), (255, 255, 255, 0)))
    else:
        image = Image.alpha_composite(image, gradient(image.size, (0, 0, 0, 210), (0, 0, 0, 60)))
    draw = ImageDraw.Draw(image)
    colors = palette(product)
    stroke = 2 if product.text_mode == "light" else 0
    x = 64
    y = 66
    draw.rectangle((x, y, x + 540, y + 6), fill=colors["rule"])
    kicker_font = fit_font(product.kicker, FONT_SANS_BOLD, 560, 31, 20)
    title_font = fit_font(product.title, product.title_font, 620, 88, 42)
    subtitle_font = fit_font(product.subtitle, product.subtitle_font, 620, 104, 46)
    y += 36
    y = draw_left(draw, product.kicker, (x, y), kicker_font, colors["muted"], stroke=stroke) + 22
    y = draw_left(draw, product.title, (x, y), title_font, colors["main"], stroke=stroke) + 4
    draw_left(draw, product.subtitle, (x, y), subtitle_font, colors["sub"], stroke=stroke)
    footer_font = fit_font(product.footer, FONT_SANS, 560, 30, 18)
    draw_left(draw, product.footer, (x, 548), footer_font, colors["muted"], stroke=stroke)
    output.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(output, "PNG", optimize=True)


def copy_background(source: Path, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source) as image:
        image.convert("RGB").save(output, "PNG", optimize=True)


def main() -> int:
    manifest: dict[str, object] = {
        "schema": "medioevo.public_product_assets.v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_dir": str(GENERATED),
        "products": [],
    }

    for product in PRODUCTS:
        source = GENERATED / product.source_file
        if not source.exists():
            raise FileNotFoundError(source)

        product_cover_dir = product.product_dir / "assets" / "cover"
        site_cover_dir = SITE_PUBLIC / "product-assets" / "covers"
        site_social_dir = SITE_PUBLIC / "product-assets" / "social"

        files = {
            "background": product_cover_dir / f"{product.slug}-background-generated-v1.png",
            "cover": product_cover_dir / f"{product.slug}-cover-v1.png",
            "square": product_cover_dir / f"{product.slug}-square-v1.png",
            "social": product_cover_dir / f"{product.slug}-social-v1.png",
            "site_cover": site_cover_dir / f"{product.slug}-cover-v1.png",
            "site_square": site_cover_dir / f"{product.slug}-square-v1.png",
            "site_social": site_social_dir / f"{product.slug}-social-v1.png",
        }

        copy_background(source, files["background"])
        render_cover(product, source, files["cover"])
        render_square(product, source, files["square"])
        render_social(product, source, files["social"])
        render_cover(product, source, files["site_cover"])
        render_square(product, source, files["site_square"])
        render_social(product, source, files["site_social"])

        product_record = {
            "slug": product.slug,
            "source_sha256": sha256(source),
            "outputs": [
                {
                    "kind": key,
                    "path": str(path.relative_to(ROOT)),
                    "sha256": sha256(path),
                    "bytes": path.stat().st_size,
                }
                for key, path in files.items()
            ],
        }
        manifest["products"].append(product_record)

    manifest_path = ROOT / "qa_artifacts" / "release_validation" / "public_product_assets_2026-05-14.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "manifest": str(manifest_path), "products": len(PRODUCTS)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
