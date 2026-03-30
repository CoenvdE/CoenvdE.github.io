import os
import markdown
import glob
from bs4 import BeautifulSoup
import re

def get_title(content):
    match = re.search(r'^title:\s*"(.*?)"', content, re.MULTILINE)
    if match: return match.group(1)

    match = re.search(r'^#\s+(.*)', content, re.MULTILINE)
    if match: return match.group(1)
    return "Chapter"

def build():
    out_dir = 'blogs/training-at-larger-scale'
    os.makedirs(out_dir, exist_ok=True)

    with open('index.html', 'r') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    head = soup.head
    for link in head.find_all('link'):
        if link.get('href', '').startswith('assets/'):
            link['href'] = '../../' + link['href']
    head = str(head)

    nav_str = str(soup.find('nav'))
    nav_str = nav_str.replace('href="#', 'href="../../index.html#')

    footer = str(soup.find('footer'))

    md = markdown.Markdown(extensions=['tables', 'fenced_code', 'toc'])

    parts = glob.glob('_blogs/training-at-larger-scale/*.md')
    def sort_key(f):
        name = os.path.basename(f)
        if name == 'index.md': return 0
        match = re.search(r'part(\d+)', name)
        return int(match.group(1)) if match else 999

    parts.sort(key=sort_key)

    chapters = []
    for part in parts:
        with open(part, 'r') as f:
            content = f.read()
            title = get_title(content)
            basename = os.path.basename(part)
            out_name = basename.replace('.md', '.html')
            chapters.append({'path': part, 'out_name': out_name, 'title': title})

    for i, chapter in enumerate(chapters):
        with open(chapter['path'], 'r') as f:
            content = f.read()
            if content.startswith('---'):
                parts_split = content.split('---', 2)
                if len(parts_split) > 2:
                    content = parts_split[2]

            content = content.replace('/images/training-blog/', '../../images/training-blog/')
            content = re.sub(r'\/blogs\/training-at-larger-scale\/([a-zA-Z0-9_-]+)\/', r'\1.html', content)

            html_content = md.convert(content)

            nav_links = "<div class=\"flex justify-between items-center mt-12 pt-8 border-t border-slate-200\">"
            if i > 0:
                prev_ch = chapters[i-1]
                nav_links += f"<a href=\"{prev_ch['out_name']}\" class=\"text-brand-600 hover:text-brand-500 font-medium text-lg px-4 py-2 border border-brand-200 rounded-lg shadow-sm bg-brand-50 hover:bg-brand-100 transition-colors\">&larr; Previous Chapter: {prev_ch['title']}</a>"
            else:
                nav_links += "<div></div>"

            if i < len(chapters) - 1:
                next_ch = chapters[i+1]
                nav_links += f"<a href=\"{next_ch['out_name']}\" class=\"text-brand-600 hover:text-brand-500 font-medium text-lg px-4 py-2 border border-brand-200 rounded-lg shadow-sm bg-brand-50 hover:bg-brand-100 transition-colors\">Next Chapter: {next_ch['title']} &rarr;</a>"
            else:
                nav_links += "<div></div>"
            nav_links += "</div>"

            # Sidebar chapter list
            sidebar = "<div class=\"md:col-span-1 hidden md:block\">\n"
            sidebar += "<div class=\"sticky top-24 bg-white shadow-xl rounded-lg p-6\">\n"
            sidebar += "<h3 class=\"text-lg font-bold text-ocean-900 mb-4 border-b pb-2\">Chapters</h3>\n"
            sidebar += "<ul class=\"space-y-3\">\n"
            for j, ch in enumerate(chapters):
                active_class = "text-brand-600 font-bold border-l-2 border-brand-500 pl-2" if i == j else "text-slate-600 hover:text-brand-600 pl-2 border-l-2 border-transparent transition-colors"
                sidebar += f"<li><a href=\"{ch['out_name']}\" class=\"text-sm block {active_class}\">{ch['title']}</a></li>\n"
            sidebar += "</ul>\n</div>\n</div>"

            # Main content wrapper
            main_content = f"<div class=\"md:col-span-3 bg-white shadow-xl rounded-lg p-8 prose prose-slate prose-brand max-w-none\">\n{html_content}\n{nav_links}\n</div>"

            # Put them together in a grid
            blog_layout = f"<div class=\"max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-32 mt-16\">\n<div class=\"grid grid-cols-1 md:grid-cols-4 gap-8\">\n{sidebar}\n{main_content}\n</div>\n</div>"

            final_html = f"""<!DOCTYPE html>
<html lang="en">
{head}
<body class="bg-slate-50 text-slate-800 antialiased selection:bg-brand-500 selection:text-white">
    {nav_str}
    {blog_layout}
    {footer}
</body>
</html>"""
            final_html = final_html.replace('<script src="https://cdn.tailwindcss.com"></script>', '<script src="https://cdn.tailwindcss.com?plugins=typography"></script>')

            out_path = os.path.join(out_dir, chapter['out_name'])
            with open(out_path, 'w') as out_f:
                out_f.write(final_html)

build()
