---
layout: post
title: "Example Collection: Part 1 - Getting Started"
description: "The first part of our example blog series, laying the groundwork."
date: 2024-07-27
# Required for Collection Structure:
collection_id: example-collection
chapter_number: 1
# Optional fields:
img: /assets/img/placeholder.jpg # Example path - replace with your actual image path
toc: true # Generate Table of Contents for this post
categories: [Tutorial, Example]
giscus_comments: true # Enable comments if configured
---

## Introduction

Welcome to the first part of our example blog collection! This series will demonstrate how the blog collections feature works in this Jekyll theme.

In this chapter, we'll set up the basic concepts.

## Section 1: Markdown Basics

Jekyll uses Markdown for formatting content. You can use various elements:

- **Bold text** and _italic text_.
- Lists, like this one.
- Code blocks:

```python
def greet(name):
  print(f"Hello, {name}!")

greet("World")
```

## Section 2: Front Matter Importance

The section at the top of this file, enclosed in `---`, is called the front matter. It contains metadata for the post:

- `layout`: Defines the page structure (using `post` layout here).
- `title`: The main title of this specific post/chapter.
- `description`: A short summary.
- `date`: The publication date.
- `collection_id`: Groups this post with others in the 'example-collection'.
- `chapter_number`: Sets the order within the collection.
- `img`: A thumbnail image used for the collection card on the main blogs page (usually set in the first chapter).
- `toc`: Enables the Table of Contents.
- `categories`: Tags for organization.
- `giscus_comments`: Enables the comment section.

Stay tuned for the next part!
