# Neosis Documentation

This directory contains the source documentation for Neosis, structured to support both GitBook (web) and LaTeX (academic paper/thesis) outputs.

## Structure

```
docs/
├── content/              # Core documentation content (shared)
│   ├── introduction/
│   ├── concepts/
│   ├── architecture/
│   ├── api/
│   └── examples/
├── gitbook/             # GitBook-specific content and config
│   ├── SUMMARY.md       # GitBook navigation
│   └── book.json        # GitBook configuration
├── latex/               # LaTeX-specific content
│   ├── main.tex         # Main LaTeX document
│   ├── preamble.tex     # LaTeX preamble (packages, etc.)
│   ├── chapters/        # LaTeX chapter files
│   └── bibliography.bib # Bibliography
├── assets/              # Shared assets (images, diagrams)
└── scripts/             # Build scripts
    ├── build_gitbook.sh
    └── build_latex.sh
```

## Workflow

1. **Write content** in `content/` using Markdown
2. **Build GitBook**: Run `scripts/build_gitbook.sh` → outputs to `_build/gitbook/`
3. **Build LaTeX**: Run `scripts/build_latex.sh` → outputs to `_build/latex/`

## Writing Guidelines

### For Shared Content (content/)

- Use standard Markdown
- Use `<!-- gitbook:include -->` and `<!-- latex:include -->` comments to mark platform-specific sections
- Images: Place in `assets/` and reference with relative paths
- Code blocks: Use language tags (```python, ```bash, etc.)

### For GitBook-Specific Content

- Add interactive elements, callouts, hints
- Use GitBook's special blocks (hints, warnings, etc.)
- Place in `gitbook/` directory

### For LaTeX-Specific Content

- Add formal definitions, theorems, proofs
- Use LaTeX math notation directly
- Place in `latex/chapters/` directory

## Building

### GitBook

```bash
cd docs
./scripts/build_gitbook.sh
```

### LaTeX

```bash
cd docs
./scripts/build_latex.sh
```

## Publishing

- **GitBook**: Push `_build/gitbook/` to GitBook repository or use GitBook CLI
- **LaTeX**: Compile `_build/latex/main.tex` with pdflatex/xelatex

