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

<div class="projects blogs">
  <div class="row row-cols-1 row-cols-md-3">
    {% assign blog_collections = site.blogs | where_exp: "item", "item.collection_id" | map: "collection_id" | uniq %}
    
    {% for collection_id in blog_collections %}
      {% assign collection_info = site.blogs | where: "collection_id", collection_id | first %}
      {% if collection_info.title != collection_info.collection_id %}
        <div class="col">
          <a href="/blogs/{{ collection_id | slugify }}/">
            <div class="card h-100 hoverable">
              {% if collection_info.img %}
                {%
                  include figure.liquid
                  loading="eager"
                  path=collection_info.img
                  sizes = "250px"
                  alt="blog collection thumbnail"
                  class="card-img-top"
                %}
              {% endif %}
              <div class="card-body">
                <h2 class="card-title">{{ collection_info.title }}</h2>
                <p class="card-text">{{ collection_info.description }}</p>
              </div>
            </div>
          </a>
        </div>
      {% endif %}
    {% endfor %}
  </div>
</div>

<style>
/* Ensuring the cards have the same hover effect as project cards */
.blogs .card.hoverable {
  transition: all 0.3s ease;
}

.blogs .card.hoverable:hover {
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
  transform: translateY(-4px);
}
</style>
