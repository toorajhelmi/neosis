# Chapter Numbering System

This documentation uses a placeholder-based system for chapter numbers to make renumbering chapters easier.

## How It Works

**Your local source files always use `{CH}` placeholders** - this makes it easy to move/renumber chapters. The placeholders are automatically replaced with actual numbers only when:
- Generating LaTeX PDF (uses temporary copies)
- Pushing to git (replaces in place, commits, then restores placeholders locally)

Instead of hardcoding chapter numbers like `# Chapter 4 — Title` or `## 4.1 Section`, we use placeholders:

- `# Chapter {CH} — Title`
- `## {CH}.1 Section`
- `### {CH}.2.1 Subsection`
- `Figure {CH}.1 — Title`
- `Table {CH}.1 — Title`
- etc.

The `{CH}` placeholder is automatically replaced with the actual chapter number based on the directory name (e.g., `chapter4/` → `4`).

## Workflow

### Normal Editing

1. **Edit files with `{CH}` placeholders** - your local files always keep placeholders
2. **Push to git** - the git hook automatically:
   - Replaces `{CH}` with actual numbers
   - Commits the changes
   - Pushes to remote
   - Restores `{CH}` placeholders in your local files

### Generating LaTeX PDF

The build script automatically:
- Creates temporary copies of your files
- Replaces `{CH}` placeholders in the copies
- Builds LaTeX from the copies
- Your source files remain unchanged with placeholders

```bash
./docs/.scripts/build_latex.sh
```

### Renumbering Chapters

1. **Rename directories**: `mv chapter4 chapter5`
2. **That's it!** Your files already use `{CH}` placeholders, so they'll automatically get the correct numbers when you push or build LaTeX

## Scripts

### `update_chapter_numbers.sh`

**Purpose:** Replaces `{CH}` placeholders with actual chapter numbers (or restores them).

**Usage:**
```bash
# Replace placeholders with numbers
./docs/.scripts/update_chapter_numbers.sh

# Restore placeholders from numbers
./docs/.scripts/update_chapter_numbers.sh --restore
```

**Note:** You typically don't need to run this manually - the git hooks and LaTeX build handle it automatically.

### `build_latex.sh`

**Purpose:** Builds LaTeX PDF from Markdown sources.

**How it works:**
- Creates temporary copies of content files
- Replaces `{CH}` placeholders in the copies
- Builds LaTeX from the copies
- Your source files remain unchanged

**Usage:**
```bash
./docs/.scripts/build_latex.sh
```

## Git Hooks

### Pre-Push Hook

Automatically runs before `git push`:
1. Detects if chapter files are being pushed
2. Replaces `{CH}` placeholders with actual numbers
3. Stages and amends the commit
4. Pushes with actual numbers

### Post-Push Hook

Automatically runs after `git push`:
1. Restores `{CH}` placeholders in your local files
2. Keeps your working directory with placeholders for easy editing

### Post-Merge Hook

Automatically runs after `git pull` or `git merge`:
1. Converts actual numbers back to `{CH}` placeholders
2. Ensures your local files always use placeholders

## Examples

### Chapter Title
```markdown
# Chapter {CH} — Micro Static Analysis of a Single Neo
```
In git/LaTeX: `# Chapter 4 — Micro Static Analysis of a Single Neo`  
In your local file: Always `# Chapter {CH} — Micro Static Analysis of a Single Neo`

### Section Header
```markdown
## {CH}.1 Neo as a Predictive System
```
In git/LaTeX: `## 4.1 Neo as a Predictive System`  
In your local file: Always `## {CH}.1 Neo as a Predictive System`

### Figure/Table References
```markdown
**Figure {CH}.1 — Conceptual Cube Diagram**
## Table {CH}.1 — Three-Axis Mapping
```
In git/LaTeX: `**Figure 7.1 — Conceptual Cube Diagram**`  
In your local file: Always `**Figure {CH}.1 — Conceptual Cube Diagram**`

## Important Notes

- **Your local files always use `{CH}` placeholders** - this makes renumbering easy
- **Git repository has actual numbers** - so GitBook and other tools display correctly
- **LaTeX builds use temporary copies** - your source files are never modified
- **Git hooks handle everything automatically** - you just edit with placeholders and push/build normally
- References to other chapters in text should still use actual numbers (e.g., "as discussed in Chapter 2")

## Troubleshooting

If placeholders aren't being restored after push:
```bash
./docs/.scripts/update_chapter_numbers.sh --restore
```

If you want to manually update numbers (not recommended):
```bash
./docs/.scripts/update_chapter_numbers.sh
```

If you want to manually restore placeholders:
```bash
./docs/.scripts/update_chapter_numbers.sh --restore
```
