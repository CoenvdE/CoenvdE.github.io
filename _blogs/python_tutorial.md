---
layout: page
title: Python Tutorial
description: Learn Python programming from the basics to advanced concepts
permalink: /blogs/python-tutorial/
nav_order: 2
---

# Python Tutorial

Welcome to the Python Tutorial series! This comprehensive guide will help you learn Python programming from basic concepts to more advanced topics.

## About This Collection

Python is one of the most popular programming languages in the world, known for its readability, versatility, and powerful ecosystem. This tutorial series is designed to take you from complete beginner to proficient Python programmer through a series of carefully structured chapters.

Whether you're interested in data science, web development, automation, or just want to learn programming, Python is an excellent language to start with. Each chapter builds on the previous one, so you can follow along step by step.

## Chapters

{% assign sorted_blogs = site.blogs | where: "collection_id", "python_tutorial" | sort: "chapter_number" %}

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
