import re

with open('build_blogs.py', 'r') as f:
    content = f.read()

# I want to add some custom css for inline code
css_to_add = """
    <style>
        .prose :where(code):not(:where([class~="not-prose"] *)) {
            background-color: theme('colors.slate.100');
            padding: 0.2em 0.4em;
            border-radius: 0.25rem;
            font-weight: 600;
        }
        .dark .prose :where(code):not(:where([class~="not-prose"] *)) {
            background-color: theme('colors.slate.800');
            color: theme('colors.brand.300');
        }
        .prose :where(pre code):not(:where([class~="not-prose"] *)) {
            background-color: transparent;
            padding: 0;
            border-radius: 0;
            color: inherit;
        }
    </style>
"""

content = content.replace('</head>', css_to_add + '\n</head>')

with open('build_blogs.py', 'w') as f:
    f.write(content)
