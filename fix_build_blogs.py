with open('build_blogs.py', 'r') as f:
    content = f.read()

content = content.replace("""            final_html = final_html.replace('
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

</head>', '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">\\n<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>\\n<script>hljs.highlightAll();</script>\\n
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

</head>')""", """            final_html = final_html.replace('</head>', '''<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<script>hljs.highlightAll();</script>
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
</head>''')""")

with open('build_blogs.py', 'w') as f:
    f.write(content)
