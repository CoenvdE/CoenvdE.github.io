---
layout: page
permalink: /blogs/
title: Blogs
description: I hope you find something useful here!
nav: true
nav_order: 3
---

<div class="projects blogs">
  <div class="row row-cols-1 row-cols-md-3">
    
    {% assign collection_ids = site.blogs | map: "collection_id" | uniq %}
    
    {% for collection_id in collection_ids %}
      
      {% assign collection_landing_page = site.blogs | where_exp: "item", "item.collection_id == collection_id and item.name == 'index.md'" | first %}
      
      
      {% if collection_landing_page %}
        <div class="col">
          <a href="{{ collection_landing_page.url | relative_url }}">
            <div class="card h-100 hoverable">
              {% if collection_landing_page.img %}
                {%
                  include figure.liquid
                  loading="eager"
                  path=collection_landing_page.img
                  sizes = "250px"
                  alt="blog collection thumbnail"
                  class="card-img-top"
                %}
              {% endif %}
              <div class="card-body">
                <h2 class="card-title">{{ collection_landing_page.title }}</h2>
                <p class="card-text">{{ collection_landing_page.description }}</p>
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
