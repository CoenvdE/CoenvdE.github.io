import re

with open("index.html", "r") as f:
    html = f.read()

# Make background and texts adapt
html = html.replace('bg-white', 'bg-white dark:bg-slate-800')
html = html.replace('bg-slate-50', 'bg-slate-50 dark:bg-slate-900')
html = html.replace('text-slate-600', 'text-slate-600 dark:text-slate-300')
html = html.replace('text-ocean-900', 'text-ocean-900 dark:text-brand-300')
html = html.replace('border-slate-200', 'border-slate-200 dark:border-slate-700')
html = html.replace('border-slate-100', 'border-slate-100 dark:border-slate-700')
html = html.replace('bg-slate-100', 'bg-slate-100 dark:bg-slate-700')

with open("index.html", "w") as f:
    f.write(html)
