---
layout: blog_chapter
title: "Chapter 5 - Optimizing the Pipeline: Model"
description: Techniques for optimizing model architecture and training
date: 2023-10-29
collection: blogs
collection_id: training_at_larger_scale
chapter_number: 5
importance: 1
category: blog-collection
---

<div class="external-content" data-repo-path="_external_blogs/training-at-larger-scale">
{% capture file_content %}{% include_relative "../_external_blogs/training-at-larger-scale/4. Optimizing the pipeline: Model.md" %}{% endcapture %}
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
