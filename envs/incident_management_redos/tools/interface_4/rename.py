#!/usr/bin/env python3
"""
Term Replacement Script

Replaces occurrences of a term with another term in both file contents and filenames.
Handles different cases: lowercase, uppercase, title case, etc.

Usage: python replace_terms.py <old_term> <new_term> [directory]
"""

import os
import sys
import re
import shutil
from pathlib import Path


def get_case_variants(old_term, new_term):
    """Generate case variants for replacement."""
    variants = []
    
    # Lowercase
    variants.append((old_term.lower(), new_term.lower()))
    
    # Uppercase
    variants.append((old_term.upper(), new_term.upper()))
    
    # Title case (first letter uppercase)
    variants.append((old_term.capitalize(), new_term.capitalize()))
    
    # All combinations with underscores
    variants.append((f"{old_term.lower()}_", f"{new_term.lower()}_"))
    variants.append((f"_{old_term.lower()}", f"_{new_term.lower()}"))
    variants.append((f"_{old_term.lower()}_", f"_{new_term.lower()}_"))
    
    # CamelCase variants
    variants.append((f"{old_term.capitalize()}", f"{new_term.capitalize()}"))
    
    return variants


def replace_in_file(file_path, old_term, new_term):
    """Replace terms in file content with precise prefix matching."""
    try:
        # Read file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Common suffixes that should NOT be replaced
        excluded_suffixes = ['id', 'date', 'by', 'at', 'on']
        excluded_pattern = '|'.join(excluded_suffixes)
        
        # Pattern 1: lowercase term at word boundary
        # Matches: "manipulate_users", "manage " but NOT "managing", "manager", "manage_id", "manage_date"
        pattern1 = re.compile(r'\b' + re.escape(old_term.lower()) + r'(?=_(?!(' + excluded_pattern + r')\b)|$)')
        content = pattern1.sub(new_term.lower(), content)
        
        # Pattern 2: Title case term followed by uppercase letter ONLY
        # Matches: "ManipulateUser" but NOT "Manager" or "Managing" or "Manage"
        title_old = old_term.capitalize()
        title_new = new_term.capitalize()
        pattern2 = re.compile(r'\b' + re.escape(title_old) + r'(?=[A-Z])')
        content = pattern2.sub(title_new, content)
        
        # Pattern 3: All uppercase term followed by underscore (excluding suffixes) or uppercase or end
        # Matches: "MANIPULATE_USER", "MANIPULATEUSER" but not "MANAGING", "MANAGE_ID"
        pattern3 = re.compile(r'\b' + re.escape(old_term.upper()) + r'(?=_(?!(' + excluded_pattern.upper() + r')\b)|[A-Z]|$)')
        content = pattern3.sub(new_term.upper(), content)
        
        # Write back if content changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Updated content in: {file_path}")
            return True
        
        return False
        
    except Exception as e:
        print(f"✗ Error processing {file_path}: {e}")
        return False


def get_new_filename(filename, old_term, new_term):
    """Generate new filename with replaced terms using prefix matching."""
    new_filename = filename
    
    # Common suffixes that should NOT be replaced
    excluded_suffixes = ['id', 'date', 'by', 'at', 'on']
    excluded_pattern = '|'.join(excluded_suffixes)
    
    # Pattern 1: lowercase term followed by underscore (excluding common suffixes) or end of word
    pattern1 = re.compile(r'\b' + re.escape(old_term.lower()) + r'(?=_(?!(' + excluded_pattern + r')\b)|$)')
    new_filename = pattern1.sub(new_term.lower(), new_filename)
    
    # Pattern 2: Title case followed by uppercase ONLY
    title_old = old_term.capitalize()
    title_new = new_term.capitalize()
    pattern2 = re.compile(r'\b' + re.escape(title_old) + r'(?=[A-Z])')
    new_filename = pattern2.sub(title_new, new_filename)
    
    # Pattern 3: Uppercase followed by underscore (excluding suffixes) or uppercase or end
    upper_old = old_term.upper()
    upper_new = new_term.upper()
    pattern3 = re.compile(r'\b' + re.escape(upper_old) + r'(?=_(?!(' + excluded_pattern.upper() + r')\b)|[A-Z]|$)')
    new_filename = pattern3.sub(upper_new, new_filename)
    
    return new_filename


def rename_file(file_path, old_term, new_term):
    """Rename file if its name contains the old term."""
    try:
        directory = file_path.parent
        old_filename = file_path.name
        new_filename = get_new_filename(old_filename, old_term, new_term)
        
        if new_filename != old_filename:
            new_path = directory / new_filename
            
            # Check if target file already exists
            if new_path.exists():
                print(f"⚠ Warning: Target file already exists: {new_path}")
                return file_path
            
            shutil.move(str(file_path), str(new_path))
            print(f"✓ Renamed: {old_filename} → {new_filename}")
            return new_path
        
        return file_path
        
    except Exception as e:
        print(f"✗ Error renaming {file_path}: {e}")
        return file_path


def process_directory(directory, old_term, new_term, file_extensions=None):
    """Process all files in directory recursively."""
    if file_extensions is None:
        # Common text file extensions
        file_extensions = {'.py', '.txt', '.md', '.js', '.html', '.css', '.json', '.xml', '.yml', '.yaml', '.sh', '.bat'}
    
    directory = Path(directory)
    files_processed = []
    files_renamed = []
    
    # Get all files first (to avoid issues with renaming during iteration)
    all_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            all_files.append(Path(root) / file)
    
    # Process file contents
    for file_path in all_files:
        if file_path.suffix.lower() in file_extensions or not file_extensions:
            if replace_in_file(file_path, old_term, new_term):
                files_processed.append(str(file_path))
    
    # Rename files (do this after content processing to avoid path issues)
    for file_path in all_files:
        new_path = rename_file(file_path, old_term, new_term)
        if new_path != file_path:
            files_renamed.append((str(file_path), str(new_path)))
    
    # Rename directories
    for root, dirs, files in os.walk(directory, topdown=False):
        for dir_name in dirs:
            dir_path = Path(root) / dir_name
            new_dir_name = get_new_filename(dir_name, old_term, new_term)
            
            if new_dir_name != dir_name:
                new_dir_path = Path(root) / new_dir_name
                try:
                    if not new_dir_path.exists():
                        shutil.move(str(dir_path), str(new_dir_path))
                        print(f"✓ Renamed directory: {dir_name} → {new_dir_name}")
                except Exception as e:
                    print(f"✗ Error renaming directory {dir_path}: {e}")
    
    return files_processed, files_renamed


def main():
    if len(sys.argv) < 3:
        print("Usage: python replace_terms.py <old_term> <new_term> [directory]")
        print("Example: python replace_terms.py manage handle .")
        sys.exit(1)
    
    old_term = sys.argv[1]
    new_term = sys.argv[2]
    directory = sys.argv[3] if len(sys.argv) > 3 else "."
    
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        sys.exit(1)
    
    print(f"Replacing '{old_term}' with '{new_term}' in directory: {directory}")
    print("=" * 60)
    
    # Ask for confirmation
    response = input("Do you want to continue? (y/N): ").strip().lower()
    if response not in ['y', 'yes']:
        print("Operation cancelled.")
        sys.exit(0)
    
    try:
        files_processed, files_renamed = process_directory(directory, old_term, new_term)
        
        print("\n" + "=" * 60)
        print("SUMMARY:")
        print(f"Files with content updated: {len(files_processed)}")
        print(f"Files/directories renamed: {len(files_renamed)}")
        
        if files_processed:
            print("\nFiles with updated content:")
            for file in files_processed:
                print(f"  - {file}")
        
        if files_renamed:
            print("\nRenamed files:")
            for old_name, new_name in files_renamed:
                print(f"  - {old_name} → {new_name}")
        
        print("\nOperation completed successfully!")
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()