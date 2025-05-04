---
layout: page
permalink: /blogs/
title: Blogs
description: Educational blog collections and individual posts
nav: true
nav_order: 5
---

# Blog Collections

Welcome to my educational blogs section! Here you'll find carefully curated collections of blog posts organized by topic. Each collection offers a comprehensive exploration of its subject, with chapters that build on each other to provide a complete learning experience.

## Featured Collections

<div class="blogs-container">
  <div class="blog-collection-card">
    <h3><a href="/blogs/my-blog-collection/">My Blog Collection</a></h3>
    <p>A comprehensive 6-chapter series covering important concepts and principles. This collection takes you from foundational knowledge to advanced applications.</p>
    <a href="/blogs/my-blog-collection/" class="btn btn-sm z-depth-0" role="button">Explore Collection →</a>
  </div>

  <div class="blog-collection-card">
    <h3><a href="/blogs/python-tutorial/">Python Tutorial</a></h3>
    <p>Learn Python programming from the basics to advanced concepts. Perfect for beginners and those looking to expand their programming skills.</p>
    <a href="/blogs/python-tutorial/" class="btn btn-sm z-depth-0" role="button">Explore Collection →</a>
  </div>

  <div class="blog-collection-card">
    <h3><a href="/blogs/web-dev-tutorial/">Web Development Tutorial</a></h3>
    <p>Master web development with HTML, CSS, and JavaScript. Build beautiful, responsive websites from scratch with this practical guide.</p>
    <a href="/blogs/web-dev-tutorial/" class="btn btn-sm z-depth-0" role="button">Explore Collection →</a>
  </div>
</div>

## Recent Blog Posts

Here are my most recent individual blog posts:

{% for post in site.posts limit: 3 %}

- [{{ post.title }}]({{ post.url | relative_url }}) - {{ post.date | date: "%B %d, %Y" }}
  {% endfor %}

<style>
.blogs-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin: 20px 0;
}

.blog-collection-card {
  flex: 1 1 300px;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  transition: all 0.3s ease;
}

.blog-collection-card:hover {
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
  transform: translateY(-2px);
}

.blog-collection-card h3 {
  margin-top: 0;
}
</style>
