#!/bin/bash

# Script to update external blog content before building the site

echo "Updating external blog content..."

# Navigate to the repository root
cd "$(dirname "$0")/.."

# Update all submodules
git submodule update --remote --merge

echo "External blog content updated successfully!" 