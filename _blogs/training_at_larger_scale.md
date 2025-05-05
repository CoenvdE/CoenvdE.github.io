---
layout: blog_collection
title: Training at Larger Scale
description: A comprehensive guide to training deep learning models at scale
permalink: /blogs/training-at-larger-scale/
nav_order: 2
collection_id: training_at_larger_scale
display_chapters: true
img: assets/img/12.jpg
---

<div class="external-content" data-repo-path="_external_blogs/training-at-larger-scale">
{% capture file_content %}{% include_relative ../_external_blogs/training-at-larger-scale/README.md %}{% endcapture %}
{{ file_content | markdownify }}
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
  const externalContent = document.querySelector('.external-content');
  if (externalContent) {
    const repoPath = externalContent.dataset.repoPath;
    const images = externalContent.querySelectorAll('img');
    
    images.forEach(img => {
      const src = img.getAttribute('src');
      if (src && src.startsWith('images/')) {
        img.setAttribute('src', `{{ site.baseurl }}/${repoPath}/${src}`);
      }
    });
  }
});
</script>

{% if page.display_chapters %}

## All Chapters

{% endif %}
