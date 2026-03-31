import re

with open('index.html', 'r') as f:
    html = f.read()

# Current classes: text-ocean-900 dark:text-brand-300 bg-brand-400 hover:bg-brand-300
old_classes = 'class="inline-flex justify-center items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-ocean-900 dark:text-brand-300 bg-brand-400 hover:bg-brand-300 transition-all shadow-lg hover:shadow-brand-500/30"'
new_classes = 'class="inline-flex justify-center items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-ocean-900 bg-brand-400 hover:bg-brand-300 dark:bg-brand-500 dark:text-slate-100 dark:hover:bg-brand-400 transition-all shadow-lg hover:shadow-brand-500/30"'

html = html.replace(old_classes, new_classes)

with open('index.html', 'w') as f:
    f.write(html)
