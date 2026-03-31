import markdown

text = """
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/CoenvdE/Training-at-larger-scale-blog.git
    cd Training-at-larger-scale-blog
    ```

2.  **Install uv (if you haven't already):**
    ```bash
    pip install uv
    ```
"""

md = markdown.Markdown(extensions=['tables', 'fenced_code', 'toc'])
print("FENCED_CODE:")
print(md.convert(text))

md = markdown.Markdown(extensions=['tables', 'pymdownx.superfences', 'toc'])
print("\nSUPERFENCES:")
print(md.convert(text))
