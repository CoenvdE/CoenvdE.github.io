with open("index.html", "r") as f:
    html = f.read()

# Make blog card completely clickable
html = html.replace(
    '<h3 class="text-xl font-bold text-ocean-900 mb-2">Training at Larger Scale</h3>',
    '<h3 class="text-xl font-bold text-ocean-900 mb-2">\n                            <a href="blogs/training-at-larger-scale/index.html" class="focus:outline-none">\n                                <span class="absolute inset-0" aria-hidden="true"></span>\n                                Training at Larger Scale\n                            </a>\n                        </h3>'
)

# Also make the project cards clickable by wrapping titles
# Card 1: OceanOS Foundation Model
html = html.replace(
    '<h3 class="text-xl font-bold text-ocean-900 mb-2 group-hover:text-brand-600 transition-colors">OceanOS Foundation Model</h3>',
    '<h3 class="text-xl font-bold text-ocean-900 mb-2 group-hover:text-brand-600 transition-colors">\n                            <a href="#" class="focus:outline-none">\n                                <span class="absolute inset-0" aria-hidden="true"></span>\n                                OceanOS Foundation Model\n                            </a>\n                        </h3>'
)
# Note: Since there's no href specified for projects, I'll use # but make the whole card a group relative.
html = html.replace(
    '<div class="bg-white rounded-xl shadow-md border border-slate-100 overflow-hidden group hover:shadow-lg transition-all duration-300">',
    '<div class="relative bg-white rounded-xl shadow-md border border-slate-100 overflow-hidden group hover:shadow-lg transition-all duration-300">'
)
# Make the blog card relative too
html = html.replace(
    '<div class="bg-white rounded-xl shadow-sm border border-slate-100 overflow-hidden hover:shadow-md transition-shadow group flex flex-col h-full">',
    '<div class="relative bg-white rounded-xl shadow-sm border border-slate-100 overflow-hidden hover:shadow-md transition-shadow group flex flex-col h-full">'
)

# Card 2: Climate Downscaling Research
html = html.replace(
    '<h3 class="text-xl font-bold text-ocean-900 mb-2 group-hover:text-brand-600 transition-colors">Climate Downscaling Research</h3>',
    '<h3 class="text-xl font-bold text-ocean-900 mb-2 group-hover:text-brand-600 transition-colors">\n                            <a href="#" class="focus:outline-none">\n                                <span class="absolute inset-0" aria-hidden="true"></span>\n                                Climate Downscaling Research\n                            </a>\n                        </h3>'
)

# Card 3: Early Disease Warning System
html = html.replace(
    '<h3 class="text-xl font-bold text-ocean-900 mb-2 group-hover:text-brand-600 transition-colors">Early Disease Warning System</h3>',
    '<h3 class="text-xl font-bold text-ocean-900 mb-2 group-hover:text-brand-600 transition-colors">\n                            <a href="#" class="focus:outline-none">\n                                <span class="absolute inset-0" aria-hidden="true"></span>\n                                Early Disease Warning System\n                            </a>\n                        </h3>'
)

with open("index.html", "w") as f:
    f.write(html)
