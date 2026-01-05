---
layout: blog_collection
title: "Optimizing the pipeline: Model"
description: "Chapter 5 of the Training at Larger Scale series"
date: 2025-12-10
collection_id: training-at-larger-scale
chapter_number: 5
toc: true
categories: [Training, ML, GPU]
giscus_comments: true
---

## Optimizing the pipeline: Model

After optimizing the data pipeline, the next step is investigating the model pipeline to catch bottlenecks like slow ops or CPU–GPU data transfers.
This is an optional step that, if the code is implemented correctly, will probably not have a big impact on the training time. For this chapter, I made a tool to help you analyse the model pipeline performance. I do suggest you to run the benchmark script and let ChatGPT or another good LLM analyse the results for you and help you figure out if you need to improve something. This part is mainly about reducing the time it takes for a batch to pass through your model pipeline. If you don't need to do it, you can skip this section and look at the [next chapter](/blogs/training-at-larger-scale/part6/).

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
### Easy timing benchmark

[This](https://github.com/CoenvdE/Training-at-larger-scale-blog/blob/main/5.%20Optimizing%20the%20pipeline%3A%20Model/timing_benchmark.py) is a tool I made to benchmark a pipeline. It is designed to work with **any** PyTorch Lightning model module and data module, so you can also use it to benchmark your own model pipeline. It measures detailed timing information for each step of the training process:
  - Data loading time
  - Forward pass time
  - Backward pass time
  - Other ops: everything that happens after the backward pass but before the end of the batch. This primarily includes:
    - The optimizer step (applying gradients to update model weights)
    - Scaler updates (when using mixed precision)
    - Any additional overhead between batches

I find the timing summary printed at the end of the script particularly useful. It gives you a good overview of the time spent in each step of the pipeline.

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
uv run python timing_benchmark.py -c config/cli_config.yaml
```


### Required Arguments

- `-c, --config`: Path to the YAML configuration file

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

## Analyzing Results

The benchmark results will help you identify bottlenecks in your training pipeline:

- If **data loading** is a big bottleneck, optimize data loading pipeline, increase workers, use caching
- If **forward pass** is a big bottleneck, consider model architecture changes or mixed precision (discussed in the [next chapter](/blogs/training-at-larger-scale/part6/))
- If **backward pass** is a big bottleneck, try gradient accumulation or mixed precision
- If **other ops** are a big bottleneck, experiment with different optimizers. A good starting point is using the AdamW optimizer with hyperparameters from related literature.

If you need to get more detailed information about the model pipeline and where specific bottlenecks are, you can use profiling. I provided a workflow for this in the [appendix](/blogs/training-at-larger-scale/part7/).

Additional information can be found in [PyTorch Lightning: `compile` for speed](https://lightning.ai/docs/pytorch/stable/advanced/compile.html) and [PyTorch Lightning: General speed-up tips](https://lightning.ai/docs/pytorch/stable/advanced/speed.html)

## Next Steps

Before moving on to actual training, I wrote a final chapter on [what is next](/blogs/training-at-larger-scale/part6/). These are some final considerations, tips and tricks that I think are important to consider before actually training your model.
