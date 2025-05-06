---
layout: blog_collection
title: "Multi-GPU training"
description: "Chapter 2 of the Training at Larger Scale series"
date: 2025-04-07
collection_id: training-at-larger-scale
chapter_number: 2
toc: true
categories: [Training, ML, GPU]
giscus_comments: true
---

## 1. Single- to Multi-GPU training

Multi-GPU training provides accelerated computing power, meaning faster training once setup correctly. This is necessary when having bigger datasets and larger models.

```
1. Multi-GPU training/
├── config/
│   ├── config.yaml
│   └── cli_config.yaml
├── output/
├── src/
│   ├── data/
│   │   ├── __pycache__/
│   │   ├── lightning_datamodule.py
│   │   └── pytorch_dataset.py
│   └── model/
│       ├── __pycache__/
│       ├── lightning_module.py
│       ├── pytorch_model.py
│       ├── pytorch_encoder.py
│       └── pytorch_decoder.py
├── tests/
│   ├── __pycache__/
│   └── test_lightning_parameters.py
├── __pycache__/
├── lightning_train.py
├── lightning_trainer.py
└── requirements.txt
```

By default, pytorch deep learning models only utilize a single GPU for training, even if multiple GPUs are available. This ofcourse is not what we want. Multi-GPU training setup for pytorch itself can be quite a pain, which is why we are going to use (Pytorch) Lightning. This is very useful and saves you a lot of work down the line (not just multi GPU stuff), you'll see.

TODO: image and source/text format nicely
![Idle GPU Utilization](/images/training-blog/idle_gpu.webp) *When your expensive GPUs sit idle while only one is working, you're wasting resources and time.*
SOURCE: https://blog.dailydoseofds.com/p/4-strategies-for-multi-gpu-training

### Strategies
---
When we have multiple GPU's there are a few strategies that can be used to train models.
I will list a few below:

**(Distributed) Data parralel**

Replicate the model across all GPUs. Divide the input data into smaller subsets, and assign each subset to a different GPU.
NOTE: the data is only shuffled within the subset, not across the subsets. (all is Multi-process)
Each GPU processes its batch independently by running a forward and backward pass using its own model replica.
After the backward pass, the gradients from all GPUs are synchronized and averaged.
These averaged gradients are then used to update the model parameters consistently across all replicas.
This strategy is commonly used because it's relatively straightforward and scales well across multiple GPUs.

<div align="center">
  <img src="/images/training-blog/data_parallel.webp" alt="Data Parallel Training" width="400">
  <img src="/images/training-blog/data_parallel_2.png" alt="Data Parallel Training" width="400">
  <p><em>Data Parallel training splits the data across GPUs, with each GPU processing a different batch of data.</em></p>
</div>

<div align="right">
  <small>Source: <a href="https://blog.dailydoseofds.com/p/4-strategies-for-multi-gpu-training">Daily Dose of Data Science</a></small>
</div>

**Model parralel**

In model parallelism, different parts of the model are placed on different GPUs. For example, GPU 0 might hold the encoder, while GPU 1 holds the decoder.
	•	Primarily used when the model is too large to fit into the memory of a single GPU (typically models with billions of parameters).
	•	Unlike data parallelism, where each GPU has a full model replica, here each GPU holds only a portion of the model.
	•	Training requires data (activations) to flow between GPUs during forward and backward passes, introducing potential communication bottlenecks.

This strategy is more complex to implement and debug and is usually reserved for advanced scenarios like training large-scale transformers (e.g., GPT-style models). Not typically needed for standard model training — not recommended for now unless working with extremely large architectures.

NOTE: INCORPORATE? You may also encounter "sharded model parallelism" (or pipeline parallelism), which are more scalable versions used in massive model training setups.

<div align="center">
  <img src="/images/training-blog/model_parallel.webp" alt="Model Parallel Training" width="400">
  <p><em>Model Parallel training splits the model across GPUs, with each GPU handling different layers of the network.</em></p>
</div>

<div align="right">
  <small>Source: <a href="https://blog.dailydoseofds.com/p/4-strategies-for-multi-gpu-training">Daily Dose of Data Science</a></small>
</div>

**pipeline parralel**

This is often considered a combination of data parallelism and model parallelism.  
Not typically needed for standard model training — not recommended for now unless working with extremely large architectures.

<div align="center">
  <img src="/images/training-blog/pipeline_parallel.webp" alt="Pipeline Parallel Training" width="400">
  <p><em>Pipeline Parallel training processes data in stages across GPUs, similar to an assembly line.</em></p>
</div>

<div align="right">
  <small>Source: <a href="https://blog.dailydoseofds.com/p/4-strategies-for-multi-gpu-training">Daily Dose of Data Science</a>, <a href="https://www.dailydoseofds.com/a-beginner-friendly-guide-to-multi-gpu-model-training/">A Beginner-Friendly Guide to Multi-GPU Model Training</a></small>
</div>

### (Pytorch) Lightning
---
In short: (Pytorch) Lightning is a wrapper around pytorch that can automatically handle multi-gpu communication along with a lot more nice stuff. The key benefit is that Lightning handles all the complexity while still allowing you to customize any part if needed. You get production-ready features without writing boilerplate code, and your code remains clean and focused on the model architecture and training logic. I deeply encourage you to start using this as it will save you a lot of time and effort down the line (At the end of this chapter, I'll state the advantages of this Lightning so you understand why it is so nice),
 I will now walk you through how to use lightning:

**How to go from pytorch to (pytorch) lightning**

This is actually quite easy. Note that earlier I named all of my components files `pytorch_*.py`. This was chosen deliberately, because now I can show you that you just have to add some `lightning_*.py` files to make full use of lightning's benefits. Examples of these can be found in the `src` folder.

***model/lightning_module.py***
- NOTE: the class AutoencoderModule(L.LightningModule) inherits from the L.LightningModule
- self.save_hyperparameters() saves all the init arguments as hyperparameters
- imports your (custom) model
- logs everything automatically with self.log
- wraps all of this nicely for Lightning use. 
- Lightning needs the following functions implemented here:
  - forward()
  - training_step()
  - validation_step()
  -  configure_optimizers()

***data/lightning_datamodule.py***
- NOTE: the class DummyDataModule(L.LightningDataModule) inherits from the L.LightningDatamodule
- self.save_hyperparameters() saves all the init arguments as hyperparameters
- imports your (custom) Dataset
- creates Dataloader objects
- wraps all of this nicely for Lightning use. 
- Lightning needs the following things:
    - setup()
    - train_loader()
    - val_loader()
    - test_loader()

***lightning_train.py***
- NOTE: look how much less code this is! pytorch_train.py had almost 200 lines of code, we now have 74.
- go through the code and see how everything is initiated. 
- especially important here is the L.trainer() with the following parameters that make multi-GPU implementation super easy
    - **accelerator**: Specifies the hardware to use (e.g. "auto", "gpu", "cpu", "tpu"). It directs Lightning to use the appropriate backend for accelerated computing. 
    - **device**: Indicates which (or the number) device(s) to run on. For example, it could be an integer (like 1 or 4) or a specific device string (e.g., "cuda:0") or "auto" to choose one or multiple GPUs. If you have 8 GPU's, use 8.
    - **strategy**: Defines the parallelization approach. Options include "dp" (data parallel), "ddp" (distributed data parallel), "auto", among others, which determine how training is distributed across GPUs.

```
python -m unittest tests/test_lightning_parameters.py
```
```
python lightning_train.py
```

***lightning_trainer.py***
- NOTE: even less code and a CLI (very useful because now you can use the --help flag to see everything that can be initiated and how)
- go through the code and see how everything is initiated. It is important to note that CLI requires a specific format for the `config.yaml` (example in `cli_config.yaml`) with specific config sections:
  - model 
  - data 
  - trainer 
  - TODO OPTIMIZER SCHEDULER????
 
Run the following commands to see the benefits: (note that you can switch between fit, validate, test, predict)

```
python -m lightning_trainer --help
```

```
python -m lightning_trainer fit --help
```

```
python -m lightning_trainer fit -c config/cli_config.yaml
```

NOTE: more reading and how to use it in: [Lightning CLI Documentation](https://lightning.ai/docs/pytorch/2.1.0/cli/lightning_cli.html)

### Managing Multiple Processes in Distributed Training
---
When transitioning from single-GPU to multi-GPU training, you need to carefully consider how processes interact with shared resources. This is a critical aspect that can cause subtle bugs if not handled properly.

#### Single Process vs. Multiple Processes

**Single-GPU Training:**
- One main process controls everything
- This process manages the GPU, spawns dataloader workers
- Handles all file operations (downloads, checkpoints, logs)

**Multi-GPU Training:**
- Multiple processes are spawned (one per GPU)
- Initially, all processes think they're the "main" process
- No hierarchy exists until PyTorch Lightning initializes it
- Multiple processes might try to access the same files or resources simultaneously, causing conflicts or corrupted data

### Handling Common Operations
---

### Handling File Downloads in Distributed Training

When training with multiple GPUs, proper coordination of file operations is critical. Here's how to implement distributed file downloads correctly:
- Only main process (rank 0) downloads data
- `dist.barrier()` synchronizes all processes (meaning the other processes have to wait before the main process finishes)
- Works in both distributed and non-distributed setups
- Prevents file corruption and redundant downloads

#### Example Implementation

```python
def is_main_process():
    """Check if the current process is the main process."""
    return not dist.is_available() or not dist.is_initialized() or dist.get_rank() == 0

def download_dummy_data():
    """Download the dummy data, only on the main process."""
    should_download = is_main_process()
    
    if should_download:
        # Only process with rank 0 performs the download
        print("Main process downloading data...")
        # Actual download code here
    
    # Synchronization point - all processes must wait here 
    # Until the main process has finished downloading.
    if dist.is_available() and dist.is_initialized():
        dist.barrier()
        
```
This is also implemented in `pytorch_dataset.py`

### Handling File Uploads in Distributed Training

When training is complete, uploading checkpoints and logs requires similar coordination to prevent conflicts. Here's how to implement distributed file uploads correctly:
- Single Process Uploads: Only rank 0 process handles uploads
- Prevents Conflicts: Eliminates race conditions and redundant operations
- Efficient: Reduces network traffic and ensures clean termination
- No need for other processes to wait, they can terminate.

#### Example Implementation

```python
def is_main_process():
    """Check if the current process is the main process."""
    return not dist.is_available() or not dist.is_initialized() or dist.get_rank() == 0

def upload_checkpoints_to_cloud(checkpoint_dir, log_dir):
    """Upload checkpoints and logs to cloud storage, only from the main process."""
    # Only process with rank 0 performs the upload
    if is_main_process():
        # Upload files
        
        print("Upload complete!")
```
This is also implemented in `lightning_trainer.py` and `lightning_train.py`


**reproducibility**

When using PyTorch Lightning's `seed_everything()`, it's important to note that by default, the seed is (as far as I have tested) not automatically propagated to worker processes or DataLoader generators. This can lead to unexpected behavior, especially in multi-GPU training scenarios. Setting `workers=True` in `seed_everything()` ensures the seed is properly propagated to worker processes, but you still need to explicitly set seeds for DataLoader generators. As far as I have tested (please correct me if I am wrong), in the CLI config you cannot specify workers=True, which is why I also made a custom worker_init_fn as an example. All of this can be seen in `1. Multi-GPU training/src/data/lightning_datamodule.py`. It ensures reproducibility across all components of your training pipeline, including data loading and augmentation steps that happen in worker processes.

**Monitoring Multi-GPU Training**

When training with multiple GPUs, it's essential to verify that the learning behavior matches expectations. Here's how to effectively monitor multi-GPU training:

1. **Use a Logging Framework**: Tools like Weights & Biases (WandB), TensorBoard, or MLflow provide visualizations of training metrics across runs.

2. **Run Controlled Experiments**: Compare identical configurations between single-GPU and multi-GPU runs for a fixed number of epochs to identify any discrepancies.

3. **Hardware Configuration Verification**: My implementation includes a configuration check in `1. Multi-GPU training/lightning_trainer.py` that prints the actual hardware setup being used:
   ```python
   print(f"\nTraining Configuration Check:")
   print(f"- Accelerator: {trainer.accelerator}")
   print(f"- Devices: {trainer.device_ids}")
   print(f"- Strategy: {trainer.strategy}\n")
   ```

**Common Causes of Performance Differences**

When comparing single-GPU to multi-GPU training, several factors can cause differences in results:

1. **Effective Batch Size**: In data parallel training, the batch size is effectively multiplied by the number of GPUs. With 4 GPUs and a batch size of 32, your effective batch size becomes 128, which affects:

   - **Learning Rate Scaling**: You typically need to scale the learning rate linearly with the batch size (the "linear scaling rule"). For example, when moving from 1 to 4 GPUs, consider increasing your learning rate by 4x.
   
   - **Batch Normalization Statistics**: Larger effective batch sizes produce different batch statistics, affecting model convergence.

2. **Learning Rate Schedulers**: With fewer steps per epoch in multi-GPU training, schedulers need adjustment:
   - Recalculate `total_steps` for step-based schedulers
   - Consider epoch-based schedulers for more consistent behavior
   - Adjust warmup periods proportionally to the effective batch size

3. **Gradient Synchronization**: Different synchronization strategies can affect weight updates and convergence patterns.

4. **Hardware Configuration**: Always explicitly set `strategy`, `accelerator`, and `devices` parameters rather than relying on "auto" settings to ensure consistent behavior across environments.

```
python lightning_train.py
```

Great! now we can train with multiple GPUs, let's tackle working with [bigger data in the cloud](/blogs/training-at-larger-scale/part3/)

### Appendix: Overview of advantages of Lightning over Raw PyTorch 
---

**1. Automatic Device/GPU Handling**
- **PyTorch**: You need to manually handle device placement with `.to(device)` and manage multi-GPU training yourself
- **Lightning**: Just specify `accelerator="auto"` and `devices="auto"` and Lightning handles:
  - Single GPU training
  - Multi-GPU training (automatically using DistributedDataParallel)
  - TPU support
  - CPU fallback

**2. Training Loop Abstractions**
- **PyTorch**: Manual implementation of:
  - Train/eval mode switching
  - Gradient zeroing
  - Loss calculation
  - Backward passes
  - Optimizer steps
- **Lightning**: All handled automatically in the `training_step` and `validation_step`

**3. Built-in Logging**
- **PyTorch**: Manual print statements or custom logging implementation
- **Lightning**: Built-in support for:
  - TensorBoard
  - WandB
  - MLflow
  - Automatic metric aggregation
  - Progress bars

**4. Callbacks System**
- **PyTorch**: Need to implement everything manually
- **Lightning**: Built-in callbacks for:
  - Model checkpointing
  - Early stopping
  - Learning rate monitoring

**5. Multi-GPU Strategies**
- **PyTorch**: Manual implementation of:
  - Data parallelism
  - Distributed training
  - Gradient synchronization
- **Lightning**: Just specify the strategy parameter in the Trainer

**6. Profiling and Debugging**
- **PyTorch**: Manual profiling setup
- **Lightning**: Built-in profilers and debugging tools

**7. Reproducibility**
- **PyTorch**: Manual seed setting everywhere
- **Lightning**: Global seed management with `seed_everything()` 
  - This does not work for the dataloader (and workers), you need to manually set the seed for the dataloader generator (and workers)

**8. Mixed Precision Training** 
- **PyTorch**: Manual AMP (Automatic Mixed Precision) implementation
- **Lightning**: Just add `precision="16-mixed"` to Trainer

**9. Automatic Sanity Checks**
- **PyTorch**: No built-in validation before training
- **Lightning**: Performs sanity validation batch before training to catch errors early
  - Validates model forward pass
  - Checks shape compatibility
  - Verifies loss calculation
  - Can be disabled with `num_sanity_val_steps=0` if needed