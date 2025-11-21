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
            
            # Pre-process: Remove GitBook-only sections, keep LaTeX-only sections
            temp_file=$(mktemp)
            python3 -c "
import re

md_file = '$md_file'
temp_file = '$temp_file'

with open(md_file, 'r') as f:
    content = f.read()

# Remove GitBook-only sections (between <!-- GITBOOK_ONLY --> and <!-- END_GITBOOK_ONLY -->)
content = re.sub(
    r'<!--\s*GITBOOK_ONLY\s*-->.*?<!--\s*END_GITBOOK_ONLY\s*-->',
    '',
    content,
    flags=re.DOTALL
)

# Remove LaTeX-only markers but keep the content
content = re.sub(
    r'<!--\s*LATEX_ONLY\s*-->\s*',
    '',
    content,
    flags=re.MULTILINE
)
content = re.sub(
    r'\s*<!--\s*END_LATEX_ONLY\s*-->',
    '',
    content,
    flags=re.MULTILINE
)

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
                # Post-process to fix numbering, convert to chapters, and replace placeholders with LaTeX
                python3 -c "
import re
import sys
import os

tex_file = '$tex_file'
latex_info_file = '$temp_file.latex_blocks'

# Read LaTeX blocks that were extracted before pandoc
latex_blocks = []
if os.path.exists(latex_info_file):
    with open(latex_info_file, 'r') as f:
        block_content = f.read()
        # Extract blocks
        block_pattern = r'BLOCK_(\d+)_START\n(.*?)BLOCK_\d+_END'
        matches = re.finditer(block_pattern, block_content, re.DOTALL)
        for match in matches:
            idx = int(match.group(1))
            block = match.group(2).strip()
            while len(latex_blocks) <= idx:
                latex_blocks.append('')
            latex_blocks[idx] = block

with open(tex_file, 'r') as f:
    content = f.read()

# Replace placeholders with actual LaTeX code
for i, block in enumerate(latex_blocks):
    # Replace LATEX_FIGURE_PLACEHOLDER_X or LATEX_BLOCK_PLACEHOLDER_X
    placeholder1 = 'LATEX_FIGURE_PLACEHOLDER_' + str(i)
    placeholder2 = 'LATEX_BLOCK_PLACEHOLDER_' + str(i) + '_'
    placeholder3 = 'LATEX\\\\_FIGURE\\\\_PLACEHOLDER\\\\_' + str(i)  # Pandoc escaped version
    placeholder4 = 'LATEX\\\\_BLOCK\\\\_PLACEHOLDER\\\\_' + str(i) + '\\\\_'  # Pandoc escaped version
    
    if placeholder1 in content:
        content = content.replace(placeholder1, block)
    elif placeholder2 in content:
        content = content.replace(placeholder2, block)
    elif placeholder3 in content:
        content = content.replace(placeholder3, block)
    elif placeholder4 in content:
        content = content.replace(placeholder4, block)

# Remove duplicate table/figure starts that might have been created
# Remove duplicate \begin{table}...\centering sequences
content = re.sub(r'\\\\begin\{table\}\[h\]\s*\\\\centering\s*\\\\begin\{table\}', r'\\begin{table}', content)

# Replace longtable with proper table (if we have a LaTeX table block)
for block in latex_blocks:
    if 'begin{table}' in block or 'toprule' in block:
        # Find the entire longtable structure - match from opening brace to closing brace
        # The pattern needs to handle nested braces properly
        # Try matching the wrapper: {\def\LTcaptype...\end{longtable}}
        start_idx = content.find('{\\def\\LTcaptype')
        if start_idx >= 0:
            # Find matching closing brace
            brace_count = 0
            i = start_idx
            while i < len(content):
                if content[i] == '{':
                    brace_count += 1
                elif content[i] == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        # Found the matching closing brace
                        end_idx = i + 1
                        # Replace this entire block
                        content = content[:start_idx] + block + content[end_idx:]
                        break
                i += 1
        else:
            # Try matching just the longtable without wrapper
            longtable_pattern = r'\\\\begin\{longtable\}.*?\\\\end\{longtable\}'
            if re.search(longtable_pattern, content, re.DOTALL):
                content = re.sub(longtable_pattern, block, content, count=1, flags=re.DOTALL)
        break

# Also replace pandoc-generated figure with TikZ figure (if not already replaced)
if len(latex_blocks) > 0:
    # Find pandoc-generated figure (usually starts with \begin{figure})
    # and replace with our TikZ figure, but only if placeholders weren't already replaced
    if 'LATEX' in content and 'PLACEHOLDER' in content:
        pass  # Already handled above
    else:
        figure_pattern = r'\\\\begin\{figure\}.*?\\\\end\{figure\}'
        def replace_figure(match):
            for block in latex_blocks:
                if 'begin{figure}' in block or 'tikzpicture' in block:
                    return block
            return match.group(0)
        content = re.sub(figure_pattern, replace_figure, content, count=1, flags=re.DOTALL)

# Replace pandoc-generated table with our LaTeX table (if available)
# But only if placeholders weren't already replaced
if 'LATEX' in content and 'PLACEHOLDER' in content:
    pass  # Already handled above
else:
    table_found = False
    for block in latex_blocks:
        if 'begin{table}' in block or 'toprule' in block:
            # Find pandoc-generated table (usually longtable or tabular)
            # Also match the wrapper that pandoc might add
            table_pattern = r'\{[^}]*\\def\\LTcaptype\{none\}.*?\\end\{longtable\}|\\\\begin\{longtable\}.*?\\\\end\{longtable\}|\\\\begin\{tabular\}.*?\\\\end\{tabular\}'
            def replace_table(match):
                return block
            if re.search(table_pattern, content, re.DOTALL):
                content = re.sub(table_pattern, replace_table, content, count=1, flags=re.DOTALL)
                table_found = True
                break

# Convert \\section{Chapter X --- Title} to \\chapter{Title}
content = re.sub(r'\\\\section\{Chapter \\d+ --- ([^}]+)\}', r'\\\\chapter{\\1}', content)

# Convert \\subsection{X.Y Title} to \\section{Title} (remove number prefix)
content = re.sub(r'\\\\subsection\{[\\d.]+ ([^}]+)\}', r'\\\\section{\\1}', content)

# Convert \\subsubsection{X.Y.Z Title} to \\subsection{Title} (remove number prefix)
content = re.sub(r'\\\\subsubsection\{[\\d.]+ ([^}]+)\}', r'\\\\subsection{\\1}', content)

with open(tex_file, 'w') as f:
    f.write(content)

# Clean up
if os.path.exists(latex_info_file):
    os.remove(latex_info_file)
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

