---
layout: page
title: Chapter 1 - Python Fundamentals
description: Introduction to Python programming language
date: 2024-05-23
collection: blogs
collection_id: python_tutorial
chapter_number: 1
img: assets/img/12.jpg
importance: 1
category: python
---

<div class="chapter-navigation">
  <a href="/blogs/python-tutorial/" class="btn">← Back to Collection</a>
</div>

# Chapter 1: Python Fundamentals

This is the first chapter of our Python tutorial series. We'll explore the basics of Python programming language.

## What is Python?

Python is a high-level, interpreted programming language known for its readability and versatility.

## Setting Up Your Environment

In this section, we'll walk through setting up Python on your computer.

## First Python Program

Let's write our first Python program:

```python
print("Hello, World!")
```

## What's Next

In the next chapter, we'll learn about Python data types and variables.

<div class="chapter-navigation bottom">
  <a href="/blogs/python-tutorial/" class="btn">← Back to Collection</a>
  {% assign chapters = site.blogs | where: "collection_id", "python_tutorial" | sort: "chapter_number" %}
  {% for chapter in chapters %}
    {% if chapter.chapter_number == 2 %}
      <a href="{{ chapter.url | relative_url }}" class="btn">Next Chapter →</a>
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
