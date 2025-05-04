---
layout: page
title: Python Tutorial
description: Learn Python programming from the basics to advanced concepts
permalink: /blogs/python-tutorial/
---

# Python Tutorial

Welcome to the Python Tutorial series. This collection will help you learn Python programming from basic concepts to more advanced topics.

## Chapters

{% assign sorted_blogs = site.blogs | where: "collection_id", "python_tutorial" | sort: "chapter_number" %}

<div class="blog-collection">
  {% for blog in sorted_blogs %}
    {% if blog.title != page.title %}
    <div class="blog-card">
      <h3 class="blog-title">
        <a href="{{ blog.url | relative_url }}">{{ blog.title }}</a>
      </h3>
      <p class="blog-description">{{ blog.description }}</p>
    </div>
    {% endif %}
  {% endfor %}
</div>

## About This Collection

This Python tutorial is designed for beginners and intermediate programmers looking to improve their Python skills. We cover everything from basic syntax to more advanced programming concepts.
