# Documentation Scripts

## update_chapter_numbers.sh

Automatically updates chapter numbers in all chapter files by replacing `{CH}` placeholders with actual chapter numbers based on directory names.

**Usage:**
```bash
./update_chapter_numbers.sh
```

**How it works:**
- Scans all `chapter*/README.md` files in `docs/content/`
- Extracts chapter number from directory name (e.g., `chapter4` → `4`)
- Replaces `{CH}` placeholders in:
  - Chapter titles: `# Chapter {CH} — Title`
  - Section headers: `## {CH}.1 Section`, `## {CH}.2 Section`, etc.
  - Subsection headers: `### {CH}.2.1 Subsection`, etc.
  - All deeper nesting levels

**When to use:**
- Before pushing to git
- Before generating LaTeX PDF
- After renumbering chapters

## pre_push.sh

Convenience script that runs chapter number updates before git operations.

**Usage:**
```bash
./pre_push.sh
# Then: git add -A && git commit -m "..." && git push
```

## build_latex.sh

Builds LaTeX PDF from Markdown sources. Automatically runs `update_chapter_numbers.sh` first.

**Usage:**
```bash
./build_latex.sh
```

## Setting up Git Hooks (Optional)

To automatically update chapter numbers before every push:

```bash
cd /path/to/Neosis
ln -s ../../docs/.scripts/pre_push.sh .git/hooks/pre-push
chmod +x .git/hooks/pre-push
```

Or manually run `./docs/.scripts/pre_push.sh` before pushing.

