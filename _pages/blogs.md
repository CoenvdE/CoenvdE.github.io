---
layout: page
permalink: /blogs/
title: Blog Collections
description: Explore my different blog collections
nav: true
nav_order: 5
---

# Blog Collections

Welcome to my blog collections! Here you'll find several distinct series of articles, each focused on a specific topic or theme. Click on any collection to explore its chapters.

<div class="blogs-container">
  <div class="blog-collection-card">
    <h3><a href="/blogs/my-blog-collection/">My Blog Collection</a></h3>
    <p>A comprehensive 6-chapter series covering important concepts and principles.</p>
    <a href="/blogs/my-blog-collection/" class="btn btn-sm z-depth-0" role="button">View Collection →</a>
  </div>

  <div class="blog-collection-card">
    <h3><a href="/blogs/python-tutorial/">Python Tutorial</a></h3>
    <p>Learn Python programming from the basics to advanced concepts.</p>
    <a href="/blogs/python-tutorial/" class="btn btn-sm z-depth-0" role="button">View Collection →</a>
  </div>

  <div class="blog-collection-card">
    <h3><a href="/blogs/web-dev-tutorial/">Web Development Tutorial</a></h3>
    <p>Master web development with HTML, CSS, and JavaScript.</p>
    <a href="/blogs/web-dev-tutorial/" class="btn btn-sm z-depth-0" role="button">View Collection →</a>
  </div>
</div>

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
  margin-bottom: 20px;
}

.blog-collection-card:hover {
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
  transform: translateY(-2px);
}

.blog-collection-card h3 {
  margin-top: 0;
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
