---
layout: blog_chapter
title: Chapter 3 - Bigger Data in the Cloud
description: Working with large datasets in cloud environments
date: 2023-10-15
collection: blogs
collection_id: training_at_larger_scale
chapter_number: 3
importance: 1
category: blog-collection
---

<div class="external-content" data-repo-path="_external_blogs/training-at-larger-scale">
{% capture file_content %}{% include_relative ../_external_blogs/training-at-larger-scale/2. Bigger data in the cloud.md %}{% endcapture %}
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
