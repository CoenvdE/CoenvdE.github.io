---
layout: blog_collection
title: "0. The Setup"
description: "Chapter 1 of the Training at Larger Scale series"
date: 2025-04-01
collection_id: training-at-larger-scale
chapter_number: 1
toc: true
categories: [Machine Learning, Training, PyTorch, Optimization]
giscus_comments: true
---

Before diving into optimizations, our starting point needs to be solid. I will walk you through some best practices and a baseline to give you a solid starting point. Note that my model and pipeline were actually a lot more complicated, but my goal is not how to recreate my complicated pipeline, it is to show you simple examples for you to optimize and improve yours.

```
0. The Setup/
├── config/
│   └── config.yaml
├── output/
├── src/
│   ├── data/
│   │   ├── __pycache__/
│   │   └── pytorch_dataset.py
│   └── model/
│       ├── __pycache__/
│       ├── pytorch_model.py
│       ├── pytorch_encoder.py
│       └── pytorch_decoder.py
├── tests/
│   ├── __pycache__/
│   ├── __init__.py
│   └── test_parameters.py
├── wandb/
├── pytorch_train.py
└── requirements.txt
```

### My Model (components and overview)

---

My model was essentially a (Masked) Autoencoder (with some cool stuff that does not matter for this guide) and had the following key components:

- `pytorch_encoder`
- `pytorch_decoder`
- `pytorch_model` – responsible for the forward pass and loss calculation (plus some additional components that aren't essential for this guide.)

### My Dataset

---

- a `pytorch_dataset`  
  I used a big, geospatial dataset for my training. For this tutorial, I created a dummy example, but feel free to swap it out for e.g. [CIFAR](https://www.cs.toronto.edu/~kriz/cifar.html) or any other dataset you like. It is important that this is wrapped into a `torch.utils.data.Dataset` object.  
  We will come back to data stuff in more detail in [Chapter 2](2.%20Bigger%20data%20in%20the%20cloud.md).  
  Note that I created a generator for the dataloader that has a set seed and I also used a `set_seed` function to keep everything reproducible in the `pytorch_train.py` file.

### Reproducibility

---

Reproducibility is very important, it allows you and others to reliably verify and compare results. In research, it ensures findings are valid and consistent. For practitioners, it makes debugging and iterative experimentation much easier. Seeding is very important for reproducibility.  
you need to seed everything (torch, numpy, python, etc.). Look at the `pytorch_train.py` file for an example.  
Seed not properly propagated to data-generators, so I created a generator for the dataloader that has a set seed and I also used a `set_seed` function to keep everything reproducible in the `pytorch_train.py` file.
Pytorch dataloader workers (I will properly explain everything this in [Chapter 3](3.%20Optimizing%20the%20pipeline%20-%20Data.md)) need to be seeded, because each worker runs in its own process, and without explicit seeding, they will use random seeds, leading to non-deterministic data loading and augmentations. look at the `worker_init_fn` in the `pytorch_train.py` file for an example.

For full reproducibility (usefull for debugging and testing), you should also set the following: - `torch.backends.cudnn.deterministic = True` # slows down training but makes results reproducible (default is False) - `torch.backends.cudnn.benchmark = False` # slows down training but makes results reproducible (default is True)
These settings control how CUDA kernels are selected and run. Setting deterministic = True ensures the same operations produce the same outputs every run, at the cost of performance. Disabling benchmark prevents the selection of non-deterministic, optimized algorithms that could vary between runs.
torch.backends.cudnn.benchmark = False disables the auto-tuner that selects the fastest convolution algorithms based on input sizes. While this can speed up training, it introduces non-determinism when input sizes vary. Setting it to False ensures consistent behavior across runs.

### Reproducibility

---

Reproducibility is essential — it allows you and others to reliably verify and compare results.  
In research, it ensures findings are valid and consistent. For practitioners, it makes debugging and iterative experimentation much easier.

A key part of reproducibility is proper seeding. You need to seed **everything**:

- Python's built-in `random`
- NumPy
- PyTorch
- Everything else that needs a seed

See the `set_seed` function in `pytorch_train.py` for an example.

By default, PyTorch `DataLoader` workers (A full explanation is provided in [Chapter 3](3.%20Optimizing%20the%20pipeline%20-%20Data.md)) are not seeded properly — each worker runs in its own process, and without explicit seeding, they will each get a random seed. This can lead to **non-deterministic data loading and augmentations**.

To fix this, create a generator for the `DataLoader` with a fixed seed and use a `worker_init_fn`.  
Check out the examples in `pytorch_train.py`.

For full reproducibility — especially useful during debugging and testing — set the following:

```python
torch.backends.cudnn.deterministic = True  # Default: False
torch.backends.cudnn.benchmark = False     # Default: True
```

These flags control how CUDA kernels are selected and run:
• deterministic = True ensures that operations produce the same results across runs, but may slow training.
• benchmark = False disables CuDNN’s auto-tuner, which usually picks the fastest convolution algorithms. While this can speed up training, it may introduce non-determinism, especially when input sizes vary.

Setting both ensures consistent, repeatable behavior across runs.w

### Config files

---

I use config files for the model, dataloader, training, optimizer, and scheduler arguments. This is best practice, allowing quick adjustments to hyperparameters without modifying the code. This makes experimentation and testing more efficient.  
An example of a config file with a few of these parameters is given in:  
`Training-at-larger-scale-blog/0. The Setup/config/config.yaml`

### Unittests

---

Before moving forward, ensure your model actually works. It is important to write tests that check:

- Shape consistency
- Correct device allocation
- Other problem specific stuff that you might need
- Proper parameter loading from config file

This last one is very important and can save you a lot of trouble debugging, I made an example test for this in my `.tests` folder

```
python -m unittest tests/test_parameters.py
```

Additionally, I set up automated testing — every push to the GitHub branch runs these tests.  
For this, look at the `.github/workflows/test.yml` file.  
While unit tests don't catch everything, they help ensure the code runs smoothly (in the cloud) and prevent accidental breakage.  
Automatically running them via GitHub gives you good feedback on if you break anything!

### Tracking & Experiment Logging (WandB)

---

Proper tracking is essential for monitoring model performance and debugging issues.  
I used Weights & Biases (WandB), but alternatives like MLflow also work.

What to track?

- Validation loss & training loss
- Learning rate
- Reconstructions & visualizations to monitor model progress
- Config files & training logs for reproducibility
- Other problem specific stuff

You can decide for yourself what you want to track and when (per step, per epoch), it never hurts to track more things!  
Give the training loop a go to see what happens:

```
python pytorch_train.py
```

### Validating My Architecture

---

The problem I needed to solve was a geospatial one. This means that my model needs to be capable of understanding multiple dimensions:  
variables (channels), height (latitude), width (longitude) and time (month).

Before I moved on to experimenting with my big geospatial dataset, I checked if my model was able to train on local hardware (and a single GPU).  
I validated my model architecture on the following datasets:

- A Dummy Dataset (randomly initialized tensors with the correct shapes): to see if the model worked with input as expected. The training signal itself does not tell you much, but it sets up the pipeline correctly.
- CIFAR-10: While CIFAR-10 isn't my actual problem, it served as a good check for my problem as the dataset has height and width dimensions, 3 variable dimensions (RGB) and a "time" dimension (time = 1 always, but it works with the model architecture)
- A small subset of my "big" geospatial dataset.

---

Once my model was working, validated and tracking was set up, it was time to dive into how to make it efficient and suitable for [larger scale training with multiple GPUs](1.%20Multi-GPU%20training.md)
