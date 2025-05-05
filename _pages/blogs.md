---
layout: page
permalink: /blogs/
title: Blog Collections
description: Explore my different blog collections
nav: true
nav_order: 5
---

<div class="projects blogs">
  <div class="row row-cols-1 row-cols-md-3">
    {% assign blog_collections = site.blogs | where_exp: "item", "item.collection_id" | map: "collection_id" | uniq %}
    
    {% for collection_id in blog_collections %}
      {% assign blog = site.blogs | where: "collection_id", collection_id | first %}
      {% if blog.title != blog.collection_id %}
        {% include blogs.liquid %}
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
