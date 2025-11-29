#!/bin/bash
# Comprehensive script to convert all hardcoded chapter numbers to {CH} placeholders
# Handles chapter titles and all section levels
# Converts based on directory name, regardless of what's currently in the file

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTENT_DIR="$SCRIPT_DIR/../content"

# Function to extract chapter number from directory name
get_chapter_num() {
    local dir_name="$1"
    if [[ "$dir_name" =~ chapter([0-9]+) ]]; then
        echo "${BASH_REMATCH[1]}"
    else
        return 1
    fi
}

# Function to convert chapter numbers to placeholders
convert_chapter_file() {
    local file="$1"
    local chapter_num="$2"
    
    # Create temporary file
    local temp_file=$(mktemp)
    
    # Read the file and perform replacements
    # Replace any chapter number in titles (not just the one matching directory)
    # Replace section numbers that start with any number followed by the pattern
    sed -E \
        -e "s/# Chapter [0-9]+ —/# Chapter {CH} —/g" \
        -e "s/## [0-9]+\.([0-9]+)/## {CH}.\1/g" \
        -e "s/### [0-9]+\.([0-9]+\.[0-9]+)/### {CH}.\1/g" \
        -e "s/#### [0-9]+\.([0-9]+\.[0-9]+\.[0-9]+)/#### {CH}.\1/g" \
        -e "s/##### [0-9]+\.([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)/##### {CH}.\1/g" \
        "$file" > "$temp_file"
    
    # Only update if file changed
    if ! cmp -s "$file" "$temp_file"; then
        mv "$temp_file" "$file"
        echo "Converted: $file (Chapter $chapter_num → {CH})"
        return 0
    else
        rm "$temp_file"
        return 1
    fi
}

# Process all chapter README.md files
converted_count=0
for chapter_dir in "$CONTENT_DIR"/chapter[0-9]*/; do
    if [ -d "$chapter_dir" ]; then
        chapter_name=$(basename "$chapter_dir")
        chapter_num=$(get_chapter_num "$chapter_name")
        
        if [ -z "$chapter_num" ]; then
            echo "Warning: Could not extract chapter number from $chapter_name" >&2
            continue
        fi
        
        readme_file="$chapter_dir/README.md"
        if [ -f "$readme_file" ]; then
            if convert_chapter_file "$readme_file" "$chapter_num"; then
                ((converted_count++))
            fi
        fi
    fi
done

if [ $converted_count -eq 0 ]; then
    echo "No files needed conversion."
else
    echo "Converted $converted_count chapter file(s) to use {CH} placeholders."
    echo "Run ./update_chapter_numbers.sh to restore actual numbers based on directory names."
fi
