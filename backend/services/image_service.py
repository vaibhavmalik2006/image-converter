import io
from pathlib import Path
from typing import Optional
from PIL import Image, ImageOps

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp", ".tiff", ".ico"}


def validate_image(file_name: str) -> bool:
    return Path(file_name).suffix.lower() in SUPPORTED_EXTENSIONS


def get_image_format(file_path: Path) -> str:
    with Image.open(file_path) as img:
        return img.format or "UNKNOWN"


def load_image(file_path: Path) -> Image.Image:
    with Image.open(file_path) as img:
        if img.mode in {"RGBA", "LA", "P"}:
            img = img.convert("RGBA")
        else:
            img = img.convert("RGB")
        return img.copy()


def process_image(
    input_path: Path,
    output_format: str,
    width: Optional[int] = None,
    height: Optional[int] = None,
    keep_aspect_ratio: bool = True,
    dpi: Optional[int] = None,
    quality: int = 90,
    target_size_kb: Optional[float] = None,
) -> tuple[bytes, str, int, int, str]:
    image = load_image(input_path)
    original_width, original_height = image.size

    if width and height:
        new_size = (width, height)
    elif width:
        if keep_aspect_ratio:
            ratio = width / original_width
            new_size = (width, max(1, int(original_height * ratio)))
        else:
            new_size = (width, original_height)
    elif height:
        if keep_aspect_ratio:
            ratio = height / original_height
            new_size = (max(1, int(original_width * ratio)), height)
        else:
            new_size = (original_width, height)
    else:
        new_size = (original_width, original_height)

    image = image.resize(new_size, Image.Resampling.LANCZOS)
    if dpi:
        image.info["dpi"] = (dpi, dpi)

    output_format = output_format.upper()
    if output_format == "JPG":
        output_format = "JPEG"

    buffer = io.BytesIO()
    save_kwargs = {"format": output_format}
    if output_format == "JPEG":
        image = image.convert("RGB")
        save_kwargs["optimize"] = True
        save_kwargs["quality"] = quality
    elif output_format == "PNG":
        save_kwargs["optimize"] = True
        save_kwargs["compress_level"] = 9
    elif output_format == "WEBP":
        save_kwargs["lossless"] = False
        save_kwargs["optimize"] = True
        save_kwargs["quality"] = quality
    elif output_format == "GIF":
        image = ImageOps.exif_transpose(image)
    elif output_format == "ICO":
        save_kwargs["bitmap_format"] = "bmp"

    if dpi:
        save_kwargs["dpi"] = (dpi, dpi)

    if target_size_kb and output_format in {"JPEG", "WEBP"}:
        quality = adjust_quality_for_target_size(image, output_format, quality, target_size_kb)
        save_kwargs["quality"] = quality

    image.save(buffer, **save_kwargs)
    buffer.seek(0)
    data = buffer.getvalue()
    final_size_kb = len(data) / 1024
    return data, output_format, image.width, image.height, f"{final_size_kb:.2f}KB"


def adjust_quality_for_target_size(image, output_format, quality, target_size_kb):
    if output_format not in {"JPEG", "WEBP"}:
        return quality

    low = 1
    high = quality
    best_quality = max(1, quality)
    best_size_diff = float('inf')

    while low <= high:
        mid = (low + high) // 2
        buffer = io.BytesIO()
        save_args = {"format": output_format, "quality": mid}
        if output_format == "WEBP":
            save_args["lossless"] = False
            save_args["optimize"] = True
        image.save(buffer, **save_args)
        size_kb = len(buffer.getvalue()) / 1024
        diff = size_kb - target_size_kb

        if abs(diff) < abs(best_size_diff) and size_kb <= target_size_kb * 1.15:
            best_quality = mid
            best_size_diff = diff

        if size_kb > target_size_kb:
            high = mid - 1
        else:
            low = mid + 1

    return max(1, min(best_quality, quality))
