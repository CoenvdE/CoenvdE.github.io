---
layout: blog_collection
title: "The Setup"
description: "Chapter 1 of the Training at Larger Scale series"
date: 2025-04-09
collection_id: training-at-larger-scale
chapter_number: 1
toc: true
categories: [Training, ML, GPU]
giscus_comments: true
---

## 0. Setup

Before diving into optimizations, I will walk you through some best practices and a baseline to give you a solid starting point. Note that my model and pipeline were actually a lot more complicated, but my goal is not how to recreate my complicated pipeline, it is to show you simple examples for you to optimize and improve your own.

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

My model is a (Masked) Autoencoder (with some cool stuff that does not matter for this guide) and has the following key components:

- [`pytorch_encoder`](https://github.com/CoenvdE/Training-at-larger-scale-blog/blob/main/0.%20The%20Setup/src/model/pytorch_encoder.py)
- [`pytorch_decoder`](https://github.com/CoenvdE/Training-at-larger-scale-blog/blob/main/0.%20The%20Setup/src/model/pytorch_decoder.py)
- [`pytorch_model`](https://github.com/CoenvdE/Training-at-larger-scale-blog/blob/main/0.%20The%20Setup/src/model/pytorch_model.py) – responsible for the forward pass and loss calculation

### My Dataset

---

- a [`pytorch_dataset`](https://github.com/CoenvdE/Training-at-larger-scale-blog/blob/main/0.%20The%20Setup/src/data/pytorch_dataset.py)
  I use a big, geospatial dataset for my training. For this tutorial, I created a dummy example, but feel free to swap it out for e.g. [CIFAR](https://www.cs.toronto.edu/~kriz/cifar.html) or any other dataset you like. It is important that this is wrapped into a `torch.utils.data.Dataset` object.  
  We will come back to data in more detail in [Chapter 2](/blogs/training-at-larger-scale/part3/).

### Reproducibility

---

Reproducibility is very important! It allows you and others to reliably verify and compare results. In research, it ensures findings are valid and consistent. For practitioners, it makes debugging and iterative experimentation much easier. Seeding is one of the prerequisites for reproducibility. It ensures consistent pseudo random number generation. Different frameworks may use different generators.
You need to seed everything (torch, numpy, python, etc.). See the `set_seed()` function in [pytorch_train.py](https://github.com/CoenvdE/Training-at-larger-scale-blog/blob/main/0.%20The%20Setup/pytorch_train.py) for an example implementation.

```python
def set_seed(seed: int = 13):
    """Set all seeds for reproducibility."""
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)
    random.seed(seed)
```

Note that I use a `set_seed` function to keep everything reproducible in the `pytorch_train.py` file. By default, this seed does _not_ propagate to the Dataloader. This is why I create a `generator` for the data loader that has a set seed, for which I use the seed from the `set_seed` function.
Pytorch dataloader workers need to be seeded, because each worker runs in its own process. Without explicit seeding, they will use random seeds, leading to **non-deterministic data loading and augmentations**. Look at the `worker_init_fn` in the `pytorch_train.py` file for an example.

For **reproducibility during debugging and testing**, set the following:

```python
torch.backends.cudnn.deterministic = True  # Default: False
torch.backends.cudnn.benchmark = False     # Default: True
```

These flags control CUDA kernel selection and execution:

- `deterministic = True`: Ensures consistent results across training runs, though this may impact training speed
- `benchmark = False`: Disables CuDNN's auto-tuner that normally selects optimal convolution algorithms. While auto-tuning can improve performance, it may introduce non-deterministic behavior, particularly with varying input sizes

When both flags are set, you get consistent, reproducible behavior across all training runs.

### Config files

---

I use config files for the model, dataloader, training, optimizer, and scheduler arguments. This is best practice, allowing quick adjustments to hyperparameters without modifying the code. This makes experimentation and testing more efficient.  
An example of a config file with a few of these parameters is given in this [config.yaml](https://github.com/CoenvdE/Training-at-larger-scale-blog/blob/main/0.%20The%20Setup/config/config.yaml)

### Unittests

---

Before moving forward, ensure your model actually works. It is important to write tests that check:

- Proper parameter loading from config file
- Shape consistency
- Correct device allocation

This first one is very important and can save you a lot of trouble debugging, I made an example test for this in my [`.tests` folder](https://github.com/CoenvdE/Training-at-larger-scale-blog/blob/main/0.%20The%20Setup/tests/test_parameters.py)

```bash
uv run python -m unittest tests/test_parameters.py
```

Additionally, I set up automated testing — every push to the GitHub branch runs these tests.  
For this, look at the [`.github/workflows/test.yml`](https://github.com/CoenvdE/Training-at-larger-scale-blog/blob/main/0.%20The%20Setup/.github/workflows/test.yml) file. While unit tests don't catch everything, they help ensure the code runs smoothly (in the cloud) and prevent accidental breakage. Automatically running them via GitHub gives you good feedback on if you break anything! This can potentially save you a lot of time and money, since it reduces the likelihood of a situation where you spin up a large GPU cluster for model training and then have to spend an hour or more fixing bugs that you failed to catch before.

### Tracking & Experiment Logging (WandB)

---

Proper tracking is essential for monitoring model performance and debugging issues.  
I use Weights & Biases (WandB), but alternatives like MLflow also work.

What to track?

- Validation loss & training loss
- Learning rate
- Reconstructions & visualizations to monitor model progress
- Config files & training logs for reproducibility

You can decide for yourself what you want to track and when (per step, per epoch), it never hurts to track more things!  
Give the training loop a go to see what happens:

```bash
uv run python pytorch_train.py
```

### Validating Your Model Architecture

---

Validating your model architecture early prevents costly debugging later in training—especially when working with large or domain-specific datasets. These problems often involve unique data formats and multi-dimensional inputs that don't fit a model architecture out of the box. Skipping this step can lead to wasted time and compute on models that silently fail to learn. These validation steps are unique for each problem, but the general idea is to validate the model on a smaller dataset that are representative of the full dataset.

Example: the problem I need to solve is a geospatial one, meaning my model had to handle multiple dimensions (channels, height, width, time). Before experimenting with my full geospatial dataset, I verified that the model could train properly on local hardware (and a single GPU). I validated the architecture using the following datasets:

- **Dummy Dataset**: Randomly initialized tensors with the correct shape. This confirmed the model accepted input as expected and helped verify the pipeline was structurally sound.
- **CIFAR-10**: Although not geospatial, CIFAR-10 contains spatial dimensions (height and width), 3 variable channels (RGB), and can simulate a time dimension (e.g. `time=1`). This made it a useful proxy for early validation.
- **Subset of the geospatial dataset**: A small slice of the real dataset ensured the model worked with actual data formats and domain-specific characteristics.

This step ensured my architecture was robust, flexible, and ready for large-scale training.

---

### Environmental Impact Monitoring

AI models consume significant computational resources and energy. Monitoring environmental impact helps quantify your carbon footprint, which is important for sustainability and responsible AI development. For this reason I made a [monitoring script](https://github.com/CoenvdE/Training-at-larger-scale-blog/blob/main/0.%20The%20Setup/monitor_training.py) to monitor the emissions of any training run. You do not need to modify anything in your training script, just run my script with your training command as shown below. My script is based on the [codecarbon](https://github.com/mlco2/codecarbon) package. You may need to fill in the password of your machine to give codecarbon access to monitoring your hardware.

```bash
# Run your training with emissions monitoring
python monitor_training.py "python pytorch_train.py"
```

For each run, the script creates a dedicated folder with:

- A timestamped log file capturing all training output
- Carbon emissions data in CSV format (detailed breakdown of emissions by component)
- Visualizations showing emissions and energy breakdown by component (CPU/GPU/RAM)
- A summary report with key metrics

---

Now that the model is working, validated and tracking was set up, it is time to dive into how to make it efficient and suitable for [larger scale training with multiple GPUs](/blogs/training-at-larger-scale/part2/). Before proceeding to the actual training, it's crucial to set up proper fail safes. Training for multiple days without these safeguards can lead to catastrophic failures, wasted resources, and lost progress. Next to the ones we already set up, I'll cover some extra ones in the next chapters.
