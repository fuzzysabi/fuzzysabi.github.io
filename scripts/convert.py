#!/bin/python

#for file in *.jpg; do cwebp "$file" -o "${file%.jpg}.webp"; done

import subprocess
import glob
import os

jpg_files = glob.glob("*.jpg")

if not jpg_files:
    print("No .jpg files found in the current directory.")
else:
    for file in jpg_files:
        output = file.rsplit(".jpg", 1)[0] + ".webp"
        result = subprocess.run(["cwebp", file, "-o", output])
        if result.returncode == 0:
            print(f"Converted: {file} -> {output}")
        else:
            print(f"Failed: {file}")