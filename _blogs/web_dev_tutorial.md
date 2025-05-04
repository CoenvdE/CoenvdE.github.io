---
layout: page
title: Web Development Tutorial
description: Master web development with HTML, CSS, and JavaScript
permalink: /blogs/web-dev-tutorial/
nav_order: 3
---

# Web Development Tutorial

Welcome to the Web Development Tutorial series! This comprehensive guide will help you learn how to build modern, responsive websites from scratch using HTML, CSS, and JavaScript.

## About This Collection

Web development is an essential skill in today's digital world. This tutorial series takes you through the foundations of front-end web development, teaching you how to create engaging, interactive, and professional-looking websites.

The tutorial is structured to provide a solid foundation in the core technologies of the web:

- **HTML** for structure and content
- **CSS** for styling and layout
- **JavaScript** for interactivity and dynamic behavior

Each chapter focuses on specific aspects of web development and includes practical examples you can follow along with.

## Chapters

{% assign sorted_blogs = site.blogs | where: "collection_id", "web_dev_tutorial" | sort: "chapter_number" %}

<div class="chapters-container">
  {% for blog in sorted_blogs %}
    {% if blog.title != page.title %}
    <div class="chapter-card">
      <div class="chapter-number">Chapter {{ blog.chapter_number }}</div>
      <h3 class="chapter-title">
        <a href="{{ blog.url | relative_url }}">{{ blog.title }}</a>
      </h3>
      <p class="chapter-description">{{ blog.description }}</p>
      <a href="{{ blog.url | relative_url }}" class="btn btn-sm">Read Chapter →</a>
    </div>
    {% endif %}
  {% endfor %}
</div>

<style>
.chapters-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin: 30px 0;
}

.chapter-card {
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  transition: all 0.3s ease;
  position: relative;
}

.chapter-card:hover {
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.chapter-number {
  font-weight: bold;
  color: #666;
  margin-bottom: 5px;
}

.chapter-title {
  margin-top: 0;
  margin-bottom: 10px;
}

.chapter-description {
  margin-bottom: 15px;
  color: #555;
}

.btn {
  display: inline-block;
  background-color: #4285f4;
  color: white;
  padding: 8px 16px;
  border-radius: 4px;
  text-decoration: none;
}

.btn:hover {
  background-color: #3367d6;
}
</style>
