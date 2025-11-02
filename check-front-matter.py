import os
import re
from pathlib import Path
import yaml

def extract_front_matter(content):
    """Extract YAML front matter from markdown file."""
    if not content.startswith('---'):
        return None
    
    parts = content.split('---', 2)
    if len(parts) < 3:
        return None
    
    try:
        return yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        return None

def validate_cr(cr_value):
    """
    Validate CR value and return issues.
    Returns: (is_valid, issue_description)
    """
    if cr_value is None:
        return False, "Missing CR field"
    
    # Check if it's a list/array (this causes Jekyll comparison error)
    if isinstance(cr_value, list):
        return False, f"CR is a list/array: {cr_value}"
    
    # Check if it's a dict/object
    if isinstance(cr_value, dict):
        return False, f"CR is a dictionary: {cr_value}"
    
    # Convert to string for validation
    cr_str = str(cr_value).strip()
    
    if not cr_str:
        return False, "CR field is empty"
    
    # Valid patterns: numbers, fractions, or decimals
    # Examples: 0, 1, 1/8, 1/4, 1/2, 0.125, 0.25, 10, 30
    valid_patterns = [
        r'^\d+$',           # Integer: 0, 1, 10, 30
        r'^\d+/\d+$',       # Fraction: 1/8, 1/4, 1/2
        r'^\d+\.\d+$',      # Decimal: 0.125, 0.25
    ]
    
    for pattern in valid_patterns:
        if re.match(pattern, cr_str):
            return True, None
    
    return False, f"Invalid CR format: '{cr_str}'"

def scan_monsters(folder_path):
    """Scan all monster files and report CR issues."""
    folder = Path(folder_path)
    
    if not folder.exists():
        print(f"Error: Folder '{folder_path}' does not exist")
        return
    
    md_files = sorted(folder.glob('*.md'))
    
    if not md_files:
        print(f"No .md files found in '{folder_path}'")
        return
    
    print(f"Scanning {len(md_files)} monster files...")
    print("=" * 70)
    
    issues_found = []
    valid_count = 0
    
    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            front_matter = extract_front_matter(content)
            
            if front_matter is None:
                issues_found.append((md_file.name, "No valid front matter"))
                continue
            
            cr_value = front_matter.get('cr')
            is_valid, issue = validate_cr(cr_value)
            
            if not is_valid:
                issues_found.append((md_file.name, issue))
            else:
                valid_count += 1
                
        except Exception as e:
            issues_found.append((md_file.name, f"Error reading file: {str(e)}"))
    
    # Report findings
    if issues_found:
        print(f"\n⚠️  ISSUES FOUND ({len(issues_found)} files):")
        print("-" * 70)
        for filename, issue in issues_found:
            print(f"  {filename}")
            print(f"    → {issue}")
            print()
    else:
        print("\n✓ All monster files have valid CR values!")
    
    print("=" * 70)
    print(f"Summary: {valid_count} valid, {len(issues_found)} with issues")
    
    return issues_found

def show_file_details(folder_path, filename):
    """Show detailed information about a specific file."""
    filepath = Path(folder_path) / filename
    
    if not filepath.exists():
        print(f"File not found: {filename}")
        return
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    front_matter = extract_front_matter(content)
    
    print(f"\nFile: {filename}")
    print("-" * 70)
    
    if front_matter is None:
        print("ERROR: No valid front matter found")
        print("\nFirst 500 characters:")
        print(content[:500])
        return
    
    print("Front Matter Fields:")
    for key, value in front_matter.items():
        value_type = type(value).__name__
        print(f"  {key}: {value} (type: {value_type})")
    
    if 'cr' in front_matter:
        cr_value = front_matter['cr']
        is_valid, issue = validate_cr(cr_value)
        print(f"\nCR Validation:")
        print(f"  Valid: {is_valid}")
        if issue:
            print(f"  Issue: {issue}")

if __name__ == "__main__":
    folder_path = "_monsters"
    
    print("Monster CR Field Validator")
    print("=" * 70)
    print(f"Scanning folder: {folder_path}\n")
    
    issues = scan_monsters(folder_path)
    
    # If you want to see details about a specific file, uncomment and modify:
    # print("\n" + "=" * 70)
    # show_file_details(folder_path, "problem-file.md")
    
    print("\nDone!")