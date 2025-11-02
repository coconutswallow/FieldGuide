import os
import re
from pathlib import Path

def parse_type_field(type_value):
    """
    Parse a type field like "Medium Fey, Chaotic Neutral" into components.
    Returns: (size, creature_type, alignment) or None if format doesn't match
    """
    # Pattern: Size Type, Alignment
    # Size: Tiny, Small, Medium, Large, Huge, Gargantuan
    # Type: Any creature type (may have multiple words like "Undead Spirit")
    # Alignment: Two words typically
    
    pattern = r'^(Tiny|Small|Medium|Large|Huge|Gargantuan)\s+(.+?),\s*(.+)$'
    match = re.match(pattern, type_value.strip())
    
    if match:
        size = match.group(1)
        creature_type = match.group(2).strip()
        alignment = match.group(3).strip()
        return size, creature_type, alignment
    
    return None

def process_markdown_file(filepath):
    """
    Process a single markdown file and update the front matter if needed.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if file has front matter
    if not content.startswith('---'):
        print(f"Skipping {filepath.name}: No front matter found")
        return False
    
    # Split into front matter and body
    parts = content.split('---', 2)
    if len(parts) < 3:
        print(f"Skipping {filepath.name}: Invalid front matter format")
        return False
    
    front_matter = parts[1]
    body = parts[2]
    
    # Find the type field
    type_match = re.search(r'^type:\s*(.+)$', front_matter, re.MULTILINE)
    
    if not type_match:
        print(f"Skipping {filepath.name}: No type field found")
        return False
    
    type_value = type_match.group(1).strip()
    parsed = parse_type_field(type_value)
    
    if not parsed:
        print(f"Skipping {filepath.name}: Type field doesn't match expected format: '{type_value}'")
        return False
    
    size, creature_type, alignment = parsed
    
    # Check if size and alignment fields already exist
    if re.search(r'^size:', front_matter, re.MULTILINE):
        print(f"Skipping {filepath.name}: size field already exists")
        return False
    
    if re.search(r'^alignment:', front_matter, re.MULTILINE):
        print(f"Skipping {filepath.name}: alignment field already exists")
        return False
    
    # Replace the type line with three new lines
    new_type_section = f"type: {creature_type}\nsize: {size}\nalignment: {alignment}"
    new_front_matter = re.sub(
        r'^type:\s*.+$',
        new_type_section,
        front_matter,
        count=1,
        flags=re.MULTILINE
    )
    
    # Reconstruct the file
    new_content = f"---{new_front_matter}---{body}"
    
    # Write back to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✓ Updated {filepath.name}: {size} {creature_type}, {alignment}")
    return True

def process_folder(folder_path):
    """
    Process all .md files in the specified folder.
    """
    folder = Path(folder_path)
    
    if not folder.exists():
        print(f"Error: Folder '{folder_path}' does not exist")
        return
    
    if not folder.is_dir():
        print(f"Error: '{folder_path}' is not a directory")
        return
    
    md_files = list(folder.glob('*.md'))
    
    if not md_files:
        print(f"No .md files found in '{folder_path}'")
        return
    
    print(f"Found {len(md_files)} markdown files")
    print("-" * 60)
    
    updated_count = 0
    skipped_count = 0
    
    for md_file in sorted(md_files):
        if process_markdown_file(md_file):
            updated_count += 1
        else:
            skipped_count += 1
    
    print("-" * 60)
    print(f"Summary: {updated_count} files updated, {skipped_count} files skipped")

if __name__ == "__main__":
    # Change this to your folder path
    folder_path = "_monsters"  # Default to _monsters folder
    
    # If you want to specify a different folder, you can do:
    # folder_path = "/path/to/your/monsters/folder"
    
    print("Monster Type Field Splitter")
    print("=" * 60)
    print(f"Processing folder: {folder_path}")
    print("=" * 60)
    
    process_folder(folder_path)
    
    print("\nDone!")