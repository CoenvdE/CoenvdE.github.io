---
layout: page
permalink: /blogs/
title: Blogs
description: Blog collections and individual posts
nav: true
nav_order: 5
---

# Blogs

## Blog Collections

- [My Blog Collection](/blogs/my-blog-collection/) - A comprehensive blog series in 6 chapters covering important concepts.
- [Python Tutorial](/blogs/python-tutorial/) - Learn Python programming from the basics to advanced concepts.
- [Web Development Tutorial](/blogs/web-dev-tutorial/) - Master web development with HTML, CSS, and JavaScript.

## Recent Blog Posts

{% for post in site.posts limit: 3 %}

- [{{ post.title }}]({{ post.url | relative_url }}) - {{ post.date | date: "%B %d, %Y" }}
  {% endfor %}
