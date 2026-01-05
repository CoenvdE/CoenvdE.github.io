---
layout: blog_collection
title: "What Is Next"
description: "Chapter 6 of the Training at Larger Scale series"
date: 2025-12-11
collection_id: training-at-larger-scale
chapter_number: 6
toc: true
categories: [Training, ML, GPU]
giscus_comments: true
---

## What's Next?

The last part before we get to the training.
Here I'll cover my last tips and tricks, one more failsafe and some final experiments to run before we get to the training.

```
6. What Is Next/
├── config/
│   └── cli_config.yaml
├── src/
│   ├── callbacks.py
│   ├── data/
│   └── model/
├── lightning_trainer.py
└── lightning_train.py
```

### Experiment First, Train Later

Before jumping into full-scale training, it's important to run some experiments first (e.g. how big should a patch be? What would be a good optimizer configuration starting point?). The idea is not to test this on the full training run, but test it for e.g. 200 (instead of 3000) epochs, and observe the loss curves over epochs.

- Select a baseline configuration
- Observe the loss curves and training speed
- Run small-scale experiments to test different settings
- Compare outcomes to identify the best setup

This approach helps avoid wasting compute and accelerates convergence.

### Failsafe: uploading to the cloud intermittently

If you are training for a longer time, it's a good idea to upload to the cloud intermittently.
Training pipelines sometimes crash due to various reasons, and it's always good to have a failsafe.
For this reason I have uploaded a `CloudUploadCallback` in [callbacks.py](https://github.com/CoenvdE/Training-at-larger-scale-blog/blob/main/6.%20What%20Is%20Next/src/callbacks.py).
This callback uploads the model checkpoints to the cloud storage at specified intervals and/or when the training is finished.

You can add this callback to your training loop by adding the following to your [`cli_config.yaml`](https://github.com/CoenvdE/Training-at-larger-scale-blog/blob/main/6.%20What%20Is%20Next/config/cli_config.yaml) file:

```yaml
callbacks:
  - class_path: src.callbacks.CloudUploadCallback
    init_args:
      local_dir: output/test/checkpoints
      cloud_storage_path: s3://your-bucket/autoencoder-checkpoints
      upload_interval: 10
      upload_during_training: true
      upload_on_fit_end: true
      filesystem: s3
```

### Docker — And Why It's Nice

Docker lets you **containerize** your environment, making sure your code runs the same everywhere—on your laptop or in the cloud.  
Why it's nice:

- Reproducible setups across different machines or cloud providers (Digital Ocean, AWS, etc.)
- Lightweight & portable
- Dependency management
- Easy to test in isolated environments

This personally helped me a lot as switching between different machines and cloud providers went almost seamless.
Get started with docker with this [guide](https://dev.to/docker/getting-started-with-docker-for-aiml-a-beginners-guide-4k6j), watch some videos and discuss with a nice LLM.

---

### Precision in Training (in PyTorch Lightning)

Choosing the right precision can significantly impact training **speed** and **efficiency**, without sacrificing performance—if used correctly.
I changed from `float32` to `16-mixed` and saw a 2x speedup. If your gpu also supports `bf16-mixed`, use that. It is more stable.

Why it's nice:

- Less memory usage
- Faster training
- Bigger batch sizes

you can change this by adding the following to your [`cli_config.yaml`](https://github.com/CoenvdE/Training-at-larger-scale-blog/blob/main/6.%20What%20Is%20Next/config/cli_config.yaml) file:

```yaml
precision: 16-mixed # Precision parameter added, default is 32-true (float32)
```

Additional information can be found in the [Lightning documentation](https://pytorch-lightning.readthedocs.io/en/1.5.10/guides/speed.html).

## Step-Based Training

When working with large-scale datasets, the concept of an "epoch" becomes less relevant, as you may only complete 2 or 3 full passes during the entire training process. In these cases, step-based training is the standard. It provides more granular control over logging, checkpointing, and learning rate updates.

To switch to step-based training in PyTorch Lightning, update your cli_config.yaml:

```YAML
trainer:
  max_steps: 100000          # Train for a fixed number of iterations
  val_check_interval: 1000   # Run validation every 1000 steps
  log_every_n_steps: 50      # Frequent logging for better visibility
```

Note: Ensure you disable epoch-based settings (like max_epochs) to prevent the trainer from stopping prematurely or do extra validation iterations.
Also make sure you configure your learning rate scheduler based on steps instead of epochs.

## Learning Rate Schedulers

When experimenting, use a flat learning rate (e.g. 1e-4). Only change to a schedulers when you are confident in the model architecture.

The Standard: Cosine Annealing with WarmupFor large-scale runs (e.g., 100k steps), a standard curve involves a short warmup phase (e.g., 3k steps) where the learning rate increases linearly, followed by a cosine decay that reduces the rate by $10\times$ or $100\times$. This prevents the model from diverging early on while ensuring it settles into a sharp local minimum at the end.

Tip: Use Cosine annealing with warm restarts.

1. **Escapes local minima**: The periodic "restarts" help the model escape poor local minima by temporarily increasing the learning rate.
2. **Faster convergence**: The cyclical learning rate schedule often leads to faster convergence than linear or step decay schedules.

I experienced a very stable training process with this. (It was recommended to me by someone from the Allan turing institute) and other foundational model builders used it in their training as well. It is recommended to set the restart frequency to a value that is around 2-3 times the number of epochs it takes for the loss to be at the same level as just before the restart. This way the model learns stable and is able to escape local minima.
As a general strategy, it typically performs better than fixed or step decay schedules with minimal tuning.

```python
torch.optim.lr_scheduler.CosineAnnealingWarmRestarts
```

---

### Environment Variables — And Why They're Nice

Env vars help you **manage secrets and config** without hardcoding.  
Why it's nice:

- Store keys/passwords securely
- Change behavior across environments (dev, prod, test)
- Fast configuration without changing code

Here's a simple `.env example` file example:

```
# Cloud storage credentials
CLOUD_STORAGE_KEY=your_secret_key_here
CLOUD_STORAGE_BUCKET=training-data-bucket

# Experiment tracking
WANDB_API_KEY=your_wandb_key_here
EXPERIMENT_NAME=transformer_v2
```

**Important**: Never commit your `.env`file to your repository. It often contains sensitive information like API keys and credentials. Instead:

1. Add `.env` to your [`.gitignore`](https://github.com/CoenvdE/Training-at-larger-scale-blog/blob/main/6.%20What%20Is%20Next/config/.gitignore)
2. Provide a `.env example` template with dummy values in the repo
3. Document the required environment variables in your README
4. For cloud deployments, use the platform's secrets management (AWS Secrets Manager, GitHub Secrets, etc.)

This approach keeps your secrets secure while making configuration straightforward for team members.

---

Thank you for reading!

I hope this guide was helpful. If you have any questions or feedback, feel very welcome to [contact](https://www.linkedin.com/in/coen-van-den-elsen/) me.
