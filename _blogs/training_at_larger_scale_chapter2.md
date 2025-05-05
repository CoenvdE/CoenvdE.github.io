---
layout: blog_chapter
title: Chapter 2 - Multi-GPU Training
description: Techniques for training deep learning models across multiple GPUs
date: 2023-10-08
collection: blogs
collection_id: training_at_larger_scale
chapter_number: 2
importance: 1
category: blog-collection
---

<div class="external-content" data-repo-path="_external_blogs/training-at-larger-scale">
{% capture file_content %}{% include_relative "../_external_blogs/training-at-larger-scale/1. Multi-GPU training.md" %}{% endcapture %}
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
