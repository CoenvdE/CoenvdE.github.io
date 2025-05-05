---
layout: page
permalink: /blogs/
title: Blogs
description: Explore my different blog collections
nav: true
nav_order: 3
---

<div class="projects blogs">
  <div class="row row-cols-1 row-cols-md-3">
    
    {% assign collection_ids = site.blogs | map: "collection_id" | uniq %}
    
    {% for collection_id in collection_ids %}
      
      {% assign collection_landing_page = site.blogs | where_exp: "item", "item.collection_id == collection_id and item.name == 'index.md'" | first %}
      
      
      {% if collection_landing_page %}
        
        {% include blogs.liquid blog=collection_landing_page %}
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
