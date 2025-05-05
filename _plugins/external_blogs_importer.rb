require 'yaml'
require 'fileutils'

Jekyll::Hooks.register :site, :after_init do |site|
  puts "Processing external blog files..."
  
  # Configuration
  source_dir = File.expand_path('../_external_blogs/training-at-scale', site.source)
  target_dir = File.expand_path('../_external_blogs', site.source)
  collection_id = 'training_at_scale'
  repo_url = 'https://github.com/CoenvdE/Training-at-larger-scale-blog'
  
  # Ensure the target directory exists
  FileUtils.mkdir_p(target_dir)
  
  # Process all markdown files in source directory
  Dir.glob(File.join(source_dir, '**', '*.md')).sort.each_with_index do |file, index|
    # Skip README or other non-content files
    basename = File.basename(file)
    next if basename.downcase == 'readme.md' || basename.start_with?('.')
    
    content = File.read(file)
    
    # Extract title from content (first h1)
    title = content.match(/^#\s+(.+)$/m)&.[](1) || basename.gsub('.md', '').gsub(/[_-]/, ' ').split.map(&:capitalize).join(' ')
    
    # Extract description (first paragraph after title)
    description = content.match(/^#\s+.+\n+(.+?)(\n\n|\n#|\z)/m)&.[](1)&.strip || "Part of the Training at Scale series"
    
    # Build front matter
    front_matter = {
      'layout' => 'external_blog',
      'title' => title,
      'description' => description,
      'date' => Time.now.strftime('%Y-%m-%d'),
      'collection' => 'external_blogs',
      'collection_id' => collection_id,
      'chapter_number' => index + 1,
      'source_repo' => repo_url,
      'original_file' => file.sub(source_dir, '')
    }
    
    # Calculate target path
    target_filename = "#{collection_id}_#{index + 1}.md"
    target_path = File.join(target_dir, target_filename)
    
    # Prepend front matter to content
    new_content = "---\n#{front_matter.to_yaml}---\n\n#{content}"
    
    # Write the file
    File.write(target_path, new_content)
    puts "Processed: #{file} -> #{target_path}"
  end
  
  puts "Done processing external blog files!"
end 