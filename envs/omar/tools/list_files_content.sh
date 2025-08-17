#!/bin/bash

# Script to list all Python files and their content from interface directories
# Usage: ./list_files_content.sh

OUTPUT_FILE="interface_files_content.txt"

# Clear the output file if it exists
> "$OUTPUT_FILE"

echo "=== INTERFACE FILES AND CONTENT ===" >> "$OUTPUT_FILE"
echo "Generated on: $(date)" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Function to process files in a directory
process_directory() {
    local dir_path="$1"
    
    if [ -d "$dir_path" ]; then
        echo "Processing directory: $dir_path"
        echo "======================================" >> "$OUTPUT_FILE"
        echo "DIRECTORY: $dir_path" >> "$OUTPUT_FILE"
        echo "======================================" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
        
        # Find all Python files in the directory
        for file in "$dir_path"/*.py; do
            if [ -f "$file" ]; then
                filename=$(basename "$file")
                echo "Processing: $filename"
                
                echo "--------------------------------------" >> "$OUTPUT_FILE"
                echo "FILE: $filename" >> "$OUTPUT_FILE"
                echo "FULL PATH: $file" >> "$OUTPUT_FILE"
                echo "--------------------------------------" >> "$OUTPUT_FILE"
                echo "" >> "$OUTPUT_FILE"
                
                # Add file content
                if [ -r "$file" ]; then
                    cat "$file" >> "$OUTPUT_FILE"
                else
                    echo "ERROR: Cannot read file $file" >> "$OUTPUT_FILE"
                fi
                
                echo "" >> "$OUTPUT_FILE"
                echo "" >> "$OUTPUT_FILE"
            fi
        done
        echo "" >> "$OUTPUT_FILE"
    else
        echo "Directory $dir_path not found"
        echo "ERROR: Directory $dir_path not found" >> "$OUTPUT_FILE"
    fi
}

# Process each interface directory
for i in {1..5}; do
    process_directory "./interface_$i"
done

echo "" >> "$OUTPUT_FILE"
echo "=== END OF FILE LISTING ===" >> "$OUTPUT_FILE"

echo "Done! All files and content saved to: $OUTPUT_FILE"
echo "Total lines written: $(wc -l < "$OUTPUT_FILE")"

# Alternative one-liner approach (commented out)
# find ./interface_* -name "*.py" -exec echo "=== {} ===" \; -exec cat {} \; > interface_files_content.txt