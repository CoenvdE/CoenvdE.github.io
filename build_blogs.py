import glob
import markdown
import os
import re
from bs4 import BeautifulSoup

BLOG_CONFIGS = [
    {
        "out_dir": "blogs/training-at-larger-scale",
        "glob_pattern": "_blogs/training-at-larger-scale/*.md",
        "replacements": [
            ("/images/training-blog/", "../../images/training-blog/"),
        ],
        "url_rewrite": (
            r"\/blogs\/training-at-larger-scale\/([a-zA-Z0-9_-]+)\/",
            r"\1.html",
        ),
    },
    {
        "out_dir": "blogs/rope",
        "glob_pattern": "_blogs/rope/*.md",
        "replacements": [
            ("/images/rope/", "../../images/rope/"),
        ],
        "url_rewrite": (r"\/blogs\/rope\/([a-zA-Z0-9_-]+)\/", r"\1.html"),
    },
    {
        "out_dir": "blogs/claude-workflow",
        "glob_pattern": "_blogs/claude-workflow/*.md",
        "replacements": [
            ("/blogs/research-template/index/", "../research-template/index.html"),
        ],
        "url_rewrite": (r"\/blogs\/claude-workflow\/([a-zA-Z0-9_-]+)\/", r"\1.html"),
    },
    {
        "out_dir": "blogs/research-template",
        "glob_pattern": "_blogs/research-template/*.md",
        "replacements": [
            ("/blogs/claude-workflow/index/", "../claude-workflow/index.html"),
        ],
        "url_rewrite": (r"\/blogs\/research-template\/([a-zA-Z0-9_-]+)\/", r"\1.html"),
    },
]


def get_title(content):
    match = re.search(r'^title:\s*"(.*?)"', content, re.MULTILINE)
    if match:
        return match.group(1)

    match = re.search(r"^#\s+(.*)", content, re.MULTILINE)
    if match:
        return match.group(1)
    return "Chapter"


def get_description(content):
    match = re.search(r'^description:\s*"(.*?)"', content, re.MULTILINE | re.DOTALL)
    return match.group(1).replace("\n", " ").strip() if match else None


def sort_key_path(path):
    name = os.path.basename(path)
    if name == "index.md":
        return (0, 0)
    match = re.search(r"part(\d+)", name)
    return (1, int(match.group(1))) if match else (999, 0)


def apply_content_transforms(content, config):
    for old, new in config["replacements"]:
        content = content.replace(old, new)
    pattern, repl = config["url_rewrite"]
    content = re.sub(pattern, repl, content)
    return content


def build_one_blog(config, head, nav_str, footer):
    out_dir = config["out_dir"]
    os.makedirs(out_dir, exist_ok=True)

    md = markdown.Markdown(extensions=["tables", "pymdownx.superfences", "toc"])

    parts = glob.glob(config["glob_pattern"])
    parts.sort(key=sort_key_path)
    if not parts:
        return

    chapters = []
    for part in parts:
        with open(part, "r") as f:
            content = f.read()
            title = get_title(content)
            basename = os.path.basename(part)
            out_name = basename.replace(".md", ".html")
            chapters.append({"path": part, "out_name": out_name, "title": title})

    for i, chapter in enumerate(chapters):
        with open(chapter["path"], "r") as f:
            content = f.read()
            description = get_description(content)
            if content.startswith("---"):
                parts_split = content.split("---", 2)
                if len(parts_split) > 2:
                    content = parts_split[2]

            content = apply_content_transforms(content, config)

            html_content = md.convert(content)
            md.reset()

            link_class = (
                "not-prose text-sm text-brand-600 dark:text-brand-300 "
                "hover:text-brand-700 dark:hover:text-brand-200 "
                "underline underline-offset-4 decoration-brand-300 "
                "dark:decoration-brand-600 transition-colors max-w-[45%]"
            )
            nav_links = '<div class="not-prose flex justify-between items-start gap-6 mt-16 pt-8 border-t border-paper-300 dark:border-ocean-800">'
            if i > 0:
                prev_ch = chapters[i - 1]
                nav_links += f'<a href="{prev_ch["out_name"]}" class="{link_class}">&larr; {prev_ch["title"]}</a>'
            else:
                nav_links += "<div></div>"

            if i < len(chapters) - 1:
                next_ch = chapters[i + 1]
                nav_links += f'<a href="{next_ch["out_name"]}" class="{link_class} text-right">{next_ch["title"]} &rarr;</a>'
            else:
                nav_links += "<div></div>"
            nav_links += "</div>"

            sidebar = '<div class="md:col-span-1 hidden md:block">\n'
            sidebar += '<div class="sticky top-24">\n'
            sidebar += '<h3 class="eyebrow text-ocean-600 dark:text-ocean-300 mb-4">Chapters</h3>\n'
            sidebar += '<ul class="space-y-2.5">\n'
            for j, ch in enumerate(chapters):
                active_class = (
                    "text-ocean-900 dark:text-paper-100 border-l border-brand-500 pl-3"
                    if i == j
                    else "text-ocean-600 dark:text-ocean-300 hover:text-brand-600 dark:hover:text-brand-300 pl-3 border-l border-paper-300 dark:border-ocean-800 transition-colors"
                )
                sidebar += f'<li><a href="{ch["out_name"]}" class="text-sm block leading-snug {active_class}">{ch["title"]}</a></li>\n'
            sidebar += "</ul>\n</div>\n</div>"

            main_content = f'<div class="md:col-span-3 prose prose-slate dark:prose-invert max-w-none prose-headings:font-serif prose-headings:font-normal prose-headings:tracking-[-0.01em] prose-a:text-brand-600 dark:prose-a:text-brand-300 prose-a:underline-offset-4 prose-img:rounded">\n{html_content}\n{nav_links}\n</div>'

            blog_layout = f'<div class="max-w-5xl mx-auto px-6 py-16">\n<div class="grid grid-cols-1 md:grid-cols-4 gap-12">\n{sidebar}\n{main_content}\n</div>\n</div>'

            final_html = f"""<!DOCTYPE html>
<html lang="en">
{head}
<body class="bg-paper-100 dark:bg-ocean-950 text-ocean-800 dark:text-ocean-100 antialiased selection:bg-brand-200 dark:selection:bg-brand-800">
    {nav_str}
    {blog_layout}
    {footer}

</body>
</html>"""
            final_html = final_html.replace(
                "</body>",
                """<script>
        function setupThemeToggle(btnId, darkIconId, lightIconId) {
            var themeToggleBtn = document.getElementById(btnId);
            var themeToggleDarkIcon = document.getElementById(darkIconId);
            var themeToggleLightIcon = document.getElementById(lightIconId);

            if (!themeToggleBtn) return;

            // Change the icons inside the button based on previous settings
            if (localStorage.getItem('color-theme') === 'dark' || (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
                themeToggleLightIcon.classList.remove('hidden');
            } else {
                themeToggleDarkIcon.classList.remove('hidden');
            }

            themeToggleBtn.addEventListener('click', function() {
                // toggle icons inside button
                themeToggleDarkIcon.classList.toggle('hidden');
                themeToggleLightIcon.classList.toggle('hidden');

                // if set via local storage previously
                if (localStorage.getItem('color-theme')) {
                    if (localStorage.getItem('color-theme') === 'light') {
                        document.documentElement.classList.add('dark');
                        localStorage.setItem('color-theme', 'dark');
                    } else {
                        document.documentElement.classList.remove('dark');
                        localStorage.setItem('color-theme', 'light');
                    }
                // if NOT set via local storage previously
                } else {
                    if (document.documentElement.classList.contains('dark')) {
                        document.documentElement.classList.remove('dark');
                        localStorage.setItem('color-theme', 'light');
                    } else {
                        document.documentElement.classList.add('dark');
                        localStorage.setItem('color-theme', 'dark');
                    }
                }
            });
        }
        setupThemeToggle('theme-toggle', 'theme-toggle-dark-icon', 'theme-toggle-light-icon');
        setupThemeToggle('theme-toggle-mobile', 'theme-toggle-dark-icon-mobile', 'theme-toggle-light-icon-mobile');
    </script>
</body>""",
            )
            final_html = final_html.replace(
                '<script src="https://cdn.tailwindcss.com"></script>',
                '<script src="https://cdn.tailwindcss.com?plugins=typography"></script>',
            )
            final_html = final_html.replace(
                "</head>",
                """<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<script>hljs.highlightAll();</script>
<style>
    .prose :where(code):not(:where([class~="not-prose"] *)) {
        background-color: theme('colors.paper.200');
        padding: 0.2em 0.4em;
        border-radius: 0.25rem;
        font-weight: 500;
    }
    .prose :where(code):not(:where([class~="not-prose"] *))::before {
        content: "" !important;
    }
    .prose :where(code):not(:where([class~="not-prose"] *))::after {
        content: "" !important;
    }
    .dark .prose :where(code):not(:where([class~="not-prose"] *)) {
        background-color: theme('colors.ocean.800');
        color: theme('colors.brand.300');
    }
    .prose :where(pre code):not(:where([class~="not-prose"] *)) {
        background-color: transparent;
        padding: 0;
        border-radius: 0;
        color: inherit;
    }
</style>
</head>""",
            )

            final_html = re.sub(
                r"<title>.*?</title>",
                f"<title>{chapter['title']} | Coen van den Elsen</title>",
                final_html,
                count=1,
            )
            if description:
                final_html = final_html.replace(
                    "</head>",
                    f'<meta name="description" content="{description}">\n</head>',
                    1,
                )

            out_path = os.path.join(out_dir, chapter["out_name"])
            with open(out_path, "w") as out_f:
                out_f.write(final_html)


def build():
    with open("index.html", "r") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    head = soup.head
    for link in head.find_all("link"):
        if link.get("href", "").startswith("assets/"):
            link["href"] = "../../" + link["href"]
    head = str(head)

    nav_str = str(soup.find("nav"))
    nav_str = nav_str.replace('href="#', 'href="../../index.html#')
    nav_str = nav_str.replace('href="index.html"', 'href="../../index.html"')

    footer = str(soup.find("footer"))

    for config in BLOG_CONFIGS:
        build_one_blog(config, head, nav_str, footer)


build()
