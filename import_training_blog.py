import os
import re
import shutil
import subprocess
from datetime import datetime, timedelta

# Repository URL and destination directories
repo_url = "https://github.com/CoenvdE/Training-at-larger-scale-blog.git"
source_dir = "Training-at-larger-scale-blog"
destination_dir = "_blogs/training-at-larger-scale"
image_dir = "images/training-blog"

# Step 1: Clone the repository
print(f"Cloning repository from {repo_url}...")
subprocess.run(["git", "clone", repo_url], check=True)
print("Repository cloned successfully.")

# Ensure destination directory exists
os.makedirs(destination_dir, exist_ok=True)
os.makedirs(image_dir, exist_ok=True)

# Get a list of all markdown files
md_files = [f for f in os.listdir(source_dir) if f.endswith('.md') and f != 'README.md']
md_files.sort(key=lambda x: x.split('.')[0] if x.split('.')[0].isdigit() else '999')

# Create mapping of original md files to their Jekyll URLs
link_mapping = {}
for i, md_file in enumerate(md_files):
    chapter_num = i + 1
    page_url = f"/blogs/training-at-larger-scale/part{chapter_num}/"
    link_mapping[md_file] = page_url
    
    # Also add variants with URL encoding to handle different link formats
    encoded_file = md_file.replace(' ', '%20')
    link_mapping[encoded_file] = page_url
    
    # Add variant without the .md extension
    filename_without_ext = os.path.splitext(md_file)[0]
    link_mapping[filename_without_ext] = page_url
    
    # Add URL-encoded variant without extension
    encoded_without_ext = filename_without_ext.replace(' ', '%20')
    link_mapping[encoded_without_ext] = page_url

# Read the README.md from the source directory to use as index content
readme_path = os.path.join(source_dir, "README.md")
with open(readme_path, "r") as f:
    readme_content = f.read()

# Function to fix links in markdown content
def fix_links(content):
    # First, fix regular markdown links [text](file.md)
    for old_link, new_url in link_mapping.items():
        # Pattern to match markdown links with the old link
        pattern = r'\[([^\]]+)\]\(({0})\)'.format(re.escape(old_link))
        # Replace with new URL
        content = re.sub(pattern, r'[\1](' + new_url + r')', content)
    
    # Fix any remaining links that might have different formats
    for md_file in md_files:
        base_name = os.path.splitext(md_file)[0]
        chapter_num = md_files.index(md_file) + 1
        new_url = f"/blogs/training-at-larger-scale/part{chapter_num}/"
        
        # Replace any variant of the filename in links
        patterns = [
            # Original filename with .md
            r'\[([^\]]+)\]\(' + re.escape(md_file) + r'\)',
            # Filename with spaces replaced by %20 with .md
            r'\[([^\]]+)\]\(' + re.escape(md_file.replace(' ', '%20')) + r'\)',
            # Just the base name without .md
            r'\[([^\]]+)\]\(' + re.escape(base_name) + r'\)',
            # Base name with spaces replaced by %20
            r'\[([^\]]+)\]\(' + re.escape(base_name.replace(' ', '%20')) + r'\)'
        ]
        
        for pattern in patterns:
            content = re.sub(pattern, r'[\1](' + new_url + r')', content)
    
    # Additional fix for remaining chapter references that have a specific pattern
    # Like [Chapter 3](3. Optimizing the pipeline: Data.md)
    for i, md_file in enumerate(md_files):
        chapter_num = i + 1
        chapter_name = os.path.splitext(md_file)[0]
        chapter_name = re.sub(r'^\d+\.\s*', '', chapter_name)
        new_url = f"/blogs/training-at-larger-scale/part{chapter_num}/"
        
        # This regex catches chapter references like "[Chapter X](...)" or references to numbered markdown files
        chapter_pattern = r'\[(Chapter\s+\d+|[^\]]+)\]\((\d+\.[^)]+)\)'
        
        # Check each chapter reference
        for match in re.finditer(chapter_pattern, content):
            text = match.group(1)
            filename = match.group(2)
            
            # Try to find which file it corresponds to by checking beginning numbers
            file_num = re.match(r'^(\d+)', filename)
            if file_num:
                num = int(file_num.group(1))
                if 0 <= num < len(md_files):  # Check if valid chapter number
                    content = content.replace(match.group(0), f"[{text}](/blogs/training-at-larger-scale/part{num+1}/)")
    
    # First, replace any already fixed paths to avoid double-fixing
    # This handles cases where "/images/training-blog/" might already be in the content
    content = content.replace("/images/training-blog/images/", "/images/training-blog/")
    
    # Fix all image references with absolute paths
    # Handle different image patterns for standard markdown images
    image_patterns = [
        # Standard markdown image: ![alt](images/file.png)
        (r'!\[([^\]]*)\]\(images/([^)]+)\)', r'![\1](/images/training-blog/\2)'),
        # Images with ./ prefix: ![alt](./images/file.png)
        (r'!\[([^\]]*)\]\(\./images/([^)]+)\)', r'![\1](/images/training-blog/\2)'),
        # Relative image path in subdirectory: ![alt](../images/file.png)
        (r'!\[([^\]]*)\]\(\.\./images/([^)]+)\)', r'![\1](/images/training-blog/\2)'),
        # Direct image path in markdown links: [text](images/file.png)
        (r'(?<!\!)\[([^\]]*)\]\(images/([^)]+)\)', r'[\1](/images/training-blog/\2)')
    ]
    
    for pattern, replacement in image_patterns:
        content = re.sub(pattern, replacement, content)
    
    # Fix HTML img tags
    # Replace src="images/..." with src="/images/training-blog/..."
    content = re.sub(
        r'(<img[^>]+src=")images/([^"]+)(")',
        r'\1/images/training-blog/\2\3',
        content
    )
    
    # Also catch single-quoted attributes
    content = re.sub(
        r"(<img[^>]+src=')images/([^']+)(')",
        r"\1/images/training-blog/\2\3",
        content
    )
    
    # Fix any remaining HTML attributes with unquoted image references
    content = re.sub(r'(src|href)=(["\']?)images/', r'\1=\2/images/training-blog/', content)
    
    # Final check to ensure we don't have doubled paths
    content = content.replace("/images/training-blog/images/", "/images/training-blog/")
    content = content.replace("src=\"/images/training-blog/images/", "src=\"/images/training-blog/")
    content = content.replace("src='/images/training-blog/images/", "src='/images/training-blog/")
    
    return content

# Apply link fixing to README content for the index page
index_content = fix_links(readme_content)

# Remove any "TODO" sections and author notes
index_content = re.sub(r'## TODO[\s\S]*?(?=##|$)', '', index_content)
index_content = re.sub(r'> Author.*?\n', '', index_content)

# Write the index.md file with "Introduction" as the title
index_file_path = os.path.join(destination_dir, "index.md")
with open(index_file_path, "w") as f:
    f.write("---\n")
    f.write("layout: blog_collection\n")
    f.write("title: \"Introduction\"\n")
    f.write("description: \"A comprehensive guide to scaling machine learning from small to larger training setups.\"\n")
    f.write("collection_id: training-at-larger-scale\n")
    f.write("display_chapters: true\n")
    f.write("---\n\n")
    f.write(index_content)

print(f"Created index.md at {index_file_path}")

# Process each markdown file in the blog repo
for i, md_file in enumerate(md_files):
    source_file_path = os.path.join(source_dir, md_file)
    chapter_num = i + 1
    destination_file_path = os.path.join(destination_dir, f"part{chapter_num}.md")

    # Read the content of the source file
    with open(source_file_path, "r") as f:
        content = f.read()

    # Extract chapter name from the filename - remove numbers and file extension
    chapter_name = os.path.splitext(md_file)[0]
    # Remove any leading numbers and dots/spaces from the filename (like "0. " or "1. ")
    chapter_name = re.sub(r'^\d+\.\s*', '', chapter_name)
    
    # Also extract the first heading as a fallback
    title_match = re.search(r'^# (.+)', content, re.MULTILINE)
    if title_match:
        title_from_content = title_match.group(1)
        # Use the heading if the filename is too generic
        if chapter_name.lower() in ['readme', 'index', 'chapter']:
            chapter_name = title_from_content

    # Fix links in the content
    content = fix_links(content)

    # Copy images if they exist
    images_dir_source = os.path.join(source_dir, "images")
    if os.path.exists(images_dir_source):
        # Copy all images to the destination
        for img_file in os.listdir(images_dir_source):
            source_img_path = os.path.join(images_dir_source, img_file)
            dest_img_path = os.path.join(image_dir, img_file)
            if os.path.isfile(source_img_path):
                shutil.copy2(source_img_path, dest_img_path)
                print(f"Copied image: {img_file}")

    # Calculate post date (use a date that orders the posts correctly)
    post_date = (datetime.now() - timedelta(days=30-i)).strftime("%Y-%m-%d")

    # Write the processed content to the destination file
    with open(destination_file_path, "w") as f:
        f.write("---\n")
        f.write("layout: blog_collection\n")
        f.write(f"title: \"{chapter_name}\"\n")
        f.write(f"description: \"Chapter {chapter_num} of the Training at Larger Scale series\"\n")
        f.write(f"date: {post_date}\n")
        f.write("collection_id: training-at-larger-scale\n")
        f.write(f"chapter_number: {chapter_num}\n")
        f.write("toc: true\n")
        f.write("categories: [Training, ML, GPU]\n")
        f.write("giscus_comments: true\n")
        f.write("---\n\n")
        f.write(content)

    print(f"Created blog post {chapter_num}: {destination_file_path} with title '{chapter_name}'")

# Step 3: Clean up - remove the cloned repository
print("Cleaning up...")
shutil.rmtree(source_dir)
print("Script completed successfully!") 