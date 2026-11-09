#!/usr/bin/env python3
"""
Convert legacy JPG/PNG images to resized WebP and update references to them
in your Jekyll source files (posts, drafts, pages, config, data).

Run from the repo root. Dry run by default; pass --apply to make changes.

    pip install pillow
    python3 convert_images.py                    # preview
    python3 convert_images.py --apply            # convert + rewrite references
    python3 convert_images.py --apply --delete-originals
"""
import argparse
from pathlib import Path
from urllib.parse import quote

from PIL import Image, ImageOps

SRC_EXTS = {".jpg", ".jpeg", ".png"}
TEXT_EXTS = {".md", ".markdown", ".html", ".yml", ".yaml", ".scss", ".css"}
SKIP_DIRS = {"_site", ".git", "vendor", "node_modules", ".jekyll-cache", ".bundle"}


def convert(src: Path, dest: Path, max_px: int, quality: int) -> None:
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im)  # bake in EXIF rotation
        im.thumbnail((max_px, max_px), Image.LANCZOS)  # shrink only, keep aspect
        has_alpha = im.mode in ("RGBA", "LA") or "transparency" in im.info
        im = im.convert("RGBA" if has_alpha else "RGB")
        # No exif= argument, so metadata (including GPS) is dropped.
        im.save(dest, "WEBP", quality=quality, method=6)


def human(n: int) -> str:
    return f"{n / 1_048_576:.1f} MB"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--images", default="pictures", help="image folder, relative to repo root")
    ap.add_argument("--max", type=int, default=1600, help="max long edge in pixels")
    ap.add_argument("--quality", type=int, default=75, help="WebP quality 1-100")
    ap.add_argument("--apply", action="store_true", help="actually write changes")
    ap.add_argument("--delete-originals", action="store_true", help="delete source images after converting")
    args = ap.parse_args()

    root = Path(".").resolve()
    img_dir = (root / args.images).resolve()
    if not img_dir.is_dir():
        raise SystemExit(f"Image folder not found: {img_dir}")

    # 1. Find and convert images -------------------------------------------
    mapping = {}  # "pictures/a/b.jpg" -> "pictures/a/b.webp"
    claimed = set()
    before = after = 0

    for src in sorted(img_dir.rglob("*")):
        if not src.is_file() or src.suffix.lower() not in SRC_EXTS:
            continue
        dest = src.with_suffix(".webp")
        if dest.exists() or dest in claimed:
            print(f"SKIP (target exists): {src.relative_to(root)}")
            continue
        claimed.add(dest)

        size_before = src.stat().st_size
        if args.apply:
            try:
                convert(src, dest, args.max, args.quality)
            except Exception as e:  # unreadable/corrupt file
                print(f"FAIL: {src.relative_to(root)} ({e})")
                claimed.discard(dest)
                continue
            size_after = dest.stat().st_size
            print(f"{src.relative_to(root)}  {human(size_before)} -> {human(size_after)}")
            after += size_after
        else:
            print(f"would convert: {src.relative_to(root)}  ({human(size_before)})")
        before += size_before
        mapping[src.relative_to(root).as_posix()] = dest.relative_to(root).as_posix()

    if not mapping:
        print("Nothing to convert.")
        return

    # Also match URL-encoded paths (spaces as %20, etc.)
    replacements = {}
    for old, new in mapping.items():
        replacements[old] = new
        enc_old, enc_new = quote(old), quote(new)
        if enc_old != old:
            replacements[enc_old] = enc_new

    # 2. Rewrite references in text files -----------------------------------
    changed_files = 0
    total_refs = 0
    for f in sorted(root.rglob("*")):
        if not f.is_file() or f.suffix.lower() not in TEXT_EXTS:
            continue
        if any(part in SKIP_DIRS for part in f.relative_to(root).parts):
            continue
        try:
            text = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        new_text, count = text, 0
        for old, new in replacements.items():
            n = new_text.count(old)
            if n:
                new_text = new_text.replace(old, new)
                count += n
        if count:
            changed_files += 1
            total_refs += count
            print(f"{'updated' if args.apply else 'would update'}: {f.relative_to(root)} ({count} refs)")
            if args.apply:
                f.write_text(new_text, encoding="utf-8")

    # 3. Optionally delete originals ----------------------------------------
    if args.apply and args.delete_originals:
        for old in mapping:
            (root / old).unlink()
        print(f"Deleted {len(mapping)} original images.")

    # Summary ---------------------------------------------------------------
    print()
    if args.apply:
        print(f"Converted {len(mapping)} images: {human(before)} -> {human(after)}")
    else:
        print(f"Dry run: {len(mapping)} images ({human(before)}) would be converted.")
        print("Re-run with --apply to make changes.")
    print(f"{total_refs} references in {changed_files} files.")


if __name__ == "__main__":
    main()