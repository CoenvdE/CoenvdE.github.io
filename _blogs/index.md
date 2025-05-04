---
layout: page
title: Blog Collections
description: A library of comprehensive blog series on various topics
permalink: /blogs/
---

# Blog Collections

Welcome to my blog collections library. Here you'll find comprehensive series on different topics, each organized into multiple chapters.

## Available Collections

### My Blog Collection

{% assign blog_collection = site.blogs | where: "collection_id", "my_blog_collection" | sort: "chapter_number" %}

<div class="blog-subcollection">
  <p>A comprehensive blog series exploring important concepts.</p>
  <div class="chapters-list">
    {% for blog in blog_collection %}
      {% if blog.title != page.title %}
      <div class="blog-item">
        <h4 class="blog-title">
          <a href="{{ blog.url | relative_url }}">{{ blog.title }}</a>
        </h4>
      </div>
      {% endif %}
    {% endfor %}
  </div>
</div>

### Python Tutorial

{% assign python_collection = site.blogs | where: "collection_id", "python_tutorial" | sort: "chapter_number" %}

<div class="blog-subcollection">
  <p>Learn Python programming from the basics to advanced concepts.</p>
  <div class="chapters-list">
    {% for blog in python_collection %}
      {% if blog.title != page.title %}
      <div class="blog-item">
        <h4 class="blog-title">
          <a href="{{ blog.url | relative_url }}">{{ blog.title }}</a>
        </h4>
      </div>
      {% endif %}
    {% endfor %}
  </div>
</div>

### Web Development Tutorial

{% assign webdev_collection = site.blogs | where: "collection_id", "web_dev_tutorial" | sort: "chapter_number" %}

<div class="blog-subcollection">
  <p>Master web development with HTML, CSS, and JavaScript.</p>
  <div class="chapters-list">
    {% for blog in webdev_collection %}
      {% if blog.title != page.title %}
      <div class="blog-item">
        <h4 class="blog-title">
          <a href="{{ blog.url | relative_url }}">{{ blog.title }}</a>
        </h4>
      </div>
      {% endif %}
    {% endfor %}
  </div>
</div>

## Creating Your Own Collection

To add a new blog collection, create markdown files in the `_blogs` directory with the same `collection_id` in the front matter.
