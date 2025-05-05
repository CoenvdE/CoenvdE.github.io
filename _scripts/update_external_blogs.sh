#!/bin/bash

# Script to update external blog content before building the site

echo "Updating external blog content..."

# Navigate to the repository root
cd "$(dirname "$0")/.."

# Update all submodules
git submodule update --remote --merge

# Create or update symbolic links directory
mkdir -p _external_blogs_links

# Create symbolic links with proper names (no spaces)
ln -sf ../_external_blogs/training-at-larger-scale/"0. The Setup.md" _external_blogs_links/setup.md
ln -sf ../_external_blogs/training-at-larger-scale/"1. Multi-GPU training.md" _external_blogs_links/multi_gpu_training.md
ln -sf ../_external_blogs/training-at-larger-scale/"2. Bigger data in the cloud.md" _external_blogs_links/bigger_data_in_cloud.md
ln -sf ../_external_blogs/training-at-larger-scale/"3. Optimizing the pipeline: Data.md" _external_blogs_links/optimizing_data.md
ln -sf ../_external_blogs/training-at-larger-scale/"4. Optimizing the pipeline: Model.md" _external_blogs_links/optimizing_model.md
ln -sf ../_external_blogs/training-at-larger-scale/"5. What Is Next.md" _external_blogs_links/what_is_next.md
ln -sf ../_external_blogs/training-at-larger-scale/"README.md" _external_blogs_links/readme.md

echo "External blog content updated successfully!" 