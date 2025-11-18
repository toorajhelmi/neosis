# Contributing to Documentation

## Writing Guidelines

### Markdown Format

- Use standard Markdown syntax
- Use `<!-- gitbook:start -->` and `<!-- gitbook:end -->` to mark GitBook-specific sections
- Use `<!-- latex:start -->` and `<!-- latex:end -->` to mark LaTeX-specific sections
- Code blocks should specify language: ` ```python `, ` ```bash `, etc.

### Platform-Specific Content

**GitBook-specific:**
- Interactive elements (callouts, hints, warnings)
- Embedded videos or interactive demos
- GitBook's special syntax blocks

**LaTeX-specific:**
- Formal definitions, theorems, proofs
- Complex mathematical notation
- Academic citations and references

### Images and Assets

- Place all images in `assets/` directory
- Use descriptive filenames
- Reference with relative paths: `![Alt text](assets/image.png)`
- For LaTeX, use `\includegraphics{assets/image.png}`

## Workflow

1. Write/edit content in `content/` directory
2. Test GitBook build: `./scripts/build_gitbook.sh`
3. Test LaTeX build: `./scripts/build_latex.sh`
4. Review outputs in `_build/` directory
5. Commit changes

## Converting Markdown to LaTeX

The build script uses `pandoc` to convert Markdown to LaTeX. For manual conversion:

```bash
pandoc input.md -f markdown -t latex -o output.tex
```

## Adding New Sections

1. Create new `.md` file in appropriate `content/` subdirectory
2. Add entry to `gitbook/SUMMARY.md`
3. Create corresponding LaTeX chapter in `latex/chapters/` (or let pandoc generate it)
4. Update `latex/main.tex` to include new chapter

