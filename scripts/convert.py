#!/usr/bin/env python3

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Recursively convert .jpg/.jpeg files to .webp using cwebp."
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Directory to search (default: current directory)",
    )
    parser.add_argument(
        "-d",
        "--delete",
        action="store_true",
        help="Delete the original JPG after a successful conversion",
    )
    args = parser.parse_args()

    if shutil.which("cwebp") is None:
        sys.exit("Error: cwebp not found. Install the webp package first.")

    root = Path(args.directory)
    jpg_files = [
        p for p in root.rglob("*")
        if p.is_file() and p.suffix.lower() in (".jpg", ".jpeg")
    ]

    if not jpg_files:
        print(f"No .jpg files found in {root} (searched recursively).")
        return

    for file in jpg_files:
        output = file.with_suffix(".webp")
        result = subprocess.run(["cwebp", str(file), "-o", str(output)])

        if result.returncode == 0 and output.exists():
            print(f"Converted: {file} -> {output}")
            if args.delete:
                file.unlink()
                print(f"Deleted: {file}")
        else:
            print(f"Failed: {file}")


if __name__ == "__main__":
    main()