import os
import tkinter as tk
from tkinter import filedialog, messagebox


def choose_files():
    paths = filedialog.askopenfilenames(title="Select files")
    return list(paths)


def choose_folder():
    folder = filedialog.askdirectory(title="Select folder")
    if not folder:
        return []
    files = []
    for root, _, filenames in os.walk(folder):
        for f in filenames:
            files.append(os.path.join(root, f))
    return files


def choose_markdown():
    return filedialog.asksaveasfilename(
        title="Select Markdown file",
        defaultextension=".md",
        filetypes=[("Markdown files", "*.md"), ("All files", "*.*")]
    )


def make_relative_links(files, md_path):
    md_dir = os.path.dirname(md_path)
    lines = []

    for i, file_path in enumerate(files, start=1):
        rel = os.path.relpath(file_path, md_dir).replace("\\", "/")
        name = os.path.splitext(os.path.basename(file_path))[0]
        lines.append(f'[{i}]: {rel} "{name}"')

    return "\n".join(lines) + "\n"


def append_links(files, md_path):
    text = make_relative_links(files, md_path)

    with open(md_path, "a", encoding="utf-8") as f:
        f.write("\n" + text)

    messagebox.showinfo("Done", f"Inserted {len(files)} link(s).")


def run(mode):
    if mode == "files":
        files = choose_files()
    else:
        files = choose_folder()

    if not files:
        return

    md = choose_markdown()
    if not md:
        return

    append_links(files, md)


def main():
    root = tk.Tk()
    root.title("Markdown Link Inserter")
    root.geometry("300x150")
    root.resizable(False, False)

    tk.Label(root, text="Select input type:", font=("Arial", 12)).pack(pady=10)

    tk.Button(root, text="Choose Files", width=20, command=lambda: run("files")).pack(pady=5)
    tk.Button(root, text="Choose Folder", width=20, command=lambda: run("folder")).pack(pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()