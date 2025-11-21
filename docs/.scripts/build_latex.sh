#!/bin/bash
# Build script for LaTeX documentation

# Update PATH to include TeX binaries (for BasicTeX/MacTeX)
if [ -d "/Library/TeX/texbin" ]; then
    export PATH="/Library/TeX/texbin:$PATH"
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCS_DIR="$(dirname "$SCRIPT_DIR")"
LATEX_DIR="$DOCS_DIR/.latex"
BUILD_DIR="$DOCS_DIR/_build/latex"

echo "Building LaTeX documentation..."

# Create build directory
mkdir -p "$BUILD_DIR"

# Copy LaTeX files
echo "Copying LaTeX files..."
cp -r "$LATEX_DIR"/* "$BUILD_DIR/" 2>/dev/null || true
cp -r "$DOCS_DIR/.assets" "$BUILD_DIR/" 2>/dev/null || true

# Convert Markdown content to LaTeX (if pandoc is available)
if command -v pandoc &> /dev/null; then
    echo "Converting Markdown content to LaTeX..."
    
    # Check if pandoc-citeproc filter is available
    CITEPROC_FILTER=""
    if command -v pandoc-citeproc &> /dev/null; then
        CITEPROC_FILTER="--filter pandoc-citeproc"
    fi
    
    # Convert each content file
    for md_file in "$DOCS_DIR"/content/**/*.md; do
        if [ -f "$md_file" ]; then
            rel_path="${md_file#$DOCS_DIR/content/}"
            tex_file="$BUILD_DIR/chapters/${rel_path%.md}.tex"
            mkdir -p "$(dirname "$tex_file")"
            
            # Pre-process: Convert inline $$ to $, but preserve display math blocks
            temp_file=$(mktemp)
            python3 -c "
import re

md_file = '$md_file'
temp_file = '$temp_file'

with open(md_file, 'r') as f:
    content = f.read()

# Convert inline $$ to $, but preserve display math blocks
lines = content.split('\n')
result = []
i = 0
dollar_dollar = '\$\$'

while i < len(lines):
    line = lines[i]
    stripped = line.strip()
    
    # Display math block: $$ on its own line
    if stripped == dollar_dollar:
        result.append(line + '\n')
        i += 1
        while i < len(lines) and lines[i].strip() != dollar_dollar:
            result.append(lines[i] + '\n')
            i += 1
        if i < len(lines):
            result.append(lines[i] + '\n')
        i += 1
        continue
    
    # For all other lines, convert $$...$$ to $...$ (inline math)
    line = line.replace(dollar_dollar, '\$')
    result.append(line + '\n')
    i += 1

# Save processed content
with open(temp_file, 'w') as f:
    f.write(''.join(result))
"
            
            # Convert with pandoc
            if pandoc "$temp_file" \
                -f markdown \
                -t latex \
                --wrap=none \
                -o "$tex_file" 2>&1; then
                # Post-process to fix numbering and convert to chapters
                python3 -c "
import re
import sys

tex_file = '$tex_file'

with open(tex_file, 'r') as f:
    content = f.read()

# Convert \\section{Chapter X --- Title} to \\chapter{Title}
content = re.sub(r'\\\\section\{Chapter \\d+ --- ([^}]+)\}', r'\\\\chapter{\\1}', content)

# Convert \\subsection{X.Y Title} to \\section{Title} (remove number prefix)
content = re.sub(r'\\\\subsection\{[\\d.]+ ([^}]+)\}', r'\\\\section{\\1}', content)

# Convert \\subsubsection{X.Y.Z Title} to \\subsection{Title} (remove number prefix)
content = re.sub(r'\\\\subsubsection\{[\\d.]+ ([^}]+)\}', r'\\\\subsection{\\1}', content)

with open(tex_file, 'w') as f:
    f.write(content)
"
                echo "  ✓ Converted: $rel_path"
            else
                echo "  ✗ Failed to convert: $rel_path"
            fi
            
            rm -f "$temp_file"
        fi
    done
else
    echo "Warning: pandoc not found. Install with: brew install pandoc (macOS) or apt-get install pandoc (Linux)"
    echo "LaTeX files copied, but Markdown content not converted."
fi

# Build LaTeX document
cd "$BUILD_DIR"

if command -v pdflatex &> /dev/null; then
    echo "Compiling LaTeX document..."
    
    # First pass
    pdflatex -interaction=nonstopmode main.tex > /dev/null 2>&1 || true
    
    # Bibliography (if bibtex is available)
    if command -v bibtex &> /dev/null && [ -f bibliography.bib ]; then
        bibtex main > /dev/null 2>&1 || true
    fi
    
    # Second pass for references
    pdflatex -interaction=nonstopmode main.tex > /dev/null 2>&1 || true
    pdflatex -interaction=nonstopmode main.tex > /dev/null 2>&1 || true
    
    echo "✓ LaTeX documentation built successfully!"
    echo "Output: $BUILD_DIR/main.pdf"
else
    echo "Warning: pdflatex not found. Install a LaTeX distribution (e.g., MacTeX, TeX Live)"
    echo "LaTeX source files prepared in: $BUILD_DIR"
    echo "You can manually compile with: pdflatex main.tex"
fi

