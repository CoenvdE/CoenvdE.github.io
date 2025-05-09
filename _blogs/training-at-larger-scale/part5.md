---
layout: blog_collection
title: "Optimizing the pipeline: Model"
description: "Chapter 5 of the Training at Larger Scale series"
date: 2025-04-13
collection_id: training-at-larger-scale
chapter_number: 5
toc: true
categories: [Training, ML, GPU]
giscus_comments: true
---

## 4. Optimizing the pipeline: Model

After optimizing the data pipeline, the next step is profiling the model pipeline to catch bottlenecks like slow ops or CPU–GPU data transfers.
This is an optional step that, if the code is implemented correctly, will probably not have a big impact on the training time.
If you don't want to do it, you can skip this section and look at the [next chapter](/blogs/training-at-larger-scale/part6/).
Note that I give a few nice tools to help you analyse the model pipeline performance. I do suggest you to run the benchmark (and a pytorch profiler) and let ChatGPT or another good LLM analyse the results for you and help you figure out if you need to change something. This part is mainly about getting the time it takes for a batch to pass through your model pipeline down.

The time it takes for a batch to pass through your model depends on several factors:

- **Batch size**: Larger batch sizes generally increase the duration of a single training step because more data is processed simultaneously. Operations like a dot product scale linearly with the batch size, so the duration of a single training step increases with the batch size. However, the relationship isn't always linear - GPUs can achieve higher utilization with larger batches, potentially making the per-sample processing time lower.
- **Model complexity**: More complex models (deeper, wider networks) take longer to process each batch.

- **Hardware**: The specs of your GPU/TPU significantly impact processing time.

In my experiments, a single training step took around 0.4 seconds for moderate-sized models with a batch size of 32. This can vary widely - from milliseconds for small models to several seconds for larger architectures. I have seen 0.1 seconds as well with other models. For my model, the time it took to complete 1 step scaled around linearly with the batch size, which makes sense given that most operations scale linearly with the batch size (e.g. a dot product).

```
4. Optimizing the pipeline: Model/
├── profiler.py
├── timing_benchmark.py
├── config/
│   ├── cli_config.yaml
├── src/
│   ├── data/
│   │   ├── lightning_datamodule.py
│   │   └── pytorch_dataset.py
│   └── model/
│       ├── lightning_module.py
│       ├── pytorch_decoder.py
│       ├── pytorch_encoder.py
│       └── pytorch_model.py
├── tests/
│   └── test_lightning_parameters.py
└── output/
```

### [Easy timing benchmark](/blogs/training-at-larger-scale/part5/)

This is a tool I made to benchmark a pipeline. It is designed to work with **any** PyTorch Lightning model module and data module, so you can also use it to benchmark your own model pipeline. It measures detailed timing information for each step of the training process:

- Data loading time
- Forward pass time
- Backward pass time
- Other ops: everything that happens after the backward pass but before the end of the batch. This primarily includes:
  - The optimizer step (applying gradients to update model weights)
  - Scaler updates (when using mixed precision)
  - Any additional overhead between batches

I find the timing summary at the end of the script to be very useful. It gives you a good overview of the time spent in each step of the pipeline.

## Usage

Replace the model and data classes with your own.

```python
# Import your model and data classes here
from src.model.lightning_module import AutoencoderModule as ModelClass
from src.data.lightning_datamodule import DummyDataModule as DataModuleClass

# Default model and data classes to use if not overridden by command line arguments
DEFAULT_MODEL_CLASS = ModelClass
DEFAULT_DATA_CLASS = DataModuleClass
```

```bash
uv run python timing_benchmark.py -c config/config.yaml --epochs 1 --save-dir results/benchmark/my_model
```

### Required Arguments

- `-c, --config`: Path to the YAML configuration file
- `--model-class`: Import path to the model class (e.g., 'src.model.lightning_module.AutoencoderModule')
- `--data-class`: Import path to the data module class (e.g., 'src.data.lightning_datamodule.DummyDataModule')

### Optional Arguments

- `--epochs`: Number of epochs to run (default: 2)
- `--save-dir`: Directory to save results (default: results/benchmark/TIMESTAMP)
- `--precision`: Training precision, choices are "16-mixed", "16", "32" (default: "32")
- `--device`: Device to run on, choices are "cuda", "cpu" (default: auto-detect)

## Output

The benchmark tool will create several files in the specified output directory:

- `timing_summary.yaml`: A YAML file containing detailed timing statistics
- `timing_results.csv`: A CSV file with raw timing data for each batch
- `batch_time_breakdown.png`: A stacked bar chart showing time breakdown per batch
- `total_batch_time.png`: A line plot of total batch time
- `time_distribution_pie.png`: A pie chart of average time distribution
- `benchmark_config.yaml`: A copy of the benchmark configuration

## Tips for Optimization

1. **Data Loading**:

   - If data loading takes >30% of batch time, check the data pipeline and the data loader again.

2. **Forward/Backward Pass**:

   - Try mixed precision training with `--precision 16-mixed` for faster computation (discussed in the [next chapter](/blogs/training-at-larger-scale/part6/))
   - Consider model architecture changes to reduce computation

3. **Optimizer**:
   - Experiment with different optimizers and their settings
   - TODO: This is a big topic in just one bullet point! More detail here? Or a link to more information?

## Analyzing Results

The benchmark results will help you identify bottlenecks in your training pipeline:

- If **data loading** is a big bottleneck, optimize data loading pipeline, increase workers, use caching
- If **forward pass** is a big bottleneck, consider model architecture changes or mixed precision
- If **backward pass** is a big bottleneck, try gradient accumulation or mixed precision

## Profiling: Check Your Pipeline

### What Is It?

Profiling helps you understand where time and resources are spent in your training pipeline. It guides optimization by identifying bottlenecks.
The profiler also looks at the data part of the pipeline, so it is a good idea to run it after the data part is done.

### How Does It Work?

Look at the provided script to profile your training loop. Import your `dataloader` and `model` modules,
then run the script 3 times with the three profilers:

- **Simple Profiler**
- **Advanced Profiler**
- **PyTorch Profiler (Chrome Trace Viewer)**

it stores the output in the `output/profiler/{config_name}/profiler_logs` folder.

```bash
uv run python profiler.py
```

### Interpreting Profiler Outputs – A Quick Guide

Understanding what the profiler outputs mean is key to optimizing your training pipeline.
Here’s what to look for in each profiler and how to make sense of the data.

### 1. `fit-simple_profiler_output.txt` – Summary View (Simple Profiler)

### What It Shows:

- High-level summary of function calls
- Average time per operation
- Relative contribution of each function to total runtime

### How to Read It:

- Look at the top-consuming operations — these are usually bottlenecks.
- Pay attention to data loading functions (`*_dataloader_next`, `__next__`) — these often take more time than expected.
- Training loops like `run_training_epoch` will typically be a large portion; the key is to ensure they're not dwarfed by overheads.

### When to Take Action (example):

- If data loading takes a large share of total time (e.g., >40%), your pipeline is I/O-bound.
- If your model training steps are taking less time than preprocessing, you're likely under-utilizing the GPU.

### 2. `fit-advanced_profiler_output.txt` – Line-Level View

### What It Shows:

- Function-level granularity (per-call stats)
- Total calls, total time, average time per call
- Stack trace to locate the exact code path

### How to Read It:

- Sort by total time and identify high-call-count, low-time ops — these may be optimized or batched.
- Use stack traces to pinpoint performance sinks inside your own code or framework code.
- Investigate setup or utility functions being called excessively (e.g., synthetic data generation, logging, checkpointing).

### When to Take Action (example):

- If any function is causing a lot of time, (where you expect it to be fast) check if it is necessary.

### 3. `pt.trace.json` – Chrome Trace Viewer (PyTorch Profiler)

### What It Shows:

- Frame-by-frame execution timeline
- Operator-level breakdown (CPU and GPU)
- Optional memory usage tracking

### How to Read It:

1. Open Chrome and go to `chrome://tracing`.
2. Drop in the `.json` file.
3. Hover over timeline blocks to see operator names, start/end times, and device usage.

### What to Look For:

- Long horizontal bars → slow operations (usually backward passes, large convolutions)
- Gaps between ops → potential I/O waits or CPU/GPU syncs
- Overlapping CPU/GPU ops → good utilization
- Memory heatmaps (if enabled) → identify peaks or leaks

### When to Take Action (example):

- If any function is causing a lot of time, (where you expect it to be fast) check if it is necessary.
- If idle gaps exist, investigate DataLoader efficiency

## Next Steps

Congratulations on optimizing your entire training pipeline! Explore what's next:

[5. What Is Next](/blogs/training-at-larger-scale/part6/)

Additional information can be found in [PyTorch Lightning: `compile` for speed](https://lightning.ai/docs/pytorch/stable/advanced/compile.html) and [PyTorch Lightning: General speed-up tips](https://lightning.ai/docs/pytorch/stable/advanced/speed.html)
