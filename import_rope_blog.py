"""
Sync the standalone RoPE article from `RoPE_blogpost` into this site.

Run from the CoenvdE.github.io repository root:
  uv run python import_rope_blog.py

What it does:
  - Clones/pulls https://github.com/CoenvdE/RoPE_blogpost.git into ./RoPE_blogpost/
  - Writes _blogs/rope/index.md (YAML frontmatter + RoPE.md body)
  - Copies optional asset folders from the blog repo into ./images/rope/:
      RoPE_blogpost/images/   -> images/rope/
      RoPE_blogpost/figures/ -> images/rope/figures/
      RoPE_blogpost/assets/  -> images/rope/assets/

When the post is ready to go live:
  1. Run this script, then `uv run python build_blogs.py`
  2. Commit _blogs/rope/index.md, images/rope/, blogs/rope/*.html, and re-add the
     RoPE card to index.html (card was removed while the post is a draft).

In RoPE.md use site-root paths so the HTML build resolves them, e.g.:
  ![diagram](/images/rope/diagram.png)
  ![plot](/images/rope/figures/loss.png)

Then commit `_blogs/rope/index.md` and push; CI runs `build_blogs.py` on deploy.
"""
import os
import shutil
import subprocess

REPO_URL = "https://github.com/CoenvdE/RoPE_blogpost.git"
CLONE_DIR = "RoPE_blogpost"
ARTICLE_FILE = "RoPE.md"
DESTINATION = os.path.join("_blogs", "rope", "index.md")
SITE_IMAGES_ROPE = os.path.join("images", "rope")

# (folder inside RoPE_blogpost/, subpath under images/rope/)
ASSET_FOLDER_MAP = (
    ("images", ""),
    ("figures", "figures"),
    ("assets", "assets"),
)

FRONTMATTER = """---
layout: blog_collection
title: "Rotary positional embeddings (RoPE)"
description: "Intuition and sketch of rotary positional embeddings (RoPE) for transformers, with references."
date: 2026-05-13
collection_id: rope
chapter_number: 1
toc: true
categories: [ML, Transformers]
giscus_comments: true
---
"""


def strip_optional_frontmatter(body: str) -> str:
    body = body.lstrip("\ufeff")
    if body.startswith("---"):
        parts = body.split("---", 2)
        if len(parts) >= 3:
            return parts[2].lstrip("\n")
    return body


def sync_asset_folders():
    """Copy images/figures/assets from the blog repo into images/rope/ for the static site."""
    os.makedirs(SITE_IMAGES_ROPE, exist_ok=True)
    for src_folder, dest_sub in ASSET_FOLDER_MAP:
        src = os.path.join(CLONE_DIR, src_folder)
        if not os.path.isdir(src):
            continue
        dst = (
            os.path.join(SITE_IMAGES_ROPE, dest_sub)
            if dest_sub
            else SITE_IMAGES_ROPE
        )
        shutil.copytree(src, dst, dirs_exist_ok=True)
        print(f"Synced {src!r} -> {dst!r}")


def main():
    if os.path.isdir(CLONE_DIR):
        subprocess.run(["git", "-C", CLONE_DIR, "pull", "--ff-only"], check=True)
    else:
        subprocess.run(["git", "clone", REPO_URL], check=True)

    src = os.path.join(CLONE_DIR, ARTICLE_FILE)
    if not os.path.isfile(src):
        raise FileNotFoundError(
            f"Missing {src!r}. Add {ARTICLE_FILE!r} to {REPO_URL} (commit + push), "
            f"then remove the {CLONE_DIR!r} folder here if it was an old clone and run again."
        )

    with open(src, "r", encoding="utf-8") as f:
        article_body = strip_optional_frontmatter(f.read())

    os.makedirs(os.path.dirname(DESTINATION), exist_ok=True)
    with open(DESTINATION, "w", encoding="utf-8") as f:
        f.write(FRONTMATTER)
        if article_body and not article_body.endswith("\n"):
            f.write("\n")
        f.write(article_body)
        if article_body and not article_body.endswith("\n"):
            f.write("\n")

    print(f"Wrote {DESTINATION}")

    sync_asset_folders()


if __name__ == "__main__":
    main()
