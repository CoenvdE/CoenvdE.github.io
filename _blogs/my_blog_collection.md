---
layout: page
title: My Blog Collection
description: A comprehensive blog series in 6 chapters
permalink: /blogs/my-blog-collection/
nav_order: 1
---

# My Blog Collection

Welcome to my comprehensive blog series divided into six chapters. This collection explores important concepts in detail, from basic concepts to future trends.

## About This Collection

This blog collection is designed to provide a comprehensive overview of important concepts. Whether you're a beginner or an expert, you'll find valuable information in these chapters.

The materials are organized into a logical progression, allowing you to build your knowledge step by step. Feel free to read from start to finish or jump to specific chapters that interest you most.

## Chapters

{% assign sorted_blogs = site.blogs | where: "collection_id", "my_blog_collection" | sort: "chapter_number" %}

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
