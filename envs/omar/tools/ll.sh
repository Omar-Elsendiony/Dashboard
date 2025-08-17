#!/bin/bash

# Source directory (where subfolders are located)
SOURCE_DIR="./"  # Replace with your source directory path if needed

# Destination directory (where all files will be copied)
DEST_DIR="./all_files"  # Replace with your desired destination path

# Create destination directory if it doesn't exist
mkdir -p "$DEST_DIR"

# Loop through all subdirectories and copy files
find "$SOURCE_DIR" -type f -exec cp {} "$DEST_DIR" \;

echo "All files have been copied to: $DEST_DIR"