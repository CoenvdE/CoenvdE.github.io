---
layout: page
title: Chapter 1 - Web Development Basics
description: Introduction to web development
date: 2024-05-23
collection: blogs
collection_id: web_dev_tutorial
chapter_number: 1
img: assets/img/12.jpg
importance: 1
category: web-development
toc:
  sidebar: left
---

<div class="chapter-navigation">
  <a href="/blogs/web-dev-tutorial/" class="btn btn-sm">← Back to Collection</a>
</div>

# Chapter 1: Web Development Basics

This is the first chapter of our web development series. We'll explore the fundamentals of building websites.

## The Three Pillars of Web Development

Web development relies on three core technologies:

- HTML (structure)
- CSS (styling)
- JavaScript (interactivity)

## Setting Up Your Development Environment

In this section, we'll set up a basic development environment for web development.

## Your First Webpage

Let's create a simple HTML page:

```html
<!doctype html>
<html>
  <head>
    <title>My First Webpage</title>
  </head>
  <body>
    <h1>Hello, World!</h1>
    <p>This is my first webpage.</p>
  </body>
</html>
```

## What's Next

In the next chapter, we'll dive deeper into HTML elements and structure.

<div class="chapter-navigation bottom">
  <a href="/blogs/web-dev-tutorial/" class="btn btn-sm">← Back to Collection</a>
  {% assign chapters = site.blogs | where: "collection_id", "web_dev_tutorial" | sort: "chapter_number" %}
  {% for chapter in chapters %}
    {% if chapter.chapter_number == 2 %}
      <a href="{{ chapter.url | relative_url }}" class="btn btn-sm">Next Chapter →</a>
    {% endif %}
  {% endfor %}
</div>

<style>
.chapter-navigation {
  margin: 20px 0;
  display: flex;
  justify-content: space-between;
}

.chapter-navigation.bottom {
  border-top: 1px solid #eee;
  padding-top: 20px;
  margin-top: 40px;
}
</style>
