"""Sync the claude-workflow and research-template blog posts FROM their GitHub
repos INTO _blogs/. The repos' BLOG.md files are the source of truth: edit
there, run this script here, then build_blogs.py.

Usage:
    uv run python import_claude_blogs.py
    uv run python build_blogs.py
"""

import re
import shutil
import subprocess
import tempfile

BLOGS = [
    {
        "repo": "https://github.com/CoenvdE/claude-code-setup.git",
        "dest": "_blogs/claude-workflow/index.md",
        "frontmatter": {
            "layout": "blog_collection",
            "title": "A Claude Code setup for fast building and research",
            "description": (
                "How I configured Claude Code for both web/app development and ML research: "
                "a small global CLAUDE.md, path-scoped rules for two work modes, on-demand "
                "skills, deterministic hooks, and an anti-drift system that keeps "
                "documentation honest."
            ),
            "collection_id": "claude-workflow",
        },
    },
    {
        "repo": "https://github.com/CoenvdE/research-template.git",
        "dest": "_blogs/research-template/index.md",
        "frontmatter": {
            "layout": "blog_collection",
            "title": "A solid research template",
            "description": (
                "A PyTorch Lightning template for efficient, trustworthy ML research: "
                "guardrail tests (overfit-one-batch, resume equality, data-leakage asserts, "
                "input contracts), timing, FLOPs/MFU and provenance callbacks, wired for "
                "collaboration with Claude Code."
            ),
            "collection_id": "research-template",
        },
    },
]


def import_one(cfg):
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(
            ["git", "clone", "--depth", "1", cfg["repo"], tmp],
            check=True,
            capture_output=True,
        )
        with open(f"{tmp}/BLOG.md") as f:
            text = f.read()

    # Drop the source-of-truth comment header; the site copy carries frontmatter instead.
    text = re.sub(r"^<!--.*?-->\s*", "", text, flags=re.DOTALL)
    # Absolute website URLs back to site-relative form (build_blogs rewrites these).
    text = re.sub(
        r"https://coenvde\.github\.io/blogs/([a-zA-Z0-9_-]+)/index\.html",
        r"/blogs/\1/index/",
        text,
    )

    fm = cfg["frontmatter"]
    front = "---\n"
    front += f'layout: {fm["layout"]}\n'
    front += f'title: "{fm["title"]}"\n'
    front += f'description: "{fm["description"]}"\n'
    front += f'collection_id: {fm["collection_id"]}\n'
    front += "display_chapters: false\n"
    front += "---\n\n"

    with open(cfg["dest"], "w") as f:
        f.write(front + text)
    print(f"synced {cfg['repo']} -> {cfg['dest']}")


if __name__ == "__main__":
    for cfg in BLOGS:
        import_one(cfg)
    print("Now run: uv run python build_blogs.py")
