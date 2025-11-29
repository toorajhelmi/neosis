#!/bin/bash
# Script to update chapter numbers in all chapter files
# Replaces {CH} placeholders with actual chapter numbers based on directory names
# Usage: ./update_chapter_numbers.sh [--restore]
#   --restore: Restore {CH} placeholders from actual numbers

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTENT_DIR="$SCRIPT_DIR/../content"

RESTORE_MODE=false
if [ "$1" = "--restore" ]; then
    RESTORE_MODE=true
fi

# Function to extract chapter number from directory name
get_chapter_num() {
    local dir_name="$1"
    if [[ "$dir_name" =~ chapter([0-9]+) ]]; then
        echo "${BASH_REMATCH[1]}"
    else
        return 1
    fi
}

# Function to update chapter numbers in a file (replace {CH} with numbers)
update_chapter_file() {
    local file="$1"
    local chapter_num="$2"
    
    # Create temporary file
    local temp_file=$(mktemp)
    
    # Replace {CH} placeholders at various levels:
    # - Chapter titles: "# Chapter {CH} —"
    # - Section headers: "## {CH}.1", "## {CH}.2", etc.
    # - Subsection headers: "### {CH}.2.1", "### {CH}.2.2", etc.
    # - Subsubsection headers: "#### {CH}.2.1.1", etc.
    sed -E \
        -e "s/# Chapter \{CH\} —/# Chapter $chapter_num —/g" \
        -e "s/## \{CH\}\./## $chapter_num./g" \
        -e "s/### \{CH\}\./### $chapter_num./g" \
        -e "s/#### \{CH\}\./#### $chapter_num./g" \
        -e "s/##### \{CH\}\./##### $chapter_num./g" \
        -e "s/Figure \{CH\}\./Figure $chapter_num./g" \
        -e "s/Table \{CH\}\./Table $chapter_num./g" \
        "$file" > "$temp_file"
    
    # Only update if file changed
    if ! cmp -s "$file" "$temp_file"; then
        mv "$temp_file" "$file"
        echo "Updated: $file (Chapter $chapter_num)"
        return 0
    else
        rm "$temp_file"
        return 1
    fi
}

# Function to restore placeholders (replace numbers with {CH})
restore_chapter_file() {
    local file="$1"
    local chapter_num="$2"
    
    # Create temporary file
    local temp_file=$(mktemp)
    
    # Replace actual numbers with {CH} placeholders
    sed -E \
        -e "s/# Chapter $chapter_num —/# Chapter {CH} —/g" \
        -e "s/## $chapter_num\./## {CH}./g" \
        -e "s/### $chapter_num\./### {CH}./g" \
        -e "s/#### $chapter_num\./#### {CH}./g" \
        -e "s/##### $chapter_num\./##### {CH}./g" \
        -e "s/Figure $chapter_num\./Figure {CH}./g" \
        -e "s/Table $chapter_num\./Table {CH}./g" \
        "$file" > "$temp_file"
    
    # Only update if file changed
    if ! cmp -s "$file" "$temp_file"; then
        mv "$temp_file" "$file"
        echo "Restored: $file (Chapter $chapter_num → {CH})"
        return 0
    else
        rm "$temp_file"
        return 1
    fi
}

# Process all chapter README.md files
updated_count=0
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
            if [ "$RESTORE_MODE" = true ]; then
                if restore_chapter_file "$readme_file" "$chapter_num"; then
                    ((updated_count++))
                fi
            else
                if update_chapter_file "$readme_file" "$chapter_num"; then
                    ((updated_count++))
                fi
            fi
        fi
    fi
done

if [ $updated_count -eq 0 ]; then
    if [ "$RESTORE_MODE" = true ]; then
        echo "No files needed restoration."
    else
        echo "No files needed updating."
    fi
else
    if [ "$RESTORE_MODE" = true ]; then
        echo "Restored $updated_count chapter file(s) to use {CH} placeholders."
    else
        echo "Updated $updated_count chapter file(s)."
    fi
fi
