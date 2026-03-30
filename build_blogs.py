import os
import markdown
import glob
from bs4 import BeautifulSoup
import re

def build():
    os.makedirs('blogs', exist_ok=True)

    with open('index.html', 'r') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    head = soup.head
    # make links absolute or relative to root
    for link in head.find_all('link'):
        if link.get('href', '').startswith('assets/'):
            link['href'] = '../' + link['href']
    head = str(head)

    nav = str(soup.find('nav'))
    footer = str(soup.find('footer'))

    md = markdown.Markdown(extensions=['tables', 'fenced_code', 'toc'])

    parts = glob.glob('_blogs/training-at-larger-scale/*.md')
    # Custom sort to handle index.md first, then part1, part2, etc.
    def sort_key(f):
        name = os.path.basename(f)
        if name == 'index.md': return 0
        match = re.search(r'part(\d+)', name)
        return int(match.group(1)) if match else 999

    parts.sort(key=sort_key)

    blog_content = "<div class=\"max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-32 bg-white shadow-xl rounded-lg my-20 prose prose-slate prose-brand\">\n"

    for part in parts:
        with open(part, 'r') as f:
            content = f.read()
            if content.startswith('---'):
                parts_split = content.split('---', 2)
                if len(parts_split) > 2:
                    content = parts_split[2]

            # fix image paths
            content = content.replace('/images/training-blog/', '../images/training-blog/')

            # Make sure we don't duplicate id "whats-next" if it appears in index and chapter 6
            if 'part6.md' in part:
                 content = content.replace('# What\'s Next?', '# What\'s Next? - Chapter 6')

            html_content = md.convert(content)
            blog_content += html_content
            blog_content += "\n<hr class=\"my-12 border-slate-200\">\n"

    blog_content += "</div>"

    final_html = f"""<!DOCTYPE html>
<html lang="en">
{head}
<body class="bg-slate-50 text-slate-800 antialiased selection:bg-brand-500 selection:text-white">
    {nav}
    {blog_content}
    {footer}
</body>
</html>"""

    final_html = final_html.replace('<script src="https://cdn.tailwindcss.com"></script>', '<script src="https://cdn.tailwindcss.com?plugins=typography"></script>')

    with open('blogs/training-at-larger-scale.html', 'w') as f:
        f.write(final_html)

build()
