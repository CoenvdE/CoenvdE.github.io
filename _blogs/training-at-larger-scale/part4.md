---
layout: blog_collection
title: "Optimizing the pipeline: Data"
description: "Chapter 4 of the Training at Larger Scale series"
date: 2025-04-12
collection_id: training-at-larger-scale
chapter_number: 4
toc: true
categories: [Training, ML, GPU]
giscus_comments: true
---

## 3. Optimizing the pipeline: Data

Efficient data loading can significantly reduce training time — especially when the GPU is fast but starved for data.

- The GPU (or TPU/HPU etc.) is **the most expensive and performance-critical component** in a training pipeline.
- If the data pipeline (i.e., loading, preprocessing, transferring) is slow, the GPU will sit idle, waiting for the next batch.
- The goal is to **saturate the GPU** — keep it busy with minimal idle time.

### What You Want

- A data pipeline **that saturates the GPU as much as possible** without introducing too much memory pressure or over demanding CPUs.
- Each DataLoader worker is effectively a producer that loads data in parallel, while your training loop (running on the main process/GPU) is the consumer. The goal is to maximize overlap: while one batch is being processed on the GPU, the next batch (or several batches) are being loaded by the CPU workers in the background.

```
3. Optimizing the pipeline: Data/
├── benchmark_datapipeline_configurations.py  # Main benchmark script
├── plot_benchmark_runs.ipynb                # Analysis notebook
├── dummydataset.py                          # Dummy dataset for testing
├── utils.py                                 # Utility functions
├── benchmark_logs/                          # Benchmark results
└── benchmark_imgs/                          # Visualizations
```

### Key Concepts and Metrics

---

- **CPU (cores)**:

  - Used by the **main process and workers** to (lazy) load, transform, and prepare data for training.
  - Ideally, you want high CPU usage (to indicate workers are busy) but not so high that the OS or other processes starve. If your CPU utilization is peaking at 100% on all cores and the system becomes unresponsive or the throughput plateaus, you may have too many workers or threads.
  - You can check available CPUs using:

  ```python
  import os
  print(os.cpu_count())
  ```

- **RAM (System Memory / CPU RAM)**:

  - Used by workers to load batches into memory.
  - Important when working with large datasets, large batch sizes, or complex transforms.
  - Too many workers without enough RAM can lead to crashes or swapping, which hurts performance.

- **GPU Saturation**:

  - The key performance target.
  - If GPU is underutilized, bottleneck is likely in data loading.

- **I/O Considerations**

  - **Bandwidth**: The maximum rate of data transfer between components in your system:

    - Disk/cloud storage to RAM
    - CPU memory to GPU memory
    - Network transfers (e.g., from cloud storage to your instance)

    Measured in MB/s or GB/s. High bandwidth allows more data to flow per second, while low bandwidth creates bottlenecks that can leave your GPU waiting for data. When working with cloud data, network bandwidth often becomes the primary constraint. Cloud servers typically have significantly higher bandwidth (often 10-100x faster) than consumer (wifi) internet connections, which can dramatically improve data transfer speeds when training in cloud environments compared to local setups.

  - **Chunking**: Use optimal chunk sizes to balance I/O overhead and memory usage
  - **Optimizations**:
    - Memory mapping for large files
    - Prefetching data to reduce latency
    - Caching frequently used data
    - Sequential access over random reads
    - Compression to reduce I/O
  - **File Formats**: Choose ML-optimized formats (Parquet, TFRecord, WebDataset, Zarr)

**Streaming Workers (Dask) vs DataLoader Workers (PyTorch)**

TODO: add image
PyTorch DataLoader and streaming frameworks like Dask can be combined effectively to stream cloud data into your training pipeline, but it's crucial to understand they operate at different layers of the data process:

- **Dask (or other streaming frameworks)** handles the low-level data access by:

  - Building a computational graph (DAG) for lazy evaluation
  - Managing how data chunks are read from storage
  - Orchestrating parallel fetching of data from cloud/disk
  - Optimizing memory usage through chunking strategies

- **PyTorch DataLoader** manages the training-specific data handling by:
  - Creating worker processes to parallelize sample preparation
  - Implementing batching, shuffling, and sampling strategies
  - Executing the preprocessing defined in your `__getitem__` method
  - Transferring prepared batches to the GPU

These systems don't automatically coordinate with each other. The connection point occurs when a DataLoader worker calls `__getitem__` on your Dataset, which then triggers Dask to materialize the required data chunks when calling a `.load()` function. By understanding this separation, you can optimize each layer independently:

1. Configure optimal data reading (e.g. chunk sizes, thread count, worker count)
2. Configure DataLoader for optimal batch preparation (e.g. num_workers, prefetch_factor)

It's important to avoid conflicting parallelism between these systems because too many concurrent processes and threads can lead to resource contention and degraded performance.

### Practical guidelines, background and setup

---

I have created scripts to help you optimize your data pipeline, but before we dive into the benchmarking and optimization, it is important to understand how everything works.

**Understanding DataLoader Workers and Process Distribution**

When optimizing your data pipeline, it's important to understand how worker processes are distributed across your available CPU cores and to leave sufficient CPU resources for main processes and system overhead.

Reserve 1-2 CPU cores per GPU for the main training process and system overhead. When using containerization solutions like Docker, you may need to reserve additional CPU resources for container management.

- **Single GPU setup**: With a single GPU and one main training process, you'll have a single DataLoader that spawns `num_workers` processes. For example, on a machine with 20 CPU cores and 1 GPU, you should reserve 1-2 cores for the main process and system overhead, leaving about 18 cores for DataLoader workers.

- **Multi-GPU setup**: With multiple GPUs (e.g., using DistributedDataParallel), each GPU has its own main process, and each main process creates its own set of DataLoader workers. For instance, on a machine with 8 GPUs and 160 CPU cores, you should reserve 8-16 cores for main processes and system overhead (1-2 per GPU), leaving approximately 144-152 cores to be distributed among all worker processes.

To avoid CPU contention, ensure the total number of worker processes doesn't exceed your available CPU cores minus the cores needed for main processes and system overhead. When workers compete for CPU resources, data loading becomes inefficient and can slow down training.

**CPU allocation examples**:

- 20 CPUs, 1 GPU: Reserve 2 CPUs for main process and overhead, use up to 18 workers
- 60 CPUs, 3 GPUs: Reserve 6 CPUs (2 per GPU) for main processes and overhead, use up to 18 workers per GPU (54 total)

Again, note that num_workers is not about CPU's but processes, and a process may use more or less than 1 cpu core.

**Set batch size**
The ideal batch size depends on your dataset characteristics, model complexity, and available GPU memory. You want a size that's stable but still provides stochastic gradient descent benefits. For my use case, 32 worked well, but you may need to adjust based on your specific requirements. This batch size is needed because it is used in my optimization benchmark script later.

**Optional: measure time for 1 batch to train**
Measuring the time it takes to (load a mini batch and) complete a single training step. This information is useful for properly configuring the benchmark script parameters to accurately reflect your real-world training conditions. For this, you can run the [`timing_benchmark.py`](https://github.com/CoenvdE/Training-at-larger-scale-blog/blob/main/3.%20Optimizing%20the%20pipeline%3A%20Data/timing_benchmark.py) script that is in the folder of [chapter 4](/blogs/training-at-larger-scale/part5/).

**No need to over-optimize the DataLoader**:
If your model is small or the GPU is not very powerful, there's no point in using 16+ workers or heavy parallel jobs when the GPU is already saturated.
I have spent quite some time doing research on this, and it is important to think about this step as it can drastically increase your performance, but there is no need to do "grid search" such-like stuff for this.
Follow my guide and your speed should already improve a lot. Experimenting endlessly with this also costs money and potential experimentation time. I'll tell you more on how to do it in a sec.

### When optimizing data loading, identify the bottleneck using the [benchmark script](https://github.com/CoenvdE/Training-at-larger-scale-blog/blob/main/3.%20Optimizing%20the%20pipeline%3A%20Data/benchmark_configurations.py) I created. Look for these key indicators:

---

• **GPU Under-utilization**: If your GPU is frequently idle, your data pipeline isn't keeping up. The benchmark will show long waits between training steps and white spaces in the "train row" of the visualization.

• **Single CPU core maxed out**: If one CPU core is at 100% while others are idle (especially with num_workers=0), increase num_workers to distribute the load across multiple cores.

• **All CPU cores busy but GPU still waiting**: This suggests an I/O bottleneck (slow disk, network, etc.). Adding more workers won't help. Instead, optimize at the dataset level with faster storage, caching, or better chunking strategies.

### what can be optimized: **_dataset_**

---

This part is not always needed. If there are no parameters, chunking or file format to be optimized, focus on the dataloader instead. (when streaming from machine's disk memory, ssd or when streaming is all handled automatically). What to optimize:

1. **Efficient Storage Formats**:

Initially, my data was stored in NetCDF files, which are common for scientific data but can be inefficient when working with streaming from cloud storage. The default chunking in these files was not optimized for machine learning, causing unnecessary data to be loaded into memory during training. To address this, I stored everything in [Zarr](https://zarr.readthedocs.io/). Zarr is specifically designed for fast cloud-based data access. I will not include the migration in this blog, as it is out of scope, I just want to show that it is important to think about the data formats used.

2. **Optimal Chunking**:

**_How to calculate (handwavy) how big your chunks should be_**

TODO: LAURENS CALCULATIONS
When migrating to Zarr, I defined chunk sizes ...

3. **Parallelize I/O: Loading Efficiently**

TODO: DOES IT GO IN TO MUCH DETAIL AS WE USE ZARR FOR THIS IN THE END? IS IT USEFUL FOR READERS?

Some libraries, like Dask, can parallelize reading within a dataset, providing their own optimization parameters. However, be careful when combining these with PyTorch DataLoader workers, as this can lead to resource contention and diminishing returns.

When working with lazy-loading/streaming data into GPU memory, there are several parameters you might need to optimize:

1. **Parallel Loading Parameters**:

   - Number of concurrent readers/workers (processes that execute computations)
   - Memory limits per worker (to prevent OOM errors)
   - Thread pool size per worker (for parallel execution within a worker)

2. **Caching Parameters**:
   - Cache size limits (to prevent OOM errors)
   - Cache eviction policies (to prevent OOM errors)
   - Persistent vs. in-memory caching (to prevent OOM errors)

I will explain how to optimize these parameters in a little bit.

**Usecase: Understanding Dask Execution Modes**

Dask offers three execution modes, each with different trade-offs:

1. **Single-Threaded Scheduler**

   - Uses `dask.config.set(scheduler="single-threaded")`
   - All tasks run sequentially in the main thread
   - No parallelism but minimal overhead
   - Useful for debugging or when relying entirely on DataLoader's parallelism
   - In multi-GPU setups, each process runs its own sequential scheduler

2. **Threaded Scheduler**

   - Uses `dask.config.set(scheduler="threads", num_workers=dask_threads)`
   - Tasks run in parallel using a thread pool within a single process
   - Good for I/O-bound operations (like reading data chunks)
   - Moderate parallelism with low overhead
   - In multi-GPU setups, be careful of the total thread count (e.g., 8 processes × 4 threads = 32 threads)

3. **Distributed Cluster**
   - Uses `LocalCluster` and `Client` to create a full Dask cluster
   - Runs multiple worker processes, each with multiple threads
   - Provides process-level parallelism, bypassing Python's GIL
   - Includes a dashboard for monitoring tasks and resource usage
   - Options for per-GPU-process clusters or a single shared cluster
   - Higher overhead but better isolation and monitoring capabilities

For a single GPU with limited CPUs (e.g., 20 cores):

- A threaded scheduler with 4-8 threads is often sufficient
- A small distributed cluster (1-2 workers, 4 threads each) offers better monitoring

For multi-GPU setups (e.g., 8 GPUs with 20 cores):

- Be careful not to oversubscribe your CPU resources
- If each GPU process uses its own Dask cluster, limit to 1 worker with 2 threads per process
- Consider using a single shared Dask cluster for all GPU processes
- Monitor CPU utilization to avoid contention

The key is balancing parallelism against resource constraints. More parallelism isn't always better, especially when resources are shared across multiple GPU processes. Start conservative and scale up while monitoring performance.

4. **Caching and Locality**: For remote data, implement caching strategies to avoid repeatedly downloading the same data. Consistent access patterns help leverage OS-level caching.

If your data pipeline doesn't use these specialized libraries, you can focus solely on DataLoader optimization.

In summary, dataset-level optimization is about making data access as efficient as possible. By storing data smartly (chunked, compressed appropriately, possibly colocated with training if remote), and by only doing minimal necessary work for each access, you ensure that the raw data supply is fast. Once that is in place, DataLoader-level tuning can further amplify the throughput.

For more insights on optimizing cloud data loading, see [Earthmover's guide to cloud-native dataloaders](https://earthmover.io/blog/cloud-native-dataloader/) covering streaming techniques, I/O optimization, and resource balancing.

### what can be optimized: **_dataloader_**

---

The DataLoader is critical for training performance. Key parameters to optimize:

1. **`num_workers`**: Controls parallel data loading subprocesses

   - Too few: GPU waits for data
   - Too many: Resource contention, diminishing returns

2. **`prefetch_factor`**: Batches loaded in advance per worker

   - Default is 2, which works for most cases
   - Adjust based on sample size and memory requirements
   - Total prefetched = `num_workers * prefetch_factor`

3. **`pin_memory`**: Enables faster CPU to GPU transfers

   - Set to `True` when using GPU
   - Creates page-locked memory for direct transfers
   - Slightly increases CPU memory usage

4. **`persistent_workers`**: Keeps workers alive between epochs

   - Reduces worker initialization overhead
   - Useful for large datasets and complex initialization
   - Significantly reduces epoch transition time

5. **`multiprocessing_context`**: Controls worker process spawning
   - Options: 'fork', 'spawn', 'forkserver'
   - Use 'forkserver' (or 'spawn') for better CUDA compatibility
   - Note: for more detail, you can read the pytorch docs [here](https://docs.pytorch.org/docs/stable/notes/multiprocessing.html)

Even with an efficient dataset, proper DataLoader settings are crucial.

### Optimizing: Benchmarking Tools for DataLoader Optimization

I created two files to help you optimize your data pipeline:

1. **[`benchmark_configurations.py`](https://github.com/CoenvdE/Training-at-larger-scale-blog/blob/main/3.%20Optimizing%20the%20pipeline%3A%20Data/benchmark_configurations.py)**

   - suitable for any pytorch Dataset object
   - Runs and logs different DataLoader configurations
   - Measures performance metrics for each configuration
   - Includes Dask integration (commented out by default for those who don't need it)
   - Contains a configurable `train_step_time` parameter (default: 0.1 seconds)
     - This simulates model training time
     - You can set this to match your actual model's training time per batch
     - The goal remains the same: minimize data loading wait times

2. **[`plot_benchmark_runs.ipynb`](https://github.com/CoenvdE/Training-at-larger-scale-blog/blob/main/3.%20Optimizing%20the%20pipeline%3A%20Data/plot_benchmark_runs.ipynb)**
   - Jupyter notebook for visualizing benchmark results
   - Creates charts comparing different configurations
   - Helps identify the optimal setup for your specific hardware

If you're using Dask, you can also leverage the Dask dashboard to monitor:

- Worker memory usage
- CPU utilization
- Task execution
- Resource bottlenecks

### Example Benchmark Results

Below are example benchmark results showing the dramatic difference between an unoptimized baseline configuration and an optimized one:
#TODO: update images so that it shows the 1400 vs 40 seconds

<div align="center">
  <img src="/images/training-blog/benchmark_logs_bad_baseline.png" alt="Unoptimized Baseline"  width="400">
</div>

<div align="center">
  <img src="/images/training-blog/benchmark_logs_good_baseline.png" alt="Optimized Configuration"  width="400">
  <p><em>Unoptimized baseline vs optimized configuration performance after 3 epochs with 50 batches</em></p>
</div>

<div align="right">
  <small>Source: <a href="https://blog.dailydoseofds.com/p/4-strategies-for-multi-gpu-training">Daily Dose of Data Science</a></small>
</div>

With these simple optimizations, my dataloader became 5 times faster than the baseline. The people that made the first version of this benchmark script was able to run 15x faster. This performance improvement is transformative for training - where others might only complete 50 epochs in a given timeframe, I was able to run 250 epochs. This acceleration dramatically reduces overall training time and allows for more experimentation and model iterations.

### Practical Optimization Approach

---

0. **Import your own dataset at the start**

- Follow these steps to systematically optimize your data pipeline:
  change the line on top of [`benchmark_configurations.py`](https://github.com/CoenvdE/Training-at-larger-scale-blog/blob/main/3.%20Optimizing%20the%20pipeline%3A%20Data/benchmark_configurations.py).

```python
from dummydataset import DummyDataset as YourDataset # replace with your dataset
```

1. **Establish a baseline**

   - Start with minimal configuration:
     - `num_workers = 0` (single-process loading)
     - `prefetch_factor = None` (default behavior)
     - `persistent_workers = False`
     - `pin_memory = False`
   - This provides a reference point for measuring improvements

2. **Implement a sensible default configuration**

   - For a system with 10 CPU cores and 1 GPU:
     - Reserve 1-2 cores for the main training process
     - Allocate remaining cores between DataLoader workers and streaming processes
     - Example allocation:
       - 5 cores for Dask streaming workers (if using Dask)
       - 8 cores for DataLoader workers
     - Note: Some CPU oversubscription (e.g., 13 workers on 10 cores) can be beneficial
       - When workers are waiting for I/O operations, they don't use CPU
       - This can increase overall throughput by reducing idle time

3. **Experiment with different configurations**

   - Test variations systematically:
     - More streaming workers, fewer DataLoader workers
     - More DataLoader workers, fewer streaming workers
     - Higher CPU oversubscription
     - Optional: Even higher oversubscription
     - Lower CPU oversubscription
     - Different `prefetch_factor` values

4. **Run benchmarks and analyze results**
   - Use [`benchmark_configurations.py`](https://github.com/CoenvdE/Training-at-larger-scale-blog/blob/main/3.%20Optimizing%20the%20pipeline%3A%20Data/benchmark_configurations.py) to test all configurations
   - Can be run locally or in the cloud
   - (Download and) analyze the files with [`plot_benchmark_runs.ipynb`](https://github.com/CoenvdE/Training-at-larger-scale-blog/blob/main/3.%20Optimizing%20the%20pipeline%3A%20Data/plot_benchmark_runs.ipynb) (use the `.log` files, not the `_workers.log` files)
   - Compare performance metrics across configurations

Use the [plotting notebook](https://github.com/CoenvdE/Training-at-larger-scale-blog/blob/main/3.%20Optimizing%20the%20pipeline%3A%20Data/plot_benchmark_runs.ipynb) to visualize differences between runs and identify which configuration has the lowest wait/batch fetching time. While I don't explicitly measure vRAM/CPU utilization in these tools (as it's complex and time-consuming to implement), the primary goal is to significantly improve training time with reasonable effort. Having that said, watch for these warning signs:

- **Memory issues**: If memory usage spikes, reduce workers, prefetch factor, or caching.

- **Diminishing returns**: If adding workers doesn't improve throughput, you've reached saturation.

- **Memory leaks**: If RAM usage continuously grows, check for Dask worker caching, large objects in persistent workers, or reference issues.

### Cloud vs. Local Performance

Note that network bandwidth varies dramatically between environments. When moving from local development (WiFi) to cloud training, you may see orders of magnitude improvement in data loading speed. In my case, I observed a 100x decrease in wait time when moving to the cloud. Always benchmark in the same environment where you'll be training, as the optimal configuration can differ significantly between local and cloud setups.

Now that we have the data-part of the pipeline optimized, lets focus on the [Model](https://github.com/CoenvdE/Training-at-larger-scale-blog/blob/main/4.%20Optimizing%20the%20pipeline%3A%20Model.md)
