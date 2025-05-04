---
layout: page
title: Web Development Tutorial
description: Master web development with HTML, CSS, and JavaScript
permalink: /blogs/web-dev-tutorial/
---

# Web Development Tutorial

Welcome to the Web Development Tutorial series. This collection will help you learn how to build modern websites using HTML, CSS, and JavaScript.

## Chapters

{% assign sorted_blogs = site.blogs | where: "collection_id", "web_dev_tutorial" | sort: "chapter_number" %}

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

This Web Development tutorial is designed for beginners who want to learn front-end web development. We'll cover HTML for structure, CSS for styling, and JavaScript for interactivity.
