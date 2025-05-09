---
layout: blog_collection
title: "Training at larger scale"
description: "A comprehensive guide to scaling machine learning from small to larger training setups."
collection_id: training-at-larger-scale
display_chapters: true
---

# Training at larger scale

<div align="center">
  <img src="/images/training-blog/intro_image_larger_scale.png" alt="Scaling up training" width="400"/>
  <br>
  <p><em>Illustration of training scale</em></p>
</div>

<div align="right">
  <small>Created with ChatGPT</a></small>
</div>

### Why am I writing this?

At university, in online blogs, and across tutorials, training machine learning models is often well explained—especially for small-scale setups. These typically involve datasets that fit on a local hard drive, training on a single GPU, and straightforward implementations without worrying about fast data loading, datasets that do not fit onto a local hard drive (lazy loading), or multi-GPU utilization/optimization.

However, when transitioning to a larger setup —not massive SOTA-scale training across thousands of GPUs with internet-scale data, but something in between— good resources are harder to find and are scattered around. I call this the "larger-scale training" realm: working with datasets that are a few terabytes (too large for local storage but far from internet-scale) and training across multiple GPUs (around 10, not 100s or 1000s).

For my research, I need to scale up my training to this realm, but I struggle to find practical, well-structured guides on bridging the gap from small-scale to mid-sized, high-performance training. This larger-scale training" is where a lot of valuable research and development happens, yet optimization and implementation for this space are harder to figure out. Maximizing hardware efficiency at this level can significantly reduce training time, costs and environmental impact.

This guide is for those stepping into this space —researchers and practitioners who want to scale their training beyond a single GPU while making the most of the resources they have. My experience comes from working with geospatial data, so some examples may be domain-specific, but the core principles apply broadly across all machine learning applications that make use of pytorch.

I want to note that this is not a definitive guide on how everything should be done. Instead, it's a collection of challenges I faced and the solutions I found along the way. I encourage you to ask questions, share feedback, and suggest improvements — the goal is to learn from each other and train more efficiently every day :)

This blog is available on [GitHub](https://github.com/coenvde/training-at-larger-scale-blog) as well as my [website](https://coenvde.github.io/blogs/training-at-larger-scale/index/). For every chapter, I created a folder on GitHub with all full code. The markdown files are available on both platforms, containing text and code examples.

## What's next

I'll walk you through my process of implementing and optimizing everything. Each chapter folder contains code examples that demonstrate the concepts discussed in the corresponding markdown file. To run the examples, navigate to the specific chapter folder on GitHub and follow the instructions as specified in the markdown files. I strongly advise to run through them in order, as they build on top of each other and I expect previous chapters as background knowledge for the following one. I especially encourage you to get familiar with pytorch lightning ([1. Multi-GPU training](/blogs/training-at-larger-scale/part2/)) as it will streamline, improve and speed up your workflow a lot.

## Chapters

1. [0. The Setup](/blogs/training-at-larger-scale/part1/) - Overview of the initial setup as a starting point
2. [1. Multi-GPU training](/blogs/training-at-larger-scale/part2/) - Scaling from a single GPU to multiple GPUs and using Lightning for better code
3. [2. Bigger data in the cloud](/blogs/training-at-larger-scale/part3/) - Working with bigger data
4. [3. Optimizing the pipeline: Data](/blogs/training-at-larger-scale/part4/) - Optimizing: Maximizing DataLoader efficiency
5. [4. Optimizing the pipeline: Model](/blogs/training-at-larger-scale/part5/) - Optimizing: Profiling and fixing slowdowns
6. [5. What Is Next](/blogs/training-at-larger-scale/part6/) - Further optimizations, experiments and improvements as the final step before training

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/CoenvdE/Training-at-larger-scale-blog.git
    cd Training-at-larger-scale-blog
    ```

2.  **Install uv (if you haven't already):**

    ```bash
    pip install uv
    ```

    Or, for other installation methods, see the [uv documentation](https://astral.sh/uv/install.sh).

3.  **Create a virtual environment and install dependencies:**

    ```bash
    uv venv
    uv sync
    ```

    This will create a virtual environment in `.venv` and install all necessary packages.

4.  **Run the code:**
    ```bash
    uv run python your_script.py
    ```
    This will run your Python script in the virtual environment with all dependencies available.
