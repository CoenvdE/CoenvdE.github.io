---
layout: blog_collection
title: "Cloud storage credentials"
description: "Part 6 of the Training at Larger Scale series"
date: 2025-04-11
collection_id: training-at-larger-scale
chapter_number: 6
toc: true
categories: [Training, ML, GPU]
giscus_comments: true
---

## 5. What's Next?

```
5. What Is Next/
├── cli_config.yaml
```

### Docker — And Why It's Nice

Docker lets you **containerize** your environment, making sure your code runs the same everywhere—on your laptop or in the cloud.  
Why it's nice:

- Reproducible setups across different machines or cloud providers (Digital Ocean, AWS, etc.)
- Lightweight & portable
- Easy to test in isolated environments

---

### Precision in Training (in PyTorch Lightning)

TODO: keep here or move to 4. Optimizing the pipeline: Model.md?

Choosing the right precision boosts training **speed** and **efficiency** without sacrificing performance—if used correctly.
Why it's nice:

- Faster training
- Bigger batch sizes
- Less memory usage

see how to add in `config/cli_config.yaml`

- **`precision="32-true"` (default)**

  - Full `float32`
  - Most stable
  - Slowest
  - Max memory use

- **`precision="16-mixed"`**

  - Mixed `float16` ops, `float32` weights
  - Fast, low memory
  - Needs loss scaling
  - Risk of numerical instability

- **`precision="bf16-mixed"`**

  - Mixed `bfloat16` ops
  - Fast and stable
  - No loss scaling
  - Requires A100+ or TPU

- **`precision="16-true"` / `bf16-true`**
  - Full low precision (float16 or bfloat16)
  - Max speed
  - Risky for training
  - Best for inference/fine-tuning
  - Hardware-dependent

### Summary Table

| Precision    | Speed   | Stability | Loss Scaling | Hardware Requirement |
| ------------ | ------- | --------- | ------------ | -------------------- |
| `32-true`    | Slow    | Highest   | No           | None                 |
| `16-mixed`   | Fast    | Medium    | Yes          | Most NVIDIA GPUs     |
| `bf16-mixed` | Fast    | High      | No           | A100+, TPUs          |
| `16-true`    | Fastest | Low       | Risky        | float16 GPUs         |
| `bf16-true`  | Fastest | Medium    | No           | A100, TPUs           |

---

## Learning Rate Schedulers

Tip: (TODO: from personal experience and advice from Andy and other model (clay)): Use cosine annealing with warm restarts:

```python
torch.optim.lr_scheduler.CosineAnnealingWarmRestarts
```

Cosine annealing with warm restarts is effective because it:

1. **Escapes local minima**: The periodic "restarts" help the model escape poor local minima by temporarily increasing the learning rate.
2. **Faster convergence**: The cyclical learning rate schedule often leads to faster convergence than linear or step decay schedules.
3. **Improved generalization**: Research shows this approach often leads to better generalization performance on test data.
4. **Parameter exploration**: The warm restarts enable broader exploration of the parameter space initially, while still allowing fine-tuning later.
5. **Works across domains**: This approach has proven effective across various model architectures and tasks.

As a general strategy, it's hard to beat and typically performs better than fixed or step decay schedules with minimal tuning.

---

### Environment Variables — And Why They're Nice

Env vars help you **manage secrets and config** without hardcoding.  
Why it's nice:

- Store keys/passwords securely
- Change behavior across environments (dev, prod, test)
- Fast configuration without changing code

Here's a simple `.env` file example:

```
# Cloud storage credentials
CLOUD_STORAGE_KEY=your_secret_key_here
CLOUD_STORAGE_BUCKET=training-data-bucket

# Experiment tracking
WANDB_API_KEY=your_wandb_key_here
EXPERIMENT_NAME=transformer_v2
```

**Important**: Never commit your `.env` file to your repository. It often contains sensitive information like API keys and credentials. Instead:

1. Add `.env` to your `.gitignore` file
2. Provide a `.env.example` template with dummy values in the repo
3. Document the required environment variables in your README
4. For cloud deployments, use the platform's secrets management (AWS Secrets Manager, GitHub Secrets, etc.)

This approach keeps your secrets secure while making configuration straightforward for team members.

---

## Pre-training Strategy: Experiment First

Before jumping into full-scale training:

- Select a baseline configuration
- Observe the loss curves over epochs
- Run small-scale experiments to test different settings
- Compare outcomes to identify the best setup

This approach helps avoid wasting compute and accelerates convergence.

TODO: add a picture of the loss curves and explain some examples

## What's After This Guide?

### Faster

- Look into **JAX** for speed and flexibility

### Bigger

- Model parallelism, sharding, and memory optimization techniques like:
  - **Zero Redundancy Optimizer (ZeRO)**  
    [Read more here](https://oracle-oci-ocas.medium.com/zero-redundancy-optimizers-a-method-for-training-machine-learning-models-with-billion-parameter-472e8f4e7a5b)

These are advanced topics — no need to rush. Focus on working with the current tools first.
