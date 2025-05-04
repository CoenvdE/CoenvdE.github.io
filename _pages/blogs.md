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

[My Blog Collection](/blogs/) - A comprehensive blog series in 6 chapters covering important topics.

## Recent Blog Posts

{% for post in site.posts limit: 3 %}

- [{{ post.title }}]({{ post.url | relative_url }}) - {{ post.date | date: "%B %d, %Y" }}
  {% endfor %}
