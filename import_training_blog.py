import os
import re
import shutil
import subprocess
from datetime import datetime, timedelta

# Repository URL and destination directories
repo_url = "https://github.com/CoenvdE/Training-at-larger-scale-blog.git"
source_dir = "Training-at-larger-scale-blog"
destination_dir = "_blogs/training-at-larger-scale"

# Step 1: Clone the repository
print(f"Cloning repository from {repo_url}...")
subprocess.run(["git", "clone", repo_url], check=True)
print("Repository cloned successfully.")

# Ensure destination directory exists
os.makedirs(destination_dir, exist_ok=True)

# Read the README.md from the source directory to use as index content
readme_path = os.path.join(source_dir, "README.md")
with open(readme_path, "r") as f:
    readme_content = f.read()

# Extract title and description from the README
title_match = re.search(r'^# (.+)', readme_content, re.MULTILINE)
title = "Training at Larger Scale: A Blog Series"
if title_match:
    title = title_match.group(1)

# Remove the title and the "TODO" section from the README
readme_content = re.sub(r'^# .+\n', '', readme_content, 1, re.MULTILINE)
readme_content = re.sub(r'```\nTODO:.+?```\n', '', readme_content, flags=re.DOTALL)

# Create index.md file for the blog collection
index_content = f"""---
layout: blog_collection
title: "{title}"
description: "A comprehensive guide to scaling machine learning from small to larger training setups."
collection_id: training-at-larger-scale
display_chapters: true
---

{readme_content.strip()}
"""

with open(os.path.join(destination_dir, "index.md"), "w") as f:
    f.write(index_content)

# Chapters to process (in order)
chapters = [
    {"file": "0. The Setup.md", "num": 1},
    {"file": "1. Multi-GPU training.md", "num": 2},
    {"file": "2. Bigger data in the cloud.md", "num": 3},
    {"file": "3. Optimizing the pipeline: Data.md", "num": 4},
    {"file": "4. Optimizing the pipeline: Model.md", "num": 5},
    {"file": "5. What Is Next.md", "num": 6}
]

# Start date for the series (one week apart)
start_date = datetime.now() - timedelta(days=len(chapters) * 7)

for chapter in chapters:
    source_file = os.path.join(source_dir, chapter["file"])
    chapter_num = chapter["num"]
    
    # Calculate publication date
    pub_date = start_date + timedelta(days=chapter_num * 7)
    date_str = pub_date.strftime("%Y-%m-%d")
    
    # Read the source file
    with open(source_file, "r") as f:
        content = f.read()
    
    # Extract title from the first heading
    title_match = re.search(r'^#+\s+(.+)$', content, re.MULTILINE)
    if title_match:
        title = title_match.group(1).strip()
    else:
        title = f"Chapter {chapter_num}"
    
    # Create front matter
    front_matter = f"""---
layout: blog_collection
title: "{title}"
description: "Chapter {chapter_num} of the Training at Larger Scale series"
date: {date_str}
collection_id: training-at-larger-scale
chapter_number: {chapter_num}
toc: true
categories: [Machine Learning, Training, PyTorch, Optimization]
giscus_comments: true
---

"""
    
    # Update image paths in content
    content = content.replace("images/", "/images/training-blog/")
    
    # Fix internal links
    for ch in chapters:
        old_link = f"[Chapter {ch['num']}]({ch['file']})"
        new_link = f"[Chapter {ch['num']}](/blogs/training-at-larger-scale/part{ch['num']})"
        content = content.replace(old_link, new_link)
    
    # Remove the first heading as it's already in the front matter
    if title_match:
        content = content.replace(title_match.group(0), "", 1)
    
    # Create the final content
    final_content = front_matter + content.strip()
    
    # Write to destination
    dest_file = os.path.join(destination_dir, f"part{chapter_num}.md")
    with open(dest_file, "w") as f:
        f.write(final_content)
    
    print(f"Processed: {chapter['file']} -> {dest_file}")

# Create images directory and copy images
source_images = os.path.join(source_dir, "images")
dest_images = "images/training-blog"

if os.path.exists(source_images):
    os.makedirs(dest_images, exist_ok=True)
    
    # Copy all images
    for img in os.listdir(source_images):
        src_path = os.path.join(source_images, img)
        dst_path = os.path.join(dest_images, img)
        
        if os.path.isfile(src_path):
            shutil.copy2(src_path, dst_path)
            print(f"Copied image: {img}")

# Step 3: Clean up - remove the cloned repository
print(f"\nCleaning up: removing cloned repository at {source_dir}...")
shutil.rmtree(source_dir)
print("Cleanup completed.")

print("\nImport completed successfully!")
print(f"Blog collection created at: {destination_dir}")
print("Don't forget to check and manually adjust the content if needed.") 