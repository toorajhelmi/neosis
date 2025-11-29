# Chapter Numbering System

This documentation uses a placeholder-based system for chapter numbers to make renumbering chapters easier.

## How It Works

Instead of hardcoding chapter numbers like `# Chapter 4 — Title` or `## 4.1 Section`, we use placeholders:

- `# Chapter {CH} — Title`
- `## {CH}.1 Section`
- `### {CH}.2.1 Subsection`
- etc.

The `{CH}` placeholder is automatically replaced with the actual chapter number based on the directory name (e.g., `chapter4/` → `4`).

## Automatic Updates

### Before LaTeX Generation

The LaTeX build script (`build_latex.sh`) **automatically** runs `update_chapter_numbers.sh` before building, so chapter numbers are always correct in the PDF.

**Usage:**
```bash
./docs/.scripts/build_latex.sh
```

### Before Git Push

You have two options:

#### Option 1: Manual (Recommended)

Run the update script before pushing:

```bash
./docs/.scripts/update_chapter_numbers.sh
git add -A
git commit -m "Your message"
git push
```

Or use the convenience script:

```bash
./docs/.scripts/pre_push.sh
git add -A
git commit -m "Your message"
git push
```

#### Option 2: Automatic Git Hook

Set up a git hook to automatically update chapter numbers before every push:

```bash
./docs/.scripts/setup_git_hooks.sh
```

This will:
- Automatically update chapter numbers before pushing
- Stage the updated files
- Prompt you to commit if changes were made

**Note:** The git hook will update numbers and stage files, but you'll still need to commit them if they changed.

## Scripts

### `update_chapter_numbers.sh`

**Purpose:** Replaces `{CH}` placeholders with actual chapter numbers.

**When to run:**
- Before pushing to git (if not using git hook)
- Before generating LaTeX PDF (already automatic)
- After renumbering chapters

**Usage:**
```bash
./docs/.scripts/update_chapter_numbers.sh
```

This script:
1. Scans all `chapter*/README.md` files in `docs/content/`
2. Extracts chapter number from directory name (e.g., `chapter4` → `4`)
3. Replaces all `{CH}` placeholders with the actual number

### `convert_all_to_placeholders.sh`

**Purpose:** One-time conversion of hardcoded numbers to placeholders.

**When to run:**
- When first setting up the system
- After manually editing files with hardcoded numbers

**Usage:**
```bash
./docs/.scripts/convert_all_to_placeholders.sh
```

### `pre_push.sh`

**Purpose:** Convenience script that updates chapter numbers before git operations.

**Usage:**
```bash
./docs/.scripts/pre_push.sh
# Then: git add -A && git commit -m "..." && git push
```

### `setup_git_hooks.sh`

**Purpose:** Sets up automatic git hooks for chapter number updates.

**Usage:**
```bash
./docs/.scripts/setup_git_hooks.sh
```

## Workflow

### Normal Editing

1. Edit chapter files using `{CH}` placeholders
2. When ready to push or build:
   ```bash
   ./docs/.scripts/update_chapter_numbers.sh
   git add -A
   git commit -m "Your message"
   git push
   ```

### Renumbering Chapters

1. Rename chapter directories (e.g., `mv chapter4 chapter5`)
2. Run the update script:
   ```bash
   ./docs/.scripts/update_chapter_numbers.sh
   ```
3. All chapter numbers will be automatically updated!

### Generating LaTeX PDF

Just run the build script - it handles everything automatically:

```bash
./docs/.scripts/build_latex.sh
```

## Examples

### Chapter Title
```markdown
# Chapter {CH} — Micro Static Analysis of a Single Neo
```
Becomes: `# Chapter 4 — Micro Static Analysis of a Single Neo`

### Section Header
```markdown
## {CH}.1 Neo as a Predictive System
```
Becomes: `## 4.1 Neo as a Predictive System`

### Subsection Header
```markdown
### {CH}.2.1 Dynamics with Concrete Parameters
```
Becomes: `### 4.2.1 Dynamics with Concrete Parameters`

### Figure/Table References
```markdown
**Figure {CH}.1 — Conceptual Cube Diagram**
## Table {CH}.1 — Three-Axis Mapping
```
Becomes: `**Figure 7.1 — Conceptual Cube Diagram**` and `## Table 7.1 — Three-Axis Mapping`

## Notes

- The placeholder system only affects chapter and section numbers
- References to other chapters in text should still use actual numbers (e.g., "as discussed in Chapter 2")
- The scripts preserve all other content exactly as written
- Files are edited in-place, so make sure to commit your work before running conversion scripts
