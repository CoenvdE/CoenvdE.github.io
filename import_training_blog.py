import os
import re
import shutil
import subprocess
from datetime import datetime, timedelta
import urllib.parse

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
def fix_links(content, md_file_original_name):
    github_base_url = "https://github.com/CoenvdE/Training-at-larger-scale-blog/blob/main/"
    
    # --- BEGIN New GitHub link conversion ---
    def github_link_replacer_closure(match):
        original_link_md = match.group(0)
        link_text = match.group(1)
        link_target = match.group(2)

        # 0. Normalize link_target for lookups (remove ./, decode)
        normalized_target_for_map = link_target
        if normalized_target_for_map.startswith('./'):
            normalized_target_for_map = normalized_target_for_map[2:]
        decoded_target_for_map = urllib.parse.unquote(normalized_target_for_map)
        
        # 1. Check link_mapping (global) first for known chapter links
        if normalized_target_for_map in link_mapping:
            return f"[{link_text}]({link_mapping[normalized_target_for_map]})"
        if decoded_target_for_map in link_mapping:
            return f"[{link_text}]({link_mapping[decoded_target_for_map]})"

        # 2. Skip absolute, mailto, or anchor links
        if link_target.startswith(('http://', 'https://', '#', '/', 'mailto:')):
            return original_link_md

        # 3. Check for .md extension (potential chapter link not in mapping - should be rare)
        cleaned_link_target_for_ext_check = link_target.split('?')[0].split('#')[0]
        if urllib.parse.unquote(cleaned_link_target_for_ext_check).lower().endswith('.md'):
            return original_link_md

        # 4. Check for image links (path or common extensions)
        image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp']
        if any(cleaned_link_target_for_ext_check.lower().endswith(ext) for ext in image_extensions):
             return original_link_md 
        if link_target.startswith("images/") or link_target.startswith("./images/") or link_target.startswith("../images/"):
            return original_link_md

        # 5. If none of the above, it's a candidate for a GitHub raw file link.
        # For file system operations, use a URL-decoded version of the link target.
        decoded_target_for_fs = urllib.parse.unquote(link_target)

        abs_md_file_path = os.path.abspath(os.path.join(source_dir, md_file_original_name))
        # Use decoded_target_for_fs for constructing the file system path to check
        abs_target_path_for_fs_check = os.path.abspath(os.path.join(os.path.dirname(abs_md_file_path), decoded_target_for_fs))
        
        abs_repo_root = os.path.abspath(source_dir)

        # Check if resolved path is within the repo boundaries
        if not abs_target_path_for_fs_check.startswith(abs_repo_root + os.sep) and abs_target_path_for_fs_check != abs_repo_root:
            # print(f"DEBUG: Link '{link_target}' (decoded: '{decoded_target_for_fs}') in '{md_file_original_name}' resolves outside repo: {abs_target_path_for_fs_check}. Keeping original.")
            return original_link_md

        # Check existence using the file system-friendly path
        if not os.path.exists(abs_target_path_for_fs_check):
            # print(f"DEBUG: Linked target '{link_target}' (decoded: '{decoded_target_for_fs}') in '{md_file_original_name}' (resolved to '{abs_target_path_for_fs_check}') does not exist. Keeping original link.")
            return original_link_md

        # If the file exists, construct the GitHub URL.
        # The path for the URL should be relative to the repo root.
        path_relative_to_repo_for_url = os.path.relpath(abs_target_path_for_fs_check, abs_repo_root)
        
        # Safeguard, though the boundary check above should handle this.
        if path_relative_to_repo_for_url.startswith(".."):
             # print(f"DEBUG: Link '{link_target}' in '{md_file_original_name}' resolved to problematic relative path '{path_relative_to_repo_for_url}'. Keeping original.")
             return original_link_md

        # Convert OS-specific path separators to forward slashes for the URL
        url_path_segment = path_relative_to_repo_for_url.replace(os.sep, '/')
        # URL-encode the path segment to handle spaces and other special characters
        encoded_url_path_segment = urllib.parse.quote(url_path_segment)
        
        final_github_url = github_base_url + encoded_url_path_segment
        return f"[{link_text}]({final_github_url})"

    # Apply the replacer function to the content for general markdown links [text](url)
    # Use non-greedy `([^)]+?)` for the URL part to handle potential nested parentheses better, though rare.
    content = re.sub(r'\[([^\]]+)\]\(([^)]+?)\)', github_link_replacer_closure, content)
    # --- END New GitHub link conversion ---

    # First, fix regular markdown links [text](file.md)
    # This loop is now mainly for .md files that might not have been caught by link_mapping in the new section,
    # or if the new section returned original_link_md for an .md file.
    # The `link_mapping` check in `github_link_replacer_closure` should handle most chapter links.
    for old_link, new_url in link_mapping.items():
        # Pattern to match markdown links with the old link (ensure it's specific to the old_link string)
        # The old_link itself might contain special regex characters, so escape it.
        # And ensure we match the whole link target, not just a part of it.
        # Using lookarounds to ensure the matched group is exactly old_link
        # (?<=\() and (?=\)) ensure we are inside link parentheses
        pattern = r'\[([^\]]+)\]\(({0})\)'.format(re.escape(old_link))
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
    for i, md_file_loop_var in enumerate(md_files): # Renamed md_file to avoid clash with outer scope if any future nesting
        chapter_num_loop = i + 1 # Renamed chapter_num
        # chapter_name_loop = os.path.splitext(md_file_loop_var)[0] # Renamed chapter_name
        # chapter_name_loop = re.sub(r'^\d+\.\s*\', '', chapter_name_loop)
        new_url_loop = f"/blogs/training-at-larger-scale/part{chapter_num_loop}/" # Renamed new_url
        
        # This regex catches chapter references like "[Chapter X](...)" or references to numbered markdown files
        # The target file (group 2) should be specific to an .md file.
        chapter_pattern = r'\[(Chapter\s+\d+|[^\]]+)\]\((\d+\.[^)]+\.md)\)' # Made .md explicit
        
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
index_content = fix_links(readme_content, "README.md")

# Remove any "TODO" sections and author notes
index_content = re.sub(r'## TODO[\s\S]*?(?=##|$)', '', index_content)
index_content = re.sub(r'> Author.*?\n', '', index_content)

# Write the index.md file with "Introduction" as the title
index_file_path = os.path.join(destination_dir, "index.md")
with open(index_file_path, "w") as f:
    f.write("---\n")
    f.write("layout: blog_collection\n")
    f.write("title: \"Training at larger scale\"\n")
    f.write("description: \"A guide on scaling machine learning from small to larger training setups.\"\n")
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
    content = fix_links(content, md_file)

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