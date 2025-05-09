---
layout: blog_collection
title: "Bigger data in the cloud"
description: "Chapter 3 of the Training at Larger Scale series"
date: 2025-04-11
collection_id: training-at-larger-scale
chapter_number: 3
toc: true
categories: [Training, ML, GPU]
giscus_comments: true
---

## 2. Bigger Data In The Cloud

In this part, I will provide a general overview of what streaming is and how to work with data in the cloud, I will also provide a use case specific example for loading and working with geospatial data (xarray) to show an example of with bigger datasets.

```
2. Bigger data in the cloud/
├── data/
│   ├── usecase_cloud_dataset.py
│   ├── utils.py
│   ├── usecase_API_access.py
│   ├── usecase_cloud_access.py
│   ├── example_cloud_access.py
│   └── __pycache__/
├── output/
│   ├── copernicus_data/
│   └── test/
└── __pycache__/
```

### Quick Recap:

**torch.utils.data.Dataset**: A PyTorch Dataset is a class that tells PyTorch how to get one data sample.
It acts as a blueprint for reading a sample from storage (local disk or cloud storage) into active memory (RAM). It has two main functions:

- `__len__`: how many samples there are
- `__getitem__`: how to get one sample (e.g., load an image, label) Note that this can be from local storage or from the cloud.

The dataset doesn't load anything. It's just a blueprint.

Cloud data is often stored on object storage servers like:

- Amazon S3
- Google Cloud Storage (GCS)
- Azure Blob Storage

NOTE: additional information can be found in the [PyTorch Dataset Tutorial](https://pytorch.org/tutorials/beginner/basics/data_tutorial.html)

## The Problem: datasets that are too big for memory or local disk

Most data that you will use lives in "the cloud": servers somewhere on the planet, with all the data you will ever need. You can access data on the internet and download it to local (like CIFAR-10, as implemented by pytorch). So what do you do when you have so much data that it does not fit on your local machine?

One solution is to buy a hard drive and store the data on there. This itself is quite expensive, but could be beneficial if you have the hardware (GPU) yourself. In this case, you can just keep the whole pipeline local, but this is only beneficial if you have (multiple GPU's), which is super expensive.

Another option is to mount a virtual SSD to your cloud compute instance. This provides very fast read/write speeds and reliable data availability. However, it is more expensive, requires additional setup effort, and total storage capacity is limited depending on the cloud provider and instance type.

Since I don't have a lot of GPUs (or money), I chose another option: streaming/lazy-loading. Streaming or lazy-loading datasets means loading data only when needed, rather than reading everything into memory upfront. This approach is useful for large datasets that don't fit in memory or are stored in remote data sources. Instead, you load samples (or chunks of data) on-the-fly as needed, directly from cloud storage servers. This avoids filling up local storage or memory while still giving you access to massive datasets that would otherwise be impossible to work with on limited hardware.

Some examples where this happens:

- Hugging Face Datasets (streaming=True)
- WebDataset format (tar files accessed remotely or locally)
- Some torch.utils.data.Dataset implementations with lazy loading
- Some APIs provide this functionality

### Getting access to the data

When you want to stream/lazy-load/get data from cloud storage, you need access to the place it is stored (commonly called buckets). This can sometimes be implemented already by APIs (e.g. Huggingface, or my usecase: Copernicus, see [`usecase_API_access.py`](https://github.com/CoenvdE/Training-at-larger-scale-blog/blob/main/2.%20Bigger%20data%20in%20the%20cloud/data/usecase_API_access.py)).

In my case, I needed to get access to the cloud storage directly without the API. This direct access gave me more flexibility and control over how I loaded the data. I implemented this using the `fsspec` library, which provides a unified interface for working with different file systems and storage backends. This approach was particularly valuable because:

1. It allowed me to work with multiple storage providers using the same code
2. It enabled parallel data access, significantly improving loading speeds
3. It gave me fine-grained control over chunking and caching strategies
4. It integrated well with my existing PyTorch data pipeline
5. It has automatic failsafes for data loading, like retrying.

I've created both a general example ([`example_cloud_access.py`](https://github.com/CoenvdE/Training-at-larger-scale-blog/blob/main/2.%20Bigger%20data%20in%20the%20cloud/data/example_cloud_access.py)) and a use-case specific ([`usecase_cloud_access.py`](https://github.com/CoenvdE/Training-at-larger-scale-blog/blob/main/2.%20Bigger%20data%20in%20the%20cloud/data/usecase_cloud_access.py)) implementation showing how to access data in the cloud efficiently

<!-- TODO: (With Laurens): COPERNICUS DIDNT WANT EVERYONE TO KNOW, IS THIS OKAY? -->

### Streaming/Lazy Loading

Now that we have access to the data, we can stream it into memory! For my geospatial data use case, I utilize libraries like Zarr, Dask and Xarray that provide optimizable, efficient lazy loading capabilities. Zarr/Dask creates a computational graph for loading data chunks from storage only when needed, while managing parallel workers to speed up the process. I'll cover optimization strategies for (streaming) data pipelines in the [next chapter](/blogs/training-at-larger-scale/part4/). To be able to work with this (lazy-loaded) data from the cloud in your training pipeline, we need to wrap everything into a PyTorch dataset. I've implemented an example in [`usecase_cloud_dataset.py`](https://github.com/CoenvdE/Training-at-larger-scale-blog/blob/main/2.%20Bigger%20data%20in%20the%20cloud/data/usecase_cloud_dataset.py) that demonstrates how to create a custom Dataset class that handles cloud data access, lazy loading and converting it to a usable dataset. Note that this is still a simplified version. When working with Xarray, xbatcher is the most efficient way to use batch generation, but this is out of the scope of this guide. Feel free to ask any questions about this.

### Quick Recap:

**torch.utils.data.Dataloader**: A PyTorch DataLoader defines how to load (many) samples (efficiently) (batching, multiprocessing, shuffling, etc.). Basically the DataLoader keeps asking the Dataset (blueprint) for samples, and handles the rest. It:

- Wraps a Dataset
- Loads batches of data (samples) (in parallel using multiple workers)
- Handles shuffling, batching, prefetching, etc.
- Dataloader has been used to parallelize the data loading as this boosts up the speed and saves memory.

The Dataloader calls the **getitem**() from the Dataset to get the needed samples. The Dataset (blueprint) defines "what" a sample is and how to get it, the DataLoader defines how to load them efficiently.

### DataLoader Parameters for Efficient Data Loading (from the cloud)

**Number of Workers (`num_workers`)**:

- Specifies how many subprocesses should be used to load data. Each of these subprocesses retrieves a batch of data from your dataset and sends it to the main training process. This is not necessarily equal to the number of cores/threads the data loader uses. Each worker operates independently, loading data in parallel. The loaded data is then sent to the main process(es) for use in training, creating an overlap between training and data loading that reduces idle GPU time. Under the hood, the dataset object is replicated in each worker.
- `num_workers=0`: Data is loaded in the main process. No parallelism.
- `num_workers=N`: Spawns N worker processes to load data in parallel.
  - Note: This is **not the number of CPU cores**, but the number of subprocesses that utilize CPU resources.
- each worker might maintain its own HTTP connection or file handle. This can increase throughput (multiple parallel reads) but also load (e.g., more network connections). Ensure your data source can handle concurrent access.

I will show how to optimize this in the [next chapter](/blogs/training-at-larger-scale/part4/)

**Persistent Workers (`persistent_workers`)**:

- If `True`, keeps worker processes alive across epochs and thus reduces worker startup overhead.
- Especially useful when using slower file systems or large datasets as opening/closing files is time expensive.
- While persistent workers reduce startup overhead, they can lead to increased memory usage over time as workers may accumulate cached data or experience memory leaks. If you notice growing memory consumption during training. In this case you should reduce the number of workers.

**Pin Memory (`pin_memory`)**:

- If `True`, enables automatic allocation of fetched tensors into page-locked (pinned) memory. This can significantly speed up host (CPU) to device (GPU) memory transfer.
  - Normal memory -> GPU: Requires copy to temporary pageable buffer first
  - Pinned memory -> GPU: Direct transfer without intermediate copies
- Requires that your dataset's `__getitem__` returns `torch.Tensor` objects.

**Prefetch Factor (`prefetch_factor`)**:

- Number of batches loaded in advance by each worker.
- Total prefetched batches = `num_workers * prefetch_factor`. This needs to taken into account for memory consumption
- Higher values increase memory usage, but can improve throughput by reducing I/O bottlenecks.
- If using streaming datasets (WebDataset tar files, tf.data pipelines, etc.), ensure you take advantage of their features like prefetching and parallel reads

I will show how to optimize this in the [next chapter](/blogs/training-at-larger-scale/part4/)

**Multiprocessing Context**: Controls how worker processes are created in the DataLoader (usable with multiple workers):

- Use `multiprocessing_context='forkserver'` (or `'spawn'`) for compatibility with CUDA and complex I/O or filesystem interactions.
- `'spawn'` is the most compatible and is default on Windows and MacOS. Creates entirely new Python processes from scratch, with clean memory space. Safest but slowest method since it needs to re-import modules in each worker.
- `'forkserver'` can also be safer than `'fork'` (default on Linux) when using CUDA. Creates a server process that handles forking child processes on demand. Offers a good balance between safety and performance.
- `'fork'` is fast but can lead to subtle bugs with CUDA or file handles. Default on Linux. Creates workers by duplicating the entire parent process memory, including all open resources. Fast but dangerous with complex resources like CUDA contexts or file handles.
- Note: additional information can be found in the [Python Documentation](https://docs.python.org/3/library/multiprocessing.html#contexts-and-start-methods)

When this is not set correctly, you can run into gridlock. This is when worker processes become deadlocked or severely bottlenecked, preventing efficient data flow. Common scenarios include:

- CUDA errors when using `'fork'` with GPU operations
- Corrupted file handles when using `'fork'` with complex I/O
- Memory leaks from improper resource sharing
- Deadlocks from competing access to shared resources

**Worker Initialization (`worker_init_fn`)**:

- Optional function to initialize each worker after it's spawned.
- For cloud use: configure filesystem-specific settings and avoid duplication randomness across workers. An example is shown in `utils.py`
- NOTE: Initialization functions are called once per worker process, not once per batch.

Additional information can be found in the [PyTorch Documentation](https://pytorch.org/docs/stable/data.html)

Now we have a clean architecture setup that is validated and set up for multi-GPU training. We've learned how to access and stream data from the cloud, and configured our DataLoader with the appropriate parameters for efficient data loading. With these foundations in place, it's time to optimize the components of our pipeline for better performance. Let's start by focusing [optimizing the data part of the pipeline](/blogs/training-at-larger-scale/part4/)
