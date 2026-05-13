"""
Sync the standalone RoPE article into this repo's `_blogs/rope/index.md`.

Run from the CoenvdE.github.io repository root:
  uv run python import_rope_blog.py

Then commit `_blogs/rope/index.md` and push; CI runs `build_blogs.py` on deploy.
"""
import os
import subprocess

REPO_URL = "https://github.com/CoenvdE/RoPE_blogpost.git"
CLONE_DIR = "RoPE_blogpost"
ARTICLE_FILE = "RoPE.md"
DESTINATION = os.path.join("_blogs", "rope", "index.md")

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


if __name__ == "__main__":
    main()
