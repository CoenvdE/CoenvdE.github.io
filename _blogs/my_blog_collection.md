---
layout: page
title: My Blog Collection
description: A comprehensive blog series in 6 chapters
permalink: /blogs/my-blog-collection/
---

# My Blog Collection

Welcome to my comprehensive blog series divided into six chapters. This collection explores important concepts in detail, from basic concepts to future trends.

## Chapters

{% assign sorted_blogs = site.blogs | where: "collection_id", "my_blog_collection" | sort: "chapter_number" %}

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

This blog collection is designed to provide a comprehensive overview of important concepts. Whether you're a beginner or an expert, you'll find valuable information in these chapters.
